import os
import subprocess
import threading
import time
import re
import sys

NAME = "CRYPTOGRAPHYTUBE XMR MINER"

def check_integrity():
    with open(__file__, "r", encoding="utf-8") as f:
        script_content = f.read()
    if "CRYPTOGRAPHYTUBE" not in script_content:
        print("\n❌ Script Integrity Check Failed! Do not modify CRYPTOGRAPHYTUBE Branding.\n")
        sys.exit(1)

check_integrity()

print(f"\n🚀 Checking Dependencies...\n")
os.system("pip install requests > /dev/null 2>&1")

print(f"\n{'='*50}")
print(f"🔥 WELCOME TO {NAME} 🔥")
print(f"{'='*50}\n")

WALLET = input("📌 Enter Your Monero Wallet Address: ").strip()
CPU_CORES = int(input(f"⚙️ Enter CPU Cores (Max {os.cpu_count()}): ").strip())
CPU_CORES = min(CPU_CORES, os.cpu_count())  
POOL = "pool.supportxmr.com:3333"

def optimize_cpu():
    try:
        os.system("echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null 2>&1")
        os.system("echo 1000 | sudo tee /proc/sys/vm/nr_hugepages > /dev/null 2>&1")
        os.system("echo 0 | sudo tee /proc/sys/kernel/numa_balancing > /dev/null 2>&1")
        print("✅ CPU Optimization Complete!\n")
    except Exception as e:
        print(f"⚠️ CPU Optimization Failed: {e}")

def start_miner():
    try:
        xmrig_cmd = f"xmrig -o {POOL} -u {WALLET} -p x -t {CPU_CORES} --donate-level=0 --randomx-mode=fast --cpu-priority=5 --av=2"
        return subprocess.Popen(xmrig_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    except Exception as e:
        print(f"❌ {NAME} Start Failed: {e}")
        return None

def display_status(miner_process):
    while True:
        if miner_process.poll() is not None:
            print(f"\n❌ {NAME} Stopped Unexpectedly!\n")
            break

        output = miner_process.stdout.readline()
        if output:
            output = output.strip()
            
            hash_match = re.search(r"(\d+\.?\d*)\s*H/s", output)
            if hash_match:
                real_hashrate = float(hash_match.group(1))
                print(f"💠 {NAME} Hash Rate: {real_hashrate} H/s")

            shares_match = re.search(r"accepted: (\d+)/(\d+)", output)
            if shares_match:
                valid_shares = shares_match.group(1)
                total_shares = shares_match.group(2)
                print(f"✅ {NAME} Shares: {valid_shares}/{total_shares}")

        time.sleep(2)

if __name__ == "__main__":
    print(f"\n🚀 Optimizing CPU & RAM for MAX Speed in {NAME}...\n")
    optimize_cpu()

    print(f"\n🚀 Starting {NAME} in Background...\n")
    miner_process = start_miner()

    if miner_process:
        stats_thread = threading.Thread(target=display_status, args=(miner_process,), daemon=True)
        stats_thread.start()

        try:
            miner_process.wait()
        except KeyboardInterrupt:
            print(f"\n❌ {NAME} Stopped by User")
            miner_process.terminate()







