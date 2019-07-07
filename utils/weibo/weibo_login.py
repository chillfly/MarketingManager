import os
import sys
import requests
import base64
import urllib
import rsa
import binascii
import re
import json
import random
import time
import logging
from configs import settings
from utils import myjson, functions as func, fateadm
from utils.myexception.weibo_exception import WeiboAjaxloginException


project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(project_dir))

logging.basicConfig(level=logging.INFO)


class Weibo(object):

    def __init__(self, user_name="", password="", proxy={}):
        """
        网页端微博
        :param user_name:
        :param password:
        """
        self.username = user_name
        self.password = password
        # 用户名加密
        self.su = base64.b64encode(urllib.request.quote(self.username).encode("utf-8"))
        self.client = "ssologin.js(v1.4.18)"
        self.host = "http://weibo.com/"
        self.uniqueid = ""
        self.userdomain = ""
        self.home = ""
        self.last_mid = 0
        self.forward_mid = []
        self.signal = 0
        self.headers = {
            "Host": "login.sina.com.cn",
            "User-Agent": random.choice(settings.USER_AGENTS)
        }

        self.req_session = requests.session()
        self.req_session.proxies = proxy

    @staticmethod
    def has_mrid_but_no_feedtype(tag):
        """
        bs过滤广告标签（广告微博）
        :param tag:
        :return:
        """
        return tag.has_attr("mrid") and not tag.has_attr("feedtype")

    def request_get(self, url, params=dict(), **kwargs):
        temp = url.split("?")
        url_after = url.split("?")[0]
        if len(temp) == 2:
            for key_value in temp[1].split("&"):
                key = key_value.split("=")[0]
                value = key_value.split("=")[1]
                params[key] = value

        return self.req_session.get(url_after, params=params, **kwargs)

    def check_login(self, cookies, headers):
        """
        检测是否登录
        :param cookies:
        :param headers:
        :return:
        """
        req_param = {}
        if not cookies:
            # cookies为空，肯定未登录
            return False
        req_param["cookies"] = func.get_cookie_jar(cookies)

        if headers:
            headers = myjson.loads(headers)
            req_param["headers"] = headers

        try:
            response = self.req_session.get("https://www.weibo.com", timeout=10, **req_param)
            if (response.status_code == 200) and (re.search(r'/u/\d+/', response.url)):
                # 登录成功
                logging.info("[check_login]: {} is login".format(self.username))
                return True
            else:
                logging.info("[check_login]: {} is not login".format(self.username))
                return False
        except Exception as ex:
            logging.error("[check_login]: raise Exception, ex={}".format(repr(ex)))
            return None

    def login(self):
        """
        执行登录
        :return:
        """
        try:

            # 获取返回的json数据，用于后续的登陆
            payload = {
                "entry": "weibo",
                "callback": "sinaSSOController.preloginCallBack",
                "su": self.su,
                "rsakt": "mod",
                "checkpin": 1,
                "client": self.client
            }
            prelogin_url = "https://login.sina.com.cn/sso/prelogin.php"
            response = self.req_session.get(prelogin_url, params=payload, headers=self.headers)
            data = re.findall("\((.*?)\)", response.text)[0]
            json_data = json.loads(data)

            # 密码进行加密
            s = str(json_data["servertime"]) + '\t' + str(json_data["nonce"]) + '\n' + self.password
            key = rsa.PublicKey(int(json_data["pubkey"], 16), int("10001", 16))
            key = rsa.encrypt(s.encode("utf-8"), key)
            sp = binascii.b2a_hex(key)
            post_data = {
                "entry": "weibo",
                "gateway": 1,
                "from": "",
                "savestate": 7,
                "useticket": 1,
                "pagerefer": "",
                "pcid": json_data["pcid"],
                "vsnf": 1,
                "su": self.su,
                "service": "miniblog",
                "servertime": int(time.time()),
                "nonce": json_data["nonce"],
                "pwencode": "rsa2",
                "rsakv": json_data["rsakv"],
                "sp": sp,
                "sr": "1440*900",
                "encoding": "UTF-8",
                "prelt": "129",
                "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
                "returntype": "META",
            }

            if json_data.get("showpin", None) == 1:
                # 判断是否有验证码
                check_verify_url = "http://login.sina.com.cn/cgi/pin.php?r={}&s=0&p={}".format(
                    "".join(random.sample("123456789", 8)),
                    json_data["pcid"])
                res = self.req_session.get(check_verify_url, headers=self.headers)
                weibo_verify_dir = "{}/static/images/weibo".format(project_dir)
                if not os.path.exists(weibo_verify_dir):
                    # 微博验证码目录不存在，创建之
                    os.makedirs(weibo_verify_dir)
                with open("{}/captcha.png".format(weibo_verify_dir), "wb") as f:
                    f.write(res.content)

                # 调用斐斐打码平台接口识别验证码内容
                captcha = fateadm.get_captcha_code("{}/captcha.png".format(weibo_verify_dir))
                post_data["door"] = captcha,

            # 登陆微博
            res = self.req_session.post(
                "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)",
                data=post_data,
                headers=self.headers,
                timeout=10,
            )

            if re.search("refresh", res.text):
                raise WeiboAjaxloginException()
            else:
                url = re.findall("location.replace\('(.*?)'\)", res.text)[0]
                # 验证登陆，此处302跳转
                self.headers["Host"] = "passport.weibo.com"
                res = self.req_session.get(url, allow_redirects=False, headers=self.headers)

                # 获得跳转链接
                location = res.headers["Location"]
                self.headers["Host"] = "weibo.com"
                # res = self.req_session.get(location, headers=self.headers)
                res = self.req_session.get(location, headers=self.headers)
                user_info = re.findall("parent.sinaSSOController.feedBackUrlCallBack\((.*?)\)", res.text)[0]
                user_info = json.loads(user_info)
                if user_info["result"]:
                    # 登录成功
                    self.userdomain = user_info["userinfo"]["userdomain"]
                    self.uniqueid = user_info["userinfo"]["uniqueid"]
                    result = {
                        "status": True,
                        "userdomain": user_info["userinfo"]["userdomain"],
                        "uniqueid": user_info["userinfo"]["uniqueid"],
                        "cookies": myjson.dumps(self.req_session.cookies.get_dict()),
                        "headers": myjson.dumps(dict(self.req_session.headers)),
                    }
                else:
                    # 登录失败
                    logging.error("[login]: 微博账号{}登录失败".format(self.username))
                    result = {"status": False, "reason": "登录失败"}
        except WeiboAjaxloginException as ex:
            logging.error("[login]: 发生异常，ex={}".format(repr(ex.msg)))
            result = {"status": False, "reason": "发生异常"}
        except Exception as ex:
            # 移除该代理
            logging.error("[login]: 发生异常，ex={}".format(repr(ex)))
            result = {"status": False, "reason": "发生异常"}
        finally:
            return result
