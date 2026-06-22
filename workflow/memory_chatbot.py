from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END, add_messages, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from tools.memory_chatbot.check_user_emotion import check_user_emotion
from tools.memory_chatbot.generate_response import generate_response

# 定义工作流状态结构
class MemoryChatbotAgentState(TypedDict):
    # 自动累加对话上下文
    messages: Annotated[list, add_messages]

    # 用户情绪
    user_emotion: str  # negative / normal / positive


def build_workflow():
    workflow = StateGraph(MemoryChatbotAgentState)

    workflow.add_node("check_user_emotion", check_user_emotion)
    workflow.add_node("generate_response", generate_response)

    # 入口节点
    workflow.set_entry_point("check_user_emotion")

    # 节点流转 start -> 检测用户情绪 -> 根据情绪回复用户 -> END
    workflow.add_edge(START, "check_user_emotion")
    workflow.add_edge("check_user_emotion", "generate_response")
    workflow.add_edge("generate_response", END)

    return workflow


def get_compiled_workflow():
    memory = MemorySaver()  # 内存存储器
    workflow = build_workflow()
    return workflow.compile(checkpointer=memory)



# ===============================================
#          对话持久化，sqlite，线上可以用mysql
# ===============================================

# def build_workflow():
#     workflow = StateGraph(MemoryChatbotAgentState)
#
#     workflow.add_node("check_user_emotion", check_user_emotion)
#     workflow.add_node("generate_response", generate_response)
#
#     # 入口节点
#     workflow.set_entry_point("check_user_emotion")
#
#     # 节点流转 start -> 检测用户情绪 -> 根据情绪回复用户 -> END
#     workflow.add_edge(START, "check_user_emotion")
#     workflow.add_edge("check_user_emotion", "generate_response")
#     workflow.add_edge("generate_response", END)
#
#     return workflow
#
#
# def get_compiled_workflow():
#     conn = SqliteSaver.from_conn_string('./chat_memory.db')  # sqlite持久化存储器
#     workflow = build_workflow()
#     return workflow.compile(checkpointer=conn)
