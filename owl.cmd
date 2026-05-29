@echo off
set "PATH=%PATH%;%WINDIR%\System32"
wsl -d Ubuntu -- /mnt/c/Users/user/.claude-relay/owl.sh
