from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


SysUserConsumeLogTable = Table("sys_user_consume_log", meta, autoload=True, autoload_with=db_engine)


class SysUserConsumeLog(ManagerDB):
    _table = SysUserConsumeLogTable
