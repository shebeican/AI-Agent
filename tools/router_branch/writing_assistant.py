import logging

from clients.xf_astron_client import ChatMessage, xf_astron


logger = logging.getLogger(__name__)

def writing_assistant(state: dict) -> dict:
    user_query = state["user_query"]

    prefix_prompt = f"""你是一个写作大佬，懂得写作，润色文案，只回答用户关于写作相关的问题"""
    messages = [ChatMessage(role="system", content=prefix_prompt), ChatMessage(role="user", content=user_query)]
    response = xf_astron.chat_sync(messages=messages, temperature=0)

    # 解析响应
    try:
        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"LLM返回内容: {content}")
    except Exception as e:
        # 解析失败，默认通过
        logger.error(e)
        content = None

    return {"user_query": user_query, "result": content}
