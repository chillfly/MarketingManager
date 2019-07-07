import hashlib
import time
import datetime

from decimal import Decimal
from tornado import web
from tornado import escape
from urllib import parse as urlparse
from urllib.parse import urlencode
from sqlalchemy import select, and_

from utils.mycache import RedisCache
from utils import myjson, myfilter
from configs import settings
from models.managerdb import db_engine
from models.sys_user import SysUser


def url_spec(**kwargs):
    return [
        # 报错页面
        (r'/404/?', Error404Handler, kwargs),
    ]


# region  -- 基类 --
class BaseHandler(web.RequestHandler):
    token_key = settings.REDIS_KEYS["token_"]
    cache = RedisCache()

    def tran_rowproxy2variable(self, rowproxy):
        if not rowproxy:
            return rowproxy
        obj_name = rowproxy.__class__.__name__
        kwargs = dict()
        for key, val in dict(rowproxy).items():
            kwargs[key] = val
        return type("Variable{}".format(obj_name), (), kwargs)

    def update_user_cache(self, data={}):
        """
        更新用户缓存
        :param data: 为空，相当于刷新缓存；不为空，存入新的数据并刷新缓存
        :return:
        """
        user = self.user
        token_key = self.token_key.format(tk=self.get_token(), uid=user.get("id"))
        for key, val in data.items():
            user[key] = val
        # 重新设置该登录用户的缓存
        self.cache.set_cache(token_key, user, 3600)

    def get_secure_cookie(self, name=""):
        res = super().get_secure_cookie(name)
        if isinstance(res, bytes):
            res = bytes.decode(res)
            # res = str(res, encoding="utf8")
        return res

    def login_delay(self):
        """
        登录状态延期
        :return:
        """
        # 续期
        token = self.get_token()
        token_key = self.token_key.format(tk=token, uid="*")
        # 延长1小时
        self.cache.expire_cache(token_key, time=3600)

    def prepare(self):
        if self.request.method in ("GET", "HEAD"):
            class_name = self.__class__.__name__
            if class_name == "LoginHandler":
                if self.current_user:
                    # 已经登录，跳转到首页
                    self.redirect("/")
                    return
                else:
                    # 未登录，直接跳出，不做下面的权限判断
                    return
            if not self.current_user:
                # 未登录
                if not self.get_argument("api", 0):
                    url = self.get_login_url()
                    if "?" not in url:
                        if urlparse.urlsplit(url).scheme:
                            # if login url is absolute, make next absolute too
                            next_url = self.request.full_url()
                        else:
                            next_url = self.request.uri
                        url += "?" + urlencode(dict(next=next_url))
                    self.redirect(url)
                    return
                self.send_fail_json(u'你还没有登录或者登录态已经过期')
                return

            # 已登录
            # 延长登录期限
            self.login_delay()

            # 验证权限
            # todo
            pass

    @property
    def current_user(self):
        token = self.get_token()
        if not token:
            return None
        # 通过token_key去redis中获取对应的token值
        token_key = self.token_key.format(tk=token, uid="*")
        # 获取token_key对应的用户信息
        return self.cache.get_cache(token_key)

    @property
    def user(self):
        return self.current_user

    def get_token(self):
        return self.get_secure_cookie(name="token") or self.request.headers.get('token')

    def write_json(self, data):
        self.set_header("Content-Type", "text/json; charset=utf-8")
        self.set_header("Cache-Control", "no-cache")
        if isinstance(data, dict):
            data = myjson.dumps(data).replace("</", "<\\/")
        self.write(data)

    def send_ok_json(self, data=None, reason=''):
        if data is None:
            data = {}
        ok_json = {'ok': True, 'reason': reason, 'data': data}
        self.write_json(escape.json_encode(ok_json))

    def send_fail_json(self, reason='', data=None, jsoned=True):
        ok_json = {'ok': False, 'reason': reason, 'data': data or {}}
        if jsoned:
            self.write_json(myjson.dumps(ok_json, ensure_ascii=False))
        else:
            self.write_json(myjson.dumps(ok_json, ensure_ascii=False).replace('\\', ''))

    def send_fail_html(self, reason=""):
        self.render("fail.html", reason=reason)

    def md5_password(self, password):
        return hashlib.md5("{}{}".format(password, settings.PLATFORM_USER_PASSWORD_SECRET).encode("utf-8")).hexdigest()

    def ip_limit(self, target_ip="", banned_time=3600, select=True):
        """
        ip限制
        :param target_ip:目标ip
        :param banned_time: 封禁时长（单位为秒）
        :param select: True：查看是否被封禁；False：添加/修改封禁ip
        :return: select为True,查看target_ip是否被封禁，是：True，否：False；select为False，返回None
        """
        conn = self.cache.conn
        banned_ip_sets = settings.REDIS_KEYS["banned_ip_sets"]

        for item in conn.sscan_iter(banned_ip_sets):
            if isinstance(item, bytes):
                temp = bytes.decode(item)
            ip_dict = myjson.loads(temp)
            if ip_dict.get("unban_time") < time.time():
                # 已经过了解封时间了，解封该ip
                conn.srem(banned_ip_sets, temp)
            else:
                # 没有过解封时间，比较是否有该ip
                # 查询ip是否被封
                if ip_dict.get("ip", "") == target_ip:
                    if select:
                        return True
                    else:
                        conn.srem(banned_ip_sets, temp)
        else:
            if select:
                return False
            else:
                # 重新添加新值
                item = myjson.dumps(dict(ip=target_ip, unban_time=time.time() + banned_time))
                conn.sadd(banned_ip_sets, item)

    def get_args(self, key, default=None, data_type=None):
        """
        获取参数
        :param key: 参数下标
        :param data_type: 参数类型，默认为str
        :param default: 默认值，当key取到的值为空时，则返回该默认值
        :return:
        """
        try:
            # 获取参数内容
            data = self.get_argument(key)
            # 如果取得的数据为str，则默认去除左右端的空白字符
            if isinstance(data, str):
                data = data.strip()

            if not data:
                # 参数内容为空
                if callable(data_type):
                    # data_type不为空，则将默认值转换后返回
                    return data_type(default)

                # data_type为空，则直接返回默认值
                return default

            if callable(data_type):
                return data_type(data)
            return data
        except (web.MissingArgumentError, ValueError):
            return default

    def get_template_namespace(self):
        """ 添加额外的模板变量, 默认有:
         handler=self,
         request=self.request,
         current_user=self.current_user,
         locale=self.locale,
          _=self.locale.translate,
         static_url=self.static_url,
         xsrf_form_html=self.xsrf_form_html,
         reverse_url=self.reverse_url
        """
        user = SysUser().get_one8id(self.user["id"]) if self.user else dict()
        add_names = dict(
            filter_none=myfilter.filter_none,
            json_loads=myjson.loads,
            settings=settings,
            user=user,
        )
        name = super().get_template_namespace()
        name.update(add_names)
        return name


# endregion


# region  -- Layer列表类 --
class LayerListHandler(BaseHandler):
    # 查询条件
    _table_query_args = ()  # 基础表查询列
    # _ex_query_args = ('time', )  # 拓展查询列
    _ex_query_args = ()  # 拓展查询列

    _time_row_name = 'create_time'  # 时间查询的列名 配合_ex_query_args = ('time', )使用

    # 查询表配置
    _table = None
    _join_on = None  # 联合查询时的条件
    _db_engine = db_engine
    _id_row_name = "id"
    _result_rows = None
    _order_by = ""

    # 查询结果展示配置
    _per_page = 30
    _template = ''
    _export_template = ''

    _stat_user = False
    _stat_deno = False

    def _csv(self, csv, filename="down.csv"):
        self.set_header("Content-Type", "text/csv; charset=GBK")
        self.set_header("Content-Disposition", "attachment; filename=" + filename)
        self.set_header("Cache-Control", "must-revalidate,post-check=0,pre-check=0")
        self.set_header("Expires", 0)
        self.finish(csv.encode('GBK'))

    def _ext_data(self, **kwargs):
        """ 返回给前端的除了列表数据以外的额外统计相关的数据, 在api接口的ext_data字段里
        :param kwargs:
        :return:
        """
        return {}

    def _handler_ex_args(self, *args, **kwargs):
        """ 添加额外的查询条件, 返回查询字典和sqlalchemy where列表
        :return:
        """
        return {}, []

    def _handler_result_data(self, data, **kwargs):
        """ 返回到前端前的数据结果处理
        :param data:
        :return:
        """
        return data

    def _get_table(self, *args, **kwargs):
        """ 获取 table
        :param args:
        :param kwargs:
        :return:
        """
        return self._table

    def _page_table_data(self, per_page, page, add_where, res_rows=None, table=None, **kwargs):
        table = table if table is not None else self._table
        page = int(page)
        per_page = int(per_page)
        # 获取记录
        with self._db_engine.connect() as conn:
            _where = []
            for k, v in kwargs.items():
                if v:
                    _where.append(getattr(table.c, k) == v)
            if add_where:
                _where.extend(add_where)
            if not res_rows:
                sql = table.select().prefix_with("SQL_CALC_FOUND_ROWS")
            else:
                sql = select([getattr(table.c, rn) for rn in res_rows]).prefix_with("SQL_CALC_FOUND_ROWS")
            if _where:
                sql = sql.where(and_(*_where))
            # sql = sql.order_by(table.c.id.desc())
            if self._order_by:
                sql = sql.order_by(self._order_by)
            else:
                sql = sql.order_by(getattr(table.c, self._id_row_name).desc())
            if page and per_page:
                offset = (page - 1) * per_page
                sql = sql.offset(offset).limit(per_page)
            data = conn.execute(sql).fetchall()
            num = conn.execute("select FOUND_ROWS();").scalar()
        return data, num, {'where': _where}

    def _do_request(self, *args, **kwargs):
        if not self.get_args("data"):
            self.render(self._template, **kwargs)
            return
        export = self.get_args("export")
        base_query = {k: self.get_args(k) for k in self._table_query_args}
        page = self.get_args("page", 1, int)
        per_page = self.get_args("limit", self._per_page, int)
        # ex
        _table = self._table if self._table is not None else self._get_table(**kwargs)  # set table

        qs = base_query.copy()
        add_where = []
        if "isdel" in _table.c.keys():
            # 软删除
            add_where.append(and_(_table.c.isdel==False))
        if 'time' in self._ex_query_args:
            now = datetime.datetime.now()
            beg = self.get_args('beg', '')
            end = self.get_args('end', '')
            beg_time, end_time = beg, end
            if beg:
                beg = datetime.datetime.strptime(beg, "%Y-%m-%d")
            else:
                beg = now - datetime.timedelta(days=1)
            if end:
                end = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1)
            else:
                end = now + datetime.timedelta(days=1)
            # if beg and end:
            if beg_time or end_time:  # 必须提供一个才进行条件检索
                if _table is not None:
                    add_where.append(and_(getattr(_table.c, self._time_row_name) >= beg,
                                          getattr(_table.c, self._time_row_name) < end))
                else:
                    add_where.append(('time', beg, end))
            qs['beg'] = beg_time
            qs['end'] = end_time
        _qs, _aw = self._handler_ex_args(**kwargs)
        qs.update(_qs)
        add_where.extend(_aw)
        res_rows = self._result_rows
        if export:
            page = 0
            res_rows = None

        data, num, st_data = self._page_table_data(
            per_page=per_page, page=page, res_rows=res_rows,
            table=_table, add_where=add_where, **base_query)
        # ext
        st_data.update(kwargs)
        # st_data.update(qs)
        ext_data = self._ext_data(data=data, **st_data)  # st_data 有where kwargs
        # field rows and convert
        res_data = [dict(t) for t in data]
        res_data = self._handler_result_data(data=res_data, ext_data=ext_data)
        for td in res_data:
            for k, v in td.items():
                if isinstance(v, (datetime.datetime, datetime.date)):
                    td[k] = v.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(v, Decimal):
                    td[k] = myfilter.format_float(v)
        if export:
            exp_tpl = self._export_template or self._template.replace("html", 'csv')
            csv = self.render_string(exp_tpl, data=res_data, ext_data=ext_data, **qs)
            # print "--: ", repr(csv)
            name = self._export_template.split('.')[0] + str(time.time())
            return self._csv(csv, '%s.csv' % name)
        # return json data
        res = {
            "code": 0,
            "msg": "",
            "count": num,
            "data": res_data,
            "ext_data": ext_data,
        }
        self.write_json(res)



# endregion


# region -- 404类 --
class Error404Handler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("404.html")
# endregion
