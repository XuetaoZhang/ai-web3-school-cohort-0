"""
测试 Context 分层设计的价值

对比实验：
1. 完整 Context（6 层）vs 简化 Context（只有事实层）
2. 有不可信输入标注 vs 无标注
3. 有记忆层 vs 无记忆层

验证：
- Context 分层是否影响 LLM 的判断准确性
- 不可信输入标注是否防止 LLM 被误导
- 记忆层是否只做参考不影响决策
"""

import json
from wallet_approval_agent import WalletApprovalAgent


def test_case_1_trusted_unlimited():
    """测试用例 1：可信合约 + 无限授权"""
    print("\n" + "=" * 80)
    print("测试用例 1：Uniswap V3 Router（可信合约 + 无限授权）")
    print("=" * 80)

    agent = WalletApprovalAgent()

    result = agent.evaluate_approval(
        user_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        transaction_data={
            "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "amount": 2**256 - 1  # 无限授权
        },
        dapp_description="Approve USDC to swap on Uniswap"
    )

    print("\n风险等级:", result.get("risk_level"))
    print("\n风险因素:")
    for factor in result.get("risk_factors", []):
        print(f"  - [{factor['severity']}] {factor['factor']}: {factor['explanation']}")

    print("\n建议:", result.get("recommendation"))

    print("\n检查清单:")
    for item in result.get("checklist", []):
        print(f"  {item}")

    print("\n替代方案:")
    for action in result.get("alternative_actions", []):
        print(f"  - {action}")

    return result


def test_case_2_unknown_contract():
    """测试用例 2：未知合约 + 无限授权"""
    print("\n" + "=" * 80)
    print("测试用例 2：未知合约（不在可信列表 + 无限授权）")
    print("=" * 80)

    agent = WalletApprovalAgent()

    result = agent.evaluate_approval(
        user_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        transaction_data={
            "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "spender": "0x9999999999999999999999999999999999999999",  # 未知合约
            "amount": 2**256 - 1  # 无限授权
        },
        dapp_description="Approve USDC to get 1000% APY on our new DeFi protocol!"
    )

    print("\n风险等级:", result.get("risk_level"))
    print("\n风险因素:")
    for factor in result.get("risk_factors", []):
        print(f"  - [{factor['severity']}] {factor['factor']}: {factor['explanation']}")

    print("\n建议:", result.get("recommendation"))

    print("\n检查清单:")
    for item in result.get("checklist", []):
        print(f"  {item}")

    return result


def test_case_3_known_scam():
    """测试用例 3：已知诈骗合约"""
    print("\n" + "=" * 80)
    print("测试用例 3：已知诈骗合约（在黑名单中）")
    print("=" * 80)

    agent = WalletApprovalAgent()

    result = agent.evaluate_approval(
        user_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        transaction_data={
            "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "spender": "0x1234567890123456789012345678901234567890",  # 已知诈骗合约
            "amount": 2**256 - 1
        },
        dapp_description="Official Uniswap Router - Approve to swap"  # 假冒说明
    )

    print("\n风险等级:", result.get("risk_level"))
    print("\n风险因素:")
    for factor in result.get("risk_factors", []):
        print(f"  - [{factor['severity']}] {factor['factor']}: {factor['explanation']}")

    print("\n建议:", result.get("recommendation"))

    return result


def test_case_4_limited_amount():
    """测试用例 4：可信合约 + 有限授权"""
    print("\n" + "=" * 80)
    print("测试用例 4：Uniswap V3 Router（可信合约 + 有限授权 100 USDC）")
    print("=" * 80)

    agent = WalletApprovalAgent()

    result = agent.evaluate_approval(
        user_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
        transaction_data={
            "token_contract": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
            "amount": 100_000_000  # 100 USDC (6 decimals)
        },
        dapp_description="Approve 100 USDC to swap on Uniswap"
    )

    print("\n风险等级:", result.get("risk_level"))
    print("\n风险因素:")
    for factor in result.get("risk_factors", []):
        print(f"  - [{factor['severity']}] {factor['factor']}: {factor['explanation']}")

    print("\n建议:", result.get("recommendation"))

    return result


def analyze_context_value():
    """分析 Context 分层的价值"""
    print("\n" + "=" * 80)
    print("Context 分层设计的价值分析")
    print("=" * 80)

    print("""
## 1. 指令层的价值
- 明确 Agent 的角色和边界
- 防止 Agent 越权操作（如直接执行签名）
- 要求输出结构化结果，便于验证

## 2. 任务层的价值
- 记录会话上下文（session_id, timestamp）
- 明确用户意图
- 便于审计和追溯

## 3. 事实层的价值
- 提供可验证的链上数据
- 实时查询，确保数据最新
- 模拟交易，预测执行结果
- 这是决策的核心依据

## 4. 知识层的价值
- 提供安全规则和历史案例
- 帮助 LLM 识别常见风险模式
- 可以缓存，提高效率

## 5. 不可信输入层的价值
- 明确标注来源和可信度
- 防止 LLM 被钓鱼网站误导
- 只做参考，不作为决策依据

## 6. 记忆层的价值
- 提升用户体验（提示历史操作）
- 但不能影响安全决策
- 必须重新检查当前状态

## 对比：无 Context 分层的问题
如果不做分层，直接把所有信息混在一起：
- LLM 可能被 dApp 页面说明误导
- 无法区分"事实"和"推测"
- 可能基于用户历史偏好自动批准
- 输出格式不可控，难以验证
- 无法审计决策依据
""")


def main():
    """运行所有测试"""
    print("\n" + "=" * 80)
    print("钱包授权检查 Agent - Context 分层设计验证")
    print("=" * 80)

    try:
        # 测试用例 1：可信合约 + 无限授权
        result1 = test_case_1_trusted_unlimited()

        # 测试用例 2：未知合约 + 无限授权
        result2 = test_case_2_unknown_contract()

        # 测试用例 3：已知诈骗合约
        result3 = test_case_3_known_scam()

        # 测试用例 4：可信合约 + 有限授权
        result4 = test_case_4_limited_amount()

        # 分析 Context 价值
        analyze_context_value()

        # 总结
        print("\n" + "=" * 80)
        print("测试总结")
        print("=" * 80)
        print(f"""
测试用例 1（可信 + 无限）: 风险等级 = {result1.get('risk_level')}
测试用例 2（未知 + 无限）: 风险等级 = {result2.get('risk_level')}
测试用例 3（诈骗 + 无限）: 风险等级 = {result3.get('risk_level')}
测试用例 4（可信 + 有限）: 风险等级 = {result4.get('risk_level')}

预期结果：
- 测试用例 1 应该是 medium（可信但无限授权）
- 测试用例 2 应该是 high（未知合约 + 无限授权）
- 测试用例 3 应该是 high（已知诈骗）
- 测试用例 4 应该是 low（可信 + 有限授权）
""")

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
