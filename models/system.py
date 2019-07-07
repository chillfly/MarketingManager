from functools import wraps
from .sys_menu import Menu
from .sys_power import Power
from .sys_role import Role, ROLE_TYPE_SP_ADMIN
from .sys_user import SysUser


def get_power_name(id):
    """
    通过id获取权限名称
    :param id: 权限id
    :return: 权限名称字符串
    """
    power = Power().get_one8id(id)
    if not power:
        # 只有一种情况获取不到数据，即menu表中的power_id是经过特殊处理的，不是从power表中取的，而特殊处理的，目前就是“系统管理”
        return "系统管理"
    return power.name


def get_role_power_marks(role_id):
    """
    通过角色id获取其所有的权限
    :param role_id: 权限id
    :return: 权限列表
    """

    # 根据role_id获取权限
    role = Role().get_one8id(role_id)
    if not role:
        return None

    # 权限id列表
    power_ids = role.power_ids.split(",")

    # 根据权限id列表获取 权限对象列表
    powers = Power().get_some8ids(power_ids)
    if not powers:
        return None

    # 权限名称列表
    power_marks = [item.mark.upper() for item in powers]
    return power_marks


def is_role_have_power(role_id, power_mark):
    """
    判断角色是否拥有某一个权限
    :param role_id: 角色id
    :param power_mark: 权限名称
    :return: True or False
    """
    temp = get_role_power_marks(role_id)
    power_mark = power_mark.upper()
    if not temp:
        return False
    return power_mark in temp


def power_check(power_mark):
    """
    权限检查
    :param power_mark: 权限名称
    :return:
    """
    def decorator(func):
        """
        内部
        :param func:
        :return:
        """
        @wraps(func)
        def wrapper(handler, *args, **kwargs):
            user = handler.user
            if not user:
                # user为空，过期，要重新登录
                handler.send_fail_html(reason="登录状态过期")
                return
            role_id = user["role_id"]
            role = Role().get_one8id(role_id)
            if not role:
                handler.send_fail_html(reason="权限不足")
                return
            ok = role.types == ROLE_TYPE_SP_ADMIN or is_role_have_power(role_id, power_mark)

            if not ok:
                handler.send_fail_html(reason="权限不足")
                return
            return func(handler, *args, **kwargs)
        return wrapper
    return decorator


def super_admin_check(func):
    """
    判断是不是超管
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(handler, *args, **kwargs):
        user = handler.user
        role = Role().get_one8id(user["role_id"])
        if not role:
            handler.send_fail_html(reason="权限不足")
            return

        ok = role.types == ROLE_TYPE_SP_ADMIN

        if not ok:
            handler.send_fail_html(reason="权限不足")
            return
        return func(handler, *args, **kwargs)
    return wrapper


def get_role_type(role_id):
    """
    获取角色类型
    :param role_id:
    :return:
    """
    role = Role().get_one8id(role_id)
    if not role:
        return None
    return role.types


def get_role_powers(role_id):
    """
    获取用户所拥有的权限
    :param role_id: 角色id
    :return: power_id为key，power_name为值的字典
    """
    if not role_id:
        return None
    role = Role().get_one8id(role_id)
    if not role or not role.power_ids:
        return None
    powers = Power().get_some8ids(role.power_ids.split(","))
    if not powers:
        return None
    return {p.id: p.name for p in powers}


def get_user_menus(user_id):
    """ 获取用户可操作的权限目录
    :param user: None 表示获取全部目录
    :return:
    [
        {name: xxx, url: xxx, "logo": xx, child: [{name: xx, url: xx, logo: xx}, ]},
    ]
    """
    if user_id is not None:
        user = SysUser().get_one8id(user_id)
        if not user:
            return []
        role_type = get_role_type(user.role_id)
        ps = get_role_powers(user.role_id) if role_type != ROLE_TYPE_SP_ADMIN else 'sp'
        if not ps:
            return []
    else:
        ps = "sp"

    menu_model = Menu()
    # 获取用户可操作的全部菜单
    if ps != "sp":
        menus = menu_model.get_some8ids(ps.keys(), ids_row="power_id", orderby="id, sort, name, create_time")
    else:
        menus = menu_model.get_all("fid, sort, id")

    data = {}
    for index, td in enumerate(menus):
        if td.fid == 0:  # 父级节点
            data[td.id] = {"name": td.name, "url": td.url, "icon": td.icon or "", "child": [],
                           "index": index, "id": td.id, "power_id": td.power_id}
        else:
            ftd = data.get(td.fid)
            if ftd:
                data[td.fid]["child"].append(
                    {"name": td.name, "url": td.url, "icon": td.icon or "", "id": td.id,
                     "power_id": td.power_id})
    return sorted(data.values(), key=lambda t: t['index'])
