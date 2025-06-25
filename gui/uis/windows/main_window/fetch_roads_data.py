import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union
import os
import requests
import time

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
    # 构造命令参数列表
    args = ["./GetRoadPOI.exe", city_code]

    if output_dir.strip():

        output_path = Path(output_dir.strip())
        if not output_path.exists():
            raise FileNotFoundError(f"输出目录不存在: {output_path}")
        args.append(str(output_path.resolve()))

    if amap_key.strip():

        args.append(amap_key.strip())

    # print(args)

    try:
        # print("启动进程...")
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

def get_road_tian(
    city_code: str,
    output_dir: str = "",  # 改为空字符串默认值
    amap_key: str = ""    # 改为空字符串默认值
) -> str:
    if not city_code.strip():
        raise ValueError("行政区划代码不能为空")

    # 处理输出目录（空字符串跳过，非空时验证路径）
    if output_dir.strip():  # 只有非空字符串才处理
        output_path = Path(output_dir.strip())
        if not output_path.exists():
            raise FileNotFoundError(f"输出目录不存在: {output_path}")
    else:
        output_path = Path.cwd()

    # 筛选关键字（空字符串跳过）
    if amap_key.strip():  # 只有非空字符串才传递
        keyword = amap_key.strip()
    # 执行命令
    msg = fetch_tian(city_code, keyword, output_dir)

    return msg

   
    
def fetch_tian(specify, keyword, output_dir):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    }

    url = 'http://api.tianditu.gov.cn/v2/search?postStr={\"keyWord\":' +'\"'+ keyword + '\"'+",\"queryType\":12,\"start\":0,\"count\":10,\"specify\":" + '\"' + specify + '\"}' + '}&type=query&tk=a35c5ae57e93f574590e0ddd83ee6acb'    
    
    response = requests.get(url, headers=headers)

    # 如果请求成功，返回 200
    if response.status_code == 200:
        # 获取 JSON 数据
        data = response.json()
    
        with open(os.path.join(output_dir, 'tian_data.json'), 'w', encoding='utf-8') as f:
            for i in data['pois']:
                print(i['name'], i['address'])
                # print(i['address'])
                f.write(str(i['name'] + ' ' + i['address'] + '\n'))
        return f"请求成功，原始数据输出路径：./{os.path.join(output_dir, 'tian_data.json')}"

    else:
        print(f"请求失败，状态码: {response.status_code}")
        return f"请求失败，状态码: {response.status_code}"

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