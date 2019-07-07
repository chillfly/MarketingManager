from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersWeiboFollowTable = Table("orders_weibo_follow", meta, autoload=True, autoload_with=db_engine)


class OrdersWeiboFollow(ManagerDB):
    _table = OrdersWeiboFollowTable

