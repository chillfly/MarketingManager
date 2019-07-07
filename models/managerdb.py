from .base_sql import BaseSql
from sqlalchemy import create_engine, MetaData
from configs import settings


db_engine = create_engine(
    settings.MANAGER_DB + '?charset=utf8',
    encoding=settings.DB_ENCODE,
    convert_unicode=settings.DB_CONVERT_UNICODE,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE_TIMEOUT,
    echo=settings.DB_ECHO,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
)
meta = MetaData(db_engine)

# 是否删除
ISDEL_OK = 1  # 是
ISDEL_NO = 0  # 否
ISDEL_LABELS = {
    ISDEL_OK: '是',
    ISDEL_NO: "否",
}


class ManagerDB(BaseSql):
    _engine = db_engine
