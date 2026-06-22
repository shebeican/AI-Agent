from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools.router_branch.check_intent import check_intent
from tools.router_branch.code_assistant import code_assistant
from tools.router_branch.writing_assistant import writing_assistant
from tools.router_branch.pos_assistant import pos_assistant
from tools.router_branch.general import general



# 定义工作流状态结构
class RouterBranchAgentState(TypedDict):
    # 用户输入
    user_query: str

    # 用户意图 None / code / writing / popularization_of_science
    user_intent: str

    # 结果
    result: str


def router_next(state: RouterBranchAgentState):
    """路由函数：判断用户意图走向具体的节点"""
    user_intent = state['user_intent']
    if user_intent == 'code':
        return "code"
    if user_intent == 'writing':
        return "writing"
    if user_intent == 'popularization_of_science':
        return "popularization_of_science"
    else:
        return "general"


def build_workflow():
    workflow = StateGraph(RouterBranchAgentState)

    workflow.add_node("check_intent", check_intent)
    workflow.add_node("code", code_assistant)
    workflow.add_node("writing", writing_assistant)
    workflow.add_node("popularization_of_science", pos_assistant)
    workflow.add_node("general", general)

    # 入口节点
    workflow.set_entry_point("check_intent")

    # 根据意图决定下一步
    workflow.add_conditional_edges(
        "check_intent",
        router_next,
        {
            "code": "code",
            "writing": "writing",
            "popularization_of_science": "popularization_of_science",
            "general": "general"
        }
    )

    # 结束节点
    workflow.add_edge("general", END)

    return workflow


def get_compiled_workflow():
    workflow = build_workflow()
    return workflow.compile()
