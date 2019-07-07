from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


OrdersLogWeiboCommentLikeTable = Table("orderslog_weibo_comment_like", meta, autoload=True, autoload_with=db_engine)


class OrdersLogWeiboCommentLike(ManagerDB):
    _table = OrdersLogWeiboCommentLikeTable
