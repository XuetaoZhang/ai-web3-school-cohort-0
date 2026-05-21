"""
模拟数据源：链上数据、安全数据库、用户记忆

在真实场景中，这些数据来自：
- RPC 节点（Infura/Alchemy）
- Etherscan API
- Tenderly Simulation API
- 内部安全数据库
"""

from datetime import datetime
from typing import Dict, List, Any


class MockRPCClient:
    """模拟 RPC 客户端"""

    def __init__(self):
        # 模拟链上数据
        self.data = {
            # USDC 合约
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48": {
                "symbol": "USDC",
                "decimals": 6,
                "balances": {
                    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb": 1000000000,  # 1000 USDC
                },
                "allowances": {
                    ("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb", "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"): 0,
                }
            }
        }

    def get_block_number(self) -> int:
        return 19234567

    def get_balance(self, token: str, user: str) -> int:
        return self.data.get(token, {}).get("balances", {}).get(user, 0)

    def get_allowance(self, token: str, user: str, spender: str) -> int:
        return self.data.get(token, {}).get("allowances", {}).get((user, spender), 0)

    def get_token_info(self, token: str) -> Dict[str, Any]:
        return {
            "symbol": self.data.get(token, {}).get("symbol", "UNKNOWN"),
            "decimals": self.data.get(token, {}).get("decimals", 18)
        }


class MockSimulationClient:
    """模拟交易模拟客户端（Tenderly）"""

    def simulate(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """模拟交易执行"""
        spender = transaction_data["spender"]
        amount = transaction_data["amount"]

        # 检查是否是无限授权
        is_unlimited = amount == 2**256 - 1

        return {
            "simulation_success": True,
            "simulation_result": {
                "state_changes": [
                    {
                        "type": "allowance_change",
                        "from": "0",
                        "to": "unlimited" if is_unlimited else str(amount),
                        "token": transaction_data["token_symbol"]
                    }
                ],
                "no_unexpected_transfers": True,
                "no_ownership_changes": True,
                "gas_estimate": "46000"
            },
            "simulation_warnings": []
        }


class MockSecurityDatabase:
    """模拟安全数据库"""

    def __init__(self):
        # 可信合约列表
        self.trusted_contracts = {
            "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45": {
                "name": "Uniswap V3 Router 2",
                "verified": True,
                "source_code_verified": True,
                "audit_reports": [
                    {
                        "auditor": "Trail of Bits",
                        "date": "2021-03-15",
                        "url": "https://github.com/Uniswap/v3-core/blob/main/audits/tob/audit.pdf"
                    }
                ],
                "deployment_date": "2021-03-23",
                "transaction_count": 15234567,
                "reputation": "excellent"
            }
        }

        # 已知诈骗合约
        self.scam_contracts = {
            "0x1234567890123456789012345678901234567890": {
                "name": "Fake Uniswap Router",
                "issue": "假冒 Uniswap Router，盗取授权",
                "date": "2024-03-15",
                "loss": "$2.3M"
            }
        }

        # 安全规则
        self.security_rules = """
## Approve 安全检查清单

### 高风险信号
- 无限授权（uint256.max）
- Spender 未验证源码
- Spender 不在可信列表
- Spender 部署时间 < 30 天
- Spender 交易量异常低

### 中风险信号
- 授权金额 > 用户余额 10 倍
- Spender 无审计报告
- dApp 域名与 Spender 不匹配

### 低风险信号
- 授权金额 ≤ 用户余额
- Spender 在可信列表
- Spender 有多次审计
"""

    def get_spender_info(self, spender: str) -> Dict[str, Any]:
        """获取 Spender 合约信息"""
        if spender in self.trusted_contracts:
            return {
                "in_trusted_list": True,
                **self.trusted_contracts[spender]
            }
        elif spender in self.scam_contracts:
            return {
                "in_trusted_list": False,
                "is_known_scam": True,
                **self.scam_contracts[spender]
            }
        else:
            return {
                "in_trusted_list": False,
                "is_known_scam": False,
                "name": "Unknown Contract",
                "verified": False
            }

    def get_security_rules(self) -> str:
        """获取安全规则"""
        return self.security_rules

    def search_similar_cases(self, spender: str) -> List[Dict[str, Any]]:
        """搜索相似案例"""
        if spender in self.trusted_contracts:
            return [{
                "type": "safe_pattern",
                "spender": spender,
                "name": self.trusted_contracts[spender]["name"],
                "usage_count": "15M+ transactions",
                "reputation": "excellent"
            }]
        elif spender in self.scam_contracts:
            return [{
                "type": "scam_case",
                "spender": spender,
                **self.scam_contracts[spender]
            }]
        else:
            return []


class MockUserMemory:
    """模拟用户记忆"""

    def __init__(self):
        self.user_data = {
            "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb": {
                "risk_preference": "conservative",
                "trusted_dapps": [
                    "app.uniswap.org",
                    "app.aave.com"
                ],
                "previous_approvals": [
                    {
                        "spender": "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",
                        "token": "USDC",
                        "date": "2026-05-10",
                        "result": "approved"
                    }
                ]
            }
        }

    def get_user_preferences(self, user_address: str) -> Dict[str, Any]:
        """获取用户偏好"""
        return self.user_data.get(user_address, {
            "risk_preference": "moderate",
            "trusted_dapps": [],
            "previous_approvals": []
        })
