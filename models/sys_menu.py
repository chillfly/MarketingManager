from utils.mylogger import write_log
from .sys_role import Role
from sqlalchemy import Table
from .managerdb import ManagerDB, meta, db_engine


MenuTable = Table("sys_menu", meta, autoload=True, autoload_with=db_engine)


class Menu(ManagerDB):
    _table = MenuTable

    # def get_role_menus(self, role_id):
    #     if not role_id:
    #         write_log("sys_menu.Menu.get_role_menus(), role_id is empty")
    #         return None
    #
    #     role = Role().get_one8id(role_id)
    #     power_ids = role.power_ids
    #     if not power_ids:
    #         write_log("sys_menu.Menu.get_role_menus(), power_ids is empty")
    #         return None
    #
    #     menus = self.get_some8ids(power_ids.split(","), ids_row="id")
    #     if not menus:
    #         write_log("sys_menu.Menu.get_role_menus(), menus is empty")
    #         return None
    #
    #     return menus
