"""
通过脚本创建平台用户，一般用于一个用户都没有的时候，用来初始化一个原始用户，后续的用户可以用原始用户通过平台来添加
"""

import datetime
import hashlib
import os
import sys
from models.sys_user import SysUser

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)

from configs import settings


def main():
    data = dict(
        role_id=1,
        name="admin",
        pwd=hashlib.md5("000000{}".format(settings.PLATFORM_USER_PASSWORD_SECRET).encode("utf-8")).hexdigest(),
        enable=True,
        comments="超管",
        create_time=datetime.datetime.now(),
    )

    SysUser().add(data=data)


if __name__ == '__main__':
    main()
