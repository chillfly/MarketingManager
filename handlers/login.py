import sys
import io
import time
import hashlib
from configs import settings
from handlers.base import BaseHandler
from models.system import SysUser
from utils.mycaptcha import create_captcha
from utils.mylogger import write_log, LOG_TYPE_OPERATE


def url_spec(**kwargs):
    return [
        (r'/login/?', LoginHandler, kwargs),
        (r'/logout/?', LogoutHandler, kwargs),
        (r'/captcha/?', CaptchaHandler, kwargs),
    ]


class LoginHandler(BaseHandler):

    def get(self):
        # 登录页面
        self.render("login.html")

    def post(self):
        try:
            # 登录操作
            user_model = SysUser()
            username = self.get_argument("username", "")
            pwd = self.get_argument("password", "")
            captcha = self.get_argument("captcha", "")
            if not username or not pwd or not captcha:
                self.send_fail_json("请输入合法的账号或者密码或者验证码")
                return

            if not self.check_captcha(captcha):
                # 验证码不正确
                self.send_fail_json("验证码不正确")
                return

            user = user_model.get_one8namepwd(username=username, pwd=self.md5_password(pwd))
            if not user:
                self.send_fail_json("请确保用户名和密码正确")
                return

            # 删除同一个用户的所有登录缓存
            cache = self.cache
            cache.delete_cache(self.token_key.format(tk="*", uid=user.id))

            # token加密
            token = hashlib.md5("{}{}{}".format(user.id, settings.PLATFORM_USER_TOKEN_SECRET, int(time.time())).encode("utf-8")).hexdigest()
            # 获取当前登录用户的token_key
            token_key = self.token_key.format(tk=token, uid=user.id)
            # 重新设置该登录用户的缓存
            cache.set_cache(token_key, dict(id=user.id, name=user.name, role_id=user.role_id, fid=user.fid), 3600)
            # 更新用户最后一次登录ip
            user_model.update_login_ip(user.id, self.request.remote_ip)

            # self.ip_limit(target_ip=self.request.remote_ip)

            self.set_secure_cookie(name="token", value=token, expires_days=1)

            write_log("'{}'用户登录成功了，登录IP为：{}".format(user.id, self.request.remote_ip), LOG_TYPE_OPERATE)
            self.send_ok_json()
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")

    def check_captcha(self, user_captcha=""):
        captcha = self.get_secure_cookie(name="captcha")
        return True if captcha.lower() == user_captcha.lower() else False


class LogoutHandler(BaseHandler):

    def post(self):
        try:
            self.clear_cookie("token")
            write_log("'{}'用户注销成功了".format(self.user["id"]), LOG_TYPE_OPERATE)
            self.send_ok_json()
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class CaptchaHandler(BaseHandler):

    def prepare(self):
        # 重写父类prepare方法，不做任何验证
        pass

    def get(self, *args, **kwargs):
        # 创建一个文件流
        imgio = io.BytesIO()
        # 生成图片对象和对应字符串
        img, code = create_captcha()
        self.set_secure_cookie(name="captcha", value=code)
        # session = Session(self)
        # session["captcha"] = code
        # 将图片信息保存到文件流
        img.save(imgio, 'PNG')
        self.write(imgio.getvalue())
