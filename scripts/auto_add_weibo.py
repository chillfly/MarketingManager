"""
自动添加微博账号到平台的脚本
"""

import datetime
import sys
import os
from models.commondb import WeiboUser
from utils.myaescrypto import aes_encrypt

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_path)


def main():
    wb = WeiboUser()
    account_file = "{}/doc/weiboaccount.txt".format(project_path)
    with open(account_file, "r") as conn:

        account_pwd = conn.readline()
        while 1:
            if not account_pwd:
                break
            try:
                temp = account_pwd.split("----")
            except:
                continue

            account = temp[0].strip("-").strip()
            pwd = temp[1].strip("-").strip()
            data = {
                "username": account,
                "pwd": aes_encrypt(pwd),
                "create_time": datetime.datetime.now()
            }
            wb.add(data=data)
            account_pwd = conn.readline()


if __name__ == '__main__':
    main()
