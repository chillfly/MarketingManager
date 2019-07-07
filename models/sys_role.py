from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


RoleTable = Table("sys_role", meta, autoload=True, autoload_with=db_engine)

# 用户类型
ROLE_TYPE_SP_ADMIN = 99  # 超级管理员用户, 无视所有权限
ROLE_TYPE_ADMIN = 98  # 普通管理员 受各种权限控制, 可以添加用户和菜单
ROLE_TYPE_NORMAL = 1  # 普通用户 受权限控制 不能添加用户和菜单
ROLE_TYPES = {ROLE_TYPE_SP_ADMIN, ROLE_TYPE_ADMIN, ROLE_TYPE_NORMAL}
ROLE_TYPE_LABELS = {
    ROLE_TYPE_SP_ADMIN: '超级管理员',
    ROLE_TYPE_ADMIN: "普通管理员",
    ROLE_TYPE_NORMAL: "普通用户",
}


class Role(ManagerDB):
    _table = RoleTable