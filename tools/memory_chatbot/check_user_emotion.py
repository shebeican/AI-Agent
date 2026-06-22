import logging

from clients.xf_astron_client import ChatMessage, xf_astron



logger = logging.getLogger(__name__)

def check_user_emotion(state: dict):
    last_msg = state["messages"][-1].content

    prompt = f"""
    判断下面用户话语的情绪，只输出一个单词：negative / normal / positive
    用户话语：{last_msg}
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = xf_astron.chat_sync(messages=messages, temperature=0)

    # 解析响应
    try:
        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"LLM返回内容: {content}")
    except Exception as e:
        logger.error(e)
        content = None

    return {'messages': state['messages'], 'user_emotion': content}
