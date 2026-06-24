"""
需求拆解子图
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)


# 子图状态定义
class RequirementDecompositionState(TypedDict):
    user_query: str
    requirement_result: str


def analyze_requirement(state: dict):
    """分析需求节点"""
    logger.info("进入节点: analyze_requirement")
    user_query = state.get("user_query", "")

    try:
        messages = [ChatMessage(role="user", content=f"拆分以下项目三个核心需求点：{user_query}")]
        response = xf_astron.chat_sync(messages=messages)

        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"需求分析完成，答案长度: {len(content)}")
        return {"requirement_result": content}
    except Exception as e:
        logger.error(f"需求分析失败: {str(e)}")
        return {"requirement_result": f"需求分析失败: {str(e)}"}


def validate_requirement(state: dict):
    """验证需求节点"""
    logger.info("进入节点: validate_requirement")
    requirement_result = state.get("requirement_result", "")

    # 如果需求分析失败，跳过验证
    if requirement_result.startswith("需求分析失败"):
        logger.warning("需求分析失败，跳过验证")
        return {"requirement_result": requirement_result}

    try:
        # 验证需求是否完整
        messages = [ChatMessage(role="user", content=f"验证以下需求是否完整和合理：{requirement_result}")]
        response = xf_astron.chat_sync(messages=messages)

        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"需求验证完成，答案长度: {len(content)}")
        return {"requirement_result": f"{requirement_result}\n\n验证结果：{content}"}
    except Exception as e:
        logger.error(f"需求验证失败: {str(e)}")
        return {"requirement_result": f"{requirement_result}\n\n验证失败: {str(e)}"}


def build_requirement_decomposition_graph():
    """构建需求拆解子图"""
    graph = StateGraph(RequirementDecompositionState)

    # 添加节点
    graph.add_node("analyze_requirement", analyze_requirement)
    graph.add_node("validate_requirement", validate_requirement)

    # 定义边
    graph.add_edge(START, "analyze_requirement")
    graph.add_edge("analyze_requirement", "validate_requirement")
    graph.add_edge("validate_requirement", END)

    return graph


def get_compiled_requirement_decomposition():
    """获取编译后的需求拆解子图"""
    graph = build_requirement_decomposition_graph()
    return graph.compile()
