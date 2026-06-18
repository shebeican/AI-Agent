import uuid
import logging
from typing import List

from pydantic import BaseModel, Field

from workflow import basic_qa, math_calc

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


def main():
    # agent = BasicQAAgent()
    # print(agent.run(query="讲解一下中国的历史"))

    agent = MathCalcAgent()
    print(agent.run(query="10除2=多少？"))


if __name__ == '__main__':
    main()
