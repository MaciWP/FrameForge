import subprocess
import datetime
import winreg
import json
import os

class BackupManager:
    def __init__(self):
        self.backup_dir = "backups"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
            
    def create_restore_point(self, description):
        """Crea un punto de restauración del sistema"""
        try:
            # Habilitar la creación de puntos de restauración
            cmd = f"""
            powershell -Command "
            Enable-ComputerRestore -Drive 'C:\\'
            Checkpoint-Computer -Description '{description}' -RestorePointType 'MODIFY_SETTINGS'
            "
            """
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error creating restore point: {e}")
            return False
            
    def backup_registry_key(self, key_path):
        """Hace backup de una clave del registro"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.backup_dir}/registry_backup_{timestamp}.reg"
        
        try:
            cmd = f'reg export "HKLM\\{key_path}" "{filename}" /y'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"Error backing up registry: {e}")
            return False
            
    def create_full_backup(self):
        """Crea un backup completo de todas las configuraciones"""
        backup_data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'registry_keys': [],
            'services': [],
            'settings': {}
        }
        
        # Backup de claves importantes del registro
        important_keys = [
            r"SYSTEM\CurrentControlSet\Control\Power",
            r"SYSTEM\CurrentControlSet\Control\Session Manager",
            r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
            r"SOFTWARE\Microsoft\Windows\Dwm"
        ]
        
        for key in important_keys:
            if self.backup_registry_key(key):
                backup_data['registry_keys'].append(key)
                
        # Guardar metadata del backup
        filename = f"{self.backup_dir}/backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(backup_data, f, indent=2)
            
        return True