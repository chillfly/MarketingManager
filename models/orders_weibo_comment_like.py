from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersWeiboCommentLikeTable = Table("orders_weibo_comment_like", meta, autoload=True, autoload_with=db_engine)

class OrdersWeiboCommentLike(ManagerDB):
    _table = OrdersWeiboCommentLikeTable

