from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersWeiboLikeTable = Table("orders_weibo_like", meta, autoload=True, autoload_with=db_engine)


class OrdersWeiboLike(ManagerDB):
    _table = OrdersWeiboLikeTable

