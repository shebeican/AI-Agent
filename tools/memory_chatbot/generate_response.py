import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)

def generate_response(state: dict):
    user_emotion = state["user_emotion"]
    mesgs = state["messages"]

    if user_emotion == 'negative':
        prompt_prefix = f"""
        用户现在情绪很低落，清闲温柔安慰一句，再回答其他问题
        """
    else:
        prompt_prefix = "正常回答问题"

    messages = [ChatMessage(role="system", content=prompt_prefix)] + [ChatMessage(role='user', content=m.content) for m in mesgs]
    response = xf_astron.chat_sync(messages=messages, temperature=0)

    # 解析响应
    try:
        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"LLM返回内容: {content}")
    except Exception as e:
        logger.error(e)
        content = None

    return {'messages': [content]}
