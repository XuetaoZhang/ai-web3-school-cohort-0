# AI Agent 快速开始指南

## 📚 什么是 AI Agent？

**AI Agent** 是能够感知环境、做出决策并采取行动的智能系统。与普通的 LLM 对话不同，Agent 可以：

1. **调用工具**：计算器、搜索引擎、数据库查询等
2. **执行任务**：自动完成多步骤的复杂任务
3. **与环境交互**：读取文件、发送请求、控制设备等

### Agent 的工作流程

```
用户提问
    ↓
Agent 思考（需要什么工具？）
    ↓
调用工具（如计算器）
    ↓
获取工具结果
    ↓
Agent 整合结果
    ↓
返回最终答案
```

### Tool Use (Function Calling) 的核心概念

**Tool Use** 是让 LLM 能够调用外部工具的技术：

1. **工具定义**：告诉 LLM 有哪些工具可用，每个工具的功能和参数
2. **工具选择**：LLM 根据用户问题，决定调用哪个工具
3. **工具执行**：实际执行工具函数，获取结果
4. **结果整合**：LLM 将工具结果整合到回答中

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd ~/ai-web3-school-cohort-0/experiments/ai-agent-deepseek

# 激活虚拟环境（如果还没有）
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install openai
```

### 2. 设置 API Key

```bash
export DEEPSEEK_API_KEY='your-api-key-here'
```

### 3. 运行简单版本

```bash
python agent_simple.py
```

**这个版本会测试 5 个案例**：
- ✅ 计算数学表达式
- ✅ 查询当前时间
- ✅ 查询天气
- ✅ 搜索知识库
- ✅ 普通对话（不需要工具）

### 4. 运行多轮对话版本

```bash
python agent_multi.py
```

**这个版本会测试复杂场景**：
- ✅ 多步计算（先算 A，再用结果算 B）
- ✅ 多个查询（同时查询时间和天气）
- ✅ 混合任务（搜索 + 计算）

---

## 📂 文件说明

### `tools.py` - 工具定义

定义了 4 个工具：

1. **calculator** - 计算器
   ```python
   calculator("2 + 3 * 4")  # 返回 14
   calculator("sqrt(16)")   # 返回 4.0
   ```

2. **get_current_time** - 获取当前时间
   ```python
   get_current_time()  # 返回当前时间信息
   ```

3. **get_weather** - 查询天气（模拟数据）
   ```python
   get_weather("北京")  # 返回北京天气
   ```

4. **search_knowledge** - 搜索知识库
   ```python
   search_knowledge("什么是 RAG")  # 搜索 RAG 相关知识
   ```

### `agent_simple.py` - 简单版本

**特点**：
- 单次对话
- 演示基本的 Tool Use 流程
- 适合理解 Agent 的工作原理

**核心代码**：
```python
# 1. 发送用户消息
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=TOOL_DEFINITIONS,  # 告诉 LLM 有哪些工具
    tool_choice="auto"       # 让 LLM 自动决定是否调用工具
)

# 2. 检查是否需要调用工具
if assistant_message.tool_calls:
    # 3. 执行工具
    tool_result = execute_tool(tool_name, tool_args)
    
    # 4. 将工具结果发送给 LLM
    final_response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages + [tool_result]
    )
```

### `agent_multi.py` - 多轮对话版本

**特点**：
- 支持多轮对话
- 可以连续调用多个工具
- 保留对话历史
- 适合复杂任务

**核心代码**：
```python
class Agent:
    def chat(self, user_message):
        # 循环处理，直到不再调用工具
        while True:
            response = self.client.chat.completions.create(...)
            
            if assistant_message.tool_calls:
                # 执行工具，继续循环
                execute_tools()
                continue
            else:
                # 返回最终答案
                return assistant_message.content
```

---

## 🎯 学习目标

通过这个实践，你将理解：

### 1. Tool Use 的工作原理

```
用户: "计算 2 + 3"
    ↓
LLM 思考: "这需要计算器工具"
    ↓
LLM 输出: {
    "tool_calls": [{
        "function": {
            "name": "calculator",
            "arguments": {"expression": "2 + 3"}
        }
    }]
}
    ↓
执行工具: calculator("2 + 3") → "5"
    ↓
LLM 整合: "计算结果是 5"
```

### 2. Agent 的决策过程

Agent 如何决定是否调用工具？

- **需要工具**：计算、查询、搜索等
- **不需要工具**：普通对话、解释概念等

### 3. 多步推理

复杂任务需要多次调用工具：

```
用户: "先计算 100 * 50，然后用结果除以 25"
    ↓
第 1 步: calculator("100 * 50") → 5000
    ↓
第 2 步: calculator("5000 / 25") → 200
    ↓
最终答案: "结果是 200"
```

---

## 🔍 观察重点

### 1. 工具定义的重要性

工具定义需要清晰描述：
- **功能**：这个工具做什么？
- **参数**：需要什么输入？
- **返回值**：返回什么格式的数据？

**好的工具定义**：
```json
{
    "name": "calculator",
    "description": "计算数学表达式，支持基本运算（+、-、*、/）和常用函数（sqrt、sin、cos等）",
    "parameters": {
        "expression": {
            "type": "string",
            "description": "要计算的数学表达式，例如：'2 + 3 * 4' 或 'sqrt(16)'"
        }
    }
}
```

### 2. Agent 的决策能力

观察 Agent 如何决定：
- 什么时候调用工具？
- 调用哪个工具？
- 传递什么参数？

### 3. 错误处理

观察 Agent 如何处理：
- 工具执行失败
- 参数错误
- 未知工具

---

## 💡 实验建议

### 实验 1：测试不同的问题

尝试问 Agent：
- "计算 (123 + 456) * 789"
- "现在几点？"
- "北京天气怎么样？"
- "什么是 LLM？"
- "你好"（不需要工具）

**观察**：Agent 如何决定是否调用工具？

### 实验 2：测试复杂任务

尝试需要多步推理的问题：
- "先查询时间，然后计算当前小时数乘以 60"
- "搜索 RAG 的定义，然后告诉我它有几个字"

**观察**：Agent 如何分解任务？

### 实验 3：添加新工具

尝试添加一个新工具，例如：
- `translate(text, target_lang)` - 翻译文本
- `generate_random(min, max)` - 生成随机数
- `search_web(query)` - 搜索网页

**步骤**：
1. 在 `tools.py` 中定义工具函数
2. 在 `TOOL_DEFINITIONS` 中添加工具定义
3. 在 `TOOLS` 字典中注册工具
4. 测试新工具

### 实验 4：观察 Agent 的局限性

尝试让 Agent 失败：
- 提供错误的参数
- 请求不存在的工具
- 提出模糊的问题

**观察**：Agent 如何处理错误？

---

## 🎓 核心概念总结

### 1. Agent = LLM + Tools + Loop

```python
while not done:
    # 1. LLM 思考
    response = llm.chat(messages)
    
    # 2. 检查是否需要工具
    if response.tool_calls:
        # 3. 执行工具
        result = execute_tool(...)
        
        # 4. 将结果添加到对话
        messages.append(result)
    else:
        # 5. 返回最终答案
        return response.content
```

### 2. Tool Use 的三个关键步骤

1. **定义工具**：告诉 LLM 有什么工具
2. **LLM 决策**：LLM 决定调用哪个工具
3. **执行工具**：实际执行工具函数

### 3. Agent 的能力边界

**Agent 能做什么**：
- ✅ 调用工具获取信息
- ✅ 执行计算和查询
- ✅ 多步推理和规划

**Agent 不能做什么**：
- ❌ 调用未定义的工具
- ❌ 理解工具的内部实现
- ❌ 保证工具执行成功

---

## 🚀 下一步

完成这个实践后，你可以：

1. **扩展工具集**：添加更多工具（文件操作、API 调用等）
2. **优化 Agent**：添加记忆、规划、反思能力
3. **连接 RAG**：让 Agent 能够搜索你的知识库
4. **Web3 集成**：让 Agent 能够查询区块链、调用智能合约

---

## 📝 实验记录模板

完成实践后，记录你的发现：

### 1. 运行结果

- 哪些案例成功了？
- 哪些案例失败了？
- Agent 的决策是否合理？

### 2. 关键发现

- Tool Use 的工作流程是什么？
- Agent 如何决定调用工具？
- 多步推理是如何实现的？

### 3. 遇到的问题

- 遇到了什么错误？
- 如何解决的？
- 有什么改进建议？

### 4. 思考

- Agent 和普通 LLM 对话的区别？
- Tool Use 的局限性是什么？
- 如何设计更好的工具？

---

## 🔗 相关资源

- [OpenAI Function Calling 文档](https://platform.openai.com/docs/guides/function-calling)
- [DeepSeek API 文档](https://platform.deepseek.com/docs)
- [LangChain Agent 教程](https://python.langchain.com/docs/modules/agents/)

---

**祝你实验顺利！🎉**
