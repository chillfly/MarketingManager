"""
定期自动登录微博
"""
import sys
import os
this_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(this_dir, '..'))
from models.commondb import WeiboUser
from utils import myaescrypto, myproxy
from utils.weibo import weibo_login


def main():
    proxy_obj = myproxy.TaiyangProxy()
    weibo_user = WeiboUser()
    generator = weibo_user.get_some_generator()
    for user_list in generator:
        proxy_list = proxy_obj.get_proxies_direct(len(user_list))
        for index, user in enumerate(user_list):
            wb = weibo_login.Weibo(
                user_name=user.username,
                password=myaescrypto.aes_decrypt(user.pwd),
                proxy=proxy_list[index],
            )
            islogin = wb.check_login(user.cookies, user.headers)
            if islogin is None:
                # 异常了，则不做处理
                continue

            if not islogin:
                # 未登录，将登录状态字段改为false
                res = wb.login()
                if res["status"]:
                    # 登录成功
                    data = {
                        "islogin": True,
                        "cookies": res["cookies"],
                        "headers": res["headers"],
                        "uniqueid": res["uniqueid"],
                        "userdomain": res["userdomain"],
                    }
                    WeiboUser().update({"id": user.id}, data)
                else:
                    # 登录失败
                    WeiboUser().update({"id": user.id}, {"islogin": False, "cookies": ""})


if __name__ == "__main__":
    main()




