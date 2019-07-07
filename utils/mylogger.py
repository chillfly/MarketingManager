import logging
import os
import datetime

from configs import settings


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日志类型
LOG_TYPE_ERROR = 1
LOG_TYPE_OPERATE = 2
LOG_TYPE_SCRIPT = 3


class Logger(object):
    def __init__(self, log_type=1):
        # 创建日志对象
        self.logger = logging.getLogger("manager")
        self.log_type = log_type
        self.file_handler = None

        # 创建FileHandler对象
        if log_type == LOG_TYPE_ERROR:
            # 错误日志
            log_path = "/logs/error"
            # 设置日志内容格式
            formatter = logging.Formatter(
                "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s",
                "%a %d %b %Y %H:%M:%S",
            )
        elif log_type == LOG_TYPE_OPERATE:
            # 操作日志
            log_path = "/logs/operate"
            # 设置日志内容格式，操作日志，去掉日志类型（CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET）
            formatter = logging.Formatter(
                "%(asctime)-15s %(filename)s %(lineno)d %(process)d %(message)s",
                "%a %d %b %Y %H:%M:%S",
            )
        elif log_type == LOG_TYPE_SCRIPT:
            # 脚本日志
            log_path = "/logs/script"
            # 设置日志内容格式
            formatter = logging.Formatter(
                "%(asctime)-15s %(filename)s %(lineno)d %(process)d %(message)s",
                "%a %d %b %Y %H:%M:%S",
            )

        # 拼接日志的绝对路径
        log_path = project_dir + log_path
        if not os.path.exists(log_path):
            # 日志文件不存在，创建之
            os.makedirs(log_path)
        log_file = "{}.log".format(datetime.datetime.now().strftime("%Y%m"))
        self.file_handler = logging.FileHandler("{}/{}".format(log_path, log_file))
        self.file_handler.setFormatter(formatter)

        # 设置日志格式和日志路径等
        self.logger.addHandler(self.file_handler)
        # 设置日志模式
        self.logger.setLevel(logging.ERROR)

    def write_log(self, logs):
        self.logger.error(logs)
        self.logger.removeHandler(self.file_handler)


def write_log(logs, log_type=LOG_TYPE_ERROR):
    """
    日志记录
    :param logs: 待写入的日志内容
    :param log_type: 日志类型
    :return:
    """
    if logs:
        Logger(log_type).write_log(logs)

