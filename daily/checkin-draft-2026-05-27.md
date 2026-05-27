# Day 5-6 打卡 - Frameworks & MCP 实践

## 📚 今日学习

### 理论学习
- ✅ 完成 Handbook Frameworks 章节阅读
- ✅ 理解 Frameworks 的核心价值：工程化工具，集成常用组件
- ✅ 掌握 LangChain、LlamaIndex、AutoGPT 的核心概念和适用场景
- ✅ 完成 Handbook MCP 章节阅读
- ✅ 理解 MCP 的核心概念：Server、Client、Tools、标准化协议
- ✅ 理解 MCP 与传统 Tool Calling 的区别

### 实践项目
**Frameworks 实践**：
- ✅ 实现项目1：不使用 Frameworks 的 Agent（手动实现 Function Calling）
- ✅ 实现项目2：使用 LangGraph 的 Agent（一行代码搞定）
- ✅ 对比两种方式的代码量、易用性、可维护性
- ✅ 验证 Frameworks 的核心价值：减少样板代码，提高开发效率

**MCP 实践**：
- ✅ 使用 MCP SDK 实现只读文档服务器
- ✅ 实现 `search_docs` 工具（搜索本地项目文档）
- ✅ 实现 `get_file` 工具（读取白名单目录文件）
- ✅ 实现完整的安全机制（白名单、路径验证、错误处理、日志审计）
- ✅ 编写测试客户端验证功能
- ✅ 设计权限升级方案（写入工具的安全设计）

---

## 🎯 核心收获

### 1. Frameworks 的价值：减少样板代码

**对比实验结果**：
- **项目1（手写）**：120 行代码，10+ 个手动步骤
  - 手动创建 while 循环
  - 手动检查 `message.tool_calls`
  - 手动解析工具参数
  - 手动执行工具函数
  - 手动构造 tool result 消息
  - 手动判断是否继续循环

- **项目2（LangGraph）**：50 行代码，2 行核心代码
  ```python
  agent_executor = create_react_agent(llm, tools)
  result = agent_executor.invoke({"messages": [("user", question)]})
  ```

**核心认知**：
- Frameworks 帮你省掉了 Agent 循环的样板代码
- 代码减少 60%，但功能完全一致
- 适合快速开发，但抽象层较多，调试相对困难

### 2. 先理解原理，再用 Frameworks

**关键验证**：
- 先手写了完整的 Function Calling 流程（项目1）
- 理解了 Agent 的工作原理（调用 LLM → 解析工具调用 → 执行工具 → 返回结果 → 循环）
- 再用 LangGraph（项目2），才能理解 Framework 帮我做了什么

**如果直接用 Framework**：
- 不理解底层逻辑
- 遇到问题无法调试
- 不知道 Framework 的价值在哪里

### 3. MCP 是标准化的工具协议

**MCP 的核心价值**：
- **标准化协议**：任何 MCP Client 都能调用你的 MCP Server
- **跨应用复用**：一个 MCP Server 可以被多个 Agent 使用
- **独立进程**：MCP Server 是独立进程，通过 stdio 通信
- **安全隔离**：明确的权限边界，白名单控制

**MCP vs LangChain Tools**：
| 维度 | MCP | LangChain Tools |
|------|-----|-----------------|
| 协议标准 | 开放协议 | LangChain 专属 |
| 通信方式 | stdio（进程间通信） | 函数调用 |
| 跨语言 | 支持 | 不支持（Python only） |
| 复用性 | 高（独立进程） | 低（需要导入代码） |

### 4. 安全设计的核心原则

**MCP Server 的安全实现**：

**1. 路径白名单**：
```python
ALLOWED_DIRECTORIES = [
    BASE_DIR / "daily",
]

def is_path_allowed(path: Path) -> bool:
    resolved_path = path.resolve()  # 防止符号链接攻击
    return any(
        resolved_path.is_relative_to(allowed_dir.resolve())  # 防止路径遍历
        for allowed_dir in ALLOWED_DIRECTORIES
    )
```

**2. 明确错误处理**：
```python
if not is_path_allowed(file_path):
    allowed_paths = '\n'.join(f"  - {d}" for d in ALLOWED_DIRECTORIES)
    raise PermissionError(
        f"Access denied: Path '{path}' is not within allowed directories.\n"
        f"Allowed directories:\n{allowed_paths}"
    )
```
- 错误消息清晰，包含上下文信息
- 不会静默失败
- 不会泄露敏感信息

**3. 日志审计**：
```json
{
  "timestamp": "2026-05-27T22:53:18.341058",
  "tool": "search_docs",
  "arguments": {"query": "Day"},
  "success": true,
  "result_summary": {"type": "str", "length": 2279}
}
```
- 所有工具调用都记录到日志
- 结构化日志（JSON 格式）
- 便于审计和调试

### 5. 权限升级的设计思路

**只读 → 写入的权限升级**：

**挑战**：
- 什么时候需要用户确认？
- 如何撤销授权？
- 如何审计每次调用？

**设计方案**（已完成设计文档）：
1. **权限分级**：只读（低风险）→ 写入（中风险）→ 删除（高风险）
2. **用户确认**：写入/删除操作需要用户明确确认
3. **授权管理**：支持临时授权、永久授权、撤销授权
4. **审计日志**：记录所有写入操作，包含操作者、时间、内容

---

## 🧪 实践成果

### Frameworks 实践

**项目结构**：
```
experiments/frameworks-practice/
├── project1-no-framework/    # 手写版本（120 行）
│   └── agent.py
└── project2-langchain/        # LangGraph 版本（50 行）
    └── agent.py
```

**测试结果**：
- ✅ 两个项目功能完全一致
- ✅ 都能正确调用 `get_eth_balance` 工具
- ✅ 都能返回正确的余额结果
- ✅ LangGraph 版本代码减少 60%

### MCP 实践

**项目结构**：
```
experiments/mcp-practice/
├── src/
│   ├── server.py      # MCP Server 实现
│   ├── config.py      # 白名单配置
│   └── logger.py      # 日志系统
├── tests/
│   └── test_client.py # 测试客户端
├── logs/
│   └── mcp_server.log # 审计日志
└── PERMISSION_UPGRADE.md  # 权限升级方案
```

**测试结果**：
- ✅ 搜索文档：成功搜索到 10 个包含 "Day" 的文档
- ✅ 读取文件：成功读取白名单内的文件（8477 字符）
- ✅ 拒绝非法访问：成功拒绝访问 `/etc/passwd`
- ✅ 日志记录：所有操作都正确记录到日志文件

---

## 💭 深度思考

### 思考题 1：何时使用 Frameworks？

**适合使用**：
- 复杂的多步骤应用
- 需要快速开发
- 团队协作（统一架构）
- 需要 Memory、Tools、Chains 等组件

**不适合使用**：
- 简单的单次 API 调用
- 需要极致性能优化
- 需要完全控制底层逻辑（比如 Day 4 的 Context 分层）
- 原型验证阶段

**结论**：先理解原理，再按需引入 Frameworks。

### 思考题 2：MCP 的核心价值是什么？

**对比传统 Tool Calling**：
- 传统方式：工具函数直接写在 Agent 代码里，难以复用
- MCP 方式：工具函数放在独立的 MCP Server，可以跨 Agent 复用

**MCP 的价值**：
1. **标准化**：统一的协议，任何 Client 都能用
2. **复用性**：一个 MCP Server 可以被多个 Agent 使用
3. **安全性**：明确的权限边界，白名单控制
4. **可组合性**：多个 MCP Server 可以组合使用

### 思考题 3：如何设计安全的 Agent 工具？

**核心原则**（从 MCP 实践中学到）：
1. **最小权限**：只给必要的权限（只读 vs 写入 vs 删除）
2. **白名单控制**：明确定义允许访问的资源
3. **路径验证**：防止路径遍历攻击（`../../../etc/passwd`）
4. **明确错误**：错误消息清晰，不会静默失败
5. **日志审计**：记录所有操作，便于追溯
6. **用户确认**：高风险操作需要用户明确确认

---

## 📊 学习统计

- **学习时间**：8 小时
- **完成进度**：Day 5-6 / 42 天
- **实践产出**：
  - Frameworks 对比实验（2 个项目）
  - MCP 只读服务器（完整实现）
  - 权限升级方案设计文档
  - 完整的测试和日志
- **GitHub 提交**：6 次 commit
- **核心理解**：
  - Frameworks 减少样板代码，但要先理解原理
  - MCP 是标准化的工具协议，支持跨应用复用
  - 安全设计的核心是最小权限 + 白名单 + 审计

---

## 🔗 相关链接

- **GitHub 仓库**：https://github.com/XuetaoZhang/ai-web3-school-cohort-0
- **Frameworks 实践**：`experiments/frameworks-practice/`
- **MCP 实践**：`experiments/mcp-practice/`
- **Handbook 章节**：
  - https://aiweb3.school/zh/handbook/ai/frameworks/
  - https://aiweb3.school/zh/handbook/ai/mcp/

---

## 🚀 下一步计划

**Week 1 完成情况**：
- ✅ Day 1-2: LLM & Prompt
- ✅ Day 3-4: Context & RAG
- ✅ Day 5-6: Agent & Frameworks & MCP

**Week 2 计划**（Day 8-14）：
- Day 8-10: Vibe Coding & Evaluation
- Day 11-14: Fine-tuning & Inference（可选深入）

**Week 3 计划**（AI × Web3 Bridge）：
- 开始学习 AI × Web3 集成
- Chain-aware Context
- Web3 Tool Use
- Agent Workflow

---

#AIxWeb3School #Day5 #Day6 #Frameworks #MCP #LangChain #ModelContextProtocol #AgentDevelopment
