import winreg
import json
import os
from datetime import datetime

class RegistryManager:
    def __init__(self):
        self.backup_dir = "backups/registry"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def read_value(self, hive, path, key):
        """Lee un valor del registro"""
        try:
            if hive == "HKLM":
                reg_hive = winreg.HKEY_LOCAL_MACHINE
            elif hive == "HKCU":
                reg_hive = winreg.HKEY_CURRENT_USER
            else:
                return None
                
            with winreg.OpenKey(reg_hive, path) as reg_key:
                value, reg_type = winreg.QueryValueEx(reg_key, key)
                return value
        except:
            return None
    
    def write_value(self, hive, path, key, value, value_type="DWORD"):
        """Escribe un valor en el registro"""
        try:
            if hive == "HKLM":
                reg_hive = winreg.HKEY_LOCAL_MACHINE
            elif hive == "HKCU":
                reg_hive = winreg.HKEY_CURRENT_USER
            else:
                return False
                
            with winreg.CreateKeyEx(reg_hive, path) as reg_key:
                reg_type = getattr(winreg, f"REG_{value_type}")
                winreg.SetValueEx(reg_key, key, 0, reg_type, value)
            return True
        except Exception as e:
            print(f"Registry write error: {e}")
            return False
    
    def backup_key(self, hive, path):
        """Hace backup de una clave del registro"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        values = {}
        
        try:
            if hive == "HKLM":
                reg_hive = winreg.HKEY_LOCAL_MACHINE
            elif hive == "HKCU":
                reg_hive = winreg.HKEY_CURRENT_USER
            else:
                return None
                
            with winreg.OpenKey(reg_hive, path) as reg_key:
                i = 0
                while True:
                    try:
                        name, value, reg_type = winreg.EnumValue(reg_key, i)
                        values[name] = {"value": value, "type": reg_type}
                        i += 1
                    except WindowsError:
                        break
                        
            # Guardar backup
            backup_file