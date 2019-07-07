from utils.mylogger import write_log
from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


SysUserTable = Table("sys_user", meta, autoload=True, autoload_with=db_engine)

# 启用enable
USER_ENABLE_OK = 1  # 启用
USER_ENABLE_NO = 0  # 禁用
USER_ENABLE_LABELS = {
    USER_ENABLE_OK: '启用',
    USER_ENABLE_NO: "禁用",
}

# 用户性别
USER_GENDER_UNKNOW = 1  # 未知
USER_GENDER_MAN = 2  # 男
USER_GENDER_WOMAN = 3  # 女
USER_GENDER_LABELS = {
    USER_GENDER_UNKNOW: '未知',
    USER_GENDER_MAN: "男",
    USER_GENDER_WOMAN: "女",
}


class SysUser(ManagerDB):
    _table = SysUserTable

    def get_one8namepwd(self, username="", pwd=""):
        if not username or not pwd:
            write_log("sys_user.SysUser.get_one(), username or pwd is empty")
            return None
        where = dict()
        where["enable"] = True
        where["name"] = username
        where["pwd"] = pwd
        return super().get_one(where)

    def update_login_ip(self, user_id, login_ip):
        if not user_id or not login_ip:
            write_log("sys_user.SysUser.update_login_ip(), user_id or login_ip is empty")
            return None
        where = dict()
        where["id"] = user_id
        data = dict(login_ip=login_ip)
        return super().update(where, data)
