"""
自定义微博异常类
"""


class WeiboAjaxloginException(Exception):
    def __init__(self):
        self.msg = "登录微博(post访问ajaxlogin.php失败)"
