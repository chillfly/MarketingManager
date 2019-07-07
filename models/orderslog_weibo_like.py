from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersLogWeiboLikeTable = Table("orderslog_weibo_like", meta, autoload=True, autoload_with=db_engine)


class OrdersLogWeiboLike(ManagerDB):
    _table = OrdersLogWeiboLikeTable
