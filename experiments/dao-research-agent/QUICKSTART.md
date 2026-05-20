# DAO Research Agent - 快速开始

## 📦 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install openai
```

## 🔑 配置 API Key

### 方法 1: 环境变量（推荐）

```bash
export DEEPSEEK_API_KEY='your-deepseek-api-key'
```

### 方法 2: 直接在代码中设置

编辑 `agent.py`，修改：

```python
client = OpenAI(
    api_key="your-deepseek-api-key",  # 直接设置
    base_url="https://api.deepseek.com"
)
```

## 🚀 运行 Agent

### 交互式模式

```bash
python agent.py
```

然后输入：

```
分析提案 #123
```

### 测试模式

```bash
# 测试所有功能
python test_agent.py

# 仅测试工具函数（不需要 API Key）
python tools.py
```

## 📝 使用示例

### 示例 1: 分析资金申请提案

```
👤 你: 分析提案 #123

🤖 Agent 执行流程：
  1. 读取提案内容
  2. 搜索论坛讨论
  3. 分析支持/反对理由
  4. 检查风险
  5. 生成检查清单
  6. 输出完整报告

📊 输出报告包含：
  - 提案概述
  - 信息来源
  - 支持理由（附来源）
  - 反对理由（附来源）
  - 证据不足的结论
  - 风险评估
  - 投票前检查清单
  - 综合建议
```

### 示例 2: 分析治理修改提案

```
👤 你: 研究提案 124

🤖 Agent 会自动识别这是治理类提案，重点关注：
  - 治理风险
  - 对 DAO 的影响
  - 是否需要回滚机制
```

## 🎯 可用的提案

当前系统包含 2 个示例提案：

- **提案 #123**: 为 DeFi 教育项目拨款 50,000 USDC（资金申请）
- **提案 #124**: 修改治理参数 - 降低提案门槛（治理修改）

## 🔧 自定义提案

编辑 `tools.py` 中的 `PROPOSALS_DB` 和 `FORUM_DISCUSSIONS` 添加新提案：

```python
PROPOSALS_DB = {
    "125": {
        "id": "125",
        "title": "你的提案标题",
        "description": "提案描述...",
        # ... 其他字段
    }
}

FORUM_DISCUSSIONS = {
    "125": [
        {
            "author": "用户名",
            "content": "讨论内容",
            "sentiment": "positive",  # positive/negative/neutral
            "votes": 10
        }
    ]
}
```

## 📚 工作流程

### Agent 的执行步骤

```
用户输入
    ↓
第 1 轮: LLM 决定调用 read_proposal
    ↓
第 2 轮: LLM 处理提案内容，决定调用 search_forum
    ↓
第 3 轮: LLM 处理讨论内容，决定调用 analyze_sentiment
    ↓
第 4 轮: LLM 处理情感分析，决定调用 check_risks
    ↓
第 5 轮: LLM 处理风险评估，决定调用 generate_checklist
    ↓
第 6 轮: LLM 综合所有信息，生成最终报告
    ↓
输出完整分析报告
```

### 关键特性

✅ **Agentic Loop** - 循环执行直到完成任务
✅ **自主决策** - LLM 自己决定调用哪些工具
✅ **多步骤任务** - 可以处理复杂的分析流程
✅ **透明性** - 明确标注信息来源和证据
✅ **安全性** - 只读操作，不直接投票

## 🐛 故障排除

### 问题 1: API Key 错误

```
❌ 错误: Incorrect API key provided
```

**解决方案**: 检查 API Key 是否正确设置

```bash
echo $DEEPSEEK_API_KEY  # 查看环境变量
```

### 问题 2: 达到最大迭代次数

```
⚠️ 达到最大迭代次数（10），任务可能未完成
```

**解决方案**: 增加 `max_iterations` 参数

```python
result = run_agent(user_input, max_iterations=20)
```

### 问题 3: 工具调用失败

```
❌ 错误: 未知的工具: xxx
```

**解决方案**: 检查 `tools.py` 中的工具函数是否正确定义

## 📖 进阶使用

### 1. 集成真实的 DAO 数据

替换 `tools.py` 中的模拟数据，连接真实的 DAO 平台：

```python
def read_proposal(proposal_id: str) -> Dict[str, Any]:
    # 调用 Snapshot API
    response = requests.get(f"https://hub.snapshot.org/api/proposals/{proposal_id}")
    return response.json()
```

### 2. 添加新工具

在 `tools.py` 中添加新工具函数：

```python
def check_on_chain_data(proposal_id: str) -> Dict[str, Any]:
    """查询链上投票数据"""
    # 使用 web3.py 查询合约
    pass

# 在 TOOLS_DEFINITION 中注册
TOOLS_DEFINITION.append({
    "type": "function",
    "function": {
        "name": "check_on_chain_data",
        "description": "查询链上投票数据",
        # ...
    }
})
```

### 3. 权限升级版本

实现投票功能（需要用户授权）：

```python
def simulate_vote(proposal_id: str, vote: str) -> Dict[str, Any]:
    """模拟投票交易"""
    pass

def generate_vote_tx(proposal_id: str, vote: str) -> Dict[str, Any]:
    """生成投票交易草稿"""
    pass
```

## 🎓 学习资源

- [AI × Web3 School Handbook - Agent 章节](https://aiweb3.school/zh/handbook/ai/agent/)
- [ARCHITECTURE.md](./ARCHITECTURE.md) - 详细架构文档
- [DeepSeek API 文档](https://platform.deepseek.com/docs)

## 💡 提示

1. **首次运行**: 建议先运行 `python tools.py` 测试工具函数
2. **调试模式**: 设置 `verbose=True` 查看详细执行过程
3. **成本控制**: DeepSeek API 价格低廉，但仍建议设置 `max_iterations` 限制
4. **数据隐私**: 不要在提案数据中包含敏感信息

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
