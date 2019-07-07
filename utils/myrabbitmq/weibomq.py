from .myrabbitmq import ExchangeRabbitMQ
from utils import myjson
from utils.weibo import weibo_worker


class WeiboMQ(ExchangeRabbitMQ):
    def receiver_callback(self, channel, method, properties, body):
        try:
            print("[{}.receiver_callback]: 接收到了消息，消息内容为：{}".format(self.__class__.__name__, body))
            # 将消息转化为字典格式
            msg = myjson.loads(body.decode("utf-8"))
            # 执行点赞脚本
            weibo_worker.do_script(msg)

            if not self.no_ack:
                # no_ack为True，显式给rabbitmq发送一个消息确认
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print("[{}.receiver_callback]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            pass