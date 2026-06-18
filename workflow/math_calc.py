from typing import TypedDict
from langgraph.graph import StateGraph, END

from tools.math_calc.check_intent import check_intent
from tools.math_calc.add import add
from tools.math_calc.divide import divide
from tools.math_calc.multiply import multiply
from tools.math_calc.subtract import subtract
from tools.math_calc.general import general



# 定义工作流状态结构
class MathCalcAgentState(TypedDict):
    # 用户输入
    user_query: str

    # 数学工具类型 None / add / divide / multiply / subtract
    math_tool_type: str

    # 结果
    result: str

    a: float
    b: float



def router_next(state: MathCalcAgentState):
    """路由函数：判断是否需要重新生成答案"""
    math_tool_type = state['math_tool_type']
    if math_tool_type == 'add':
        return "add"
    if math_tool_type == 'divide':
        return "divide"
    if math_tool_type == 'multiply':
        return "multiply"
    if math_tool_type == 'subtract':
        return "subtract"
    else:
        return "general"


def build_workflow():
    workflow = StateGraph(MathCalcAgentState)

    workflow.add_node("check_intent", check_intent)
    workflow.add_node("add", add)
    workflow.add_node("divide", divide)
    workflow.add_node("multiply", multiply)
    workflow.add_node("subtract", subtract)
    workflow.add_node("general", general)

    # 入口节点
    workflow.set_entry_point("check_intent")

    # 根据意图决定下一步
    workflow.add_conditional_edges(
        "check_intent",
        router_next,
        {
            "add": "add",
            "divide": "divide",
            "multiply": "multiply",
            "subtract": "subtract",
            "general": "general"
        }
    )

    # 结束节点
    workflow.add_edge("general", END)

    return workflow


def get_compiled_workflow():
    workflow = build_workflow()
    return workflow.compile()
