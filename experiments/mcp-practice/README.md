# MCP Readonly Server

一个只读的 MCP (Model Context Protocol) 服务器，提供安全的文档搜索和文件读取功能。

## 功能特性

### 核心工具

1. **search_docs(query)** - 搜索文档
   - 在白名单目录中搜索包含指定查询的文档
   - 返回匹配的文件路径和上下文预览
   - 显示匹配次数和行号

2. **get_file(path)** - 读取文件
   - 读取白名单目录中的文件内容
   - 返回完整内容和元数据（大小、行数）
   - 包含源路径信息

### 安全特性

- ✅ **路径白名单**: 只能访问预定义的安全目录
- ✅ **路径验证**: 防止路径遍历攻击（如 `../../../etc/passwd`）
- ✅ **明确错误**: 所有错误都有清晰的错误消息，不会静默失败
- ✅ **日志记录**: 所有工具调用都会记录到日志文件
- ✅ **源路径追踪**: 所有返回结果都包含源文件路径

## 项目结构

```
mcp-practice/
├── src/
│   ├── __init__.py
│   ├── config.py      # 配置和白名单管理
│   ├── logger.py      # 日志记录工具
│   └── server.py      # MCP 服务器实现
├── tests/
│   └── test_client.py # 测试客户端
├── logs/
│   └── mcp_server.log # 服务器日志
├── pyproject.toml     # 项目配置
└── README.md
```

## 安装

```bash
cd experiments/mcp-practice
pip install -e .
```

## 使用

### 启动服务器

```bash
python -m src.server
```

### 运行测试客户端

```bash
cd experiments/mcp-practice
python tests/test_client.py
```

### 配置白名单

编辑 `src/config.py` 中的 `ALLOWED_DIRECTORIES` 列表：

```python
ALLOWED_DIRECTORIES: List[Path] = [
    BASE_DIR / "daily",
    BASE_DIR / "notes",  # 添加更多允许的目录
]
```

## 示例

### 搜索文档

```python
result = await session.call_tool("search_docs", arguments={"query": "Context"})
```

输出：
```
Found 2 document(s) matching 'Context':

📄 /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md
   Matches: 3
   Preview:
   Line 15: ## Context 学习笔记
   Line 20: Context 是 AI Agent 的核心概念...
```

### 读取文件

```python
result = await session.call_tool(
    "get_file",
    arguments={"path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md"}
)
```

输出：
```
📄 File: /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md
📏 Size: 1234 characters
📝 Lines: 45
────────────────────────────────────────────────────────────────────────────────
[文件内容]
────────────────────────────────────────────────────────────────────────────────
✓ Source: /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md
```

### 错误处理

尝试访问白名单外的文件：

```python
result = await session.call_tool("get_file", arguments={"path": "/etc/passwd"})
```

输出：
```
Error: Access denied: Path '/etc/passwd' is not within allowed directories.
Allowed directories:
  - /Users/zhangxuetao/ai-web3-school-cohort-0/daily
```

## 日志

所有工具调用都会记录到 `logs/mcp_server.log`：

```json
{
  "timestamp": "2026-05-27T16:30:00.123456",
  "tool": "get_file",
  "arguments": {
    "path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md"
  },
  "success": true,
  "result_summary": {
    "type": "str",
    "length": 1234
  }
}
```

## 安全考虑

1. **路径解析**: 使用 `Path.resolve()` 解析符号链接和相对路径
2. **白名单检查**: 使用 `is_relative_to()` 确保路径在允许的目录内
3. **错误处理**: 所有异常都会被捕获并返回明确的错误消息
4. **日志审计**: 所有操作都有完整的审计日志

## 下一步：权限升级方案

参见 [PERMISSION_UPGRADE.md](./PERMISSION_UPGRADE.md) 了解如何安全地添加写入工具。
