import customtkinter as ctk
from tkinter import messagebox
import json
import sys
import os
from modules.hardware_detector import HardwareDetector
from modules.optimizer_engine import OptimizerEngine
from modules.backup_manager import BackupManager
import threading
import time

# Configuración de CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class UltraOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("UltraOptimizer v1.0 - Gaming Performance")
        self.geometry("1200x700")
        self.resizable(False, False)
        
        # Variables
        self.hardware_info = {}
        self.optimizations_applied = []
        self.current_profile = "Safe"
        
        # Inicializar módulos
        self.hardware_detector = HardwareDetector()
        self.optimizer = OptimizerEngine()
        self.backup_manager = BackupManager()
        
        # Crear interfaz
        self.create_widgets()
        self.detect_hardware()
        
    def create_widgets(self):
        # Frame principal con grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)
        
        # Logo/Título
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="🎮 UltraOptimizer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Perfil selector
        self.profile_label = ctk.CTkLabel(self.sidebar, text="Optimization Profile:")
        self.profile_label.grid(row=1, column=0, padx=20, pady=(20, 0))
        
        self.profile_selector = ctk.CTkSegmentedButton(
            self.sidebar,
            values=["Safe", "Balanced", "Aggressive", "Ultra"],
            command=self.change_profile,
            width=210
        )
        self.profile_selector.set("Safe")
        self.profile_selector.grid(row=2, column=0, padx=20, pady=10)
        
        # Botones de acción
        self.scan_btn = ctk.CTkButton(
            self.sidebar,
            text="🔍 Scan System",
            command=self.scan_system,
            width=210,
            height=40
        )
        self.scan_btn.grid(row=3, column=0, padx=20, pady=10)
        
        self.optimize_btn = ctk.CTkButton(
            self.sidebar,
            text="⚡ Apply Optimizations",
            command=self.apply_optimizations,
            width=210,
            height=40,
            fg_color="green"
        )
        self.optimize_btn.grid(row=4, column=0, padx=20, pady=10)
        
        self.backup_btn = ctk.CTkButton(
            self.sidebar,
            text="💾 Create Backup",
            command=self.create_backup,
            width=210,
            height=40
        )
        self.backup_btn.grid(row=5, column=0, padx=20, pady=10)
        
        self.restore_btn = ctk.CTkButton(
            self.sidebar,
            text="🔄 Restore Default",
            command=self.restore_defaults,
            width=210,
            height=40,
            fg_color="orange"
        )
        self.restore_btn.grid(row=6, column=0, padx=20, pady=10)
        
        # Botón de salida
        self.exit_btn = ctk.CTkButton(
            self.sidebar,
            text="Exit",
            command=self.quit,
            width=210,
            fg_color="red"
        )
        self.exit_btn.grid(row=9, column=0, padx=20, pady=(10, 20))
        
        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Hardware Info Panel
        self.hw_frame = ctk.CTkFrame(self.main_frame)
        self.hw_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        self.hw_title = ctk.CTkLabel(
            self.hw_frame,
            text="🖥️ System Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.hw_title.pack(pady=10)
        
        self.hw_info_text = ctk.CTkTextbox(self.hw_frame, height=150, width=850)
        self.hw_info_text.pack(padx=10, pady=(0, 10))
        
        # Optimizations Panel
        self.opt_frame = ctk.CTkFrame(self.main_frame)
        self.opt_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.opt_title = ctk.CTkLabel(
            self.opt_frame,
            text="⚙️ Available Optimizations",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.opt_title.pack(pady=10)
        
        # Scrollable frame para optimizaciones
        self.opt_scroll = ctk.CTkScrollableFrame(self.opt_frame, height=250, width=850)
        self.opt_scroll.pack(padx=10, pady=(0, 10))
        
        # Progress and Status
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.grid(row=2, column=0, sticky="ew")
        
        self.progress = ctk.CTkProgressBar(self.status_frame, width=850)
        self.progress.pack(padx=10, pady=10)
        self.progress.set(0)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to optimize your system",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(0, 10))
        
    def detect_hardware(self):
        """Detecta el hardware del sistema"""
        self.update_status("Detecting hardware...")
        self.hardware_info = self.hardware_detector.get_system_info()
        
        # Mostrar info en el textbox
        info_text = f"""
CPU: {self.hardware_info['cpu']['name']}
Cores: {self.hardware_info['cpu']['cores']} | Threads: {self.hardware_info['cpu']['threads']}
Frequency: {self.hardware_info['cpu']['freq_current']:.2f} GHz

GPU: {self.hardware_info['gpu']['name']}
Driver: {self.hardware_info['gpu']['driver']}
VRAM: {self.hardware_info['gpu']['vram']} MB

RAM: {self.hardware_info['ram']['total']:.1f} GB
Speed: {self.hardware_info['ram']['speed']} MHz

OS: {self.hardware_info['os']['name']}
Build: {self.hardware_info['os']['build']}
        """
        self.hw_info_text.delete("1.0", "end")
        self.hw_info_text.insert("1.0", info_text)
        self.update_status("Hardware detection complete")
        
    def scan_system(self):
        """Escanea el sistema para encontrar optimizaciones disponibles"""
        self.update_status("Scanning system for optimization opportunities...")
        self.progress.set(0)
        
        # Limpiar frame de optimizaciones
        for widget in self.opt_scroll.winfo_children():
            widget.destroy()
        
        optimizations = self.optimizer.get_available_optimizations(self.current_profile)
        
        # Crear checkboxes para cada optimización
        self.opt_vars = {}
        for i, (key, opt) in enumerate(optimizations.items()):
            # Frame para cada optimización
            opt_item = ctk.CTkFrame(self.opt_scroll)
            opt_item.pack(fill="x", padx=5, pady=5)
            
            # Checkbox
            var = ctk.BooleanVar(value=opt['default'])
            self.opt_vars[key] = var
            
            cb = ctk.CTkCheckBox(
                opt_item,
                text=opt['name'],
                variable=var,
                width=300
            )
            cb.pack(side="left", padx=10, pady=5)
            
            # Risk label
            risk_color = {"Low": "green", "Medium": "orange", "High": "red"}
            risk_label = ctk.CTkLabel(
                opt_item,
                text=f"Risk: {opt['risk']}",
                text_color=risk_color.get(opt['risk'], "white"),
                width=100
            )
            risk_label.pack(side="left", padx=10)
            
            # Impact label
            impact_label = ctk.CTkLabel(
                opt_item,
                text=f"Impact: {opt['impact']}",
                width=150
            )
            impact_label.pack(side="left", padx=10)
            
            # Description
            desc_label = ctk.CTkLabel(
                opt_item,
                text=opt['description'],
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            desc_label.pack(side="left", padx=10)
            
            # Actualizar progreso
            self.progress.set((i + 1) / len(optimizations))
            self.update()
            
        self.update_status(f"Found {len(optimizations)} optimizations available")
        
    def apply_optimizations(self):
        """Aplica las optimizaciones seleccionadas"""
        selected = [key for key, var in self.opt_vars.items() if var.get()]
        
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one optimization")
            return
            
        if not messagebox.askyesno("Confirm", f"Apply {len(selected)} optimizations?\n\nA backup will be created first."):
            return
            
        # Crear backup primero
        self.create_backup()
        
        # Aplicar optimizaciones en thread separado
        thread = threading.Thread(target=self._apply_optimizations_thread, args=(selected,))
        thread.start()
        
    def _apply_optimizations_thread(self, selected):
        """Thread para aplicar optimizaciones sin bloquear la UI"""
        total = len(selected)
        
        for i, opt_key in enumerate(selected):
            self.update_status(f"Applying {opt_key}...")
            self.progress.set((i + 1) / total)
            
            try:
                result = self.optimizer.apply_optimization(opt_key)
                if result:
                    self.optimizations_applied.append(opt_key)
                time.sleep(0.5)  # Pequeña pausa para visualización
            except Exception as e:
                print(f"Error applying {opt_key}: {e}")
                
        self.update_status(f"✅ Successfully applied {len(self.optimizations_applied)} optimizations")
        messagebox.showinfo("Success", "Optimizations applied!\n\nRestart your PC for changes to take effect.")
        
    def create_backup(self):
        """Crea un punto de restauración"""
        self.update_status("Creating backup...")
        result = self.backup_manager.create_restore_point("UltraOptimizer Backup")
        if result:
            self.update_status("✅ Backup created successfully")
            messagebox.showinfo("Backup", "System restore point created successfully")
        else:
            self.update_status("❌ Failed to create backup")
            messagebox.showerror("Error", "Failed to create restore point")
            
    def restore_defaults(self):
        """Restaura la configuración por defecto"""
        if not messagebox.askyesno("Confirm", "Restore all settings to default?\n\nThis will undo all optimizations."):
            return
            
        self.update_status("Restoring defaults...")
        result = self.optimizer.restore_all()
        if result:
            self.update_status("✅ Settings restored to default")
            messagebox.showinfo("Success", "All settings restored to default")
        else:
            self.update_status("❌ Failed to restore defaults")
            
    def change_profile(self, value):
        """Cambia el perfil de optimización"""
        self.current_profile = value
        self.update_status(f"Profile changed to: {value}")
        self.scan_system()
        
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.configure(text=message)
        self.update()
        
if __name__ == "__main__":
    # Verificar permisos de administrador
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("Admin Required", "Please run as Administrator")
        sys.exit(1)
        
    app = UltraOptimizer()
    app.mainloop()