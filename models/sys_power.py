from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


PowerTable = Table("sys_power", meta, autoload=True, autoload_with=db_engine)


class Power(ManagerDB):
    _table = PowerTable


