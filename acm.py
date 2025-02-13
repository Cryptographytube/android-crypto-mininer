import os
import subprocess
import threading
import time
import re
import sys

NAME = "CRYPTOGRAPHYTUBE XMR MINER"

def get_max_threads():
    try:
        output = subprocess.check_output("lscpu | grep 'Thread(s) per core'", shell=True, text=True)
        threads_per_core = int(output.split(":")[1].strip())  
        physical_cores = os.cpu_count() // threads_per_core  
        total_threads = physical_cores * threads_per_core  
        return physical_cores, total_threads  
    except Exception:
        return os.cpu_count(), os.cpu_count()  

PHYSICAL_CORES, TOTAL_THREADS = get_max_threads()

def install_dependencies():
    print("\n🚀 Installing Required Packages...\n")
    subprocess.run("sudo apt update && sudo apt install -y xmrig > /dev/null 2>&1", shell=True)
    subprocess.run("pip install requests > /dev/null 2>&1", shell=True)
    print("\n✅ All Dependencies Installed!\n")

install_dependencies()

print(f"\n{'='*50}")
print(f"🔥 WELCOME TO {NAME} 🔥")
print(f"{'='*50}\n")

WALLET = input("📌 Enter Your Monero Wallet Address: ").strip()

while True:
    try:
        CPU_CORES = int(input(f"⚙️ Enter CPU Threads (Physical: {PHYSICAL_CORES}, Virtual: {TOTAL_THREADS}): ").strip())
        if 1 <= CPU_CORES <= TOTAL_THREADS:
            break
        else:
            print(f"❌ Invalid Input! Please enter a number between 1 and {TOTAL_THREADS}")
    except ValueError:
        print("❌ Invalid Input! Please enter a valid number.")

POOL = "pool.supportxmr.com:3333"

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
                print(f"💠 {NAME} Hash Rate: {real_hashrate} H/s | Using {CPU_CORES} Threads (Physical + Virtual)")

            shares_match = re.search(r"accepted: (\d+)/(\d+)", output)
            if shares_match:
                valid_shares = shares_match.group(1)
                total_shares = shares_match.group(2)
                print(f"✅ {NAME} Shares: {valid_shares}/{total_shares}")

        time.sleep(2)

if __name__ == "__main__":
    print(f"\n🚀 Starting {NAME} with {CPU_CORES} Threads (Physical: {PHYSICAL_CORES}, Virtual: {TOTAL_THREADS})...\n")
    miner_process = start_miner()

    if miner_process:
        stats_thread = threading.Thread(target=display_status, args=(miner_process,), daemon=True)
        stats_thread.start()

        try:
            miner_process.wait()
        except KeyboardInterrupt:
            print(f"\n❌ {NAME} Stopped by User")
            miner_process.terminate()







