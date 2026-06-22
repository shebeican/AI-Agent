from typing import TypedDict

from langgraph.constants import START
from langgraph.graph import StateGraph, END
from langgraph.types import Send

from tools.parallel_task.get_example import get_example
from tools.parallel_task.get_definition import get_definition
from tools.parallel_task.get_pros_cons import get_pros_cons
from tools.parallel_task.summary import summary



# 定义工作流状态结构
class ParallelTaskAgentState(TypedDict):
    user_query: str          # 用户输入问题
    definition: str          # 任务A：定义
    pros_cons: str           # 任务B：优缺点
    demo_example: str        # 任务C：实操案例
    summary: str             # 汇总后的完整综述

# 定义并发节点，同时发送三个任务，实现并行
def dispatch_task(state: dict):
    return [
        Send("get_definition", state),
        Send("get_pros_cons", state),
        Send("get_example", state),
    ]

def build_workflow():
    workflow = StateGraph(ParallelTaskAgentState)

    workflow.add_node("get_definition", get_definition)
    workflow.add_node("get_pros_cons", get_pros_cons)
    workflow.add_node("get_example", get_example)
    workflow.add_node("summary", summary)

    # 条件路由
    workflow.add_conditional_edges(
        source=START,
        path=dispatch_task,
    )

    # 所有节点结束后，都走向总结节点
    workflow.add_edge("get_definition", "summary")
    workflow.add_edge("get_pros_cons", "summary")
    workflow.add_edge("get_example", "summary")

    return workflow


def get_compiled_workflow():
    workflow = build_workflow()
    return workflow.compile()
