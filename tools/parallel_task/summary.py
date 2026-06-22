import logging

from clients.xf_astron_client import ChatMessage, xf_astron


logger = logging.getLogger(__name__)

def summary(state:dict) -> dict:
    definition = state.get("definition")
    example = state.get("example")
    pros_cons = state.get("pros_cons")
    logger.info("进入节点: summary")
    user_query = state.get("user_query", "")
    prompt = f"""
    将下面这段话整合一下
    原句：{user_query},
    定义：{definition},
    优缺点: {pros_cons},
    示例: {example}
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = xf_astron.chat_sync(messages=messages)

    # 解析响应
    content = response.get("content", [{}])[0].get("text", "")
    logger.info(f"生成完成，答案长度: {len(content)}")
    return {"summary": content}
