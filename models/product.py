from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


ProductTable = Table("product", meta, autoload=True, autoload_with=db_engine)
# 产品类型
PRODUCT_SOURCE = {
    "weibo": 1,
}
# 微博产品类型
# 微博赞
PRODUCT_TYPES_WEIBO_LIKE = 1
# 微博评论赞
PRODUCT_TYPES_WEIBO_COMMENT_LIKE = 2
# 微博评论
PRODUCT_TYPES_WEIBO_COMMENT = 3
# 微博转发
PRODUCT_TYPES_WEIBO_FORWARD = 4
# 微博关注
PRODUCT_TYPES_WEIBO_FOLLOW = 5

PRODUCT_WEIBO_TYPES_LABELS = {
    PRODUCT_TYPES_WEIBO_LIKE: "微博赞",
    PRODUCT_TYPES_WEIBO_COMMENT_LIKE: "评论赞",
    PRODUCT_TYPES_WEIBO_COMMENT: "微博评论",
    PRODUCT_TYPES_WEIBO_FORWARD: "微博转发",
    PRODUCT_TYPES_WEIBO_FOLLOW: "微博关注",
}


class Product(ManagerDB):
    _table = ProductTable
