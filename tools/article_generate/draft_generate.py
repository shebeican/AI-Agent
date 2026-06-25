import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)


def draft_generate(state: dict):
    logger.info("进入节点: draft_generate")
    user_query = state.get("user_query", "")
    ai_review_result = state.get("ai_review_result")
    manual_review_result = state.get("manual_review_result")
    reject_reason = state.get("reject_reason", "")
    draft = state.get("draft", "")

    # 更新重试次数
    max_retries = state.get("max_retries", 0) + 1

    if ai_review_result is None and manual_review_result is None:
        # 首次生成
        prompt = f"根据下方这份文字，生成对应的自媒体内容：{user_query}"
    else:
        # 审核不通过，重新生成
        prompt = f"用户输入：{user_query}\n\n生成内容：{draft}\n\n审核不通过原因：{reject_reason}\n\n请根据以上信息重新生成一份改进的内容。"

    try:
        messages = [ChatMessage(role="system", content="你是一个文案专家"), ChatMessage(role="user", content=prompt)]
        response = xf_astron.chat_sync(messages=messages)

        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"文稿生成完成，答案长度: {len(content)}")
        return {"draft": content, "max_retries": max_retries}
    except Exception as e:
        logger.error(f"文稿生成失败: {str(e)}")
        return {"draft": f"文稿生成失败: {str(e)}", "max_retries": max_retries}
