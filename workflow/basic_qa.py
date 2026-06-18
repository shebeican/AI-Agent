from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools.basic_qa.check_answer import check_answer_tool
from tools.basic_qa.generate_answer import generate_answer_tool


# 定义工作流状态结构
class BasicQAAgentState(TypedDict):
    # 用户输入
    user_query: str

    # LLM初次生成的答案
    raw_answer: str

    # 纠错标记（True要重新生成，False否）
    need_revise: bool


def router_next(state: BasicQAAgentState):
    """路由函数：判断是否需要重新生成答案"""
    need_revise = state['need_revise']
    if need_revise:
        return "generate_answer"
    else:
        return END


def build_workflow():
    workflow = StateGraph(BasicQAAgentState)

    workflow.add_node("generate_answer", generate_answer_tool)
    workflow.add_node("check_answer", check_answer_tool)

    # 入口点：先生成答案
    workflow.set_entry_point("generate_answer")

    # 生成答案 -> 校验答案
    workflow.add_edge("generate_answer", "check_answer")

    # 校验答案 -> 根据结果决定下一步
    workflow.add_conditional_edges(
        "check_answer",
        router_next,
        {
            "generate_answer": "generate_answer",
            END: END
        }
    )

    return workflow


def get_compiled_workflow():
    workflow = build_workflow()
    return workflow.compile()
