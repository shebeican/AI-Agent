import requests
from typing import List, Dict, Generator
from pydantic import BaseModel

from config.config import settings


class ChatMessage(BaseModel):
    role: str
    content: str


class XfAstronClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic",
        model: str = "astron-code-latest",
        timeout: int = 60
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def chat_sync(
        self,
        messages: List[ChatMessage],
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Dict:
        """同步一次性返回完整回答"""
        url = f"{self.base_url}/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [msg.model_dump() for msg in messages]
        }
        try:
            resp = requests.post(
                url=url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"讯飞MaaS网络请求异常: {str(e)}")

        if resp.status_code != 200:
            raise Exception(f"讯飞接口错误: {resp.text}")
        return resp.json()

    def chat_stream(
        self,
        messages: List[ChatMessage],
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Generator[str, None, None]:
        """流式SSE逐块输出，适配FastAPI StreamingResponse"""
        url = f"{self.base_url}/v1/messages"
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
            "messages": [msg.model_dump() for msg in messages]
        }
        try:
            resp = requests.post(
                url=url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                stream=True
            )
        except requests.exceptions.RequestException as e:
            yield f"error: {str(e)}"
            return

        if resp.status_code != 200:
            yield f"error: status={resp.status_code}, msg={resp.text}"
            return

        # 逐行解析SSE数据流
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            data_str = line[6:]
            if data_str == "[DONE]":
                break
            try:
                import json
                chunk = json.loads(data_str)
                # 提取文本增量
                if chunk.get("type") == "content_block_delta":
                    text = chunk["delta"].get("text", "")
                    yield text
            except Exception:
                continue


# 全局单例实例
xf_astron = XfAstronClient(
    api_key=settings.XF_API_KEY,
)
