"""
校验 raw_answer 质量，不达标则置 need_revise=True
"""
import json
import logging
from clients.xf_astron_client import xf_astron, ChatMessage

logger = logging.getLogger(__name__)


def check_answer_tool(state: dict) -> dict:
    """
    校验答案质量的节点函数

    :param state: 工作流状态
    :return: 状态更新
    """
    logger.info("进入节点: check_answer")
    raw_answer = state.get("raw_answer", "")
    user_query = state.get("user_query", "")

    # 如果还没有答案，需要生成
    if not raw_answer:
        logger.info("答案为空，需要重新生成")
        return {"need_revise": True}

    # 使用讯飞星辰 LLM 校验答案质量
    prompt = f"""请判断以下回答是否合格。

    用户问题: {user_query}
    
    回答: {raw_answer}
    
    判断标准:
    1. 回答是否与问题相关
    2. 回答是否有实质内容（不是空话或重复）
    3. 回答是否完整
    
    请以 JSON 格式返回结果，格式如下：
    {{"is_valid": true/false, "reason": "判断理由"}}"""

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
        is_valid = result_data.get("is_valid", False)
        logger.info(f"校验结果: is_valid={is_valid}, reason={result_data.get('reason', 'N/A')}")
    except (json.JSONDecodeError, KeyError, IndexError):
        # 解析失败，默认通过
        logger.warning("JSON解析失败，默认通过")
        is_valid = True

    logger.info(f"need_revise={not is_valid}")
    return {"need_revise": not is_valid}
