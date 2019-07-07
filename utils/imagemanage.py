import os
from utils.mylogger import write_log


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def image_save(content, filename=""):
    try:
        if not content:
            # 待写入的内容为空
            write_log("imagemanage.image_save()，待写入的内容为空")
            return

        # 申明使用全局变量
        global project_dir

        # 路径处理
        file_path = "{}/static/images".format(project_dir)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        if not filename:
            full_name = "{}/verifyimage.png".format(file_path)
        else:
            full_name = "{}/{}".format(file_path, filename)

        if isinstance(content, bytes):
            f = open(full_name, "wb")
        elif isinstance(content, str):
            f = open(full_name, "w")

        f.write(content)

        f.close()
    except Exception as ex:
        write_log("imagemanage.image_save() raise Exception, ex=".format(repr(ex)))
