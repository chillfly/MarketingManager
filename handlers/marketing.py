"""
营销处理
"""
import sys
import re
from decimal import Decimal
from configs import settings
from .base import BaseHandler
from models.system import power_check
from models.product import Product
from models.managerdb import db_engine
from models.product import PRODUCT_SOURCE, PRODUCT_TYPES_WEIBO_LIKE, PRODUCT_TYPES_WEIBO_COMMENT_LIKE, \
    PRODUCT_TYPES_WEIBO_COMMENT, PRODUCT_TYPES_WEIBO_FORWARD, PRODUCT_TYPES_WEIBO_FOLLOW
from models.sys_user import SysUser
from utils.myfilter import is_empty
from utils.mylogger import write_log, LOG_TYPE_OPERATE
from utils.tradecore import dbengine_transaction, create_orders


def url_spec(**kwargs):
    return [
        (r'/marketing/weibo/like/?', MarketingWeiboLikeHandler, kwargs),  # 微博点赞
        (r'/marketing/weibo/comment/like/?', MarketingWeiboCommentLikeHandler, kwargs),  # 微博评论点赞
        (r'/marketing/weibo/comment/?', MarketingWeiboCommentHandler, kwargs),  # 微博评论
        (r'/marketing/weibo/forward/?', MarketingWeiboForwardHandler, kwargs),  # 微博转发
        (r'/marketing/weibo/follow/?', MarketingWeiboFollowHandler, kwargs),  # 微博关注
    ]


class MarketingWeibo(BaseHandler):
    """
    微博营销类
    """

    # 产品来源
    product_source = PRODUCT_SOURCE.get("weibo")
    # 产品类型，默认为微博赞
    product_types = PRODUCT_TYPES_WEIBO_LIKE
    # 模板
    template = "marketing/weibo.html"

    @power_check("MARKETING_WEIBO")
    def get(self, *args, **kwargs):
        where = {"source": self.product_source, "types": self.product_types}
        product = Product().get_one(where=where)
        self.render(
            self.template,
            product=product,
            commentlike="1" if product.types == PRODUCT_TYPES_WEIBO_COMMENT_LIKE else "0"
        )

    @power_check("MARKETING_WEIBO")
    def post(self, *args, **kwargs):
        try:
            # 产品id
            product_id = self.get_args("product_id")
            if is_empty(product_id):
                self.send_fail_json("产品id不能为空")
                return

            product = Product().get_one8id(product_id)

            # 微博地址
            weibo_url = self.get_args("weibo_url")
            res = re.match(r'^https://weibo\.com/\S*', weibo_url)
            if res is None:
                self.send_fail_json("微博地址不正确")
                return

            # 产品数量
            product_numbers = self.get_args("amount")
            res = re.match(r'^\d+$', str(product_numbers))
            if res is None:
                self.send_fail_json("数量必须为整数")
                return
            # 数量处理，乘以精度
            product_numbers = int(product_numbers) * settings.PRODUCT_BUY_PRECISION

            data = dict(
                user_id=self.user["id"],
                product_id=product_id,
                product_name=product.name,
                product_types=self.product_types,
                product_price=product.price,
                product_numbers=product_numbers,
                weibo_url=weibo_url,
            )

            if product.types == PRODUCT_TYPES_WEIBO_COMMENT_LIKE:
                # 如果是微博评论赞，则必须要一个评论id
                comment_id = self.get_args("comment_id", "")
                if not comment_id:
                    self.send_fail_json("评论id不能为空")
                    return
                data.update(comment_id=comment_id)

            # 备注
            comments = self.get_args("comments")
            if not is_empty(comments):
                data.update(comments=comments)

            # 查看用户账户余额是否足够支撑本次订单
            user = SysUser().get_one8id(self.user["id"])
            if (user.balance - product_numbers * product.price) < 0:
                self.send_fail_json("创建订单失败，账户余额不足")
                return

            # 创建订单
            res = db_engine.transaction(
                dbengine_transaction,
                func=create_orders,
                user=user,
                order_data=data)
            if not res:
                self.send_fail_json("创建订单失败")
                return

            write_log("'{}'添加了一个订单(product_id：{}，产品名为：{}，数量为：{}，单价为：{})".format(
                user["id"], product_id, product.name, product_numbers, product.price),
                LOG_TYPE_OPERATE)
            self.send_ok_json("创建订单成功，可去\"个人中心->我的订单\"中查看")
        except Exception as ex:
            write_log("{}.{} raise exception, ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)
            ))
            self.send_fail_json("系统错误，稍会儿再试")


class MarketingWeiboLikeHandler(MarketingWeibo):
    """
    微博赞营销
    """
    product_types = PRODUCT_TYPES_WEIBO_LIKE


class MarketingWeiboCommentLikeHandler(MarketingWeibo):
    """
    微博评论赞营销
    """
    product_types = PRODUCT_TYPES_WEIBO_COMMENT_LIKE


class MarketingWeiboCommentHandler(MarketingWeibo):
    """
    微博评论营销
    """
    product_types = PRODUCT_TYPES_WEIBO_COMMENT


class MarketingWeiboForwardHandler(MarketingWeibo):
    """
    微博赞营销
    """
    product_types = PRODUCT_TYPES_WEIBO_FORWARD


class MarketingWeiboFollowHandler(MarketingWeibo):
    """
    微博赞营销
    """
    product_types = PRODUCT_TYPES_WEIBO_FOLLOW
