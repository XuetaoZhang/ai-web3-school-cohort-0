"""
DAO Research Agent - 测试脚本
非交互式测试，验证 Agent 的完整工作流程
"""

import os
from agent import run_agent


def test_proposal_123():
    """测试提案 #123 的分析"""
    print("\n" + "=" * 60)
    print("测试案例 1: 分析提案 #123（资金申请）")
    print("=" * 60)

    result = run_agent(
        user_input="分析提案 #123",
        max_iterations=10,
        verbose=True
    )

    print("\n" + "=" * 60)
    print("📊 最终报告")
    print("=" * 60)
    print(result)
    print("\n" + "=" * 60)

    return result


def test_proposal_124():
    """测试提案 #124 的分析"""
    print("\n" + "=" * 60)
    print("测试案例 2: 分析提案 #124（治理修改）")
    print("=" * 60)

    result = run_agent(
        user_input="研究提案 124",
        max_iterations=10,
        verbose=True
    )

    print("\n" + "=" * 60)
    print("📊 最终报告")
    print("=" * 60)
    print(result)
    print("\n" + "=" * 60)

    return result


def test_tools_only():
    """仅测试工具函数（不调用 LLM）"""
    print("\n" + "=" * 60)
    print("测试案例 3: 工具函数测试（无 LLM）")
    print("=" * 60)

    from tools import (
        read_proposal,
        search_forum,
        analyze_sentiment,
        check_risks,
        generate_checklist
    )
    import json

    # 1. 读取提案
    print("\n1️⃣ 读取提案 #123")
    proposal = read_proposal("123")
    print(f"   标题: {proposal['title']}")
    print(f"   类型: {proposal['category']}")
    print(f"   金额: {proposal['requested_amount']}")
    print(f"   支持率: {proposal['support_percentage']}%")

    # 2. 搜索讨论
    print("\n2️⃣ 搜索论坛讨论")
    discussions = search_forum("123")
    print(f"   讨论数: {discussions['total_discussions']}")
    print(f"   情感分布: {discussions['sentiment_distribution']}")

    # 3. 分析情感
    print("\n3️⃣ 分析情感倾向")
    sentiment = analyze_sentiment(discussions)
    print(f"   支持: {sentiment['summary']['total_support']}")
    print(f"   反对: {sentiment['summary']['total_oppose']}")
    print(f"   中立: {sentiment['summary']['total_neutral']}")

    # 4. 检查风险
    print("\n4️⃣ 检查风险")
    risks = check_risks(proposal)
    print(f"   风险数: {risks['total_risks']}")
    print(f"   风险等级: {risks['risk_level']}")
    for risk in risks['risks']:
        print(f"   - {risk['type']}: {risk['description']}")

    # 5. 生成检查清单
    print("\n5️⃣ 生成检查清单")
    checklist = generate_checklist({
        "proposal": proposal,
        "risks": risks
    })
    print(f"   检查类别: {checklist['total_categories']}")

    print("\n✅ 所有工具函数测试通过")


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 DAO Research Agent 测试套件")
    print("=" * 60)

    # 检查 API Key
    if not os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEPSEEK_API_KEY") == "your-api-key-here":
        print("\n⚠️  未设置 DEEPSEEK_API_KEY，只运行工具函数测试")
        test_tools_only()
        return

    try:
        # 测试 1: 资金申请提案
        print("\n" + "🔬 开始测试...")
        test_proposal_123()

        # 询问是否继续
        print("\n" + "-" * 60)
        response = input("是否继续测试提案 #124？(y/n): ").strip().lower()
        if response == 'y':
            test_proposal_124()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n⚠️  测试被中断")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
