# MCP 只读服务器 - 项目总结

## 项目概述

这是一个基于 Model Context Protocol (MCP) 的只读文档服务器，提供安全的文档搜索和文件读取功能。项目完整实现了白名单访问控制、日志记录、错误处理等安全特性。

## 实现的功能

### ✅ 核心工具

1. **search_docs(query)** - 文档搜索
   - 在白名单目录中搜索包含查询字符串的文档
   - 返回匹配的文件路径、匹配次数和上下文预览
   - 支持多行预览，显示行号

2. **get_file(path)** - 文件读取
   - 读取白名单目录中的文件内容
   - 返回完整内容和元数据（文件大小、行数）
   - 包含源路径信息便于追溯

### ✅ 安全特性

- **路径白名单**: 只能访问 `/Users/zhangxuetao/ai-web3-school-cohort-0/daily` 目录
- **路径验证**: 使用 `Path.resolve()` 和 `is_relative_to()` 防止路径遍历攻击
- **明确错误**: 所有错误都返回清晰的错误消息，包含允许的目录列表
- **日志记录**: 所有工具调用都记录到 `logs/mcp_server.log`
- **源路径追踪**: 所有返回结果都包含完整的源文件路径

### ✅ 日志系统

每次工具调用都会生成结构化的 JSON 日志：

```json
{
  "timestamp": "2026-05-27T22:53:18.341058",
  "tool": "search_docs",
  "arguments": {"query": "Day"},
  "success": true,
  "result_summary": {
    "type": "str",
    "length": 2279
  }
}
```

## 项目结构

```
mcp-practice/
├── src/
│   ├── __init__.py
│   ├── config.py          # 配置和白名单管理
│   ├── logger.py          # 日志记录工具
│   └── server.py          # MCP 服务器实现
├── tests/
│   └── test_client.py     # 自动化测试客户端
├── examples/
│   └── usage_demo.py      # 使用示例
├── logs/
│   └── mcp_server.log     # 服务器日志
├── run_server.py          # 服务器启动脚本
├── pyproject.toml         # 项目配置
├── README.md              # 使用文档
├── PERMISSION_UPGRADE.md  # 权限升级方案
└── PROJECT_SUMMARY.md     # 本文档
```

## 测试结果

### 测试场景

1. ✅ **搜索文档**: 成功搜索到 10 个包含 "Day" 的文档
2. ✅ **读取文件**: 成功读取白名单内的文件（8477 字符）
3. ✅ **拒绝非法访问**: 成功拒绝访问 `/etc/passwd`
4. ✅ **日志记录**: 所有操作都正确记录到日志文件

### 测试输出示例

```
=== Testing search_docs ===
Found 10 document(s) matching 'Day':

📄 /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-27.md
   Matches: 14
   Preview:
   Line 1: # Day 6: MCP (Model Context Protocol) - 2026-05-27
   ...

=== Testing get_file (valid path) ===
📄 File: /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md
📏 Size: 8477 characters
📝 Lines: 295
────────────────────────────────────────────────────────────────────────────────
[文件内容]
────────────────────────────────────────────────────────────────────────────────
✓ Source: /Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-19.md

=== Testing get_file (invalid path - should fail) ===
Error: Access denied: Path '/etc/passwd' is not within allowed directories.
Allowed directories:
  - /Users/zhangxuetao/ai-web3-school-cohort-0/daily
```

## 安全设计

### 1. 白名单机制

```python
ALLOWED_DIRECTORIES: List[Path] = [
    BASE_DIR / "daily",
]

def is_path_allowed(path: Path) -> bool:
    """检查路径是否在白名单内"""
    try:
        resolved_path = path.resolve()
        return any(
            resolved_path.is_relative_to(allowed_dir.resolve())
            for allowed_dir in ALLOWED_DIRECTORIES
        )
    except (ValueError, OSError):
        return False
```

### 2. 错误处理

所有错误都会：
- 捕获异常并返回明确的错误消息
- 记录到日志文件
- 不会静默失败
- 不会泄露敏感信息

## 使用方法

### 1. 安装依赖

```bash
cd experiments/mcp-practice
python3 -m pip install -e .
```

### 2. 运行测试

```bash
python3 tests/test_client.py
```

### 3. 运行示例

```bash
python3 examples/usage_demo.py
```

### 4. 查看日志

```bash
cat logs/mcp_server.log
```

## 技术栈

- **Python 3.10+**: 编程语言
- **MCP SDK 1.27.1**: Model Context Protocol 实现
- **asyncio**: 异步 I/O
- **pathlib**: 路径操作
- **logging**: 日志记录

## 学习收获

### 1. MCP 协议理解

- 理解了 MCP 的工具注册和调用机制
- 掌握了 stdio 通信方式
- 学会了使用 `@app.list_tools()` 和 `@app.call_tool()` 装饰器

### 2. 安全设计实践

- 实现了完整的白名单访问控制
- 防止了路径遍历攻击（`../../../etc/passwd`）
- 设计了分级权限管理方案

### 3. 错误处理最佳实践

- 所有错误都有明确的错误消息
- 错误消息包含上下文信息（如允许的目录列表）
- 不会静默失败

### 4. 日志和审计

- 结构化日志（JSON 格式）
- 完整的操作审计追踪
- 便于后续分析和调试

## 可能的改进

1. **性能优化**
   - 添加搜索结果缓存
   - 支持增量搜索
   - 并行处理多个文件

2. **功能增强**
   - 支持正则表达式搜索
   - 支持文件类型过滤
   - 添加全文索引

3. **安全增强**
   - 添加速率限制
   - 支持多用户权限管理
   - 集成外部认证系统

4. **监控和告警**
   - 添加 Prometheus metrics
   - 异常操作告警
   - 性能监控

## 总结

这个项目成功实现了一个安全、可靠的只读 MCP 服务器，具备：

- ✅ 完整的功能实现（搜索、读取）
- ✅ 严格的安全控制（白名单、路径验证）
- ✅ 完善的日志审计
- ✅ 清晰的错误处理
- ✅ 详细的权限升级方案

通过这个项目，深入理解了 MCP 协议的工作原理，掌握了安全编程的最佳实践，为后续开发更复杂的 MCP 工具打下了坚实的基础。
