from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


SysUserChargeLogTable = Table("sys_user_charge_log", meta, autoload=True, autoload_with=db_engine)


class SysUserChargeLog(ManagerDB):
    _table = SysUserChargeLogTable
