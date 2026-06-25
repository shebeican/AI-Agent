from typing import TypedDict
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END, START
from tools.article_generate.summary import summary
from tools.article_generate.ai_review import ai_review
from tools.article_generate.manual_review import manual_review
from tools.article_generate.draft_generate import draft_generate

# 定义工作流状态结构
class ArticleGenerateAgentState(TypedDict):
    # 用户输入
    user_query: str

    # 初稿 / 草稿
    draft: str

    # 审核拒绝的原因
    reject_reason: str

    # AI 审核结果 True: 通过, False: 不通过
    ai_review_result: bool

    # 人工审核结果 True: 通过, False: 不通过 （AI做初审，人工做终审）
    manual_review_result: bool

    # 最大重试次数，预防死循环
    max_retries: int

    # 最终结果
    result: str


def ai_review_router_next(state: ArticleGenerateAgentState):
    """AI审核路由函数：判断是否需要重新生成草稿"""
    # max_retries = state.get('max_retries', 0)
    # if max_retries >= 3:
    #     # 超过重试次数，直接结束
    #     return END

    ai_review_result = state.get('ai_review_result', False)
    if not ai_review_result:
        return "draft_generate"
    else:
        return "manual_review"


def manual_review_router_next(state: ArticleGenerateAgentState):
    """人工审核路由函数：判断是否需要重新生成草稿"""
    manual_review_result = state.get('manual_review_result', False)
    if not manual_review_result:
        return "draft_generate"
    else:
        return "summary"


def build_workflow():
    """
    文章生成工作流：草稿生成 -> AI审核 -> 人工审核 -> 汇总
    """
    workflow = StateGraph(ArticleGenerateAgentState)

    # 添加节点
    workflow.add_node("draft_generate", draft_generate)
    workflow.add_node("ai_review", ai_review)
    workflow.add_node("manual_review", manual_review)
    workflow.add_node("summary", summary)

    # 入口点：先生成草稿
    workflow.set_entry_point("draft_generate")

    # 定义边
    workflow.add_edge("draft_generate", "ai_review")

    workflow.add_conditional_edges(
        "ai_review",
        ai_review_router_next,
        {
            "draft_generate": "draft_generate",
            "manual_review": "manual_review",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "manual_review",
        manual_review_router_next,
        {
            "draft_generate": "draft_generate",
            "summary": "summary",
        }
    )

    # summary 后结束
    workflow.add_edge("summary", END)

    return workflow


def get_compiled_workflow():
    """
    SQLite 持久化存储，数据库文件存放在 data 目录
    使用 sqlite3 连接创建 SqliteSaver
    """
    import os
    os.makedirs('./data', exist_ok=True)

    conn = sqlite3.connect('./data/article_generate.db', check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    workflow = build_workflow()
    # 在 manual_review 节点前中断，等待人工审核输入
    return workflow.compile(checkpointer=checkpointer, interrupt_before=["manual_review"])
