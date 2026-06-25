import json
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)


def ai_review(state: dict):
    logger.info("进入节点: ai_review")
    draft = state.get("draft", "")
    prompt = f"""请判断以下文案是否包含敏感词。

    文案: {draft}

    请以 JSON 格式返回结果，格式如下：
    {{"ai_review_result": 正常返回true/不正常返回false, "reason": "判断理由"}}"""

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
        ai_review_result = result_data.get("ai_review_result", False)
        reason = result_data.get("reason", 'N/A')
        logger.info(f"校验结果: ai_review_result={ai_review_result}, reason={result_data.get('reason', 'N/A')}")
    except (json.JSONDecodeError, KeyError, IndexError):
        # 解析失败，默认不通过
        logger.warning("JSON解析失败，默认不通过")
        ai_review_result, reason = False, 'N/A'

    return {"ai_review_result": ai_review_result, "reject_reason": reason}
