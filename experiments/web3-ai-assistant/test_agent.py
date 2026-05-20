#!/usr/bin/env python3
"""
Web3 AI Assistant 测试脚本
非交互式测试，验证所有工具功能
"""

import os
from tools import security_check, generate_contract, explain_contract, optimize_gas

def test_security_check():
    """测试安全审计功能"""
    print("\n" + "="*60)
    print("🔍 测试 1: 安全审计")
    print("="*60)

    # 读取有漏洞的合约
    with open("examples/vulnerable_contract.sol", "r") as f:
        vulnerable_code = f.read()

    print("\n📄 分析合约: vulnerable_contract.sol")
    result = security_check(vulnerable_code)
    print(result)

    # 读取安全的合约
    with open("examples/safe_contract.sol", "r") as f:
        safe_code = f.read()

    print("\n📄 分析合约: safe_contract.sol")
    result = security_check(safe_code)
    print(result)

def test_generate_contract():
    """测试代码生成功能"""
    print("\n" + "="*60)
    print("🔨 测试 2: 代码生成")
    print("="*60)

    contract_type = "erc20"
    params = "name=MyToken, symbol=MTK, decimals=18"
    print(f"\n📝 生成 {contract_type} 合约")
    print(f"参数: {params}")
    result = generate_contract(contract_type, params)
    print(result[:500] + "...\n[输出已截断]")

def test_explain_contract():
    """测试合约解释功能"""
    print("\n" + "="*60)
    print("📖 测试 3: 合约解释")
    print("="*60)

    # 读取安全的合约
    with open("examples/safe_contract.sol", "r") as f:
        code = f.read()

    print("\n📄 解释合约: safe_contract.sol")
    result = explain_contract(code)
    print(result)

def test_optimize_gas():
    """测试 Gas 优化功能"""
    print("\n" + "="*60)
    print("⚡ 测试 4: Gas 优化")
    print("="*60)

    # 读取有漏洞的合约（也有 Gas 优化空间）
    with open("examples/vulnerable_contract.sol", "r") as f:
        code = f.read()

    print("\n📄 分析合约: vulnerable_contract.sol")
    result = optimize_gas(code)
    print(result)

def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🧪 Web3 AI Assistant 功能测试")
    print("="*60)

    try:
        # 测试所有功能
        test_security_check()
        test_generate_contract()
        test_explain_contract()
        test_optimize_gas()

        print("\n" + "="*60)
        print("✅ 所有测试完成")
        print("="*60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
