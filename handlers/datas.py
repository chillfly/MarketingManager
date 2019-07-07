"""
数据管理
"""
from .base import LayerListHandler
from models.system import SysUser, power_check
from models.orders import ORDER_STATUS_LABELS, ORDER_TYPES_LABELS, get_orders_obj
from models.orderslog import get_orderslog_obj
from models.sys_user_consume_log import SysUserConsumeLog
from models.sys_user_charge_log import SysUserChargeLog
from models.product import PRODUCT_WEIBO_TYPES_LABELS


def url_spec(**kwargs):
    return [
        (r'/datas/user/orders/?', UserOrderListHandler, kwargs),
        (r'/datas/user/orders/log/?', UserOrdersLogListHandler, kwargs),
        (r'/datas/user/consume/log/?', UserConsumeLogListHandler, kwargs),  # 用户消费日志
        (r'/datas/user/charge/log/?', UserChargeLogListHandler, kwargs),  # 用户充值日志
    ]


class UserOrderListHandler(LayerListHandler):
    """
    用户订单列表
    """

    _template = "datas/user-orders-list.html"
    _order_by = "create_time desc"
    _table_query_args = ("id", "order_number", "user_id",)
    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = []
        return {}, add_where

    def _handler_result_data(self, data, **kwargs):
        for td in data:
            td["product_types"] = PRODUCT_WEIBO_TYPES_LABELS[td["product_types"]]
            td["status"] = ORDER_STATUS_LABELS[td["status"]]
        return data

    @power_check("DATA_MANAGE")
    def get(self, *args, **kwargs):
        order_types_default = list(ORDER_TYPES_LABELS.keys())[0]
        order_types = self.get_args("order_types", order_types_default, data_type=int)
        obj = get_orders_obj(order_types)
        self._table = obj._table

        self._do_request(order_types_labels=ORDER_TYPES_LABELS)


class UserOrdersLogListHandler(LayerListHandler):
    """
    用户订单处理日志列表
    """

    _template = "datas/user-orders-log.html"
    _order_by = "create_time desc"
    _table_query_args = ("order_id",)
    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = []
        return {}, add_where

    @power_check("DATA_MANAGE")
    def get(self, *args, **kwargs):
        order_types_default = list(ORDER_TYPES_LABELS.keys())[0]
        order_types = self.get_args("order_types", order_types_default, data_type=int)
        obj = get_orderslog_obj(order_types)
        self._table = obj._table

        self._do_request(order_types_labels=ORDER_TYPES_LABELS)


class UserConsumeLogListHandler(LayerListHandler):
    """
    用户消费日志
    """

    _table = SysUserConsumeLog._table
    _template = "datas/user-consume-log.html"
    _order_by = "create_time desc"
    _table_query_args = ("user_id",)
    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = []
        return {}, add_where

    @power_check("DATA_MANAGE")
    def get(self, *args, **kwargs):
        self._do_request()


class UserChargeLogListHandler(LayerListHandler):
    """
    用户充值日志
    """

    _table = SysUserChargeLog._table
    _template = "datas/user-charge-log.html"
    _order_by = "create_time desc"
    _table_query_args = ("user_id",)
    _ex_query_args = ("time",)  # 拓展查询列 额外处理

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        add_where = []
        return {}, add_where

    @power_check("DATA_MANAGE")
    def get(self, *args, **kwargs):
        self._do_request()
