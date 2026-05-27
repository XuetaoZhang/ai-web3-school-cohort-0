# Frameworks Practice - Agent 对比实验

## 📋 项目简介

这是一个对比实验项目，展示使用和不使用 Frameworks 创建 Agent 的区别。

**实验目标**：查询以太坊地址余额
- **输入**：`0x1234567890abcdef1234567890abcdef12345678`
- **输出**：该地址的 ETH 余额
- **工具**：`get_eth_balance` - 调用 Sepolia 测试网 RPC 接口

## 🎯 两个项目对比

### 项目1：不使用 Frameworks（手动实现）
**位置**：`project1-no-framework/`

使用 DeepSeek API（OpenAI 兼容接口）的 Function Calling，**手动实现完整流程**：

```python
# 需要手动编写的代码：
1. ✋ 手动定义工具 schema（OpenAI 格式）
2. ✋ 手动创建 while 循环
3. ✋ 手动调用 LLM API
4. ✋ 手动检查 response.tool_calls
5. ✋ 手动解析工具参数
6. ✋ 手动执行工具函数
7. ✋ 手动构造 tool result 消息
8. ✋ 手动添加到消息列表
9. ✋ 手动判断是否继续循环
10. ✋ 手动解析最终答案

# 代码量：约 120 行
```

**优点**：
- 完全控制每个步骤
- 理解 Agent 工作原理
- 可以精细调试
- 无框架依赖

**缺点**：
- 代码量大（120+ 行）
- 需要处理各种边界情况
- 容易出错
- 维护成本高

### 项目2：使用 LangGraph Framework
**位置**：`project2-langchain/`

使用 **LangGraph** 的 `create_react_agent`，**一行代码搞定**：

```python
# Framework 自动处理的事情：
1. ✅ 自动调用 LLM
2. ✅ 自动解析工具调用
3. ✅ 自动执行工具
4. ✅ 自动把结果给 LLM
5. ✅ 自动生成最终答案
6. ✅ 自动处理循环逻辑
7. ✅ 自动错误处理
8. ✅ 自动状态管理

# 核心代码：仅 1 行！
agent_executor = create_react_agent(llm, tools)
result = agent_executor.invoke({"messages": [("user", question)]})

# 代码量：约 50 行（减少 60%）
```

**优点**：
- 代码极简（50 行 vs 120 行）
- 开箱即用
- 内置错误处理
- 社区支持
- 易于维护

**缺点**：
- 抽象层较多
- 调试相对困难
- 需要学习框架 API
- 增加依赖

## 📁 项目结构

```
frameworks-practice/
├── README.md                           # 本文件
├── project1-no-framework/              # 项目1：不使用框架
│   ├── agent.py                        # Agent 主程序
│   └── requirements.txt                # 依赖列表
└── project2-langchain/                 # 项目2：使用 LangChain
    ├── agent.py                        # Agent 主程序
    └── requirements.txt                # 依赖列表
```

## 🚀 快速开始

### 项目1：不使用 Frameworks

```bash
# 进入项目目录
cd experiments/frameworks-practice/project1-no-framework

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export DEEPSEEK_API_KEY='your-deepseek-api-key-here'

# 运行 Agent
python agent.py
```

### 项目2：使用 LangChain

```bash
# 进入项目目录
cd experiments/frameworks-practice/project2-langchain

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 设置 API Key
export DEEPSEEK_API_KEY='your-deepseek-api-key-here'

# 运行 Agent
python agent.py
```

## 🔧 工具说明

### get_eth_balance

**功能**：查询以太坊地址余额

**参数**：
- `eth_address` (string): 以太坊地址

**返回**：
- 地址的 ETH 余额（字符串格式）

**实现**：
- 网络：Sepolia 测试网
- RPC URL：`https://sepolia.infura.io/v3/a741720a2c33491da85d6f877f3cc1ba`
- 方法：`eth_getBalance`

## 📊 执行流程对比

### 项目1（手动实现）

```
用户输入
    ↓
手动创建消息列表
    ↓
手动 while 循环开始
    ↓
手动调用 client.chat.completions.create()
    ↓
手动检查 message.tool_calls
    ↓
手动解析 tool_call.function.name
    ↓
手动解析 tool_call.function.arguments
    ↓
手动执行 process_tool_call()
    ↓
手动构造 tool result 消息
    ↓
手动 append 到消息列表
    ↓
手动 continue 循环
    ↓
手动检查是否结束
    ↓
手动解析 message.content
    ↓
输出结果
```

**代码示例**：
```python
# 需要写 120+ 行代码
while True:
    response = client.chat.completions.create(...)
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        tool_name = tool_call.function.name
        tool_input = json.loads(tool_call.function.arguments)
        tool_result = process_tool_call(tool_name, tool_input)
        messages.append({"role": "assistant", ...})
        messages.append({"role": "tool", ...})
        continue
    else:
        break
```

### 项目2（LangGraph）

```
用户输入
    ↓
agent_executor.invoke()
    ↓
[LangGraph 自动处理所有步骤]
    ↓
输出结果
```

**代码示例**：
```python
# 只需要 2 行核心代码！
agent_executor = create_react_agent(llm, tools)
result = agent_executor.invoke({"messages": [("user", question)]})
```

**对比**：
- 项目1：120 行代码，10+ 个手动步骤
- 项目2：2 行代码，0 个手动步骤
- **代码减少 98%！**

## 💡 学习要点

1. **理解 Agent 工作原理**
   - 项目1 展示了 Agent 的完整工作流程
   - 每个步骤都是显式的

2. **Framework 的价值**
   - 项目2 展示了框架如何简化开发
   - 减少样板代码，提高开发效率

3. **权衡取舍**
   - 手动实现：控制力强，但代码多
   - 使用框架：开发快，但抽象层多

## 🎓 扩展练习

1. **添加更多工具**
   - 查询交易记录
   - 查询 Gas 价格
   - 查询区块信息

2. **错误处理**
   - 无效地址处理
   - 网络错误重试
   - 超时处理

3. **性能优化**
   - 缓存查询结果
   - 批量查询
   - 异步调用

4. **尝试其他框架**
   - LlamaIndex
   - Haystack
   - AutoGPT

## 📚 相关资源

- [DeepSeek API 文档](https://platform.deepseek.com/api-docs/)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [LangChain 文档](https://python.langchain.com/)
- [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [Sepolia 测试网](https://sepolia.etherscan.io/)

## 🤔 思考题

1. 什么场景下应该手动实现 Agent？
2. 什么场景下应该使用 Framework？
3. 如何在两者之间找到平衡？
4. Framework 的抽象是否总是有益的？
