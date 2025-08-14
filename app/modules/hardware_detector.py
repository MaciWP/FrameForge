import psutil
import platform
import wmi
import GPUtil

class HardwareDetector:
    def __init__(self):
        self.wmi = wmi.WMI()
        
    def get_system_info(self):
        """Obtiene información completa del sistema"""
        info = {
            'cpu': self.get_cpu_info(),
            'gpu': self.get_gpu_info(),
            'ram': self.get_ram_info(),
            'os': self.get_os_info()
        }
        return info
        
    def get_cpu_info(self):
        """Obtiene información del CPU"""
        cpu = self.wmi.Win32_Processor()[0]
        return {
            'name': cpu.Name.strip(),
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
            'freq_max': cpu.MaxClockSpeed,
            'freq_current': psutil.cpu_freq().current / 1000,
            'architecture': platform.machine()
        }
        
    def get_gpu_info(self):
        """Obtiene información de la GPU"""
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.name,
                    'driver': gpu.driver,
                    'vram': gpu.memoryTotal,
                    'uuid': gpu.uuid
                }
        except:
            pass
            
        # Fallback to WMI
        gpu = self.wmi.Win32_VideoController()[0]
        return {
            'name': gpu.Name,
            'driver': gpu.DriverVersion,
            'vram': int(gpu.AdapterRAM / 1024 / 1024) if gpu.AdapterRAM else 0,
            'uuid': None
        }
        
    def get_ram_info(self):
        """Obtiene información de la RAM"""
        ram = psutil.virtual_memory()
        
        # Intentar obtener velocidad de WMI
        speed = "Unknown"
        try:
            for mem in self.wmi.Win32_PhysicalMemory():
                if mem.Speed:
                    speed = mem.Speed
                    break
        except:
            pass
            
        return {
            'total': ram.total / 1024 / 1024 / 1024,
            'available': ram.available / 1024 / 1024 / 1024,
            'used_percent': ram.percent,
            'speed': speed
        }
        
    def get_os_info(self):
        """Obtiene información del sistema operativo"""
        return {
            'name': platform.system() + " " + platform.release(),
            'version': platform.version(),
            'build': platform.win32_ver()[1],
            'architecture': platform.machine()
        }