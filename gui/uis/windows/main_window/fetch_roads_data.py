import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union
import os

def get_road_poi(
    city_code: str,
    output_dir: str = "",
    amap_key: str = ""
) -> Union[Tuple[str, str], subprocess.Popen]:
    """
    获取道路POI数据，非阻塞模式，创建新进程进行数据获取

    Args:
        city_code: 行政区划代码（必填，如"110000"）
        output_dir: 输出目录路径（空字符串表示使用默认值）
        amap_key: 高德地图API Key（空字符串表示使用默认值）
        non_blocking: 是否非阻塞运行（True返回进程对象）

    Returns:
        阻塞模式: Tuple[标准输出, 错误输出]
        非阻塞模式: subprocess.Popen 进程对象

    Raises:
        ValueError: 参数验证失败
        FileNotFoundError: 指定输出目录不存在
    """
    # 参数验证
    if not city_code.strip():
        raise ValueError("行政区划代码不能为空")
    
    # 构造命令参数列表
    args = ["./GetRoadPOI.exe", city_code]
    
    if output_dir.strip():
        output_path = Path(output_dir.strip())
        if not output_path.exists():
            raise FileNotFoundError(f"输出目录不存在: {output_path}")
        args.append(str(output_path.resolve()))
    
    if amap_key.strip():
        args.append(amap_key.strip())

    try:
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        return process
    except Exception as e:
        raise RuntimeError(f"启动进程失败: {str(e)}") from e
