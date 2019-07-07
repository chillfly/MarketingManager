"""
rabbitmq 消息队列处理
"""
import sys
import pika
from utils import myjson
from utils.weibo import weibo_login
from configs import settings


class MyRabbitMQ(object):
    def __init__(self, rabbitmq_host="", rabbitmq_port=0, user_name="", user_pwd="", virtual_host="", no_ack=False):
        self.rabbitmq_host = rabbitmq_host or "localhost"
        self.rabbitmq_port = rabbitmq_port or 5672
        self.user_name = user_name or "test"
        self.user_pwd = user_pwd or "test"
        self.virtual_host = virtual_host or "/test"

        # 默认为False，就是说要回调，就是说要手动告诉rabbitmq说该消息已经处理过了，让rabbitmq从队列中删除掉这个消息
        self.no_ack = no_ack

    def get_connection(self):
        if not self.rabbitmq_host or not self.rabbitmq_port or not self.user_name or not self.user_pwd or not self.virtual_host:
            # 主机、端口、用户名、用户密码、虚拟主机，任何一项为空，则返回None
            return
        try:
            credentials = pika.PlainCredentials(self.user_name, self.user_pwd)
            conn_params = pika.ConnectionParameters(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                virtual_host=self.virtual_host,
                credentials=credentials)

            # 创建连接，默认端口为5672
            conn = pika.BlockingConnection(conn_params)
        except:
            conn = None
        finally:
            return conn

    def sender(self, **kwargs):
        """
        定义生产者，发送消息
        :param kwargs:参数
        :return: True，发送成功；False，发送失败
        """
        pass

    def receiver(self, **kwargs):
        """
        定义消费者接收消息
        :param kwargs:参数
        :return:
        """
        pass

    def receiver_callback(self, channel, method, properties, body):
        """
        接收者接收到消息时的回调方法，可以在该回调方法里做消息的处理
        :param channel: 管道对象
        :param method:
        :param properties:
        :param body:
        :return:
        """
        pass


class SimpleRabbitMQ(MyRabbitMQ):
    """
    简单模式
    模型：一个队列，一个消费者，不存在谁先干完，谁后干完，就不存在消息分配的问题
    """

    def sender(self, queue_name="", body=""):
        """
        定义生产者，发送消息
        :param queue_name:队列名称
        :param body: 消息内容
        :return: True，发送成功；False，发送失败
        """
        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return False

        try:
            # 使用连接创建通道
            channel = conn.channel()

            # 使用通道创建队列
            # durable=True，声明队列永久化
            channel.queue_declare(queue=queue_name, durable=True)

            # 使用通道像队列发送消息，routing_key必须为队列名称，这样消费者才能收到消息
            # properties=pika.BasicProperties(delivery_mode=2)，声明消息永久化
            channel.basic_publish(exchange="", routing_key=queue_name, body=body,
                                  properties=pika.BasicProperties(delivery_mode=2))

            print("sented")

            # 关闭通道
            channel.close()

            # 关闭连接
            conn.close()

            return True
        except Exception as ex:
            print("[{}.sender]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            return False

    def receiver(self, queue_name=""):
        """
        定义消费者接收消息
        :param queue_name:队列名称
        :return:
        """
        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return

        try:
            # 创建通道
            channel = conn.channel()

            # 使用通道创建队列（消费者只跟队列相关，所以此处不必声明交换机）
            # durable=True，声明队列永久化
            channel.queue_declare(queue=queue_name, durable=True)

            # 绑定消费者
            channel.basic_consume(
                self.receiver_callback,
                queue=queue_name,
                no_ack=self.no_ack,
            )
            print("[{}.receiver] queue={}, Wating for messages. To exit press CTRL+C".format(self.__class__.__name__,
                                                                                             queue_name))
            channel.start_consuming()

        except Exception as ex:
            print("[{}.receiver]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))

    def receiver_callback(self, channel, method, properties, body):
        """
        消费者回调函数（这四个参数是标准格式）
        :param channel: 管道对象
        :param method:
        :param properties:
        :param body:
        :return:
        """
        try:
            print(body)
            if not self.no_ack:
                # no_ack为True，显式给rabbitmq发送一个消息确认
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print("[{}.receiver_callback]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            pass


class WorkRabbitMQ(MyRabbitMQ):
    """
    工作队列模式
    模型：一个队列，多个消费者。正常情况下是依次分配。
    假如发了10条消息，只有2个消费者，那么最后肯定是各分5条消息；如果是3个消费者，那第一个消费者占4条，后两个消费者各3条。
    basic_qos的作用就是不依次分配，谁先处理完就给其分配消息
    """

    def sender(self, queue_name="", body=""):

        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return False

        try:
            # 使用连接创建通道
            channel = conn.channel()

            # 使用通道创建队列
            # durable=True，声明队列永久化
            channel.queue_declare(queue=queue_name, durable=True)

            # 使用通道像队列发送消息，routing_key必须为队列名称，这样消费者才能收到消息
            # properties=pika.BasicProperties(delivery_mode=2)，声明消息永久化
            channel.basic_publish(exchange="", routing_key=queue_name, body=body,
                                  properties=pika.BasicProperties(delivery_mode=2))

            # 关闭通道
            channel.close()

            # 关闭连接
            conn.close()

            return True
        except Exception as ex:
            print("[{}.sender]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            return False

    def receiver(self, queue_name=""):
        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return

        try:

            # 创建通道
            channel = conn.channel()

            # 使用通道创建队列
            # durable=True，声明队列永久化
            channel.queue_declare(queue=queue_name, durable=True)

            # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息
            channel.basic_qos(prefetch_count=1)

            # 绑定消费者
            channel.basic_consume(
                self.receiver_callback,
                queue=queue_name,
                no_ack=self.no_ack,
            )
            print("[{}.receiver]: queue={}, Wating for messages. To exit press CTRL+C".format(self.__class__.__name__,
                                                                                              queue_name))
            channel.start_consuming()

        except Exception as ex:
            print("[{}.receiver]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))

    def receiver_callback(self, channel, method, properties, body):
        """
        消费者回调函数（这四个参数是标准格式）
        :param channel: 管道对象
        :param method:
        :param properties:
        :param body:
        :return:
        """
        try:
            print(body)
            if not self.no_ack:
                # no_ack为False，显式给rabbitmq发送一个消息确认
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print("[{}.receiver_callback]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            pass


class ExchangeRabbitMQ(MyRabbitMQ):
    """
    交换机模式
    模型：一个交换机，多个队列，多个消费者
    发布订阅(fanout)模式：消息发送到交换机，交换机依次分配给队列，队列依次(如果设置了basic_qos，则哪个消费者先干完就先分配给它)分配给消费者
    路由(direct)模式：消息发送到交换机（指定一个routing_key的值），交换机将消息分配给指定了对应routing_key的队列，队列依次(如果设置了basic_qos，则哪个消费者先干完就先分配给它)分配给消费者
    通配符(topic)模式：消息发送到交换机（指定一个routing_key的值），交换机将消息分配给指定了对应routing_key的通配符的队列，队列依次(如果设置了basic_qos，则哪个消费者先干完就先分配给它)分配给消费者
    """

    def __init__(self, rabbitmq_host="", rabbitmq_port=0, user_name="", user_pwd="", virtual_host="", no_ack=False,
                 exchange_type="fanout"):
        super().__init__(rabbitmq_host=rabbitmq_host, rabbitmq_port=rabbitmq_port, user_name=user_name,
                         user_pwd=user_pwd, virtual_host=virtual_host, no_ack=False)
        self.exchange_type = exchange_type

    def sender(self, body="", exchange_name="", routing_key=""):
        """
        定义生产者，发送消息
        :param body: 消息内容
        :param exchange_name: 交换机名称
        :param routing_key: 路由key
        :return: True，发送成功；False，发送失败
        """
        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return False

        try:
            # 使用连接创建通道
            channel = conn.channel()

            # 定义一个交换机
            channel.exchange_declare(exchange=exchange_name, exchange_type=self.exchange_type)

            # 使用通道向交换机发送消息
            # 发布订阅模式是没有routing_key的，所以直接给“”
            # properties=pika.BasicProperties(delivery_mode=2)，声明消息永久化
            channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=body,
                                  properties=pika.BasicProperties(delivery_mode=2))

            # 关闭通道
            channel.close()

            # 关闭连接
            conn.close()

            return True
        except Exception as ex:
            print("[{}.sender]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            return False

    def receiver(self, queue_name="", exchange_name="", routing_key=""):
        """
        定义消费者接收消息
        :param queue_name: 队列名
        :param exchange_name: 交换机名
        :param routing_key: 路由key
        :return:
        """
        # 定义连接
        conn = self.get_connection()

        if not conn:
            # 定义连接失败
            return

        try:
            # 创建通道
            channel = conn.channel()

            # 定义一个交换机（虽说消费者是与交换机无关的，只是与队列相关的，但是会需要绑定到交换机，如果在此之前没有该交换机的话会报错）
            channel.exchange_declare(exchange=exchange_name, exchange_type=self.exchange_type)

            # 使用通道创建队列（消费者只跟队列相关，所以此处不必声明交换机）
            # durable=True，声明队列永久化
            channel.queue_declare(queue=queue_name, durable=True)

            # 绑定队列到交换机
            channel.queue_bind(queue_name, exchange_name, routing_key=routing_key)

            # 消费者给rabbitmq发送一个信息：在消费者处理完消息之前不要再给消费者发送消息
            channel.basic_qos(prefetch_count=1)

            # 绑定消费者
            channel.basic_consume(
                self.receiver_callback,
                queue=queue_name,
                no_ack=self.no_ack,
            )

            print("[{}.receiver]: exchange={},queue={}, Wating for messages. To exit press CTRL+C".format(
                self.__class__.__name__,
                exchange_name,
                queue_name))
            channel.start_consuming()

        except Exception as ex:
            print("[{}.receiver]: raise exception,ex={}".format(self.__class__.__name__, repr(ex)))

    def receiver_callback(self, channel, method, properties, body):
        try:
            print("[{}.receiver_callback]: 接收到了消息，消息内容为：{}".format(self.__class__.__name__, body))
            # 将消息转化为字典格式
            msg = myjson.loads(body.decode("utf-8"))
            # 执行点赞脚本
            weibo_login.do_script(msg)

            if not self.no_ack:
                # no_ack为True，显式给rabbitmq发送一个消息确认
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as ex:
            print("{}.receiver_callback raise exception,ex={}".format(self.__class__.__name__, repr(ex)))
            pass


if __name__ == "__main__":
    arg = sys.argv[1]

    # mq = SimpleRabbitMQ()
    # if arg == "send":
    #     # 发送方
    #     mq.sender(queue_name="test_simple_queue2", body="simple msg")
    # else:
    #     # 接收方
    #     mq.receiver(queue_name="test_simple_queue2")

    # mq = WorkRabbitMQ()
    # if arg == "send":
    #     # 发送方
    #     for i in range(10):
    #         mq.sender(queue_name="test_work", body="workmsg,i={}".format(i))
    # else:
    #     # 接收方
    #     mq.receiver(queue_name="test_work")

    mq = ExchangeRabbitMQ(
        rabbitmq_host=settings.RABBITMQ_HOST,
        rabbitmq_port=settings.RABBITMQ_PORT,
        exchange_type="direct",
        user_name=settings.RABBITMQ_USER,
        user_pwd=settings.RABBITMQ_PWD,
        virtual_host=settings.RABBITMQ_VIRTUAL_HOST
    )
    if arg == "send":
        # 发送方
        mq.sender(body="exchange msg", exchange_name="test_exchange_exchange4",
                  routing_key="hahaa")
    else:
        # 接收方
        mq.receiver(queue_name="test_exchange_queue", exchange_name="test_exchange_exchange4", routing_key="haha")
