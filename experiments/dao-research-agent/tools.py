"""
DAO Research Agent - Tools
工具函数实现
"""

import json
from typing import Dict, List, Any
from datetime import datetime, timedelta


# ==================== 模拟数据 ====================
# 在实际应用中，这些数据应该从真实的 DAO 平台获取

PROPOSALS_DB = {
    "123": {
        "id": "123",
        "title": "提案：为 DeFi 教育项目拨款 50,000 USDC",
        "description": """
## 提案概述
申请 50,000 USDC 用于开发一个面向新手的 DeFi 教育平台。

## 项目目标
1. 创建 20 个交互式教程
2. 开发模拟交易环境
3. 建立社区问答系统

## 资金使用计划
- 开发成本：30,000 USDC
- 内容创作：15,000 USDC
- 运营费用：5,000 USDC

## 时间线
- 第 1-2 月：平台开发
- 第 3-4 月：内容创作
- 第 5-6 月：测试和优化

## 团队介绍
- Alice: 全栈工程师，5 年 Web3 经验
- Bob: 内容创作者，DeFi 研究员
- Carol: 社区运营，3 年 DAO 经验
        """,
        "proposer": "0x1234...5678",
        "proposer_name": "Alice (DeFi Educator)",
        "status": "active",
        "created_at": "2026-05-15",
        "voting_start": "2026-05-18",
        "voting_end": "2026-05-25",
        "votes_for": 1200000,
        "votes_against": 300000,
        "quorum": 1000000,
        "category": "funding",
        "requested_amount": "50,000 USDC"
    },
    "124": {
        "id": "124",
        "title": "提案：修改治理参数 - 降低提案门槛",
        "description": """
## 提案概述
建议将创建提案所需的最低代币数量从 10,000 降低到 5,000。

## 理由
1. 当前门槛过高，限制了社区参与
2. 其他成功的 DAO 使用更低的门槛
3. 可以增加提案多样性

## 风险评估
- 可能增加垃圾提案
- 需要更多的社区审核资源

## 缓解措施
- 增加提案审核期
- 引入提案质量评分系统
        """,
        "proposer": "0xabcd...efgh",
        "proposer_name": "Bob (Community Member)",
        "status": "active",
        "created_at": "2026-05-16",
        "voting_start": "2026-05-19",
        "voting_end": "2026-05-26",
        "votes_for": 800000,
        "votes_against": 600000,
        "quorum": 1000000,
        "category": "governance",
        "requested_amount": "0"
    }
}

FORUM_DISCUSSIONS = {
    "123": [
        {
            "author": "Charlie",
            "timestamp": "2026-05-16 10:30",
            "content": "强烈支持这个提案！DeFi 教育对于行业发展至关重要。我看过团队之前的工作，质量很高。",
            "sentiment": "positive",
            "votes": 45
        },
        {
            "author": "David",
            "timestamp": "2026-05-16 14:20",
            "content": "我有一些担忧：1) 50,000 USDC 是否过高？2) 团队是否有足够的 track record？3) 如何衡量项目成功？",
            "sentiment": "neutral",
            "votes": 32
        },
        {
            "author": "Eve",
            "timestamp": "2026-05-17 09:15",
            "content": "反对。预算不够透明，没有看到详细的成本分解。建议团队提供更详细的预算表。",
            "sentiment": "negative",
            "votes": 28
        },
        {
            "author": "Alice",
            "timestamp": "2026-05-17 16:45",
            "content": "感谢反馈！我们会在下周提供详细的预算分解表。关于 track record，我们团队之前完成了 XYZ 项目（链接）。",
            "sentiment": "neutral",
            "votes": 50
        },
        {
            "author": "Frank",
            "timestamp": "2026-05-18 11:00",
            "content": "支持，但建议分阶段拨款。先拨 20,000 完成第一阶段，验证后再拨剩余资金。",
            "sentiment": "positive",
            "votes": 67
        }
    ],
    "124": [
        {
            "author": "Grace",
            "timestamp": "2026-05-17 10:00",
            "content": "支持降低门槛。当前门槛确实太高了，很多好的想法因为门槛问题无法提出。",
            "sentiment": "positive",
            "votes": 38
        },
        {
            "author": "Henry",
            "timestamp": "2026-05-17 15:30",
            "content": "担心会导致垃圾提案泛滥。建议同时引入提案保证金机制，如果提案被拒绝则扣除保证金。",
            "sentiment": "negative",
            "votes": 42
        },
        {
            "author": "Iris",
            "timestamp": "2026-05-18 09:20",
            "content": "中立。降低门槛是好的，但需要配套措施。建议先试运行 3 个月，观察效果。",
            "sentiment": "neutral",
            "votes": 29
        }
    ]
}


# ==================== 工具函数 ====================

def read_proposal(proposal_id: str) -> Dict[str, Any]:
    """
    读取 DAO 提案的完整内容

    Args:
        proposal_id: 提案 ID（如 "123" 或 "#123"）

    Returns:
        提案的详细信息，包括标题、描述、投票状态等
    """
    # 清理 proposal_id（移除 # 符号）
    proposal_id = proposal_id.strip().lstrip('#')

    if proposal_id not in PROPOSALS_DB:
        return {
            "error": f"提案 #{proposal_id} 不存在",
            "available_proposals": list(PROPOSALS_DB.keys())
        }

    proposal = PROPOSALS_DB[proposal_id].copy()

    # 计算投票进度
    total_votes = proposal["votes_for"] + proposal["votes_against"]
    if total_votes > 0:
        proposal["support_percentage"] = round(proposal["votes_for"] / total_votes * 100, 2)
    else:
        proposal["support_percentage"] = 0

    # 检查是否达到 quorum
    proposal["quorum_reached"] = total_votes >= proposal["quorum"]

    # 计算剩余时间
    voting_end = datetime.strptime(proposal["voting_end"], "%Y-%m-%d")
    now = datetime.now()
    days_left = (voting_end - now).days
    proposal["days_left"] = max(0, days_left)

    return proposal


def search_forum(proposal_id: str, keywords: str = None) -> Dict[str, Any]:
    """
    搜索论坛中关于该提案的讨论

    Args:
        proposal_id: 提案 ID
        keywords: 可选的关键词过滤

    Returns:
        讨论列表和统计信息
    """
    proposal_id = proposal_id.strip().lstrip('#')

    if proposal_id not in FORUM_DISCUSSIONS:
        return {
            "error": f"没有找到关于提案 #{proposal_id} 的讨论",
            "discussions": []
        }

    discussions = FORUM_DISCUSSIONS[proposal_id]

    # 如果有关键词，进行过滤
    if keywords:
        keywords_lower = keywords.lower()
        discussions = [
            d for d in discussions
            if keywords_lower in d["content"].lower()
        ]

    # 统计信息
    total_discussions = len(discussions)
    positive_count = sum(1 for d in discussions if d["sentiment"] == "positive")
    negative_count = sum(1 for d in discussions if d["sentiment"] == "negative")
    neutral_count = sum(1 for d in discussions if d["sentiment"] == "neutral")

    return {
        "proposal_id": proposal_id,
        "total_discussions": total_discussions,
        "sentiment_distribution": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        },
        "discussions": discussions
    }


def analyze_sentiment(discussions: List[Dict]) -> Dict[str, Any]:
    """
    分析讨论的情感倾向，提取支持和反对理由

    Args:
        discussions: 讨论列表（从 search_forum 获取）

    Returns:
        支持理由、反对理由、中立观点的总结
    """
    if isinstance(discussions, dict) and "discussions" in discussions:
        discussions = discussions["discussions"]

    support_reasons = []
    oppose_reasons = []
    neutral_points = []

    for d in discussions:
        item = {
            "author": d["author"],
            "content": d["content"],
            "votes": d["votes"],
            "timestamp": d["timestamp"]
        }

        if d["sentiment"] == "positive":
            support_reasons.append(item)
        elif d["sentiment"] == "negative":
            oppose_reasons.append(item)
        else:
            neutral_points.append(item)

    # 按投票数排序
    support_reasons.sort(key=lambda x: x["votes"], reverse=True)
    oppose_reasons.sort(key=lambda x: x["votes"], reverse=True)
    neutral_points.sort(key=lambda x: x["votes"], reverse=True)

    return {
        "support_reasons": support_reasons,
        "oppose_reasons": oppose_reasons,
        "neutral_points": neutral_points,
        "summary": {
            "total_support": len(support_reasons),
            "total_oppose": len(oppose_reasons),
            "total_neutral": len(neutral_points),
            "most_voted_support": support_reasons[0] if support_reasons else None,
            "most_voted_oppose": oppose_reasons[0] if oppose_reasons else None
        }
    }


def check_risks(proposal: Dict[str, Any]) -> Dict[str, Any]:
    """
    检查提案的潜在风险

    Args:
        proposal: 提案信息（从 read_proposal 获取）

    Returns:
        风险评估结果
    """
    risks = []

    # 检查资金风险
    if proposal.get("category") == "funding":
        amount_str = proposal.get("requested_amount", "0")
        try:
            amount = float(amount_str.replace(",", "").split()[0])

            if amount > 100000:
                risks.append({
                    "type": "资金风险",
                    "severity": "高",
                    "description": f"请求金额较大（{amount_str}），需要特别审慎",
                    "mitigation": "建议分阶段拨款，根据里程碑验证后再拨付剩余资金"
                })
            elif amount > 50000:
                risks.append({
                    "type": "资金风险",
                    "severity": "中",
                    "description": f"请求金额适中（{amount_str}），需要详细的预算分解",
                    "mitigation": "要求团队提供详细的成本明细和资金使用计划"
                })
        except:
            pass

    # 检查治理风险
    if proposal.get("category") == "governance":
        risks.append({
            "type": "治理风险",
            "severity": "高",
            "description": "该提案会修改 DAO 的治理参数，可能影响未来的决策流程",
            "mitigation": "建议设置试运行期，并保留回滚机制"
        })

    # 检查投票参与度
    if not proposal.get("quorum_reached"):
        risks.append({
            "type": "参与度风险",
            "severity": "中",
            "description": "当前投票未达到 quorum，提案可能无法通过",
            "mitigation": "需要更多社区成员参与投票"
        })

    # 检查投票时间
    if proposal.get("days_left", 0) < 2:
        risks.append({
            "type": "时间风险",
            "severity": "低",
            "description": f"投票即将结束（剩余 {proposal.get('days_left')} 天），时间紧迫",
            "mitigation": "尽快完成分析和投票决策"
        })

    # 检查提案者信息
    if "proposer_name" not in proposal or not proposal.get("proposer_name"):
        risks.append({
            "type": "信任风险",
            "severity": "中",
            "description": "提案者信息不完整，难以评估可信度",
            "mitigation": "调查提案者的历史记录和社区声誉"
        })

    return {
        "total_risks": len(risks),
        "risks": risks,
        "risk_level": "高" if any(r["severity"] == "高" for r in risks) else
                      "中" if any(r["severity"] == "中" for r in risks) else "低"
    }


def generate_checklist(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成投票前检查清单

    Args:
        analysis: 综合分析结果

    Returns:
        需要人工确认的事项列表
    """
    checklist = []

    # 基础检查项
    checklist.append({
        "category": "提案理解",
        "items": [
            "✓ 我已完整阅读提案内容",
            "✓ 我理解提案的目标和实施计划",
            "✓ 我了解提案对 DAO 的影响"
        ]
    })

    # 资金相关检查
    if analysis.get("proposal", {}).get("category") == "funding":
        checklist.append({
            "category": "资金审查",
            "items": [
                "□ 预算是否合理？是否有详细的成本分解？",
                "□ 团队是否有相关经验和 track record？",
                "□ 是否有明确的里程碑和验收标准？",
                "□ 资金使用是否有监督机制？",
                "□ 是否考虑分阶段拨款？"
            ]
        })

    # 治理相关检查
    if analysis.get("proposal", {}).get("category") == "governance":
        checklist.append({
            "category": "治理影响",
            "items": [
                "□ 修改是否会降低 DAO 的安全性？",
                "□ 是否有回滚机制？",
                "□ 是否需要试运行期？",
                "□ 对现有提案和投票的影响？"
            ]
        })

    # 社区意见检查
    checklist.append({
        "category": "社区反馈",
        "items": [
            "□ 我已阅读论坛讨论",
            "□ 我理解支持和反对的主要理由",
            "□ 提案者是否回应了社区的关切？",
            "□ 是否有重大的未解决问题？"
        ]
    })

    # 风险检查
    if analysis.get("risks", {}).get("risks"):
        risk_items = [
            f"□ {risk['description']}"
            for risk in analysis["risks"]["risks"]
        ]
        checklist.append({
            "category": "风险评估",
            "items": risk_items
        })

    # 最终决策
    checklist.append({
        "category": "最终决策",
        "items": [
            "□ 我已权衡所有信息",
            "□ 我的投票符合 DAO 的长期利益",
            "□ 我准备好投票了"
        ]
    })

    return {
        "checklist": checklist,
        "total_categories": len(checklist),
        "note": "请在投票前确认所有检查项。标记为 □ 的项目需要人工判断。"
    }


# ==================== 工具定义（给 LLM 的）====================

TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "read_proposal",
            "description": "读取 DAO 提案的完整内容，包括标题、描述、提议者、投票状态、资金请求等信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "proposal_id": {
                        "type": "string",
                        "description": "提案 ID，如 '123' 或 '#123'"
                    }
                },
                "required": ["proposal_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_forum",
            "description": "搜索论坛中关于该提案的讨论，获取社区成员的观点和反馈",
            "parameters": {
                "type": "object",
                "properties": {
                    "proposal_id": {
                        "type": "string",
                        "description": "提案 ID"
                    },
                    "keywords": {
                        "type": "string",
                        "description": "可选的关键词过滤，用于搜索特定主题的讨论"
                    }
                },
                "required": ["proposal_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_sentiment",
            "description": "分析论坛讨论的情感倾向，提取支持理由、反对理由和中立观点",
            "parameters": {
                "type": "object",
                "properties": {
                    "discussions": {
                        "type": "object",
                        "description": "从 search_forum 获取的讨论数据"
                    }
                },
                "required": ["discussions"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_risks",
            "description": "检查提案的潜在风险，包括资金风险、治理风险、技术风险等",
            "parameters": {
                "type": "object",
                "properties": {
                    "proposal": {
                        "type": "object",
                        "description": "从 read_proposal 获取的提案数据"
                    }
                },
                "required": ["proposal"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_checklist",
            "description": "生成投票前检查清单，列出需要人工确认的事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "analysis": {
                        "type": "object",
                        "description": "综合分析结果，包括提案、讨论、风险等信息"
                    }
                },
                "required": ["analysis"]
            }
        }
    }
]


if __name__ == "__main__":
    # 测试工具函数
    print("=" * 60)
    print("测试工具函数")
    print("=" * 60)

    # 测试 read_proposal
    print("\n1. 读取提案 #123")
    proposal = read_proposal("123")
    print(json.dumps(proposal, indent=2, ensure_ascii=False))

    # 测试 search_forum
    print("\n2. 搜索论坛讨论")
    discussions = search_forum("123")
    print(f"找到 {discussions['total_discussions']} 条讨论")
    print(f"情感分布: {discussions['sentiment_distribution']}")

    # 测试 analyze_sentiment
    print("\n3. 分析情感倾向")
    sentiment = analyze_sentiment(discussions)
    print(f"支持: {sentiment['summary']['total_support']}")
    print(f"反对: {sentiment['summary']['total_oppose']}")
    print(f"中立: {sentiment['summary']['total_neutral']}")

    # 测试 check_risks
    print("\n4. 检查风险")
    risks = check_risks(proposal)
    print(f"发现 {risks['total_risks']} 个风险")
    print(f"风险等级: {risks['risk_level']}")

    # 测试 generate_checklist
    print("\n5. 生成检查清单")
    checklist = generate_checklist({
        "proposal": proposal,
        "risks": risks
    })
    print(f"生成 {checklist['total_categories']} 个检查类别")
