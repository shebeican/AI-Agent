import logging

from clients.xf_astron_client import ChatMessage, xf_astron


logger = logging.getLogger(__name__)

def summary(state:dict) -> dict:
    draft = state.get("draft", "")
    user_query = state.get("user_query", "")
    logger.info("进入节点: summary")
    prompt = f"""
    将下面这段话整合成一个最终文稿
    用户输入：{user_query},
    文稿：{draft}
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = xf_astron.chat_sync(messages=messages)

    # 解析响应
    content = response.get("content", [{}])[0].get("text", "")
    logger.info(f"生成完成，答案长度: {len(content)}")
    return {"result": content}
