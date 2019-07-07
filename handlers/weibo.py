import sys
import os
from datetime import datetime
from .base import LayerListHandler, BaseHandler
from models.system import power_check
from models.commondb import common_db_engine, WeiboUser
from models.product import Product, PRODUCT_SOURCE, PRODUCT_WEIBO_TYPES_LABELS
from utils.myfilter import is_empty
from utils.myaescrypto import aes_encrypt, aes_decrypt
from utils.mylogger import write_log, LOG_TYPE_OPERATE
from utils.weibo.weibo_login import Weibo
from utils import myjson

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def url_spec(**kwargs):
    return [
        (r'/weibo/account/list/?', WeiboUserListHandler, kwargs),
        (r'/weibo/account/add/?', WeiboUserAddHandler, kwargs),  # 用户添加
        (r'/weibo/account/edit/?', WeiboUserEditHandler, kwargs),  # 用户修改
        (r'/weibo/account/del/?', WeiboUserDelHandler, kwargs),  # 用户删除（硬删除）

        (r'/weibo/account/loadloginpage/?', WeiboUserLoadLoginPageHandler, kwargs),  # 用户是否需要验证码
        (r'/weibo/account/login/?', WeiboUserLoginHandler, kwargs),  # 用户登录
        (r'/weibo/account/verifycode/?', WeiboUserVerifycodeHandler, kwargs),  # 用户登录

        (r'/weibo/product/list/?', WeiboProductListHandler, kwargs),  # 微博产品列表
        (r'/weibo/product/add/?', WeiboProductAddHandler, kwargs),  # 微博产品添加
        (r'/weibo/product/edit/?', WeiboProductEditHandler, kwargs),  # 微博产品修改
    ]


class WeiboUserListHandler(LayerListHandler):
    """
    微博账号列表
    """
    _db_engine = common_db_engine
    _table = WeiboUser._table
    _template = "weibo/account-list.html"
    _order_by = "create_time desc"
    _table_query_args = ("username", )

    def _handler_result_data(self, data, **kwargs):
        data = super()._handler_result_data(data)
        for td in data:
            td["pwd"] = aes_decrypt(td["pwd"])
        return data

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        self._do_request()


class WeiboUserAddHandler(BaseHandler):
    _db_engine = common_db_engine

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        """
        加载添加微博账号表单页
        :param args:
        :param kwargs:
        :return:
        """
        self.render("weibo/account-add.html", one="")

    @power_check("WEIBO_MANAGE")
    def post(self, *args, **kwargs):
        """
        执行添加微博账号
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # 用户名
            username = self.get_args("username")
            if is_empty(username):
                # 用户名不能为空
                self.send_fail_json("账号不能为空")
                return

            # 登录密码
            pwd = self.get_args("pwd")
            if is_empty(pwd):
                # 密码不能为空
                self.send_fail_json("密码不能为空")
                return
            pwd = aes_encrypt(pwd)

            data = dict(
                username=username,
                pwd=pwd,
                create_time=datetime.now(),
            )

            # 备注
            comments = self.get_args("comments")
            if comments:
                data["comments"] = comments

            res = WeiboUser().add(data=data)
            if not res:
                self.send_fail_json("添加失败")
                return

            write_log("'{}'添加了一个微博账号(username为：{})".format(self.user["id"], username), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboUserEditHandler(BaseHandler):
    _db_engine = common_db_engine

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        """
        加载修改微博账号表单页
        :param args:
        :param kwargs:
        :return:
        """
        # 获取用户
        account_id = self.get_args("id", "")
        if is_empty(account_id):
            self.send_fail_json("用户id不能为空")
            return
        user = WeiboUser().get_one8id(account_id)
        if not user:
            self.send_fail_json("查无用户")
            return
        user = self.tran_rowproxy2variable(user)
        user.pwd = aes_decrypt(user.pwd)

        self.render("weibo/account-add.html", one=user)

    @power_check("WEIBO_MANAGE")
    def post(self, *args, **kwargs):
        """
        执行修改微博账号
        :param args:
        :param kwargs:
        :return:
        """
        try:
            account_id = self.get_args("account_id", "")
            if is_empty(account_id):
                self.send_fail_json("账号id不能为空")
                return

            # 用户名
            username = self.get_args("username")
            if is_empty(username):
                # 用户名不能为空
                self.send_fail_json("用户名不能为空")
                return

            # 登录密码
            pwd = self.get_args("pwd", "")
            if is_empty(pwd):
                # 密码不能为空
                self.send_fail_json("密码不能为空")
                return
            pwd = aes_encrypt(pwd)

            data = dict(
                username=username,
                pwd=pwd,
                update_time=datetime.now(),
            )

            # 备注
            comments = self.get_args("comments")
            if comments:
                data["comments"] = comments

            res = WeiboUser().update(where={"id": account_id}, data=data)
            if not res:
                self.send_fail_json("修改失败")
                return

            write_log("'{}'修改了一个微博账号(ID为：{})".format(self.user["id"], account_id), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboUserDelHandler(BaseHandler):
    """
    删除微博账号（硬删除）
    """

    _db_engine = common_db_engine

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        try:
            account_id = self.get_args("id", "")
            if not account_id:
                self.send_fail_json("id不能为空")
                return

            user_model = WeiboUser()
            res = user_model.delete(where={"id": account_id})
            if not res:
                self.send_fail_json("删除失败")
                return

            write_log("'{}'删除了一个微博账号(ID为：{})".format(self.user["id"], account_id), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboUserLoadLoginPageHandler(BaseHandler):
    """
    加载微博登录页面
    """

    _db_engine = common_db_engine

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        try:
            account_id = self.get_args("id", "")
            if not account_id:
                self.send_fail_json("account_id不能为空")
                return

            user = WeiboUser().get_one_specific_fields8id(("id", "username", "pwd", "cookies"), account_id)

            res = Weibo().load_login_page(user)
            if res["islogin"]:
                # 已登录
                self.send_ok_json("")
            else:
                # 未登录
                self.send_fail_json(data={"needverify": res["needverify"]})
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboUserLoginHandler(BaseHandler):
    """
    微博账号登录
    """

    _db_engine = common_db_engine

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        """
        登录页面
        :param args:
        :param kwargs:
        :return:
        """
        account_id = self.get_args("id", "")
        if not account_id:
            self.send_fail_json("account_id不能为空")
            return

        self.render("weibo/account-login.html", account_id=account_id)

    @power_check("WEIBO_MANAGE")
    def post(self, *args, **kwargs):
        """
        执行登录
        :param args:
        :param kwargs:
        :return:
        """
        try:
            weibouser_model = WeiboUser()

            account_id = self.get_args("id", "")
            if not account_id:
                self.send_fail_json("account_id不能为空")
                return

            # 获取验证码
            verifycode = self.get_args("verifycode", "")

            # 执行登录
            user = WeiboUser().get_one_specific_fields8id(("id", "username", "pwd", "cookies"), account_id)
            res = Weibo(init_session=False).do_login(user, verifycode)
            # res = do_login(verifycode)
            if not res.get("status"):
                # 登录失败，账号或者密码错误，或者需要验证码
                self.send_fail_json(res.get("reason"), data={"needverify": res.get("needverify")})
                return

            # 登录成功
            data = dict(islogin=True, last_login_time=datetime.now())

            # cookies 入库
            cookies = res.get("cookies", "")
            if cookies:
                data.update(cookies=myjson.dumps(cookies))

            uniqueid = res.get("uniqueid", "")
            if uniqueid:
                data.update(uniqueid=uniqueid)

            userdomain = res.get("userdomain", "")
            if userdomain:
                data.update(userdomain=userdomain)

            weibouser_model.update({"id": account_id}, data)

            write_log("'{}'成功登录了微博(微博ID为：{})".format(self.user["id"], account_id), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboUserVerifycodeHandler(BaseHandler):
    """
    微博登录验证码
    """
    def prepare(self):
        # 重写父类prepare方法，不做任何验证
        pass

    def get(self, *args, **kwargs):
        verifycode_image = "{}/static/images/weibo/verifycode.png".format(project_dir)
        f = open(verifycode_image, "rb")
        verifycode = f.read()
        f.close()
        self.write(verifycode)


class WeiboProductListHandler(LayerListHandler):
    """
    微博产品列表
    """

    _table = Product._table
    _template = "weibo/product-list.html"
    _order_by = "create_time desc"

    def _handler_result_data(self, data, **kwargs):
        data = super()._handler_result_data(data)
        res = list()
        for td in data:
            if td["source"] == PRODUCT_SOURCE["weibo"]:
                td["types"] = PRODUCT_WEIBO_TYPES_LABELS[td["types"]]
                res.append(td)
        return res

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        self._do_request()


class WeiboProductAddHandler(BaseHandler):
    """
    添加微博产品
    """

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        """
        加载添加微博产品表单页
        :param args:
        :param kwargs:
        :return:
        """
        self.render("weibo/product-add.html", one="", types=PRODUCT_WEIBO_TYPES_LABELS)

    @power_check("WEIBO_MANAGE")
    def post(self, *args, **kwargs):
        """
        执行添加微博产品
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # 产品类型
            types = self.get_args("types")
            if is_empty(types):
                # 产品类型不能为空
                self.send_fail_json("产品类型不能为空")
                return

            # 产品名
            product_name = self.get_args("name")
            if is_empty(product_name):
                # 产品名不能为空
                self.send_fail_json("产品名不能为空")
                return

            # 产品单价
            price = self.get_args("price")
            if is_empty(price):
                # 产品单价不能为空
                self.send_fail_json("单价不能为空")
                return

            data = dict(
                source=PRODUCT_SOURCE["weibo"],
                types=types,
                name=product_name,
                price=price,
                create_time=datetime.now(),
            )

            # 备注
            comments = self.get_args("comments")
            if comments:
                data["comments"] = comments

            res = Product().add(data=data)
            if not res:
                self.send_fail_json("添加失败")
                return

            write_log("'{}'添加了一个微博产品(product_name为：{})".format(self.user["id"], product_name), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class WeiboProductEditHandler(BaseHandler):
    """
    修改微博产品
    """

    @power_check("WEIBO_MANAGE")
    def get(self, *args, **kwargs):
        """
        加载修改微博产品表单页
        :param args:
        :param kwargs:
        :return:
        """
        # 获取用户
        product_id = self.get_args("id", "")
        if is_empty(product_id):
            self.send_fail_json("用户id不能为空")
            return
        product = Product().get_one8id(product_id)
        if not product:
            self.send_fail_json("查无产品")
            return

        self.render("weibo/product-add.html", one=product, types=PRODUCT_WEIBO_TYPES_LABELS)

    @power_check("WEIBO_MANAGE")
    def post(self, *args, **kwargs):
        """
        执行修改微博产品
        :param args:
        :param kwargs:
        :return:
        """
        try:
            product_id = self.get_args("product_id", "")
            if is_empty(product_id):
                self.send_fail_json("产品id不能为空")
                return

            # 产品名
            name = self.get_args("name")
            if is_empty(name):
                # 产品名不能为空
                self.send_fail_json("产品名不能为空")
                return

            # 产品类型
            types = self.get_args("types")
            if is_empty(types):
                # 产品名不能为空
                self.send_fail_json("类型不能为空")
                return

            # 产品单价
            price = self.get_args("price")
            if is_empty(price):
                # 产品单价不能为空
                self.send_fail_json("单价不能为空")
                return

            data = dict(
                types=types,
                price=price,
                update_time=datetime.now(),
            )

            # 备注
            comments = self.get_args("comments")
            if comments:
                data["comments"] = comments

            res = Product().update(where={"id": product_id}, data=data)
            if not res:
                self.send_fail_json("修改失败")
                return

            write_log("'{}'修改了一个微博产品(ID为：{})".format(self.user["id"], product_id), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")

