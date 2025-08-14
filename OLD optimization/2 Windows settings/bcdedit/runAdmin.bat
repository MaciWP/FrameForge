@echo off
bcdedit /set bootux disabled
bcdedit /set tscsyncpolicy enhanced
bcdedit /set x2apicpolicy Enable
bcdedit /set uselegacyapicmode No
echo All commands executed successfully.

