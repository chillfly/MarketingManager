from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersLogWeiboForwardTable = Table("orderslog_weibo_forward", meta, autoload=True, autoload_with=db_engine)


class OrdersLogWeiboForward(ManagerDB):
    _table = OrdersLogWeiboForwardTable
