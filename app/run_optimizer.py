#!/usr/bin/env python
"""
UltraOptimizer Quick Launcher
Verifica dependencias y lanza la aplicación
"""

import sys
import os
import subprocess
import ctypes

def is_admin():
    """Verifica si se ejecuta como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    required = ['customtkinter', 'psutil', 'GPUtil', 'wmi', 'win32com']
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Faltan dependencias: {', '.join(missing)}")
        print("\n📦 Instalando dependencias...")
        
        packages = {
            'customtkinter': 'customtkinter',
            'psutil': 'psutil', 
            'GPUtil': 'GPUtil',
            'wmi': 'WMI',
            'win32com': 'pywin32'
        }
        
        for module in missing:
            package = packages.get(module, module)
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ Dependencias instaladas!")
        return False
    return True

def main():
    print("=" * 50)
    print("🎮 UltraOptimizer v1.0 - Gaming Performance Tool")
    print("=" * 50)
    
    # Verificar admin
    if not is_admin():
        print("\n⚠️  ATENCIÓN: Necesitas ejecutar como Administrador")
        print("Reiniciando con permisos de administrador...")
        
        # Reiniciar como admin
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)
    
    print("✅ Ejecutando como Administrador")
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n⚠️  Reinicia el script después de instalar las dependencias")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    print("✅ Todas las dependencias están instaladas")
    
    # Lanzar aplicación principal
    print("\n🚀 Iniciando UltraOptimizer...")
    print("-" * 50)
    
    try:
        import main
        main.UltraOptimizer().mainloop()
    except Exception as e:
        print(f"\n❌ Error al iniciar: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()