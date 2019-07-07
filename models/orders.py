from .product import PRODUCT_TYPES_WEIBO_LIKE, PRODUCT_TYPES_WEIBO_COMMENT_LIKE, PRODUCT_TYPES_WEIBO_COMMENT, \
    PRODUCT_TYPES_WEIBO_FOLLOW, PRODUCT_TYPES_WEIBO_FORWARD
from .orders_weibo_like import OrdersWeiboLike
from .orders_weibo_comment_like import OrdersWeiboCommentLike
from .orders_weibo_comment import OrdersWeiboComment
from .orders_weibo_forward import OrdersWeiboForward
from .orders_weibo_follow import OrdersWeiboFollow


# 订单表status状态
ORDER_STATUS_NEW = 0
ORDER_STATUS_DOING = 1
ORDER_STATUS_DONE = 2
ORDER_STATUS_CANCEL = 3
ORDER_STATUS_LABELS = {
    ORDER_STATUS_NEW: "新建",
    ORDER_STATUS_DOING: "处理中",
    ORDER_STATUS_DONE: "已完成",
    ORDER_STATUS_CANCEL: "已取消",
}

# 微博赞订单
ORDER_TYPES_WEIBO_LIKE = PRODUCT_TYPES_WEIBO_LIKE
# 微博评论赞订单
ORDER_TYPES_WEIBO_COMMENT_LIKE = PRODUCT_TYPES_WEIBO_COMMENT_LIKE
# 微博评论订单
ORDER_TYPES_WEIBO_COMMENT = PRODUCT_TYPES_WEIBO_COMMENT
# 微博关注订单
ORDER_TYPES_WEIBO_FOLLOW = PRODUCT_TYPES_WEIBO_FOLLOW
# 微博转发订单
ORDER_TYPES_WEIBO_FORWARD = PRODUCT_TYPES_WEIBO_FORWARD

ORDER_TYPES_LABELS = {
    ORDER_TYPES_WEIBO_LIKE: "微博赞",
    ORDER_TYPES_WEIBO_COMMENT_LIKE: "微博评论赞",
    ORDER_TYPES_WEIBO_COMMENT: "微博评论",
    ORDER_TYPES_WEIBO_FOLLOW: "微博关注",
    ORDER_TYPES_WEIBO_FORWARD: "微博转发",
}


def get_orders_obj(types=1):
    """
    根据产品类型，获取订单实体类
    :param types: 产品类型，或者说订单类型（订单类型由产品类型而来）
    :return:
    """
    if types == PRODUCT_TYPES_WEIBO_LIKE:
        # 微博赞

        # 实例化微博赞订单类
        orders = OrdersWeiboLike()

    elif types == PRODUCT_TYPES_WEIBO_FOLLOW:
        # 微博关注

        # 实例化微博关注订单类
        orders = OrdersWeiboFollow()

    elif types == PRODUCT_TYPES_WEIBO_FORWARD:
        # 微博关注

        # 实例化微博转发订单类
        orders = OrdersWeiboForward()

    elif types == PRODUCT_TYPES_WEIBO_COMMENT:
        # 微博关注

        # 实例化微博评论订单类
        orders = OrdersWeiboComment()

    elif types == PRODUCT_TYPES_WEIBO_COMMENT_LIKE:
        # 微博评论赞

        # 实例化微博评论赞订单类
        orders = OrdersWeiboCommentLike()

    return orders