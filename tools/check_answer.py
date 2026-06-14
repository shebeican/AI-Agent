"""
校验raw_answer长度/空洞度，不达标则置need_revise=True
"""
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CheckAnswerInput(BaseModel):
    raw_answer: str = Field(description="LLM 初次生成答案")

@tool(args_schema=CheckAnswerInput)
def check_answer_tool(raw_answer: str):
    pass