import uuid
import logging
from typing import List

from langchain_core.messages import HumanMessage

from workflow import basic_qa, math_calc, memory_chatbot, router_branch, parallel_task, subplot_nesting, article_generate

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BasicQAAgent:
    """基础问答代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = basic_qa.get_compiled_workflow()

    def run(self, query: str):
        """
        执行用户问答
        """
        workflow_id = str(uuid.uuid4())[:8]
        init_state = {
            'user_query': query,
            'raw_answer': '',
            'need_revise': False
        }
        config = {'configurable': {'thread_id': workflow_id}}
        result = self.workflow.invoke(init_state, config)

        return result.get('raw_answer', '执行失败')


class MathCalcAgent:
    """数学计算代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = math_calc.get_compiled_workflow()

    def run(self, query: str):
        """
        执行用户问答
        """
        workflow_id = str(uuid.uuid4())[:8]
        init_state = {
            'user_query': query,
            'math_tool_type': None,
            'result': None,
            'a': 0,
            'b': 0
        }
        config = {'configurable': {'thread_id': workflow_id}}
        result = self.workflow.invoke(init_state, config)

        return result.get('result', '执行失败')


class MemoryChatbotAgent:
    """内存持久对话代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = memory_chatbot.get_compiled_workflow()
        self.workflow_id = str(uuid.uuid4())[:8]
        self.config = {'configurable': {'thread_id': self.workflow_id}}

    def run(self, query: str):
        """
        执行用户问答
        """
        init_state = {
            'messages': [HumanMessage(query)],
            'user_emotion': None,
        }
        result = self.workflow.invoke(init_state, self.config)

        return result.get('messages', '执行失败')[-1].content

    def get_state(self):
        return self.workflow.get_state(self.config)


class RouterBranchAgent:
    """路由分支代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = router_branch.get_compiled_workflow()

    def run(self, query: str):
        """
        执行用户问答
        """
        init_state = {
            'check_intent': None,
            'user_query': query,
            'result': None,
        }
        result = self.workflow.invoke(init_state)

        return result.get('result', '执行失败')


class ParallelTaskAgent:
    """并行任务代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = parallel_task.get_compiled_workflow()

    def run(self, query: str):
        """
        执行用户问答
        """
        init_state = {
            'user_query': query,
            'definition': None,
            'pros_cons': None,
            'demo_example': None,
            'summary': None,
        }
        result = self.workflow.invoke(init_state)

        return result.get('summary', '执行失败')

class SubplotNestingAgent:
    """子图嵌套代理"""

    def __init__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = subplot_nesting.get_compiled_workflow()

    def run(self, query: str):
        """
        执行用户问答
        """
        init_state = {
            'user_query': query,
            'budget_decomposition': '',
            'requirement_decomposition': '',
            'result': '',
        }
        result = self.workflow.invoke(init_state)

        return result.get('result', '执行失败')


class ArticleGenerateAgent:
    """文案生成器代理"""

    def __init__(self, max_retries: int = 3, thread_id: str = None):
        """
        初始化代理
        :param max_retries: 最大重试次数
        :param thread_id: 工作流ID，用于持久化和恢复。如果不指定，则生成新的ID
        """
        self.max_retries = max_retries
        self.workflow = article_generate.get_compiled_workflow()
        # 支持自定义 thread_id，便于恢复之前的工作流
        self.workflow_id = thread_id if thread_id else str(uuid.uuid4())[:8]
        self.config = {'configurable': {'thread_id': self.workflow_id}}

    def run(self, query: str):
        """
        执行文案生成，循环等待人工审核直到通过
        """
        # 检查是否有历史状态
        snapshot = self.workflow.get_state(self.config)
        if snapshot.values and snapshot.values.get("draft"):
            print(f"=== 恢复历史工作流 (thread_id: {self.workflow_id}) ===")
            draft = snapshot.values.get("draft", "")
            print(f"\n===== 待人工审核文稿 =====\n{draft}")
        else:
            # 首次生成稿件
            print(f"=== 生成文章并自动审核 (thread_id: {self.workflow_id}) ===")
            init_state = {
                'user_query': query,
                'draft': None,
                'reject_reason': None,
                'ai_review_result': None,
                'manual_review_result': None,
                'max_retries': 0,
                'result': None
            }
            self.workflow.invoke(init_state, self.config)

        # 循环等待人工审核，直到通过或超过最大重试次数
        while True:
            # 读取当前状态
            snapshot = self.workflow.get_state(self.config)
            max_retries = snapshot.values.get("max_retries", 0)

            # 检查是否已有最终结果
            if snapshot.values.get("result"):
                print("\n✅ 审核通过，最终发布稿：")
                print(snapshot.values["result"])
                break

            # 显示待审核文稿
            draft = snapshot.values.get("draft", "")
            print(f"\n===== 待人工审核文稿 (第 {max_retries} 次生成) =====\n{draft}")
            print(f"\n提示：下次启动可使用 thread_id={self.workflow_id} 恢复此工作流")
            print("请人工操作：输入 pass 直接发布 / reject 驳回重写")

            op = input("操作：").strip()
            sug = ""
            if op == "reject":
                sug = input("请输入修改建议：")

            # 更新人工审核结果
            self.workflow.update_state(
                self.config,
                values={
                    "manual_review_result": op,
                    "reject_reason": sug
                }
            )

            # 执行工作流（会继续到下一个中断点或结束）
            print("\n=== 执行审核结果 ===")
            self.workflow.invoke(None, self.config)


def main():

    # ================================================================================================
    #                                              练手
    # ================================================================================================

    # ================================================
    #                 基础对话Agent
    # ================================================
    # agent = BasicQAAgent()
    # print(agent.run(query="讲解一下中国的历史"))


    # ================================================
    #                 数学计算Agent
    # ================================================
    # agent = MathCalcAgent()
    # print(agent.run(query="10除2=多少？"))


    # ================================================
    #                 内存保留对话框Agent
    # ================================================
    # agent = MemoryChatbotAgent(max_retries=3)
    # print(agent.run(query="今天工作好烦，事事不顺心"))
    # print(agent.run(query="有什么缓解压力的办法吗？"))
    # print("完整对话上下文：", agent.get_state().values["messages"])

    # ================================================
    #                 路由分支Agent
    # ================================================
    # agent = RouterBranchAgent()
    # print(agent.run(query="python的装饰器如何使用"))


    # ================================================
    #                 并行任务Agent
    # ================================================
    # agent = ParallelTaskAgent()
    # print(agent.run(query="python的装饰器如何使用"))

    # ================================================
    #                 子图嵌套Agent
    # ================================================
    # agent = SubplotNestingAgent()
    # print(agent.run(query="python的装饰器如何使用"))


    # ================================================================================================
    #                                              实战
    # ================================================================================================

    # ================================================
    #                 人工审核干预的内容发布流程
    #  完整流程：
    #  1. AI 生成文章初稿
    #  2. 审核节点自动检测违规 / 敏感内容
    #  3. 不合格：退回重写
    #  4. 合格：触发人工等待节点（模拟人工确认输入：通过 / 驳回修改）
    #  5. 人工通过 → 最终格式化发布文本；驳回则带回修改意见重写
    #  6. 要点：中断 graph、恢复执行、状态可暂停
    #
    #  使用方法：
    #  - 首次运行：ArticleGenerateAgent() 会生成新的 thread_id
    #  - 恢复工作流：ArticleGenerateAgent(thread_id="xxx") 使用之前的 thread_id
    # ================================================
    # agent = ArticleGenerateAgent()  # 新建工作流
    agent = ArticleGenerateAgent(thread_id="3333")  # 恢复之前的工作流
    print(agent.run(query="python的装饰器如何使用"))

if __name__ == '__main__':
    main()
