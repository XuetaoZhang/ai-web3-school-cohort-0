"""
MCP 只读服务器使用示例

演示如何使用 search_docs 和 get_file 工具。
"""
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

async def example_usage():
    """演示 MCP 服务器的各种使用场景"""

    # 配置服务器参数
    server_script = Path(__file__).parent / "run_server.py"
    server_params = StdioServerParameters(
        command="python3",
        args=[str(server_script)],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=" * 80)
            print("MCP 只读服务器使用示例")
            print("=" * 80)

            # 示例 1: 搜索包含特定关键词的文档
            print("\n【示例 1】搜索包含 'Context' 的文档")
            print("-" * 80)
            result = await session.call_tool("search_docs", arguments={"query": "Context"})
            print(result.content[0].text)

            # 示例 2: 搜索另一个关键词
            print("\n【示例 2】搜索包含 'MCP' 的文档")
            print("-" * 80)
            result = await session.call_tool("search_docs", arguments={"query": "MCP"})
            print(result.content[0].text)

            # 示例 3: 读取特定文件
            print("\n【示例 3】读取最新的学习笔记")
            print("-" * 80)
            result = await session.call_tool(
                "get_file",
                arguments={"path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/2026-05-27.md"}
            )
            # 只显示前 500 个字符
            content = result.content[0].text
            print(content[:500] + "...\n[内容已截断]")

            # 示例 4: 尝试访问白名单外的文件（应该失败）
            print("\n【示例 4】尝试访问白名单外的文件（安全测试）")
            print("-" * 80)
            result = await session.call_tool(
                "get_file",
                arguments={"path": "/etc/hosts"}
            )
            print(result.content[0].text)

            # 示例 5: 尝试读取不存在的文件
            print("\n【示例 5】尝试读取不存在的文件（错误处理测试）")
            print("-" * 80)
            result = await session.call_tool(
                "get_file",
                arguments={"path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/nonexistent.md"}
            )
            print(result.content[0].text)

            print("\n" + "=" * 80)
            print("所有示例执行完成！")
            print("查看日志文件: logs/mcp_server.log")
            print("=" * 80)

if __name__ == "__main__":
    asyncio.run(example_usage())
