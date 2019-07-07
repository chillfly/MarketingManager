"""
交易核心数据处理
"""
import time
from decimal import Decimal
from datetime import datetime
from models.sys_user import SysUser
from models.sys_user_consume_log import SysUserConsumeLog
from utils.functions import get_rabbitmq_exchange_name
from models.orders import get_orders_obj
from utils.myrabbitmq.myrabbitmq import ExchangeRabbitMQ
from utils import myjson
from configs import settings


def dbengine_transaction(conn, **kwargs):
    """
    事务
    :param conn: 固定格式，不能删
    :param kwargs:
    :return:
    """
    func = kwargs.pop("func")
    res = func(**kwargs)
    if not res:
        # 如果结果为false，抛出异常，外部接收到异常后就会rollback
        raise Exception
    return res


def create_orders(user={}, order_data={}):
    """
    创建订单
    :param user:
    :param order_data:
    :return:
    """
    now = datetime.now()

    amount = Decimal(order_data["product_numbers"]) * Decimal(order_data["product_price"])
    balance_after = Decimal(user["balance"]) - amount

    if not user or not order_data or balance_after < 0:
        return False
    try:
        # 第一步：更新用户账户余额信息
        now_timestamp = int(time.time() * (10 ** 6))
        res = SysUser().update({"id": user["id"]}, {"balance": balance_after})
        if not res:
            return False

        # 第二步：创建订单
        # 更新订单字典
        order_data.update(create_time=now, order_number=now_timestamp)
        # 实例化订单实体
        orders = get_orders_obj(order_data["product_types"])
        order_res = orders.add(order_data)
        if not order_res:
            return False

        # 第三步：插入日志到用户消费日志表
        consume_log_data = {
            "user_id": user["id"],
            "amount": amount,
            "create_time": now,
            "comments": "购买“{}”产品，订单号为：{}".format(order_data["product_name"], now_timestamp)
        }
        log_res = SysUserConsumeLog().add(consume_log_data)
        if not log_res:
            return False

        # 第四步：将订单信息插入到消息队列rabbitmq中
        # 消息队列名称
        rabbit_exchange_name = get_rabbitmq_exchange_name(product_types=order_data["product_types"])
        # 待插入到消息队列中的数据
        rabbit_msg = dict(
            product_types=order_data["product_types"],
            product_numbers=order_data["product_numbers"],
            weibo_url=order_data["weibo_url"],
            order_id=order_res.lastrowid,
            comment_id=order_data.get("comment_id", "")
        )
        # 插入消息到消息队列
        res_status = ExchangeRabbitMQ(
            rabbitmq_host=settings.RABBITMQ_HOST,
            rabbitmq_port=settings.RABBITMQ_PORT,
            user_name=settings.RABBITMQ_USER,
            user_pwd=settings.RABBITMQ_PWD,
            virtual_host=settings.RABBITMQ_VIRTUAL_HOST
        ).sender(body=myjson.dumps(rabbit_msg), exchange_name=rabbit_exchange_name)
        if not res_status:
            return False

        return True
    except:
        return False


def user_charge(user_id, charge_num):
    try:

        # 检查支付账户余额是否满足此次充值
        payment_account = SysUser().get_one8id(settings.PaymentAccount)
        if payment_account.balance - charge_num < 0:
            # 支付账户余额不足
            return False

        # 更新支付账户余额
        res = SysUser().update(
            where={"id": payment_account.id},
            data={"balance": payment_account.balance - Decimal(charge_num)}
        )
        if not res:
            return False

        # 更新待充值账户余额
        user = SysUser().get_one8id(user_id)
        res = SysUser().update(where={"id": user_id}, data={"balance": user.balance + Decimal(charge_num)})
        if not res:
            return False

        return True
    except:
        return False



