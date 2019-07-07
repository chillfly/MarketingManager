import time
import re
from decimal import Decimal, ROUND_DOWN, ROUND_05UP


def format_float(m, precision=10, cut=True):
    return decimal_to_str(m, pcs=precision, cut=cut)


def decimal_to_str(v, pcs=-1, cut=True, rz=False):
    """
    :param v: decimal or string
    :param pcs: -1 表示不进行精度处理
    :param cut: 是否切割
    :param rz: 右侧是否保留0 比如 11.00 => 11
    :return:
    """
    if not v and not rz:
        return "0"
    dv = v
    if isinstance(v, float):
        dv = Decimal.from_float(v)
    elif not isinstance(v, Decimal):
        dv = Decimal(str(v))
    if pcs >= 0:
        m = ROUND_DOWN if cut else ROUND_05UP
        dv = dv.quantize(Decimal(1) / (10 ** pcs), m)
    # ss = str(md)
    ss = dv.to_eng_string()
    if "E" in ss.upper() or not cut:
        di, de = dv._int, dv._exp
        len_di = len(di)
        ld = de + len_di
        if ld <= 0:
            ss = '0.' + di.rjust(len_di - ld, '0')
        else:
            li = list(di)
            li.insert(ld, '.')
            ss = ''.join(li)
    if not rz and ss.find(".") > -1:
        ss = ss.rstrip("0").rstrip(".")
    return ss


def format_time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))


def is_empty(strs):
    """
    判断是否为空
    :param strs:
    :return:
    """
    if not strs:
        # "" 或者 None 或者 数字0
        return True
    elif isinstance(strs, str) and not strs.strip():
        # 空字符串
        return True
    else:
        return False


def is_pwd(pwd=""):
    """
    检测密码格式是否正确
    :param pwd:
    :return:
    """
    if not pwd:
        return False

    pattern = r'^[A-Za-z0-9]{6,12}$'
    res = re.findall(pattern, pwd)
    if not res:
        return False
    return True


def filter_none(strs):
    """
    过滤None值（None值，会当做“None”字符串填入到表单中）
    :param strs:
    :return:
    """
    if not strs:
        return ""
    return strs
