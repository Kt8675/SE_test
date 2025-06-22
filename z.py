# import subprocess
# from pathlib import Path
# from typing import Optional, Tuple, Union
# import os
# import requests

# args = ["./GetRoadPOI.exe", "110100", "E:\\empty", "b3b33af2c53dae929c336dcb1aec5824 "]
# print("执行命令:", args)
# process = subprocess.Popen(
#             args,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,

#             shell=False
#         )

# stdout, stderr = process.communicate()
# print(stdout)
import subprocess
import threading
import time
def run_task():
    # 启动子进程
    process = subprocess.Popen(['echo', 'Hello from subprocess'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print("Subprocess completed:", stdout.decode())

def main():
    print("Main process starts.")
    
    # 创建并启动子进程线程
    thread = threading.Thread(target=run_task)
    thread.start()

    
    # 主进程可以继续执行其他任务
    while thread.is_alive():
        print("Main process doing other tasks...")
        time.sleep(1)
    
    print("Main process finished.")

if __name__ == "__main__":
    main()
