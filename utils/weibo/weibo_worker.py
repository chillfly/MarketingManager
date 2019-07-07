"""
微博脚本
"""

import sys
import os
import math
import threading
import time
import re
import random
import requests
import logging

this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from configs import settings
from utils import functions as func, myjson, mycache, myproxy
from models import commondb, orderslog, product, orders

logging.basicConfig(level=logging.INFO)
rabbitmq_receivers = {}

# 每一个消息最多开启10个线程
thread_num_every_msg = 1
_lock = threading.Lock()
redis_conn = mycache.RedisCache()
http_proxy = {"http": "http://171.211.101.235:4216"}
proxy_obj = myproxy.TaiyangProxy()


# 微博脚本父类
class WeiboWorker(threading.Thread):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
        self.orders = None
        self.orderslog = None
        self.req_session = requests.session()
        self.proxies = None
        self.done_count_key = "{}_done_count".format(msg["order_id"])

    def mark_all_done(self, order_id):
        """
        标记全部处理完成
        :param order_id:
        :return:
        """
        # 修改订单状态为“已完成”
        self.orders.update(where={"id": order_id}, data={"status": orders.ORDER_STATUS_DONE})
        # 添加处理日志
        self.orderslog.add({"order_id": order_id, "comments": "处理完成"})

    def mark_part_done(self, order_id, comments):
        """
        标记处理部分
        :param order_id:
        :param comments:
        :return:
        """
        # 修改订单状态为“处理中”
        self.orders.update(where={"id": order_id}, data={"status": orders.ORDER_STATUS_DOING})
        # 添加处理日志
        self.orderslog.add({"order_id": order_id, "comments": comments})

    def resp_convert(self, response, loadpage=False):
        # 定义要返回的数据
        res = {"status": False}

        if loadpage:
            pattern1 = "location.replace\(\"(.*?)\"\)"
            pattern2 = "location.replace\(\"(.*?)\"\)"
            url_list = re.findall(pattern1, response.text) or re.findall(pattern2, response.text)
            if url_list:
                # 重定向
                url = url_list[0]
                if url.find("login.sina.com") >= 0:
                    # 微博未登录，重定向到微博登录页面
                    res["code"] = settings.WEIBO_NOT_LOGIN
                else:
                    # 普通的重定向
                    res["code"] = 302
            else:
                res["status"] = True
        else:
            if response.status_code == 200:
                try:
                    temp_res = myjson.loads(response.text)
                    code = temp_res.get("code", "")
                    if not code:
                        # code为空，则去msg中找错误码
                        err_code = re.search(r'\d+', temp_res.get("msg")).group() or ""
                        res.update(code=err_code)
                    else:
                        if code == "100000":
                            # 成功
                            res["status"] = True
                        res.update(code=code)
                        res.update(reason=temp_res.get("msg", ""))
                except Exception:
                    # 返回内容为非json格式，则肯定是出错了
                    res.update(reason="response返回结果为非json格式")

                    if response.url == 'https://weibo.com/sorry?pagenotfound':
                        # 报页面找不到，说明是账号异常
                        res.update(code=settings.WEIBO_ERROR_CODE_PAGE_NOT_FOUND)
            else:
                # 默认返回失败
                res.update(reason="返回非200")

        return res

    def get(self, url="", **kwargs):
        """
        微博请求
        :param url: 路由
        :param kwargs: 其他参数
        :return:
        """
        # 判断url是否为空
        if not url:
            return

        # 添加cookie
        if kwargs.get("cookies") and isinstance(kwargs.get("cookies"), str):
            kwargs["cookies"] = func.get_cookie_jar(kwargs.get("cookies", ""))

        # 添加headers
        if kwargs.get("headers") and isinstance(kwargs.get("headers"), str):
            kwargs["headers"] = myjson.loads(kwargs.get("headers"))

        params = dict()
        temp = url.split("?")
        url_after = url.split("?")[0]
        if len(temp) == 2:
            for key_value in temp[1].split("&"):
                key = key_value.split("=")[0]
                value = key_value.split("=")[1]
                params[key] = value

        return self.req_session.get(url_after, params=params, timeout=5, **kwargs)

    def post(self, url="", **kwargs):
        """
        微博请求
        :param url: 路由
        :param kwargs: 其他参数
        :return:
        """
        # 判断url是否为空
        if not url:
            return

        # 添加cookie
        if "cookies" in kwargs.keys():
            kwargs["cookies"] = func.get_cookie_jar(kwargs.get("cookies", ""))

        # 添加headers
        if kwargs.get("headers") and isinstance(kwargs.get("headers"), str):
            kwargs["headers"] = myjson.loads(kwargs.get("headers"))

        return self.req_session.post(url, timeout=5, **kwargs)

    def get_weibo_users(self):
        """
        获取登录状态的微博账号
        :return:
        """
        with _lock:
            # 当前是第几次执行run方法
            level_key = "type_{}_order_{}_thread_run_level".format(self.msg["product_types"], self.msg["order_id"])
            thread_run_level = int(redis_conn.get_cache(level_key) or 1)
            redis_conn.set_cache(level_key, (thread_run_level + 1), ex=24 * 3600)

            product_numbers = int(self.msg["product_numbers"])
            thread_exec_nums = math.ceil(product_numbers / thread_num_every_msg)
            offset = (thread_run_level - 1) * thread_exec_nums
            return commondb.WeiboUser().get_some(where={"islogin": True}, offset=offset, limit=thread_exec_nums)


# 微博点赞类
class WeiboLikeWorker(WeiboWorker):
    def __init__(self, msg):
        super().__init__(msg)
        self.orders = orders.OrdersWeiboForward()
        self.orderslog = orderslog.OrdersLogWeiboLike()

    def run(self):
        """
        执行线程
        :return:
        """

        weibo_users = self.get_weibo_users()
        if not weibo_users:
            return

        # 获取代理
        proxy_list = proxy_obj.get_proxies_direct(len(weibo_users))
        if not proxy_list:
            # 没有取到代理，则退出
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成微博点赞数：{}，还差微博点赞数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )
            return

        try:
            for index, account in enumerate(weibo_users):
                # 每一次循环，先取“已经完成的数量”的缓存
                with _lock:
                    done_count = int(redis_conn.get_cache(self.done_count_key) or 0)

                if done_count < int(self.msg["product_numbers"]):
                    # 微博点赞数量暂未达标
                    if account.cookies and self.msg["weibo_url"]:
                        # region 执行微博微博点赞
                        try:
                            self.req_session = requests.session()
                            self.req_session.proxies = proxy_list[index]

                            # 加载微博页面
                            response = self.get(
                                self.msg["weibo_url"],
                                cookies=account.cookies,
                                headers=account.headers,
                            )
                            resp = self.resp_convert(response, loadpage=True)
                            if not resp.get("status"):
                                # 重定向
                                if resp.get("code") == settings.WEIBO_NOT_LOGIN:
                                    # 重定向到登录页，更新数据表，将该账号的登录状态改为0
                                    commondb.WeiboUser().update({"id": account.id}, {"islogin": False})
                                continue

                            if not response:
                                logging.error("[WeiboLikeWorker]: {}微博点赞失败，reason=加载页面失败".format(account.username))
                                continue
                            # 判断是否微博点赞过
                            has_not_like = re.search(
                                r'version=mini&qid=heart&mid=\d+&loc=profile&cuslike=1\\\"\s+title=\\\"赞',
                                response.text)
                            if not has_not_like:
                                logging.error("[WeiboLikeWorker]: {}微博点赞失败，reason=已经微博点赞过了".format(account.username))
                                continue

                            # 还没有微博点赞过
                            mid = re.search(r'\d{3,}', has_not_like.group()).group()

                            headers = {
                                "User-Agent": random.choice(settings.USER_AGENTS),
                                "Host": "weibo.com",
                                "Origin": "https://weibo.com",
                                "Referer": self.msg["weibo_url"]
                            }
                            # 定义微博点赞数据
                            post_data = {
                                "location": "v6_content_home",
                                "group_source": "group_all",
                                "version": "mini",
                                "qid": "heart",
                                "cuslike": "1",
                                "mid": mid,
                            }
                            # 执行微博点赞
                            resp = self.post(
                                "https://weibo.com/aj/v6/like/add?ajwvr=6",
                                data=post_data,
                                cookies=account.cookies,
                                headers=headers,
                            )
                            resp = self.resp_convert(resp)
                            if resp.get("status"):
                                # 微博点赞成功
                                with _lock:
                                    redis_conn.set_cache(self.done_count_key, (done_count + 1), ex=24 * 3600)
                                logging.info("[WeiboLikeWorker]: {}微博点赞成功".format(account.username))
                            else:
                                # 微博点赞失败
                                err_code = resp.get("code", 0)
                                if int(err_code) in settings.WEIBO_ERROR_CODES:
                                    # 账号异常，删除该账号
                                    commondb.WeiboUser().delete({"id": account.id})

                                logging.error("[WeiboLikeWorker]: {}微博点赞失败，错误码为：{}，reason={}".format(
                                    account.username,
                                    err_code,
                                    resp.get("reason", "")
                                ))
                        except Exception as ex:
                            # 微博点赞失败
                            logging.error("[WeiboLikeWorker]: {}微博点赞失败，发生异常，ex={}".format(account.username, repr(ex)))

                        # endregion
                else:
                    # 微博点赞数量已经达标
                    self.mark_all_done(self.msg["order_id"])
                    return

            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成微博点赞数：{}，还差微博点赞数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )

            # 能执行到这，说明没有全部执行完
            self.run()
        except Exception as ex:
            logging.error("[WeiboLikeWorker]: {}微博点赞失败，发生异常，ex={}".format(account.username, repr(ex)))


# 微博评论点赞类
class WeiboCommentLikeWorker(WeiboWorker):
    """
    微博评论点赞类
    """

    def __init__(self, msg):
        super().__init__(msg)
        self.orders = orders.OrdersWeiboCommentLike()
        self.orderslog = orderslog.OrdersLogWeiboCommentLike()

    def run(self):
        """
        执行线程
        :return:
        """
        weibo_users = self.get_weibo_users()
        if not weibo_users:
            return

        # 获取代理
        proxy_list = proxy_obj.get_proxies_direct(len(weibo_users))
        if not proxy_list:
            # 没有取到代理，则退出
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成评论点赞数：{}，还差评论点赞数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )
            return

        try:
            for index, account in enumerate(weibo_users):
                # 每一次循环，先取“已经完成的数量”的缓存
                with _lock:
                    done_count = int(redis_conn.get_cache(self.done_count_key) or 0)

                if done_count < int(self.msg["product_numbers"]):

                    # 评论点赞数量暂未达标
                    if account.cookies and self.msg["weibo_url"] and self.msg["comment_id"]:
                        # region 执行评论点赞
                        try:
                            self.req_session = requests.session()
                            self.req_session.proxies = proxy_list[index]

                            # 定义请求头
                            headers = {
                                "User-Agent": random.choice(settings.USER_AGENTS),
                                "Host": "weibo.com",
                                "Origin": "https://weibo.com",
                                "Referer": self.msg["weibo_url"]
                            }
                            # 定义评论点赞数据
                            post_data = {
                                'location': 'v6_content_home',
                                'group_source': 'group_all',
                                'object_type': 'comment',
                                "object_id": self.msg["comment_id"],
                                # "commentmid": "4349042768537033",
                            }
                            # 执行评论点赞
                            resp = self.post(
                                "https://weibo.com/aj/v6/like/objectlike?ajwvr=6",
                                data=post_data,
                                headers=headers,
                                cookies=account.cookies,
                            )
                            resp = self.resp_convert(resp)
                            if resp.get("status"):
                                # 评论点赞成功
                                with _lock:
                                    redis_conn.set_cache(self.done_count_key, (done_count + 1), ex=24 * 3600)
                                logging.info("[WeiboCommentLikeWorker]: {}评论点赞成功".format(account.username))
                            else:
                                # 评论点赞失败
                                err_code = resp.get("code", 0)
                                if int(err_code) in settings.WEIBO_ERROR_CODES:
                                    # 账号异常，删除该账号
                                    commondb.WeiboUser().delete({"id": account.id})
                                logging.error(
                                    "[WeiboCommentLikeWorker]: {}评论点赞失败，错误码为：{}，reason={}".format(
                                        account.username,
                                        err_code,
                                        resp.get("reason", ""),
                                    ))
                        except Exception as ex:
                            # 评论点赞失败
                            logging.error("[WeiboLikeWorker]: {}评论点赞失败，发生异常，ex={}".format(account.username, repr(ex)))

                        # endregion
                else:
                    # 评论点赞数量已经达标
                    self.mark_all_done(self.msg["order_id"])
                    return

            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成评论点赞数：{}，还差评论点赞数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )

            # 能执行到这，说明没有全部执行完
            self.run()
        except Exception as ex:
            logging.error("[WeiboCommentLikeWorker]: {}评论点赞失败，发生异常，ex={}".format(account.username, repr(ex)))


# 微博评论类
class WeiboCommentWorker(WeiboWorker):
    """
    微博评论类
    """

    def __init__(self, msg):
        super().__init__(msg)
        self.orders = orders.OrdersWeiboComment()
        self.orderslog = orderslog.OrdersLogWeiboComment()

    def run(self):
        """
        执行线程
        :return:
        """
        weibo_users = self.get_weibo_users()
        if not weibo_users:
            return

        # 获取代理
        proxy_list = proxy_obj.get_proxies_direct(len(weibo_users))
        if not proxy_list:
            # 没有取到代理，则退出
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成微博评论数：{}，还差微博评论数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )
            return

        try:
            mid = 0  # 要微博评论的微博id
            for index, account in enumerate(weibo_users):

                # 每一次循环，先取“已经完成的数量”的缓存
                with _lock:
                    done_count = int(redis_conn.get_cache(self.done_count_key) or 0)

                if done_count < int(self.msg["product_numbers"]):
                    # 微博评论数量暂未达标
                    if account.cookies and self.msg["weibo_url"]:
                        # region 执行微博评论
                        try:
                            self.req_session = requests.session()
                            self.req_session.proxies = proxy_list[index]

                            if not mid:
                                # 加载微博页面
                                response = self.get(
                                    self.msg["weibo_url"],
                                    cookies=account.cookies,
                                    headers=account.headers,
                                )
                                resp = self.resp_convert(response, loadpage=True)
                                if not resp.get("status"):
                                    # 重定向
                                    if resp.get("code") == settings.WEIBO_NOT_LOGIN:
                                        # 重定向到登录页，更新数据表，将该账号的登录状态改为0
                                        commondb.WeiboUser().update({"id": account.id}, {"islogin": False})
                                    continue
                                if not response:
                                    logging.error("[WeiboCommentWorker]: {}微博评论失败，reason=加载页面失败".format(account.username))
                                    continue
                                # 获取mid
                                mid_obj = re.search(
                                    r'version=mini&qid=heart&mid=\d+&loc=profile&cuslike=1',
                                    response.text)
                                if not mid_obj:
                                    # 取不到mid
                                    logging.error("[WeiboCommentWorker]: {}微博评论失败，获取不到微博ID".format(account.username))
                                    continue
                                mid = re.search(r'\d{3,}', mid_obj.group()).group()

                            # 定义请求头
                            headers = {
                                "User-Agent": random.choice(settings.USER_AGENTS),
                                "Host": "weibo.com",
                                "Origin": "https://weibo.com",
                                "Referer": self.msg["weibo_url"]
                            }
                            # 定义微博评论数据
                            post_data = {
                                'location': 'v6_content_home',
                                'group_source': 'group_all',
                                "mid": mid,
                                "content": random.choice(settings.WEIBO_COMMENT_FACES),
                            }
                            # 执行微博评论
                            resp = self.post(
                                "https://weibo.com/aj/v6/comment/add?ajwvr=6",
                                data=post_data,
                                headers=headers,
                                cookies=account.cookies
                            )
                            resp = self.resp_convert(resp)
                            if resp.get("status"):
                                # 微博评论成功
                                with _lock:
                                    redis_conn.set_cache(self.done_count_key, (done_count + 1), ex=24 * 3600)
                                logging.info("[WeiboCommentWorker]: {}微博评论成功".format(account.username))
                            else:
                                # 微博评论失败
                                err_code = resp.get("code", 0)
                                if int(err_code) in settings.WEIBO_ERROR_CODES:
                                    # 账号异常，删除该账号
                                    commondb.WeiboUser().delete({"id": account.id})

                                    logging.error(
                                        "[WeiboCommentWorker]: {}微博评论失败，错误码为：{}，reason={}".format(
                                            account.username,
                                            err_code,
                                            resp.get("reason", ""),
                                        ))
                        except Exception as ex:
                            # 点赞失败
                            logging.error("[WeiboCommentWorker]: {}微博评论失败，发生异常，ex={}".format(account.username, repr(ex)))

                        # endregion
                else:
                    # 微博评论数量已经达标
                    self.mark_all_done(self.msg["order_id"])
                    return

            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成微博评论数：{}，还差微博评论数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )

            # 能执行到这，说明没有全部执行完
            self.run()

        except Exception as ex:
            logging.error("[WeiboCommentWorker]: {}微博评论失败，发生异常，ex={}".format(account.username, repr(ex)))


# 微博关注类
class WeiboFollowWorker(WeiboWorker):
    """
    微博关注类
    """

    def __init__(self, msg):
        super().__init__(msg)
        self.orders = orders.OrdersWeiboFollow()
        self.orderslog = orderslog.OrdersLogWeiboFollow()

    def run(self):
        """
        执行线程
        :return:
        """
        weibo_users = self.get_weibo_users()
        if not weibo_users:
            return

        # 获取代理
        proxy_list = proxy_obj.get_proxies_direct(len(weibo_users))
        if not proxy_list:
            # 没有取到代理，则退出
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成关注数：{}，还差关注数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )
            return

        try:
            for index, account in enumerate(weibo_users):

                # 每一次循环，先取“已经完成的数量”的缓存
                with _lock:
                    done_count = int(redis_conn.get_cache(self.done_count_key) or 0)

                if done_count < int(self.msg["product_numbers"]):
                    # 关注数量暂未达标
                    if account.cookies and self.msg["weibo_url"]:
                        # region 执行微博关注
                        try:
                            self.req_session = requests.session()
                            self.req_session.proxies = proxy_list[index]

                            # 加载微博页面
                            response = self.get(
                                self.msg["weibo_url"],
                                cookies=account.cookies,
                                headers=account.headers,
                            )
                            resp = self.resp_convert(response, loadpage=True)
                            if not resp.get("status"):
                                # 重定向
                                if resp.get("code") == settings.WEIBO_NOT_LOGIN:
                                    # 重定向到登录页，更新数据表，将该账号的登录状态改为0
                                    commondb.WeiboUser().update({"id": account.id}, {"islogin": False})
                                continue
                            if not response:
                                logging.error("[WeiboFollowWorker]: {}关注失败，reason=加载页面失败".format(account.username))
                                continue
                            # 判断是否关注过
                            has_not_follow = re.search(
                                r'key=tblog_attention_click&value=\d+\\\"\s+action-type=\\\"follow',
                                response.text)
                            if not has_not_follow:
                                logging.error("[WeiboFollowWorker]: {}关注失败，reason=已经关注过了".format(account.username))
                                continue

                            # 获取用户唯一uid
                            uid = re.search(r'\d{3,}', has_not_follow.group()).group()

                            # 定义请求头
                            headers = {
                                "User-Agent": random.choice(settings.USER_AGENTS),
                                "Host": "weibo.com",
                                "Origin": "https://weibo.com",
                                "Referer": self.msg["weibo_url"]
                            }
                            # 定义关注数据
                            post_data = {
                                'location': 'v6_content_home',
                                'group_source': 'group_all',
                                "uid": uid,
                            }
                            # 执行关注
                            resp = self.post(
                                "https://weibo.com/aj/f/followed?ajwvr=6",
                                data=post_data,
                                headers=headers,
                                cookies=account.cookies
                            )
                            resp = self.resp_convert(resp)
                            if resp.get("status"):
                                # 点赞成功
                                with _lock:
                                    redis_conn.set_cache(self.done_count_key, (done_count + 1), ex=24 * 3600)
                                logging.info("[WeiboFollowWorker]: {}关注成功".format(account.username))
                            else:
                                # 点赞失败
                                err_code = resp.get("code", 0)
                                if int(err_code) in settings.WEIBO_ERROR_CODES:
                                    # 账号异常，删除该账号
                                    commondb.WeiboUser().delete({"id": account.id})

                                logging.error("[WeiboFollowWorker]: {}关注失败，错误码为：{}，reason={}".format(
                                    account.username,
                                    err_code,
                                    resp.get("reason", ""),
                                ))
                        except Exception as ex:
                            # 关注失败
                            logging.error("[WeiboFollowWorker]: {}关注失败，发生异常，ex={}".format(account.username, repr(ex)))

                        # endregion
                else:
                    # 关注数量已经达标
                    self.mark_all_done(self.msg["order_id"])
                    return

            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成关注数：{}，还差关注数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )

            # 能执行到这，说明没有全部执行完
            self.run()

        except Exception as ex:
            logging.error("[WeiboFollowWorker]: {}关注失败，发生异常，ex={}".format(account.username, repr(ex)))


class WeiboForwardWorker(WeiboWorker):
    """
    微博转发类
    """

    def __init__(self, msg):
        super().__init__(msg)
        self.orders = orders.OrdersWeiboForward()
        self.orderslog = orderslog.OrdersLogWeiboForward()

    def run(self):
        """
        执行线程
        :return:
        """
        weibo_users = self.get_weibo_users()
        if not weibo_users:
            return

        # 获取代理
        proxy_list = proxy_obj.get_proxies_direct(len(weibo_users))
        if not proxy_list:
            # 没有取到代理，则退出
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成转发数：{}，还差转发数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )
            return

        try:
            mid = 0  # 待转发的微博ID

            for index, account in enumerate(weibo_users):

                # 每一次循环，先取“已经完成的数量”的缓存
                with _lock:
                    done_count = int(redis_conn.get_cache(self.done_count_key) or 0)

                if done_count < int(self.msg["product_numbers"]):
                    # 转发数量暂未达标
                    if account.cookies and self.msg["weibo_url"]:
                        # region 执行微博转发
                        try:
                            self.req_session = requests.session()
                            self.req_session.proxies = proxy_list[index]

                            if not mid:
                                # 加载微博页面
                                response = self.get(
                                    self.msg["weibo_url"],
                                    cookies=account.cookies,
                                    headers=account.headers,
                                )
                                resp = self.resp_convert(response, loadpage=True)
                                if not resp.get("status"):
                                    # 重定向
                                    if resp.get("code") == settings.WEIBO_NOT_LOGIN:
                                        # 重定向到登录页，更新数据表，将该账号的登录状态改为0
                                        commondb.WeiboUser().update({"id": account.id}, {"islogin": False})
                                    continue
                                if not response:
                                    logging.error("[WeiboForwardWorker]: {}转发失败，reason=加载页面失败".format(account.username))
                                    continue
                                # 获取mid
                                has_not_like = re.search(
                                    r'version=mini&qid=heart&mid=\d+&loc=profile&cuslike=1',
                                    response.text)
                                if not has_not_like:
                                    # 取不到mid
                                    logging.error("[WeiboForwardWorker]: {}转发失败，没有取到微博ID".format(account.username))
                                    continue

                                mid = re.search(r'\d{3,}', has_not_like.group()).group()

                            # 定义请求头
                            headers = {
                                "User-Agent": random.choice(settings.USER_AGENTS),
                                "Host": "weibo.com",
                                "Origin": "https://weibo.com",
                                "Referer": self.msg["weibo_url"]
                            }
                            # 定义转发数据
                            post_data = {
                                'location': 'v6_content_home',
                                'group_source': 'group_all',
                                "mid": mid,
                                "reason": "转发微博",
                            }
                            # 执行转发
                            resp = self.post(
                                "https://weibo.com/aj/v6/mblog/forward?ajwvr=6",
                                data=post_data,
                                headers=headers,
                                cookies=account.cookies
                            )
                            resp = self.resp_convert(resp)
                            if resp.get("status"):
                                # 转发成功
                                with _lock:
                                    redis_conn.set_cache(self.done_count_key, (done_count + 1), ex=24 * 3600)
                                logging.info("[WeiboForwardWorker]: {}转发成功".format(account.username))
                            else:
                                # 转发失败
                                err_code = resp.get("code", 0)
                                if int(err_code) in settings.WEIBO_ERROR_CODES:
                                    # 账号异常，删除该账号
                                    commondb.WeiboUser().delete({"id": account.id})

                                logging.error("[WeiboForwardWorker]: {} 转发失败，错误码为：{}，reason={}".format(
                                    account.username,
                                    err_code,
                                    resp.get("reason", ""),
                                ))
                        except Exception as ex:
                            # 关注失败
                            logging.error("[WeiboForwardWorker]: {}转发失败，发生异常，ex={}".format(account.username, repr(ex)))

                        # endregion
                else:
                    # 转发数量已经达标
                    self.mark_all_done(self.msg["order_id"])
                    return
            with _lock:
                done_count = int(redis_conn.get_cache(self.done_count_key) or 0)
                self.mark_part_done(
                    self.msg["order_id"],
                    "已完成转发数：{}，还差转发数：{}".format(done_count, int(self.msg["product_numbers"]) - done_count)
                )

            # 能执行到这，说明没有全部执行完
            self.run()
        except Exception as ex:
            logging.error("[WeiboForwardWorker]: {}转发失败，发生异常，ex={}".format(account.username, repr(ex)))


def do_script(msg):
    """
    针对不同类型的微博产品类型，执行不同的脚本
    :param msg:
    :return:
    """
    # 线程个数
    print("-----------------------------start do_script------------------------")
    product_types = msg.get("product_types", 1)
    if product_types == product.PRODUCT_TYPES_WEIBO_LIKE:
        # 微博点赞
        th = WeiboLikeWorker(msg)
    elif product_types == product.PRODUCT_TYPES_WEIBO_COMMENT_LIKE:
        # 微博评论赞
        th = WeiboCommentLikeWorker(msg)
    elif product_types == product.PRODUCT_TYPES_WEIBO_COMMENT:
        # 微博评论
        th = WeiboCommentWorker(msg)
    elif product_types == product.PRODUCT_TYPES_WEIBO_FOLLOW:
        # 微博关注
        th = WeiboFollowWorker(msg)
    elif product_types == product.PRODUCT_TYPES_WEIBO_FORWARD:
        # 微博转发
        th = WeiboForwardWorker(msg)
    th.start()

    print("-----------------------------end do_script------------------------")


if __name__ == '__main__':
    # # 测试
    msg = dict(
        product_types=1,
        product_numbers=100,
        weibo_url="https://weibo.com/6489202878/Hn8itqgx0?from=page_1005056489202878_profile&wvr=6&mod=weibotime",
        order_id=1,
        comment_id=""
    )
    WeiboLikeWorker(msg).run()
    pass
