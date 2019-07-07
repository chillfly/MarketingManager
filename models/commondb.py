from sqlalchemy import Table
from .base_sql import BaseSql
from sqlalchemy import create_engine, MetaData
from configs import settings

common_db_engine = create_engine(
    settings.COMMON_DB + '?charset=utf8',
    encoding=settings.DB_ENCODE,
    convert_unicode=settings.DB_CONVERT_UNICODE,
    pool_size=settings.DB_POOL_SIZE,
    pool_recycle=settings.DB_POOL_RECYCLE_TIMEOUT,
    echo=settings.DB_ECHO,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
)
common_meta = MetaData(common_db_engine)

IpproxyTable = Table("free_ipproxy", common_meta, autoload=True, autoload_with=common_db_engine)
HttpbinTable = Table("httpbin", common_meta, autoload=True, autoload_with=common_db_engine)
WeiboUserTable = Table("weibo_user", common_meta, autoload=True, autoload_with=common_db_engine)

IsWeiboNotLogin = 0
IsWeiboLogin = 1
IsWeiboLoginLabel = {
    IsWeiboNotLogin: "未登录",
    IsWeiboLogin: "已登录",
}


class CommonDB(BaseSql):
    _engine = common_db_engine


class Ipproxy(CommonDB):
    _table = IpproxyTable


class Httpbin(CommonDB):
    _table = HttpbinTable


class WeiboUser(CommonDB):
    _table = WeiboUserTable