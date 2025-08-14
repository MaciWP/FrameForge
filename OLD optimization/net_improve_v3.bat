@echo off
REM -------------------------------------------------------------------
REM Archivo: C:\NetworkOptimizations\optimize_network.bat
REM Descripción: Optimización de parámetros de red para reducir latencia
REM             y minimizar picos (bufferbloat) en Windows para gaming.
REM             Se busca acercarse a 5ms (+1) en descarga activa y 0+ en carga.
REM Autor: [Tu Nombre]
REM Fecha: 2025-04-05
REM -------------------------------------------------------------------

REM Crear directorio para logs si no existe
if not exist "C:\NetworkOptimizations" mkdir "C:\NetworkOptimizations"

REM Verificar que el script se ejecute como administrador
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Este script debe ejecutarse con privilegios de administrador.
    pause
    exit /b 1
)

REM Habilitar expansión de variables retrasada
setlocal EnableDelayedExpansion

REM Archivo de registro para guardar la salida de los comandos
set "LOGFILE=C:\NetworkOptimizations\APB_Log.txt"

cls
echo -------------------------------------------------------------------
echo           Optimización de Red - Reducción de Bufferbloat
echo         (Optimización para gaming con baja latencia)
echo -------------------------------------------------------------------
echo.

REM --- Menú de Opciones ---
echo 1. Crear Punto de Restauracion
echo 2. Aplicar Ajustes de Red
echo 3. Salir
echo.
set /p choice="Seleccione una opción (1/2/3): "
if "%choice%"=="1" goto :CreateRestorePoint
if "%choice%"=="2" goto :NetworkTweaks
if "%choice%"=="3" goto :Exit
echo Opción no válida.
pause
goto :EOF

:CreateRestorePoint
echo Creando Punto de Restauracion...
REM Permitir creación inmediata de puntos de restauración
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore" /v "SystemRestorePointCreationFrequency" /t REG_DWORD /d 0 /f >> "%LOGFILE%"
REM Crear el punto de restauración mediante PowerShell
powershell -ExecutionPolicy Bypass -Command "Checkpoint-Computer -Description 'Optimización de Red' -RestorePointType 'MODIFY_SETTINGS'" >> "%LOGFILE%"
echo Punto de restauracion creado.
timeout /t 3 /nobreak > NUL
goto :NetworkTweaks

:NetworkTweaks
cls
echo Aplicando ajustes de red...
echo.

REM --- Sección 1: Resetear Configuraciones de Red ---
echo [1/6] Reiniciando configuraciones de red...
ipconfig /release
ipconfig /renew
ipconfig /flushdns
netsh int ip reset >> "%LOGFILE%"
netsh int ipv4 reset >> "%LOGFILE%"
netsh int ipv6 reset >> "%LOGFILE%"
netsh int tcp reset >> "%LOGFILE%"
netsh winsock reset >> "%LOGFILE%"
netsh advfirewall reset >> "%LOGFILE%"
netsh branchcache reset >> "%LOGFILE%"
netsh http flush logbuffer >> "%LOGFILE%"
timeout /t 3 /nobreak > NUL

REM --- Sección 2: Ajustes Globales de TCP ---
echo [2/6] Ajustando parámetros TCP globales...
echo Deshabilitando Network Throttling...
reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v "NetworkThrottlingIndex" /t REG_DWORD /d 4294967295 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Configurando AutoTuning y ECN...
netsh int tcp set global autotuninglevel=disabled >> "%LOGFILE%"
netsh int tcp set global ecncapability=disabled >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Habilitando Direct Cache Access (DCA) y NetDMA...
netsh int tcp set global dca=enabled >> "%LOGFILE%"
netsh int tcp set global netdma=enabled >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Deshabilitando Receive Side Coalescing (RSC) y habilitando Receive Side Scaling (RSS)...
netsh int tcp set global rsc=disabled >> "%LOGFILE%"
netsh int tcp set global rss=enabled >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Ndis\Parameters" /v "RssBaseCpu" /t REG_DWORD /d 1 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Deshabilitando TCP Timestamps y configurando el RTO inicial...
netsh int tcp set global timestamps=disabled >> "%LOGFILE%"
netsh int tcp set global initialRto=2000 >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Habilitando CTCP (algoritmo de congestión)...
netsh int tcp set global congestionprovider=ctcp >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Habilitando TCP Fast Open...
netsh int tcp set global fastopen=enabled >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

REM --- Sección 3: Ajustes de Registro TCP/IP ---
echo [3/6] Ajustando registros TCP/IP...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "DefaultTTL" /t REG_DWORD /d 64 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "Tcp1323Opts" /t REG_DWORD /d 1 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Configurando TcpMaxDupAcks y deshabilitando SACK...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "TcpMaxDupAcks" /t REG_DWORD /d 2 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "SackOpts" /t REG_DWORD /d 0 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Incrementando MaxUserPort y reduciendo TcpTimedWaitDelay...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "MaxUserPort" /t REG_DWORD /d 65534 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters" /v "TcpTimedWaitDelay" /t REG_DWORD /d 30 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

REM --- Sección 4: Ajustes de Prioridad y Socket ---
echo [4/6] Ajustando prioridades de red y parámetros de socket...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider" /v "LocalPriority" /t REG_DWORD /d 4 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider" /v "HostsPriority" /t REG_DWORD /d 5 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider" /v "DnsPriority" /t REG_DWORD /d 6 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\ServiceProvider" /v "NetbtPriority" /t REG_DWORD /d 7 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Ajustando tamaño de direcciones de socket...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Winsock" /v "MinSockAddrLength" /t REG_DWORD /d 16 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Winsock" /v "MaxSockAddrLength" /t REG_DWORD /d 16 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo Deshabilitando el algoritmo de Nagle...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v "TcpAckFrequency" /t REG_DWORD /d 1 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v "TCPNoDelay" /t REG_DWORD /d 1 /f >> "%LOGFILE%"
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces" /v "TcpDelAckTicks" /t REG_DWORD /d 0 /f >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

REM --- Sección 5: Ajustes Específicos para Adaptadores de Red ---
echo [5/6] Ajustando configuraciones específicas de la NIC...
for /f "tokens=*" %%n in ('Reg query "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}" /v "*SpeedDuplex" /s ^| findstr "HKEY"') do (
    echo Configurando adaptador: %%n

    REM Deshabilitar ahorro de energía y otras características de la NIC
    reg add "%%n" /v "AutoPowerSaveModeEnabled" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "AutoDisableGigabit" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "AdvancedEEE" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "DisableDelayedPowerUp" /t REG_SZ /d "2" /f >> "%LOGFILE%"
    reg add "%%n" /v "*EEE" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EEE" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnablePME" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EEELinkAdvertisement" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnableGreenEthernet" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnableSavePowerNow" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnablePowerManagement" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnableDynamicPowerGating" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnableConnectedPowerGating" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "EnableWakeOnLan" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "GigaLite" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "NicAutoPowerSaver" /t REG_SZ /d "2" /f >> "%LOGFILE%"
    reg add "%%n" /v "PowerDownPll" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "PowerSavingMode" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "ReduceSpeedOnPowerDown" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "SmartPowerDownEnable" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "S5NicKeepOverrideMacAddrV2" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "S5WakeOnLan" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "ULPMode" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "WakeOnDisconnect" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "*WakeOnMagicPacket" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "*WakeOnPattern" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "WakeOnLink" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "WolShutdownLinkSpeed" /t REG_SZ /d "2" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Deshabilitando Jumbo Frame en %%n...
    reg add "%%n" /v "JumboPacket" /t REG_SZ /d "1514" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Configurando buffers de transmisión y recepción en %%n...
    reg add "%%n" /v "TransmitBuffers" /t REG_SZ /d "4096" /f >> "%LOGFILE%"
    reg add "%%n" /v "ReceiveBuffers" /t REG_SZ /d "512" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Configurando Offloads en %%n...
    reg add "%%n" /v "IPChecksumOffloadIPv4" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "LsoV1IPv4" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "LsoV2IPv4" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "LsoV2IPv6" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "PMARPOffload" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "PMNSOffload" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "TCPChecksumOffloadIPv4" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "TCPChecksumOffloadIPv6" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "UDPChecksumOffloadIPv6" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "UDPChecksumOffloadIPv4" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Habilitando RSS en la NIC %%n...
    reg add "%%n" /v "RSS" /t REG_SZ /d "1" /f >> "%LOGFILE%"
    reg add "%%n" /v "*NumRssQueues" /t REG_SZ /d "2" /f >> "%LOGFILE%"
    reg add "%%n" /v "RSSProfile" /t REG_SZ /d "3" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Deshabilitando Flow Control en %%n...
    reg add "%%n" /v "*FlowControl" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "FlowControlCap" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Removiendo delays de interrupción en %%n...
    reg add "%%n" /v "TxIntDelay" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "TxAbsIntDelay" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "RxIntDelay" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    reg add "%%n" /v "RxAbsIntDelay" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL

    echo Removiendo notificaciones de adaptador y deshabilitando Interrupt Moderation en %%n...
    reg add "%%n" /v "FatChannelIntolerant" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL
    reg add "%%n" /v "*InterruptModeration" /t REG_SZ /d "0" /f >> "%LOGFILE%"
    timeout /t 1 /nobreak > NUL
)

REM --- Sección Opcional: DSCP/QoS para Tráfico Gaming ---
echo [Opcional] Configurando DSCP para tráfico Gaming...
echo (Verifique que su router soporte DSCP QoS y ajuste los puertos según sus juegos.)
powershell -Command "New-NetQosPolicy -Name 'GamingTraffic' -IPProtocol 'TCP' -LocalPort 3074,27015,7777 -DSCPAction 46 -PolicyStore ActiveStore" >> "%LOGFILE%" 2>&1
timeout /t 1 /nobreak > NUL

REM --- Sección Final: Ajustes Adicionales ---
echo [6/6] Ajustando configuraciones finales...
echo Habilitando WeakHost Send y Receive en todos los adaptadores...
powershell -Command "Get-NetAdapter -IncludeHidden | Set-NetIPInterface -WeakHostSend Enabled -WeakHostReceive Enabled -ErrorAction SilentlyContinue" >> "%LOGFILE%"
timeout /t 1 /nobreak > NUL

echo.
echo -------------------------------------------------------------------
echo       Optimización de Red Completada con Éxito.
echo -------------------------------------------------------------------
echo.
pause
REM La ventana permanecerá abierta para que puedas copiar la información.
exit /b 0

:Exit
echo Saliendo del script.
pause
exit /b 0
