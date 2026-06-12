#!/usr/bin/env python3
"""
診斷並修復 Hermes VPS 的 gh auth 問題
執行方式：python3 ~/.openclaw/workspace/scripts/fix_hermes_gh_auth.py
"""
import subprocess
import sys

HOST = "113.29.232.178"
USER = "root"
PASS = "C8GwSuyj"

def run_remote(cmd):
    """用 sshpass 執行遠端指令"""
    result = subprocess.run(
        ["sshpass", "-p", PASS, "ssh", "-o", "StrictHostKeyChecking=no",
         "-o", "ConnectTimeout=10", f"{USER}@{HOST}", cmd],
        capture_output=True, text=True
    )
    return result.stdout + result.stderr

def run_remote_paramiko(cmd):
    """用 paramiko 執行遠端指令"""
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=PASS, timeout=10)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode() + stderr.read().decode()
    client.close()
    return out

# 嘗試 sshpass，失敗就用 paramiko
try:
    subprocess.run(["sshpass", "--version"], capture_output=True, check=True)
    run_fn = run_remote
    print("使用 sshpass 連線...")
except (subprocess.CalledProcessError, FileNotFoundError):
    try:
        import paramiko
        run_fn = run_remote_paramiko
        print("使用 paramiko 連線...")
    except ImportError:
        print("安裝 paramiko...")
        subprocess.run([sys.executable, "-m", "pip", "install", "paramiko", "-q"])
        import paramiko
        run_fn = run_remote_paramiko
        print("使用 paramiko 連線...")

print("\n=== 1. 診斷 gh auth 狀態 ===")
print(run_fn("gh auth status 2>&1 || echo 'gh 未認證'"))

print("=== 2. 現有設定檔 ===")
print(run_fn("cat ~/.config/gh/hosts.yml 2>/dev/null || echo '無 hosts.yml'"))

print("=== 3. 環境變數 ===")
print(run_fn("echo GH_TOKEN=${GH_TOKEN:-空}; echo GITHUB_TOKEN=${GITHUB_TOKEN:-空}"))

print("=== 4. .bashrc / .profile 裡的 token ===")
print(run_fn("grep -E 'GH_TOKEN|GITHUB_TOKEN|gh auth' ~/.bashrc ~/.profile ~/.bash_profile 2>/dev/null || echo '無相關設定'"))

print("=== 5. gh 版本 ===")
print(run_fn("gh --version 2>&1 || echo 'gh 未安裝'"))

print("\n--- 診斷完成，請把以上輸出給助教看 ---")
