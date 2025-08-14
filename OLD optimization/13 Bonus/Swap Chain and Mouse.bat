@echo off

setx DXGL_FRAME_LATENCY_WAITABLE_OBJECT "1" /M
setx DXGI_ALLOW_TEARING "1" /M
setx DXGI_SWAPCHAIN_FLUSH "0" /M
setx GPU_MAX_ALLOC_PERCENT "100" /M
setx GPU_SINGLE_ALLOC_PERCENT "100" /M
setx MOUSE_RAW_INPUT "1" /M
setx KEYBOARD_FAST_INIT "1" /M
setx DX12_AGGRESSIVE_PIPELINE "1" /M
setx DX12_FORCE_WARP "0" /M
setx GPU_SYNC_OBJECTS "0" /M

reg add "HKLM\SYSTEM\CurrentControlSet\Services\mouclass" /v "PollingInterval" /t REG_DWORD /d "0" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\mouhid" /v "MaximumPortsServiced" /t REG_DWORD /d "16" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS" /v "EnableHwCursor" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS" /v "DisableDWM" /t REG_DWORD /d "1" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\nvlddmkm\FTS" /v "UsePolledSwapChain" /t REG_DWORD /d "1" /f
