import logging

from clients.xf_astron_client import ChatMessage, xf_astron


logger = logging.getLogger(__name__)

def summary(state:dict) -> dict:
    budget_decomposition = state.get("budget_decomposition")
    requirement_decomposition = state.get("requirement_decomposition")
    user_query = state.get("user_query", "")
    logger.info("进入节点: summary")
    prompt = f"""
    将下面这段话整合一下
    项目：{user_query},
    三个需求：{budget_decomposition},
    估算金额: {requirement_decomposition},
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = xf_astron.chat_sync(messages=messages)

    # 解析响应
    content = response.get("content", [{}])[0].get("text", "")
    logger.info(f"生成完成，答案长度: {len(content)}")
    return {"result": content}
