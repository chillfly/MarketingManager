from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersWeiboForwardTable = Table("orders_weibo_forward", meta, autoload=True, autoload_with=db_engine)


class OrdersWeiboForward(ManagerDB):
    _table = OrdersWeiboForwardTable

