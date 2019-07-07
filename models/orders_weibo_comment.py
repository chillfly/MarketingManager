from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersWeiboCommentTable = Table("orders_weibo_comment", meta, autoload=True, autoload_with=db_engine)


class OrdersWeiboComment(ManagerDB):
    _table = OrdersWeiboCommentTable

