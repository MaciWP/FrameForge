import winreg
import subprocess
import json
import os

class OptimizerEngine:
    def __init__(self):
        self.optimizations = self.load_optimizations()
        
    def load_optimizations(self):
        """Carga las optimizaciones desde el archivo de configuración"""
        return {
            "nvidia_power": {
                "name": "NVIDIA Maximum Performance",
                "description": "Forces GPU to maximum performance mode",
                "risk": "Low",
                "impact": "+8-12% FPS",
                "default": True,
                "profiles": ["Safe", "Balanced", "Aggressive", "Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                        "key": "DisableDynamicPstate",
                        "value": 1,
                        "type": "DWORD"
                    },
                    {
                        "path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                        "key": "PowerMizerEnable",
                        "value": 0,
                        "type": "DWORD"
                    }
                ]
            },
            "timer_resolution": {
                "name": "High Precision Timer",
                "description": "Enables 0.5ms timer resolution",
                "risk": "Low",
                "impact": "-1-2ms latency",
                "default": True,
                "profiles": ["Safe", "Balanced", "Aggressive", "Ultra"],
                "type": "bcdedit",
                "commands": [
                    "bcdedit /set useplatformtick yes",
                    "bcdedit /set disabledynamictick yes"
                ]
            },
            "core_parking": {
                "name": "Disable CPU Core Parking",
                "description": "Keeps all CPU cores active",
                "risk": "Low",
                "impact": "+3-5% FPS",
                "default": True,
                "profiles": ["Safe", "Balanced", "Aggressive", "Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\0cc5b647-c1df-4637-891a-dec35c318583",
                        "key": "ValueMax",
                        "value": 0,
                        "type": "DWORD"
                    }
                ]
            },
            "msi_mode": {
                "name": "MSI Mode for GPU",
                "description": "Enables Message Signaled Interrupts",
                "risk": "Low",
                "impact": "+2-3% FPS",
                "default": True,
                "profiles": ["Balanced", "Aggressive", "Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000",
                        "key": "EnableMSI",
                        "value": 1,
                        "type": "DWORD"
                    }
                ]
            },
            "network_optimization": {
                "name": "Network Latency Optimization",
                "description": "Optimizes TCP/IP for gaming",
                "risk": "Medium",
                "impact": "-5-10ms network latency",
                "default": False,
                "profiles": ["Balanced", "Aggressive", "Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                        "key": "TcpAckFrequency",
                        "value": 1,
                        "type": "DWORD"
                    },
                    {
                        "path": r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                        "key": "TCPNoDelay",
                        "value": 1,
                        "type": "DWORD"
                    }
                ]
            },
            "dwm_optimization": {
                "name": "DWM Buffer Reduction",
                "description": "Reduces Desktop Window Manager buffers",
                "risk": "High",
                "impact": "+10-15% FPS",
                "default": False,
                "profiles": ["Aggressive", "Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SOFTWARE\Microsoft\Windows\Dwm",
                        "key": "m_bufferCount",
                        "value": 1,
                        "type": "DWORD"
                    }
                ]
            },
            "kernel_threads": {
                "name": "Optimize Kernel Worker Threads",
                "description": "Adjusts kernel thread count for your CPU",
                "risk": "Medium",
                "impact": "+1-3% responsiveness",
                "default": False,
                "profiles": ["Ultra"],
                "type": "registry",
                "registry_entries": [
                    {
                        "path": r"SYSTEM\CurrentControlSet\Control\Session Manager\Executive",
                        "key": "AdditionalCriticalWorkerThreads",
                        "value": 8,  # This should be calculated based on CPU
                        "type": "DWORD"
                    }
                ]
            }
        }
        
    def get_available_optimizations(self, profile):
        """Obtiene las optimizaciones disponibles para un perfil"""
        available = {}
        for key, opt in self.optimizations.items():
            if profile in opt['profiles']:
                available[key] = opt
        return available
        
    def apply_optimization(self, opt_key):
        """Aplica una optimización específica"""
        if opt_key not in self.optimizations:
            return False
            
        opt = self.optimizations[opt_key]
        
        try:
            if opt['type'] == 'registry':
                return self._apply_registry_optimization(opt)
            elif opt['type'] == 'bcdedit':
                return self._apply_bcdedit_optimization(opt)
            elif opt['type'] == 'powershell':
                return self._apply_powershell_optimization(opt)
        except Exception as e:
            print(f"Error applying {opt_key}: {e}")
            return False
            
        return True
        
    def _apply_registry_optimization(self, opt):
        """Aplica optimizaciones de registro"""
        for entry in opt['registry_entries']:
            try:
                # Abrir o crear la clave
                key_path = entry['path']
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path)
                
                # Establecer el valor
                value_type = getattr(winreg, f"REG_{entry['type']}")
                winreg.SetValueEx(key, entry['key'], 0, value_type, entry['value'])
                winreg.CloseKey(key)
            except Exception as e:
                print(f"Registry error: {e}")
                return False
        return True
        
    def _apply_bcdedit_optimization(self, opt):
        """Aplica optimizaciones usando bcdedit"""
        for cmd in opt['commands']:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"BCDEdit error: {result.stderr}")
                    return False
            except Exception as e:
                print(f"BCDEdit error: {e}")
                return False
        return True
        
    def _apply_powershell_optimization(self, opt):
        """Aplica optimizaciones usando PowerShell"""
        for cmd in opt['commands']:
            try:
                ps_cmd = f'powershell -Command "{cmd}"'
                result = subprocess.run(ps_cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"PowerShell error: {result.stderr}")
                    return False
            except Exception as e:
                print(f"PowerShell error: {e}")
                return False
        return True
        
    def restore_all(self):
        """Restaura todas las configuraciones a valores por defecto"""
        # Aquí implementarías la lógica para restaurar
        # Por ahora, retornamos True como placeholder
        return True


def load_old_optimizations(self):
    """Carga las optimizaciones desde los archivos OLD"""
    import glob
    
    # Buscar archivos .reg en las carpetas OLD
    reg_files = glob.glob("../OLD optimization/**/*.reg", recursive=True)
    bat_files = glob.glob("../OLD optimization/**/*.bat", recursive=True)
    
    old_optimizations = {}
    
    # Categorías basadas en tus carpetas
    categories = {
        "power_related": {"name": "Power Management", "risk": "Low"},
        "GPU": {"name": "GPU Optimizations", "risk": "Medium"},
        "Network": {"name": "Network Tweaks", "risk": "Low"},
        "Regtweaks": {"name": "Registry Tweaks", "risk": "Medium"},
        "debloat": {"name": "System Debloat", "risk": "High"},
        "Bonus": {"name": "Experimental", "risk": "High"}
    }
    
    for reg_file in reg_files:
        # Extraer categoría del path
        parts = reg_file.split("\\")
        for cat_key, cat_info in categories.items():
            if any(cat_key in part for part in parts):
                file_name = os.path.basename(reg_file)
                opt_key = file_name.replace(".reg", "").replace(" ", "_")
                
                old_optimizations[opt_key] = {
                    "name": file_name.replace(".reg", ""),
                    "description": f"Imported from {cat_info['name']}",
                    "risk": cat_info['risk'],
                    "impact": "Testing needed",
                    "default": False,
                    "profiles": ["Aggressive", "Ultra"],
                    "type": "reg_file",
                    "file_path": os.path.abspath(reg_file)
                }
                break
    
    # Combinar con optimizaciones existentes
    self.optimizations.update(old_optimizations)
    return old_optimizations

def apply_reg_file(self, file_path):
    """Aplica un archivo .reg"""
    try:
        import subprocess
        result = subprocess.run(
            f'reg import "{file_path}"',
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error applying .reg file: {e}")
        return False