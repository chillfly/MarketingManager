from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersLogWeiboFollowTable = Table("orderslog_weibo_follow", meta, autoload=True, autoload_with=db_engine)


class OrdersLogWeiboFollow(ManagerDB):
    _table = OrdersLogWeiboFollowTable
