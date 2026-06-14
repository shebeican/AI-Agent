"""
接收状态，调用 LLM，写入 raw_answer，默认 need_revise=False
"""
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GenerateAnswerInput(BaseModel):
    need_revise: bool = Field(default=False, description="LLM 初次生成答案是否达标")

@tool(args_schema=CheckAnswerInput)
def generate_answer_tool(need_revise: bool):
    pass