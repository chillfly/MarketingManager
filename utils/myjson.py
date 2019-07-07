import json
import datetime
from decimal import Decimal
from . import myfilter


class ComplexEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, Decimal):
            return myfilter.format_float(o)
        return json.JSONEncoder.default(self, o)


def load(fp, **kwargs):
    return json.load(fp, **kwargs)


def loads(strs, **kwargs):
    return json.loads(strs, **kwargs)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, **kwargs)


def dumps(obj, **kwargs):
    return json.dumps(obj, **kwargs, cls=ComplexEncoder)

