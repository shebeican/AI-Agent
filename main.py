import uuid
import logging
from typing import List

from langchain_core.messages import HumanMessage

from workflow import basic_qa, math_calc, memory_chatbot, router_branch, parallel_task, subplot_nesting

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

def main():
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
    agent = SubplotNestingAgent()
    print(agent.run(query="python的装饰器如何使用"))

if __name__ == '__main__':
    main()
