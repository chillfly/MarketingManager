import sys
from utils.mylogger import write_log
from sqlalchemy import select


class BaseSql(object):
    _engine = None  # 数据库引擎
    _table = None  # 表，sqlalchemy.Table类

    def get_one8id(self, id):
        """
        根据id获取某条数据
        :param id:
        :return:
        """
        if not id:
            write_log("function {}.get_one8id() no id")
            return None
        where = dict()
        where["id"] = id
        return self.get_one(where)

    def get_one_specific_fields8id(self, fields, id=0):
        """
        根据id获取某条数据（指定字段）
        :param fields: 待查找的字段列表
        :param id:
        :return:
        """
        try:
            if not fields or not id:
                None
            with self._engine.connect() as conn:
                sql = select([getattr(self._table.c, rn) for rn in fields]).where(self._table.c.id==id).limit(1)
                res = conn.execute(sql).fetchone()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_one(self, where, orderby=""):
        """
        根据条件获取一条记录
        :param where:
        :param orderby:
        :return:
        """
        try:
            if not where:
                None
            with self._engine.connect() as conn:
                sql = self._table.select()
                sql = self._set_where(sql, where)
                if orderby:
                    sql = sql.order_by(orderby)
                sql = sql.limit(1)
                res = conn.execute(sql).fetchone()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_one_specific_fields(self, fields, where, orderby=""):
        """
        根据条件获取一条记录（指定字段）
        :param fields: 待查找的字段列表 指定字段
        :param where: 条件
        :param orderby: 排序
        :return:
        """
        try:
            if not fields or not where:
                None
            with self._engine.connect() as conn:
                sql = select([getattr(self._table.c, rn) for rn in fields])
                sql = self._set_where(sql, where)
                if orderby:
                    sql = sql.order_by(orderby)
                sql = sql.limit(1)
                res = conn.execute(sql).fetchone()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_some(self, where={}, orderby="", offset=0, limit=0):
        """
        获取满足条件的一些数据
        :param where: 条件字典
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :param offset:
        :param limit:
        :return:
        """
        try:
            with self._engine.connect() as conn:
                sql = self._table.select()
                if "isdel" in self._table.c.keys():
                    # 如果表中有isdel字段，则取isdel为False的结果
                    sql = self._set_where(sql, {"isdel": False})
                sql = self._set_where(sql, where)
                if orderby:
                    sql = sql.order_by(orderby)

                if limit:
                    sql = sql.offset(offset).limit(limit)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_some_specific_fields(self, fields, where={}, orderby="", offset=0, limit=0):
        """

        获取满足条件的一些数据（指定字段）
        :param where: 条件字典
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :param offset:
        :param limit:
        :return:
        """
        try:
            with self._engine.connect() as conn:
                sql = select([getattr(self._table.c, rn) for rn in fields])
                if "isdel" in self._table.c.keys():
                    # 如果表中有isdel字段，则取isdel为False的结果
                    sql = self._set_where(sql, {"isdel": False})
                sql = self._set_where(sql, where)
                if orderby:
                    sql = sql.order_by(orderby)
                if limit:
                    sql = sql.offset(offset).limit(limit)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_some8ids(self, ids, ids_row="id", orderby="", offset=0, limit=0):
        """
        根据id列表获取一些数据
        :param ids: id列表
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :param offset:
        :param limit:
        :return:
        """
        if not ids:
            return None
        try:
            with self._engine.connect() as conn:
                sql = self._table.select().where(getattr(self._table.c, ids_row).in_(ids))
                if "isdel" in self._table.c.keys():
                    sql = sql.where(self._table.c.isdel==False)
                if orderby:
                    sql = sql.order_by(orderby)
                if limit:
                    sql = sql.offset(offset).limit(limit)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_some8ids_specific_fields(self, fields, ids, ids_row="id", orderby="", offset=0, limit=0):
        """
        根据id列表获取一些数据（指定字段）
        :param fields:
        :param ids: id列表
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :param offset:
        :param limit:
        :return:
        """
        if not fields or not ids:
            return None
        try:
            with self._engine.connect() as conn:
                sql = select([getattr(self._table.c, rn) for rn in fields]).where(self._table.c.id.in_(ids))
                if orderby:
                    sql = sql.order_by(orderby)
                if limit:
                    sql = sql.offset(offset).limit(limit)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_all(self, orderby=""):
        """
        获取所有
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :return:
        """
        try:
            with self._engine.connect() as conn:
                sql = self._table.select()
                if "isdel" in self._table.c.keys():
                    # 如果表中有isdel字段，则取isdel为False的结果
                    sql = self._set_where(sql, {"isdel": False})
                if orderby:
                    sql = sql.order_by(orderby)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def get_all_specific_fields(self, fields, orderby=""):
        """
        获取所有（指定字段）
        :param orderby: 排序字段。如："id"  或者  "id  desc"
        :return:
        """
        try:
            if not fields:
                return None
            with self._engine.connect() as conn:
                sql = select([getattr(self._table.c, rn) for rn in fields])
                if "isdel" in self._table.c.keys():
                    # 如果表中有isdel字段，则取isdel为False的结果
                    sql = self._set_where(sql, {"isdel": False})
                if orderby:
                    sql = sql.order_by(orderby)
                res = conn.execute(sql).fetchall()
                return res
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def add(self, data):
        """
        添加
        :param data:待添加的数据字典
        :return:
        """
        try:
            with self._engine.connect() as conn:
                sql = self._table.insert().values(data)
                return conn.execute(sql)
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def update(self, where, data):
        """
        更新
        :param where:更新时的条件字典
        :param data: 待更新的数据字典
        :return:
        """
        try:
            with self._engine.connect() as conn:
                sql = self._table.update()
                sql = self._set_where(sql, where)
                sql = sql.values(data)
                return conn.execute(sql)
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def delete(self, where, real_del=True):
        """
        删除，默认真删除
        :param where: 条件字典
        :param real_del: 是否真删除，默认为True
        :return:
        """
        try:
            with self._engine.connect() as conn:
                if real_del:
                    # 真删除
                    sql = self._table.delete()
                    sql = self._set_where(sql, where)
                    return conn.execute(sql)
                else:
                    # 软删除
                    if "isdel" in self._table.c.keys():
                        sql = self._table.update()
                        sql = self._set_where(sql, where)
                        sql = sql.values({"isdel": True})
                        return conn.execute(sql)
                    else:
                        # 表中没有标记删除的字段
                        write_log(
                            "function {}.{}, table has no “isdel” field!".format(
                                self.__class__.__name__,
                                sys._getframe().f_code.co_name,))
                        return None
        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None

    def _set_where(self, sql, where):
        """
        设置条件
        :param sql:待设置的sql对象
        :param where: 待转换的条件字典。如：{"id":1} => {Column("id"):1}
        :return:
        """
        for key, val in where.items():
            if isinstance(val, tuple) or isinstance(val, list):
                value = val[0]
                operator = val[1]
                if operator == ">":
                    sql = sql.where(getattr(self._table.c, key) > value)
                elif operator == ">=":
                    sql = sql.where(getattr(self._table.c, key) >= value)
                elif operator == "<":
                    sql = sql.where(getattr(self._table.c, key) < value)
                elif operator == "<=":
                    sql = sql.where(getattr(self._table.c, key) <= value)
            else:
                sql = sql.where(getattr(self._table.c, key) == val)
        return sql

    def get_some_generator(self, where={}, orderby="", offset=0, limit=100):
        try:
            num_all = 0
            while 1:
                with self._engine.connect() as conn:
                    sql = self._table.select().prefix_with("SQL_CALC_FOUND_ROWS")

                    if "isdel" in self._table.c.keys():
                        # 如果表中有isdel字段，则取isdel为False的结果
                        sql = self._set_where(sql, {"isdel": False})

                    sql = self._set_where(sql, where)

                    if orderby:
                        sql = sql.order_by(orderby)

                    sql = sql.offset(offset).limit(limit)
                    res = conn.execute(sql).fetchall()

                    if not num_all:
                        num_all = conn.execute("select FOUND_ROWS();").scalar()

                    offset += limit
                    yield res

                    if offset > num_all:
                        return None

        except Exception as ex:
            write_log("{}.{} raise exception,ex={}".format(
                self.__class__.__name__,
                sys._getframe().f_code.co_name,
                repr(ex)))
            return None