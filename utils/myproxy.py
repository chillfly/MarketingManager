"""
代理
"""

import requests
import random
import time
import datetime
from configs import settings
from utils.mylogger import write_log
from utils import myjson
from utils import mycache

db_redis = 0
db_mongodb = 1
db_mysql = 2
proxy_key = "proxy"

# 无效的http代理
proxy_http_invalid_key = "proxy_http_invalid"
# 有效的http代理
proxy_http_valid_key = "proxy_http_valid"

# 无效的https代理
proxy_https_invalid_key = "proxy_https_invalid"
# 有效的https代理
proxy_https_valid_key = "proxy_https_valid"

proxy_type_http = "http"
proxy_type_https = "https"
redis_conn = mycache.RedisCache().conn


class Proxy(object):
    def __init__(self, db_type=db_redis, proxy_type=proxy_type_https, is_foreign=False, is_direct=True):
        """
        初始化
        :param db_type: 数据库类型（redis，mongodb，mysql 等）
        :param proxy_type: 代理类型（http或者http 等）
        :param is_foreign: 是否国外代理
        :param is_direct: 是否直接取代理
        """
        self.is_direct = is_direct  # 直接从代理服务商那里获取代理ip；或者先从代理服务商那里获取ip存入缓存中，从缓存中取
        self.db_type = db_type
        self.proxy_type = proxy_type
        if proxy_type == proxy_type_http:
            self.proxy_valid_key = "{}_{}".format(proxy_http_valid_key, self.__class__.__name__)
            self.proxy_invalid_key = "{}_{}".format(proxy_http_invalid_key, self.__class__.__name__)
        elif proxy_type == proxy_type_https:
            self.proxy_valid_key = "{}_{}".format(proxy_https_valid_key, self.__class__.__name__)
            self.proxy_invalid_key = "{}_{}".format(proxy_https_invalid_key, self.__class__.__name__)
        self.is_foreign = is_foreign
        self.host_port = None

    def is_proxy_valid(self, proxies):
        """
        判断该代理host是否可用
        :param proxies: 代理，如：http://123.12.43.35:3280
        :return:
        """
        # http类型的代理
        try:
            test_url = "http://pv.sohu.com/cityjson?ie=utf-8"
            response = requests.get(
                test_url,
                proxies={self.proxy_type: proxies},
                headers={"User-Agent": random.choice(settings.USER_AGENTS)},
                timeout=3,
            )
            if response.text.find("returnCitySN") == -1:
                # 代理没用
                write_log("request is right,but response is not true")
                return False
            else:
                return True
        except Exception as e:
            write_log("raise exception in is_proxy_valid(),message={}".format(repr(e)))
            return False

    def add_proxy_to_redis(self):
        pass

    def get_proxy_from_redis(self):
        """
        从redis中获取代理一个ip
        :return:
        """
        while 1:
            for proxy in redis_conn.sscan_iter(self.proxy_valid_key):
                # 判断代理有效性
                if self.is_proxy_valid(proxy):
                    return {self.proxy_type: proxy}
                else:
                    redis_conn.srem(self.proxy_valid_key, proxy)
            else:
                # 没有找到代理，则执行添加代理的操作
                while 1:
                    add_res = self.add_proxy_to_redis()
                    if add_res:
                        # 添加代理成功
                        break
                    else:
                        # 添加代理失败，继续添加
                        continue

    def get_proxies_from_redis(self):
        """
        从redis中获取代理列表
        :return:
        """
        res = []
        while 1:
            for proxy in redis_conn.sscan_iter(self.proxy_valid_key):
                # 判断代理有效性
                if self.is_proxy_valid(proxy):
                    res.append({self.proxy_type: proxy})
                else:
                    redis_conn.srem(self.proxy_valid_key, proxy)
            else:
                if res:
                    # 如果取到了，则返回
                    return res

                # 没有找到代理，则执行添加代理的操作
                while 1:
                    add_res = self.add_proxy_to_redis()
                    if add_res:
                        # 添加代理成功
                        break
                    else:
                        # 添加代理失败，继续添加
                        continue

    def remove_proxy(self, proxy):
        """
        移除某个无用的代理
        :param proxy: 代理
        :return:
        """
        if not proxy:
            return
        if self.db_type == db_redis:
            # 往无效集合中添加该代理
            redis_conn.sadd(self.proxy_invalid_key, proxy)
            # 从有效集合中删除该代理
            redis_conn.srem(self.proxy_valid_key, proxy)

    def get_proxy_page(self, proxy_page_url):
        """
        获取代理页面
        :return:
        """
        pass

    def get_proxy_direct(self):
        pass

    def get_proxies_direct(self):
        pass


class TaiyangProxy(Proxy):

    def __init__(self, db_type=db_redis, proxy_type=proxy_type_https, is_foreign=False, is_direct=True):
        """
        初始化
        :param db_type: 数据库类型（redis，mongodb，mysql 等）
        :param proxy_type: 代理类型（http或者http 等）
        :param is_foreign: 是否国外代理
        :param is_direct: 是否直接取代理
        """
        super().__init__(db_type=db_type, proxy_type=proxy_type, is_foreign=is_foreign, is_direct=is_direct)
        self.redis_set_key = "taiyang_https_proxies_set"

    def get_proxy_list(self, num=1):
        # 当前系统时间
        now = datetime.datetime.now()
        # 待返回的代理列表
        res = list()

        balance_url = "http://ty-http-d.upupfile.com/index/index/get_my_pack_info?" \
                      "neek=525535&appkey=1ecf62d62c0b4fa31ce1d9e22070a1ea"
        headers = {
            "User-Agent": random.choice(settings.USER_AGENTS)
        }
        try:
            response = requests.get(balance_url, headers=headers)
            if response.status_code == 200:
                    balance_data = myjson.loads(response.text)
                    if balance_data.get("code") == 0:
                        balance_list = balance_data.get("data")
        except:
            return res

        try:
            for item in balance_list:

                pack = item["pack"]
                balance = item["balance"]
                if balance < num:
                    # 总额不够，则全部取
                    temp_num = balance
                else:
                    # 总额有的多，则取差额
                    temp_num = num

                if not temp_num or now > datetime.datetime.fromtimestamp(item["near_fill_time"]):
                    # 数量为0，或者已经过期，跳过下面直接执行下一次循环
                    continue

                ip_url = "http://http.tiqu.qingjuhe.cn/getip?" \
                         "num={}&type=2&pack={}&port=11&ts=1&lb=1&pb=4&regions=".format(temp_num, pack)
                response = requests.get(ip_url, headers=headers)
                if response.status_code == 200:
                    json_data = myjson.loads(response.text)
                    if json_data.get("code") == 0:
                        res.extend(json_data.get("data"))

                        num = num - temp_num
                        if num <= 0:
                            # 已经取够了
                            return
        except:
            pass
        finally:
            return res

    def get_proxy_direct(self):
        """
        获取单个ip代理
        :return:
        """
        for one in redis_conn.sscan_iter(self.redis_set_key):

            # 当前系统时间
            now = datetime.datetime.now()

            # 转json
            item = myjson.loads(one)

            expire_time = datetime.datetime.strptime(item["expire_time"], "%Y-%m-%d %H:%M:%S")
            if now > expire_time:
                # 过期了
                redis_conn.srem(self.redis_set_key, one)
                continue

            # 拼接代理
            temp = "http://{}:{}".format(item.get("ip"), item.get("port"))

            # 检测代理有效性
            if self.is_proxy_valid(temp):
                return {self.proxy_type: temp}

        data = self.get_proxy_list(1)
        for item in data:
            temp = "http://{}:{}".format(item.get("ip"), item.get("port"))
            if self.is_proxy_valid(temp):
                redis_conn.sadd(self.redis_set_key, myjson.dumps(item))
                return {self.proxy_type: temp}

    def get_proxies_direct(self, num=1):
        """
        获取多个代理
        :param num:
        :return:
        """

        res = list()
        current_num = 0
        for one in redis_conn.sscan_iter(self.redis_set_key):

            # 当前系统时间
            now = datetime.datetime.now()

            # 转json
            item = myjson.loads(one)

            expire_time = datetime.datetime.strptime(item["expire_time"], "%Y-%m-%d %H:%M:%S")
            if now > expire_time:
                # 过期了
                redis_conn.srem(self.redis_set_key, one)
                continue

            # 拼接代理
            temp = "http://{}:{}".format(item.get("ip"), item.get("port"))

            # 检测代理有效性
            if self.is_proxy_valid(temp):
                res.append({self.proxy_type: temp})
                current_num += 1
                if current_num >= num:
                    break

        if current_num < num:
            data = self.get_proxy_list(num=(num - current_num))
            for item in data:
                temp = "http://{}:{}".format(item.get("ip"), item.get("port"))
                if self.is_proxy_valid(temp):
                    redis_conn.sadd(self.redis_set_key, myjson.dumps(item))
                    res.append({self.proxy_type: temp})

        return res


if __name__ == '__main__':
    obj = TaiyangProxy()
    obj.get_proxies_direct(2)
