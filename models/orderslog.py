from .product import PRODUCT_TYPES_WEIBO_LIKE, PRODUCT_TYPES_WEIBO_COMMENT_LIKE, PRODUCT_TYPES_WEIBO_COMMENT, \
    PRODUCT_TYPES_WEIBO_FOLLOW, PRODUCT_TYPES_WEIBO_FORWARD
from .orderslog_weibo_like import OrdersLogWeiboLike
from .orderslog_weibo_comment_like import OrdersLogWeiboCommentLike
from .orderslog_weibo_comment import OrdersLogWeiboComment
from .orderslog_weibo_forward import OrdersLogWeiboForward
from .orderslog_weibo_follow import OrdersLogWeiboFollow


def get_orderslog_obj(types=1):
    """
    根据产品类型，获取订单日志实体类
    :param types: 产品类型，或者说订单类型（订单类型由产品类型而来）
    :return:
    """
    if types == PRODUCT_TYPES_WEIBO_LIKE:
        # 微博赞

        # 实例化微博赞订单日志类
        orderslog = OrdersLogWeiboLike()

    elif types == PRODUCT_TYPES_WEIBO_FOLLOW:
        # 微博关注

        # 实例化微博关注订单日志类
        orderslog = OrdersLogWeiboFollow()

    elif types == PRODUCT_TYPES_WEIBO_FORWARD:
        # 微博关注

        # 实例化微博转发订单日志类
        orderslog = OrdersLogWeiboForward()

    elif types == PRODUCT_TYPES_WEIBO_COMMENT:
        # 微博关注

        # 实例化微博评论订单日志类
        orderslog = OrdersLogWeiboComment()

    elif types == PRODUCT_TYPES_WEIBO_COMMENT_LIKE:
        # 微博评论赞

        # 实例化微博评论赞订单日志类
        orderslog = OrdersLogWeiboCommentLike()

    return orderslog