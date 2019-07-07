import requests
import random
import redis
from configs import settings
from utils import myjson
from models.product import PRODUCT_TYPES_WEIBO_LIKE, PRODUCT_TYPES_WEIBO_COMMENT_LIKE, PRODUCT_TYPES_WEIBO_FOLLOW, \
    PRODUCT_TYPES_WEIBO_FORWARD, PRODUCT_TYPES_WEIBO_COMMENT


pool = redis.ConnectionPool(host=settings.REDIS_HOST,
                            port=settings.REDIS_PORT,
                            decode_responses=settings.REDIS_DECODE_RESPONSE)
redis_conn = redis.Redis(connection_pool=pool)

REFRESH_CACHE = True


def redis_list_iter(name):
    """
    redis列表迭代器
    :param r:redis实例
    :param name: redis中的name，即：迭代name对应的列表
    :return: yield 返回 列表元素
    """
    list_count = redis_conn.llen(name)
    for index in range(list_count):
        yield redis_conn.lindex(name, index)


def get_request_header():
    res = dict()
    # 随机设置user-agent
    res["User-Agent"] = random.choice(settings.USER_AGENTS)
    return res


def get_rabbitmq_exchange_name(product_types=1):
    """
    根据产品类型获取交换机名称
    :param product_types:
    :return:
    """
    if product_types == PRODUCT_TYPES_WEIBO_LIKE:
        exchange_name = "exchange_weibo_like"
    elif product_types == PRODUCT_TYPES_WEIBO_COMMENT_LIKE:
        exchange_name = "exchange_weibo_comment_like"
    elif product_types == PRODUCT_TYPES_WEIBO_COMMENT:
        exchange_name = "exchange_weibo_comment"
    elif product_types == PRODUCT_TYPES_WEIBO_FORWARD:
        exchange_name = "exchange_weibo_forward"
    elif product_types == PRODUCT_TYPES_WEIBO_FOLLOW:
        exchange_name = "exchange_weibo_follow"
    else:
        exchange_name = "exchange_urgent"

    return "{}_{}".format(settings.RABBITMQ_PRE, exchange_name)


def get_cookie_jar(cookies):
    """
    根据cookies的json字符串，来获取一个RequestsCookieJar对象
    :param cookies: cookie的json字符串
    :return:RequestsCookieJar对象
    """
    # 添加cookie
    if not cookies:
        # 如果cookies为空，则必定刷不成功，直接返回
        return

    # 实例化cookiejar对象
    cookie_jar = requests.cookies.RequestsCookieJar()

    # 遍历cookie列表，设置到cookiejar中
    cookies = myjson.loads(cookies)
    for key, val in cookies.items():
        cookie_jar.set(key, val)

    return cookie_jar
