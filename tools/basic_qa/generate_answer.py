"""
接收状态，调用 LLM，写入 raw_answer
"""
import logging
from clients.xf_astron_client import xf_astron, ChatMessage

logger = logging.getLogger(__name__)


def generate_answer_tool(state: dict) -> dict:
    """
    生成答案的节点函数

    :param state: 工作流状态
    :return: 状态更新
    """
    logger.info("进入节点: generate_answer")
    user_query = state.get("user_query", "")

    # 使用讯飞星辰 LLM 生成答案
    messages = [ChatMessage(role="user", content=f"请回答以下问题：{user_query}")]
    response = xf_astron.chat_sync(messages=messages)

    # 解析响应
    content = response.get("content", [{}])[0].get("text", "")
    logger.info(f"生成完成，答案长度: {len(content)}")
    return {"raw_answer": content, "need_revise": False}
