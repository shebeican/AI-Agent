"""
预算拆解子图
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END, START
import logging

from clients.xf_astron_client import ChatMessage, xf_astron

logger = logging.getLogger(__name__)


# 子图状态定义
class BudgetDecompositionState(TypedDict):
    user_query: str
    budget_result: str


def estimate_budget(state: dict):
    """估算预算节点"""
    logger.info("进入节点: estimate_budget")
    user_query = state.get("user_query", "")

    try:
        messages = [ChatMessage(role="user", content=f"估算以下项目所需的金额：{user_query}")]
        response = xf_astron.chat_sync(messages=messages)

        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"预算估算完成，答案长度: {len(content)}")
        return {"budget_result": content}
    except Exception as e:
        logger.error(f"预算估算失败: {str(e)}")
        return {"budget_result": f"预算估算失败: {str(e)}"}


def optimize_budget(state: dict):
    """优化预算节点"""
    logger.info("进入节点: optimize_budget")
    budget_result = state.get("budget_result", "")

    # 如果预算估算失败，跳过优化
    if budget_result.startswith("预算估算失败"):
        logger.warning("预算估算失败，跳过优化")
        return {"budget_result": budget_result}

    try:
        # 优化预算分配
        messages = [ChatMessage(role="user", content=f"优化以下预算分配方案：{budget_result}")]
        response = xf_astron.chat_sync(messages=messages)

        content = response.get("content", [{}])[0].get("text", "")
        logger.info(f"预算优化完成，答案长度: {len(content)}")
        return {"budget_result": f"{budget_result}\n\n优化建议：{content}"}
    except Exception as e:
        logger.error(f"预算优化失败: {str(e)}")
        return {"budget_result": f"{budget_result}\n\n优化失败: {str(e)}"}


def build_budget_decomposition_graph():
    """构建预算拆解子图"""
    graph = StateGraph(BudgetDecompositionState)

    # 添加节点
    graph.add_node("estimate_budget", estimate_budget)
    graph.add_node("optimize_budget", optimize_budget)

    # 定义边
    graph.add_edge(START, "estimate_budget")
    graph.add_edge("estimate_budget", "optimize_budget")
    graph.add_edge("optimize_budget", END)

    return graph


def get_compiled_budget_decomposition():
    """获取编译后的预算拆解子图"""
    graph = build_budget_decomposition_graph()
    return graph.compile()
