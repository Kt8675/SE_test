import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union
import os
import requests

args = ["./GetRoadPOI.exe", "110100", "E:\\empty", "b3b33af2c53dae929c336dcb1aec5824 "]
print("执行命令:", args)
process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,

            shell=False
        )

stdout, stderr = process.communicate()
print(stdout)