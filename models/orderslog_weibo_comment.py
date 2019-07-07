from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersLogWeiboCommentTable = Table("orderslog_weibo_comment", meta, autoload=True, autoload_with=db_engine)


class OrdersLogWeiboComment(ManagerDB):
    _table = OrdersLogWeiboCommentTable
