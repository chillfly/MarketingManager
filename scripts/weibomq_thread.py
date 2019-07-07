"""
微博mq消息线程脚本
针对不同的微博产品类型，各自开启一个交换机N个队列的线程，如：
微博点赞产品：
    开启一个交换机，名为：exchange_weibo_like
    该交换机下开启5个队列，分别是：
        exchange_weibo_like_queue_0
        exchange_weibo_like_queue_1
        exchange_weibo_like_queue_2
        exchange_weibo_like_queue_3
        exchange_weibo_like_queue_4

微博评论赞产品：
    开启一个交换机，名为：exchange_weibo_comment_like
    该交换机下开启5个队列，分别是：
        exchange_weibo_comment_like_queue_0
        exchange_weibo_comment_like_queue_1
        exchange_weibo_comment_like_queue_2
        exchange_weibo_comment_like_queue_3
        exchange_weibo_comment_like_queue_4

等等。。。
"""

import sys
import os
import threading
import time
import logging
this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from configs import settings
from utils import functions as func
from utils.myrabbitmq import weibomq
from models import product


logging.basicConfig(level=logging.INFO)
rabbitmq_receivers = {}


def main():
    while 1:
        try:
            for key in product.PRODUCT_WEIBO_TYPES_LABELS.keys():
                # 遍历微博产品列表
                exchange_name = func.get_rabbitmq_exchange_name(key)
                for i in range(settings.RABBITMQ_QUEUE_NUMBERS_EVERY_EXCHANGE):
                    # 根据指定的次数，开启指定次数个队列
                    queue_name = "{}_queue_{}".format(exchange_name, i)

                    curr_th = rabbitmq_receivers.get(queue_name)
                    if curr_th is None or not curr_th.is_alive():
                        # 如果当前队列的进程不是活跃状态，则重新启动一个线程来指向当前队列
                        temp_mq = weibomq.WeiboMQ(
                            rabbitmq_host=settings.RABBITMQ_HOST,
                            rabbitmq_port=settings.RABBITMQ_PORT,
                            user_name=settings.RABBITMQ_USER,
                            user_pwd=settings.RABBITMQ_PWD,
                            virtual_host=settings.RABBITMQ_VIRTUAL_HOST
                        )
                        th = threading.Thread(target=temp_mq.receiver,
                                              kwargs=dict(exchange_name=exchange_name, queue_name=queue_name))
                        th.start()
                        rabbitmq_receivers[queue_name] = th
        except Exception as ex:
            logging.error("[main]: weibo_script.py main() raise Exception,ex={}".format(repr(ex)))

        # 5秒钟重新循环检测一遍
        time.sleep(5)


if __name__ == "__main__":
    main()

