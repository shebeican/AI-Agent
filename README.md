# AI Agent Workflows

基于 LangGraph 构建的智能 Agent 工作流集合，演示多种常见的 Agent 设计模式。

## 特性

- 🔀 **路由分支** - 意图识别与多分支分发
- 🔄 **循环自检** - 自动校验与迭代优化
- 💾 **对话记忆** - 多轮对话上下文保持
- ⚡ **并行执行** - 多任务并发处理
- 🧮 **工具调用** - 数学计算等工具集成

## 项目结构

```
ai-agent/
├── clients/           # LLM 客户端封装
│   └── xf_astron_client.py
├── config/            # 配置管理
├── tools/             # 工具节点
│   ├── basic_qa/      # 问答工具
│   ├── math_calc/     # 数学工具
│   ├── memory_chatbot/
│   ├── router_branch/
│   └── parallel_task/
├── workflow/          # 工作流定义
│   ├── basic_qa.py
│   ├── math_calc.py
│   ├── memory_chatbot.py
│   ├── router_branch.py
│   └── parallel_task.py
├── main.py            # 入口文件
└── requirements.txt
```

## 工作流示例

### 1. 基础问答 (Basic QA)

生成答案后自动校验，不合格则重新生成。

```
用户问题 → 生成答案 → 校验答案 → [不合格则循环]
```

```python
agent = BasicQAAgent()
print(agent.run(query="讲解一下中国的历史"))
```

### 2. 数学计算 (Math Calc)

识别用户意图，路由到对应计算工具。

```
用户问题 → 意图识别 → [加/减/乘/除/通用]
```

```python
agent = MathCalcAgent()
print(agent.run(query="10除以2等于多少？"))
```

### 3. 记忆聊天机器人 (Memory Chatbot)

保持多轮对话上下文，识别用户情绪。

```python
agent = MemoryChatbotAgent()
print(agent.run(query="今天工作好烦"))
print(agent.run(query="有什么缓解办法？"))
print(agent.get_state().values["messages"])  # 查看完整上下文
```

### 4. 路由分支 (Router Branch)

根据用户意图分发到专门助手。

```
用户问题 → 意图识别 → [代码/写作/科普/通用]
```

```python
agent = RouterBranchAgent()
print(agent.run(query="Python 装饰器如何使用？"))
```

### 5. 并行任务 (Parallel Task)

多个子任务并行执行，最终汇总结果。

```
              ┌→ 获取定义 ─┐
用户问题 → 分发 ─┼→ 分析优劣 ─┼→ 汇总输出
              └→ 实操案例 ─┘
```

```python
agent = ParallelTaskAgent()
print(agent.run(query="Python 装饰器如何使用？"))
```

## 快速开始

### 环境要求

- Python 3.10+
- 讯飞星辰 API Key

### 安装

```bash
# 克隆项目
git clone https://github.com/your-repo/ai-agent.git
cd ai-agent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

创建 `.env.dev` 文件：

```env
XF_API_KEY=your_api_key_here
```

### 运行

```bash
python main.py
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 工作流框架 | LangGraph |
| LLM API | 讯飞星辰 |
| 配置管理 | Pydantic Settings |
| 类型系统 | Python TypedDict |

## License

MIT
