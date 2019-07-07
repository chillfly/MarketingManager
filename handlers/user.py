import sys
from decimal import Decimal
from datetime import datetime
from .base import BaseHandler, LayerListHandler, db_engine
from models.system import SysUser, power_check
from models.orders import ORDER_STATUS_LABELS, ORDER_TYPES_LABELS, get_orders_obj
from models.sys_user_consume_log import SysUserConsumeLog
from models.sys_user_charge_log import SysUserChargeLog
from models.product import PRODUCT_WEIBO_TYPES_LABELS
from utils.myfilter import is_pwd, is_empty, decimal_to_str
from utils.mylogger import write_log, LOG_TYPE_OPERATE


def url_spec(**kwargs):
    return [
        (r'/user/info/?', SysUserInfoHandler, kwargs),
        (r'/user/pwd/?', SysUserEditPwdHandler, kwargs),
        (r'/user/charge/?', SysUserChargeHandler, kwargs),

        (r'/user/orders/?', UserOrderListHandler, kwargs),  # 用户订单列表
        (r'/user/log/consume/?', UserConsumeLogHandler, kwargs),  # 用户消费日志
        (r'/user/log/charge/?', UserChargeLogHandler, kwargs),  # 用户充值日志
    ]


class SysUserInfoHandler(BaseHandler):
    """
    修改用户基本信息
    """

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        # 用户个人信息
        user = SysUser().get_one8id(self.user["id"])
        self.render("user/user-info.html", user=user)

    @power_check("USER_CENTER")
    def post(self, *args, **kwargs):
        try:
            data = dict()

            real_name = self.get_args("real_name")
            if real_name:
                data.update(real_name=real_name)

            tel = self.get_args("tel")
            if tel:
                data.update(tel=tel)

            email = self.get_args("email")
            if email:
                data.update(email=email)

            gender = self.get_args("gender")
            if gender:
                data.update(gender=gender)

            birthday = self.get_args("birthday")
            if birthday:
                data.update(birthday=birthday)

            comments = self.get_args("comments")
            if comments:
                data.update(comments=comments)

            cache_user = self.user
            if not cache_user:
                # 缓存为空，跳转到登录页
                self.redirect("/login/")
                return

            # 更新用户数据表
            res = SysUser().update({"id": cache_user.get("id", "")}, data)
            if not res:
                self.send_fail_json("修改失败")
                return

            # 更新用户缓存
            self.update_user_cache(data)

            write_log("'{}'修改了个人信息".format(self.user["id"]), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class SysUserEditPwdHandler(BaseHandler):
    """
    修改用户登录密码
    """

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        # 用户个人信息
        user = SysUser().get_one8id(self.user["id"])
        self.render("user/user-pwd.html", user=user)

    @power_check("USER_CENTER")
    def post(self, *args, **kwargs):
        try:
            cache_user = self.user
            password1 = self.get_args("password1")
            if not password1:
                self.send_fail_json("旧密码不能为空")
                return

            password2 = self.get_args("password2")
            if not password2:
                self.send_fail_json("新密码不能为空")
                return

            password3 = self.get_args("password3")
            if not password3:
                self.send_fail_json("重复密码不能为空")
                return

            if password2 != password3:
                self.send_fail_json("新密码必须一致")
                return

            if not is_pwd(password2):
                self.send_fail_json("密码格式不正确")
                return

            user_model = SysUser()
            res = user_model.get_one8namepwd(username=cache_user["name"], pwd=self.md5_password(password1))
            if not res:
                self.send_fail_json("旧密码错误")
                return

            # 更新数据库
            pwd = self.md5_password(password2)
            data = dict(pwd=pwd)
            update_res = user_model.update({"id": cache_user.get("id", "")}, data)
            if not update_res:
                self.send_fail_json("修改密码失败")
                return

            # 更新缓存
            self.update_user_cache({"pwd": pwd})

            write_log("'{}'修改了登录密码，修改后的密码为：{}".format(self.user["id"], password2), LOG_TYPE_OPERATE)
            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class SysUserChargeHandler(BaseHandler):
    """
    用户充值
    """

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        # 用户个人信息
        user = SysUser().get_one8id(self.user["id"])
        self.render("user/user-charge.html", user=user)

    @power_check("USER_CENTER")
    def post(self, *args, **kwargs):
        try:

            if not self.user:
                # 缓存为空，跳转到登录页
                self.redirect("/login/")
                return

            user = SysUser().get_one8id(self.user["id"])

            # todo 收款成功，则修改用户余额
            # pass

            charge_num = self.get_args("charge_num")
            if is_empty(charge_num):
                self.send_fail_json("充值金额不能为空")
                return
            user_balance = Decimal(user.balance) + Decimal(charge_num)

            with db_engine.connect() as conn:
                tran = conn.begin()
                try:
                    # 更新用户数据表
                    res = SysUser().update({"id": user.id}, {"balance": user_balance})
                    if not res:
                        tran.rollback()
                        self.send_fail_json("充值失败")
                        return

                    # 掺入用户充值记录
                    res = SysUserChargeLog().add({
                        "user_id": user.id,
                        "amount": charge_num,
                        "comments": "用户充值",
                        "create_time": datetime.now(),
                    })
                    if not res:
                        tran.rollback()
                        self.send_fail_json("充值失败")
                        return

                    # 提交事务
                    tran.commit()
                except Exception as ex:
                    tran.rollback()
                    write_log("{}.{} raise exception, ex={}".format(
                        self.__class__.__name__,
                        sys._getframe().f_code.co_name,
                        repr(ex)
                    ))
                    self.send_fail_json("充值失败，稍会儿再试")

            self.send_ok_json("")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class UserOrderListHandler(LayerListHandler):
    """
    用户订单列表
    """

    _template = "user/user-orders-list.html"
    _order_by = "create_time desc"
    _ex_query_args = ("time",)  # 拓展查询列 额外处理
    _table_query_args = ("order_number",)

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = [self._table.c.user_id == self.user["id"]]
        return {}, add_where

    def _handler_result_data(self, data, **kwargs):
        for td in data:
            td["product_types"] = PRODUCT_WEIBO_TYPES_LABELS[td["product_types"]]
            td["status"] = ORDER_STATUS_LABELS[td["status"]]
        return data

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        order_types_default = list(ORDER_TYPES_LABELS.keys())[0]
        order_types = self.get_args("order_types", order_types_default, data_type=int)
        obj = get_orders_obj(order_types)
        self._table = obj._table

        self._do_request(order_types_labels=ORDER_TYPES_LABELS)


class UserConsumeLogHandler(LayerListHandler):
    """
    用户消费日志
    """

    _table = SysUserConsumeLog._table
    _template = "user/user-consume-log.html"
    _order_by = "create_time desc"

    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = [self._table.c.user_id == self.user["id"]]
        return {}, add_where

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        self._do_request()


class UserChargeLogHandler(LayerListHandler):
    """
    用户充值日志
    """

    _table = SysUserChargeLog._table
    _template = "user/user-charge-log.html"
    _order_by = "create_time desc"
    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = [self._table.c.user_id == self.user["id"]]
        return {}, add_where

    @power_check("USER_CENTER")
    def get(self, *args, **kwargs):
        self._do_request()
