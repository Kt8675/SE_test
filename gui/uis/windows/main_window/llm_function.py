# lmm_function.py
import os
import json
from openai import OpenAI
import openai

CONFIG_PATH = "llm_config.json"

def save_api_key(api_key: str):
    config = {"api_key": api_key}
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def load_api_key() -> str:
    print(os.path.abspath(__file__))
    print(CONFIG_PATH)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("api_key", "")
    return ""

import os
import re
import requests
import unicodedata
from string import Template
from typing import cast

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

class BaseModel:
    name = "base"
    envs = {}
    lang_map: dict[str, str] = {}
    CustomPrompt = False

    def __init__(self, model: str, ignore_cache: bool = False):
        self.model = model
        self.ignore_cache = ignore_cache

    def set_envs(self, envs):
        self.envs = self.__class__.envs.copy()
        if envs is not None:
            self.envs.update(envs)

    def translate(self, text: str, ignore_cache: bool = False) -> str:
        return self.do_translate(text)

    def prompt(self, text: str, prompt_template: Template | None = None) -> list[dict[str, str]]:
        try:
            return [
                {
                    "role": "user",
                    "content": cast(Template, prompt_template).safe_substitute(
                        {
                            "text": text,
                        }
                    ),
                }
            ]
        except Exception:
            pass

        return [
            {
                "role": "user",
                "content": (
                    f"{text}"
                ),
            }
        ]

class ModelScopeModel(BaseModel):
    name = "modelscope"
    envs = {
        "MODELSCOPE_BASE_URL": "https://api-inference.modelscope.cn/v1",
        "MODELSCOPE_API_KEY": None,
        "MODELSCOPE_MODEL": "Qwen/Qwen2.5-7B-Instruct",
    }

    def __init__(
        self,
        model: str = None,
        base_url: str = None,
        api_key: str = None,
        envs: dict = None,
        prompt: Template = None,
        ignore_cache: bool = False,
    ):
        super().__init__(model, ignore_cache)
        self.set_envs(envs)
        self.base_url = base_url or self.envs["MODELSCOPE_BASE_URL"]
        self.api_key = api_key or self.envs["MODELSCOPE_API_KEY"]
        self.model = model or self.envs["MODELSCOPE_MODEL"]
        self.prompt_template = prompt

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def do_translate(self, text: str) -> str:
        try:
            messages = self.prompt(text, self.prompt_template)
            body = {
                "model": self.model,
                "messages": messages
            }
            response = self.session.post(f"{self.base_url}/chat/completions", json=body)
            
            # 直接告知用户部分常见错误的具体解决措施
            if response.status_code == 401:
                return "认证失败：请检查 ModelScope API Key 是否正确或已过期。"

            elif response.status_code == 403:
                return "权限不足：您的 API Key 没有访问该模型的权限。"

            elif response.status_code == 429:
                return "请求过于频繁：触发了速率限制，请稍后再试。"

            elif response.status_code >= 400:
                return f"API请求错误（HTTP {response.status_code}）：{response.text}"
            
            response.raise_for_status()  # 触发HTTP错误（4xx/5xx）
            content = response.json()["choices"][0]["message"]["content"]
            return remove_control_characters(content.strip())

        except requests.exceptions.RequestException as e:
            # 网络请求异常（超时/连接错误等）
            return f"API请求失败，如是max entries请检查电脑网络连接情况: {str(e)}"
        except ValueError as e:
            # JSON解析错误
            return f"响应数据解析失败: {str(e)}"
        except KeyError as e:
            # 响应数据结构异常
            return f"响应数据缺少必要字段: {str(e)}"
        except Exception as e:
            # 其他未知异常
            return f"处理过程中发生未知错误: {str(e)}"

class DeepSeekModel(BaseModel):
    name = "deepseek"
    envs = {
        "DEEPSEEK_BASE_URL": "https://api.deepseek.com/v1",
        "DEEPSEEK_API_KEY": None,
        "DEEPSEEK_MODEL": "deepseek-chat"
    }

    def __init__(self, 
        api_key: str,        
        model: str = None,
        base_url: str = None,
        envs: dict = None,
        prompt: Template = None,
        ignore_cache: bool = False,):
        super().__init__(model, ignore_cache)
        self.base_url = self.envs["DEEPSEEK_BASE_URL"]
        self.model = self.envs["DEEPSEEK_MODEL"]
        self.prompt_template = prompt
        
        # 扩展请求头
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def do_chat(self, text: str) -> str:
        try:
            # 构造消息体（兼容OpenAI格式）
            messages = self.prompt(text, self.prompt_template)
            
            # 直接使用requests模拟OpenAI SDK的请求结构
            body = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,  # 可配置参数（默认值参考DeepSeek文档）
                "max_tokens": 1000,  # 可配置参数
                "stream": False      # 明确关闭流式响应
            }

            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a expert in searching road-related information."},
                    {"role": "user", "content": f"{messages}"},
                ],
                stream=False
            )

            # 验证响应结构
            if not hasattr(response, 'choices') or not response.choices:
                return "错误：API返回了无效的响应结构"

            if not hasattr(response.choices[0], 'message') or not hasattr(response.choices[0].message, 'content'):
                return "错误：API返回的消息格式不符合预期"

            # 获取并清理响应内容
            content = response.choices[0].message.content
            if not content:
                return "警告：模型返回了空内容"

            # 解析响应（与官方SDK返回结构一致）
            print(response.choices[0].message.content)
            return response.choices[0].message.content

        except openai.APIError as e:
                return f"API错误：{str(e)}"

        except openai.APIConnectionError as e:
            # 处理网络连接错误
            return f"网络连接错误：{str(e)}。请检查您的网络连接是否正常"

        except openai.RateLimitError as e:
            # 处理速率限制错误(429)
            return "请求过于频繁：已触发速率限制，请稍后再试"

        except openai.BadRequestError as e:
            # 处理请求参数错误(4xx)
            error_detail = e.body.get('error', {}).get('message', '未知错误')
            return f"参数错误：{error_detail}"

        except Exception as e:
            # 处理其他所有异常(包括requests异常，因为OpenAI SDK内部可能抛出)
            return f"处理过程中发生错误：{str(e)}"

def handle_llm_query(model_provider:str, api_key: str, user_input: str, prompt_prefix: str = "") -> str:

    # 需要设置 ModelScope 的 API KEY
    API_KEY = api_key
    
    if model_provider == "ModelScope":
        translator = ModelScopeModel(
            api_key=API_KEY
        )
    else:
        translator = DeepSeekModel(
            api_key=API_KEY
        )

    # 拼接提示词与用户输入
    full_input = f"{prompt_prefix.strip()} {user_input.strip()}".strip()

    # 调用大模型
    output = translator.translate(full_input)

    return output



