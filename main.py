from workflow import basic_qa

class BasicQAAgent:
    """基础问答代理"""

    def __inti__(self, max_retries: int = 3):
        """
        初始化代理
        :param max_retries 最大重试次数:
        """
        self.max_retries = max_retries
        self.workflow = basic_qa.get_compiled_workflow()

    def run(self):
        