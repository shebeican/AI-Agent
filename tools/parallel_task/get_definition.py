import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)

def get_definition(state: dict):
    logger.info("进入节点: get_definition")
    user_query = state.get("user_query", "")

    messages = [ChatMessage(role="system", content=f"你是一个善于发现文案定义的专家，请找出用户文案的定义"), ChatMessage(role="user", content=f"请回答以下问题：{user_query}")]
    response = xf_astron.chat_sync(messages=messages)

    # 解析响应
    content = response.get("content", [{}])[0].get("text", "")
    logger.info(f"生成完成，答案长度: {len(content)}")
    return {"definition": content}
