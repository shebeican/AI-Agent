from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from tools.subplot_nesting.requirement_decomposition import get_compiled_requirement_decomposition
from tools.subplot_nesting.budget_decomposition import get_compiled_budget_decomposition
from tools.subplot_nesting.summary import summary


# 定义工作流状态结构
class SubplotNestingAgentState(TypedDict):
    # 用户输入
    user_query: str

    # 需求拆解图结果（从子图的 requirement_result 映射而来）
    requirement_decomposition: str

    # 预算拆解图结果（从子图的 budget_result 映射而来）
    budget_decomposition: str

    # 最终结果
    result: str


def _get_requirement_subgraph():
    """获取需求拆解子图实例（懒加载）"""
    _requirement_subgraph = get_compiled_requirement_decomposition()
    return _requirement_subgraph


def _get_budget_subgraph():
    """获取预算拆解子图实例（懒加载）"""
    _budget_subgraph = get_compiled_budget_decomposition()
    return _budget_subgraph


def requirement_decomposition_node(state: dict):
    """
    需求拆解子图节点
    子图执行完毕后，将结果映射到主图状态
    """
    # 获取子图实例
    subgraph = _get_requirement_subgraph()

    # 调用子图
    result = subgraph.invoke({
        "user_query": state.get("user_query", "")
    })

    # 将子图结果映射到主图状态
    return {
        "requirement_decomposition": result.get("requirement_result", "")
    }


def budget_decomposition_node(state: dict):
    """
    预算拆解子图节点
    子图执行完毕后，将结果映射到主图状态
    """
    # 获取子图实例
    subgraph = _get_budget_subgraph()

    # 调用子图
    result = subgraph.invoke({
        "user_query": state.get("user_query", "")
    })

    # 将子图结果映射到主图状态
    return {
        "budget_decomposition": result.get("budget_result", "")
    }


def dispatch_tasks(state: dict):
    """并行分发任务"""
    return [
        Send("requirement_decomposition", state),
        Send("budget_decomposition", state),
    ]


def build_workflow():
    """
    主图 - 并行执行需求拆解子图和预算拆解子图，最后汇总
    """
    workflow = StateGraph(SubplotNestingAgentState)

    # 添加子图节点
    workflow.add_node("requirement_decomposition", requirement_decomposition_node)
    workflow.add_node("budget_decomposition", budget_decomposition_node)
    workflow.add_node("summary", summary)

    # 从 START 并行分发到两个子图节点
    workflow.add_conditional_edges(START, dispatch_tasks)

    # 两个子图节点完成后都走向 summary
    workflow.add_edge("requirement_decomposition", "summary")
    workflow.add_edge("budget_decomposition", "summary")

    # summary 结束
    workflow.add_edge("summary", END)

    return workflow


def get_compiled_workflow():
    workflow = build_workflow()
    return workflow.compile()
