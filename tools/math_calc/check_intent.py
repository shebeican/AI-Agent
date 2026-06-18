import json
import logging

from clients.xf_astron_client import ChatMessage, xf_astron


logger = logging.getLogger(__name__)

def check_intent(state: dict) -> dict:
    user_query = state["user_query"]
    result = state["result"]

    if result:
        return {"math_tool_type": None}  # 设置为 None 让路由走向结束

    # 使用讯飞星辰 LLM 校验答案质量
    prompt = f"""请判断以下问题需要用到什么数学工具。

    用户问题: {user_query}

    请以 JSON 格式返回结果，格式如下：
    {{"a": 10, "b": 2, "math_tool_type": None / add / divide / multiply / subtract, "reason": "判断理由"}}"""

    messages = [ChatMessage(role="user", content=prompt)]
    response = xf_astron.chat_sync(messages=messages, temperature=0)

    # 解析响应
    try:
        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"LLM返回内容: {content}")

        # 提取 markdown 代码块中的 JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result_data = json.loads(content)
        math_tool_type = result_data.get("math_tool_type", None)
        reason = result_data.get("reason", None)
        a = result_data.get("a", 0)
        b = result_data.get("b", 0)
        logger.info(f"校验结果: math_tool_type={math_tool_type}, reason={reason}, a={a}, b={b}")
    except (json.JSONDecodeError, KeyError, IndexError):
        # 解析失败，默认通过
        logger.warning("JSON解析失败，默认通过")
        math_tool_type, reason, a, b = None, None, 0, 0

    logger.info(f"math_tool_type={math_tool_type}")
    return {"math_tool_type": math_tool_type, "result": reason, 'a': a, 'b': b}
