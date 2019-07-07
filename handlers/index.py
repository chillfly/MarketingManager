from .base import BaseHandler
from models.system import get_user_menus, SysUser
from datetime import datetime


def url_spec(**kwargs):
    return [
        (r'/?', MainHandler, kwargs),
        (r'/welcome/?', WelcomeHandler, kwargs),
    ]


class MainHandler(BaseHandler):
    def get(self, *args, **kwargs):
        if self.current_user:
            menus = get_user_menus(self.user.get("id"))
            self.render("base.html", user=self.current_user, menus=menus)
        else:
            self.redirect("/login/")


class WelcomeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # 当前时间段
        current_time_period = ""
        now = datetime.now()
        if 6 > now.hour >= 0:
            current_time_period = "凌晨"
        elif 8 > now.hour >= 6:
            current_time_period = "早上"
        elif 11 > now.hour >= 8:
            current_time_period = "上午"
        elif 14 > now.hour >= 11:
            current_time_period = "中午"
        elif 18 > now.hour >= 14:
            current_time_period = "下午"
        elif 20 > now.hour >= 18:
            current_time_period = "傍晚"
        elif now.hour > 20:
            current_time_period = "晚上"
        user = SysUser().get_one8id(self.user["id"])
        self.render("index/welcome.html", user=user, current_time_period=current_time_period)
