import os
from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado.options import define, options, parse_command_line
from configs import settings


# region tornado模块介绍
#
# tornado.httpserver
# 解决web服务器的http协议问题，实现客户端和服务端的胡同，非阻塞、单线程
#
# tornado.ioloop
# 实现非阻塞socket循环，不能胡同一次就结束
#
# tornado.options
# 命令行解析模块
#
# tornado.web
# 核心！提供web框架与异步，从而使其扩展到大量打开的连接，使其成为理想的长论询
#
# endregion

# 定义监听端口
define("port", default=settings.PORT, help="默认端口，9000")
define("debug", settings.DEBUG, "是否调试模式")
define("template_path", default=os.path.join(os.path.dirname(__file__), "templates"), help="模板路径")
define("static_path", default=os.path.join(os.path.dirname(__file__), "static"), help="静态文件路径")


class MyApplication(web.Application):
    def __init__(self):
        handler_list = [os.path.splitext(item)[0] for item in os.listdir("handlers")]
        handlers = list()
        for handler in handler_list:
            module = __import__("handlers."+handler, fromlist=["url_spec"])
            if hasattr(module, "url_spec"):
                handlers.extend(module.url_spec())
        config = dict(
            template_path=options.template_path,
            static_path=options.static_path,
            debug=options.debug,
            cookie_secret=settings.PLATFORM_COOKIE_SECRET,
            login_url=r"/login/",
            xsrf_cookies=True,  # 开启xsrf防御机制
        )
        super().__init__(handlers=handlers, **config)


def main():
    # 开始监听命令行数据
    parse_command_line()

    # 构建web项目
    myapplication = MyApplication()

    # 项目部署
    server = httpserver.HTTPServer(myapplication)
    # # 绑定端口，并启动
    # server.listen(options.port)
    # 绑定端口
    server.bind(options.port, address=settings.HOST)
    # 启动
    if options.debug:
        # 调试模式
        server.start()
    else:
        # 非调试模式，开启多个进程
        server.start(settings.DEFAULT_PROCESS_NUM)

    # 论询监听
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
