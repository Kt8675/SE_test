import subprocess
from pathlib import Path
from typing import Optional, Tuple
import os

def get_road_poi(
    city_code: str,
    output_dir: str = "",  # 改为空字符串默认值
    amap_key: str = ""    # 改为空字符串默认值
) -> Tuple[str, str]:
    """
    调用GetRoadPOI.exe获取道路POI数据（阻塞式）

    Args:
        city_code: 行政区划代码（必填，如"110000"）
        output_dir: 输出目录路径（空字符串表示使用默认值）
        amap_key: 高德地图API Key（空字符串表示使用默认值）

    Returns:
        Tuple[标准输出, 错误输出]

    Raises:
        subprocess.CalledProcessError: 程序返回非0状态码
        ValueError: 参数验证失败
        FileNotFoundError: 指定输出目录不存在
    """
    # 参数验证
    if not city_code.strip():
        raise ValueError("行政区划代码不能为空")
    
    # 构造命令参数列表
    args = ["./GetRoadPOI.exe", city_code]
    
    # 处理输出目录（空字符串跳过，非空时验证路径）
    if output_dir.strip():  # 只有非空字符串才处理
        output_path = Path(output_dir.strip())
        if not output_path.exists():
            raise FileNotFoundError(f"输出目录不存在: {output_path}")
        args.append(str(output_path.resolve()))
    
    # 处理高德Key（空字符串跳过）
    if amap_key.strip():  # 只有非空字符串才传递
        args.append(amap_key.strip())

    # 执行命令
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True,
            shell=False
        )
    except subprocess.CalledProcessError as e:
        # 增强错误信息可读性
        err_msg = f"程序执行失败(返回码:{e.returncode})\n错误输出:\n{e.stderr}"
        raise subprocess.CalledProcessError(e.returncode, e.cmd, err_msg) from None

    # 提取成功信息（兼容不同输出格式）
    success_msg = ""
    for line in result.stdout.splitlines():
        if "数据已保存到" in line or "Saved to" in line.lower():
            success_msg = line
            break

    return (
        f"{success_msg}\n[程序输出]\n{result.stdout}" if success_msg else result.stdout,
        result.stderr
    )

# 使用示例
if __name__ == "__main__":
    test_cases = [
        ("110000", "", ""),          # 仅必填参数
        ("110000", "./output", ""),  # 自定义输出目录
        # ("110000", "", "your_key"),  # 自定义Key
        ("", "", ""),                # 错误测试：空city_code
        ("110000", "/nonexistent", "")  # 错误测试：不存在路径
    ]

    for code, out_dir, key in test_cases:
        print(f"\n测试用例: code={code}, out_dir={out_dir}, key={key}")
        try:
            output, err = get_road_poi(code, out_dir, key)
            print("✅ 调用成功")
            print(output)
        except Exception as e:
            print(f"❌ 错误: {type(e).__name__}: {str(e)}")