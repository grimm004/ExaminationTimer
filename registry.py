# Registry Editor
# 06/06/2015
# @version: 4.0
# @author Max Grimmett (10.3), hugo24
from winreg import *


def set_reg_value(hkey, reg_path, name, value):
    try:
        CreateKey(hkey, reg_path)
        registry_key = OpenKey(hkey, reg_path, 0,
                               KEY_WRITE)
        SetValueEx(registry_key, name, 0, REG_SZ, value)
        CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def get_reg_value(hkey, reg_path, name):
    try:
        registry_key = OpenKey(hkey, reg_path, 0,
                               KEY_READ)
        value, regtype = QueryValueEx(registry_key, name)
        CloseKey(registry_key)
        return value
    except WindowsError:
        return None
