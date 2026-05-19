"""
Web3 AI Assistant - 工具定义
定义智能合约分析、生成、解释和优化工具
"""

import json
import re


# ============================================
# 工具函数定义
# ============================================

def security_check(code: str) -> str:
    """
    检查 Solidity 代码的安全问题

    Args:
        code: Solidity 合约代码

    Returns:
        安全检查报告（JSON 格式）
    """
    issues = []

    # 1. 检测重入攻击
    if re.search(r'\.call\{value:', code) and re.search(r'balances\[.*\]\s*=\s*0', code):
        call_pos = code.find('.call{value:')
        balance_pos = code.find('balances[')
        if call_pos < balance_pos:
            issues.append({
                "type": "重入攻击 (Reentrancy)",
                "severity": "高危",
                "description": "在更新状态之前进行外部调用，可能导致重入攻击",
                "suggestion": "先更新状态变量，再进行外部调用（Checks-Effects-Interactions 模式）"
            })

    # 2. 检测 tx.origin 使用
    if 'tx.origin' in code:
        issues.append({
            "type": "tx.origin 使用",
            "severity": "中危",
            "description": "使用 tx.origin 进行身份验证不安全",
            "suggestion": "使用 msg.sender 代替 tx.origin"
        })

    # 3. 检测未检查的外部调用
    if re.search(r'\.call\(|\.delegatecall\(|\.send\(', code):
        if not re.search(r'require\(.*\.call|if\s*\(.*\.call', code):
            issues.append({
                "type": "未检查的外部调用",
                "severity": "中危",
                "description": "外部调用的返回值未检查",
                "suggestion": "使用 require() 或 if 语句检查调用结果"
            })

    # 4. 检测访问控制
    if re.search(r'function\s+\w+\s*\([^)]*\)\s+public', code):
        if not re.search(r'modifier\s+onlyOwner|require\(msg\.sender\s*==', code):
            issues.append({
                "type": "缺少访问控制",
                "severity": "高危",
                "description": "敏感函数缺少访问控制",
                "suggestion": "添加 onlyOwner 或其他访问控制修饰符"
            })

    # 5. 检测时间戳依赖
    if 'block.timestamp' in code or 'now' in code:
        issues.append({
            "type": "时间戳依赖",
            "severity": "低危",
            "description": "依赖 block.timestamp 可能被矿工操纵",
            "suggestion": "避免在关键逻辑中依赖时间戳，或使用更安全的时间源"
        })

    # 6. 检测整数溢出（Solidity < 0.8.0）
    if not re.search(r'pragma solidity \^0\.[89]', code):
        if re.search(r'\+\+|\-\-|\+|\-|\*', code):
            issues.append({
                "type": "潜在整数溢出",
                "severity": "中危",
                "description": "Solidity < 0.8.0 不自动检查整数溢出",
                "suggestion": "升级到 Solidity >= 0.8.0 或使用 SafeMath 库"
            })

    result = {
        "total_issues": len(issues),
        "issues": issues,
        "summary": f"发现 {len(issues)} 个安全问题" if issues else "未发现明显的安全问题"
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


def generate_contract(contract_type: str, params: str) -> str:
    """
    生成智能合约代码

    Args:
        contract_type: 合约类型 (erc20, erc721, multisig, simple)
        params: 参数（JSON 格式），如 {"name": "MyToken", "symbol": "MTK"}

    Returns:
        生成的合约代码
    """
    try:
        params_dict = json.loads(params) if params else {}
    except:
        params_dict = {}

    if contract_type == "erc20":
        name = params_dict.get("name", "MyToken")
        symbol = params_dict.get("symbol", "MTK")
        initial_supply = params_dict.get("initial_supply", "1000000")

        code = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract {name} is ERC20, Ownable {{
    constructor() ERC20("{name}", "{symbol}") {{
        _mint(msg.sender, {initial_supply} * 10 ** decimals());
    }}

    function mint(address to, uint256 amount) public onlyOwner {{
        _mint(to, amount);
    }}

    function burn(uint256 amount) public {{
        _burn(msg.sender, amount);
    }}
}}'''

    elif contract_type == "erc721":
        name = params_dict.get("name", "MyNFT")
        symbol = params_dict.get("symbol", "MNFT")

        code = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract {name} is ERC721, Ownable {{
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    constructor() ERC721("{name}", "{symbol}") {{}}

    function mint(address to) public onlyOwner returns (uint256) {{
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        _mint(to, newTokenId);
        return newTokenId;
    }}
}}'''

    elif contract_type == "multisig":
        required = params_dict.get("required", "2")

        code = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MultiSigWallet {{
    event Deposit(address indexed sender, uint256 amount);
    event Submit(uint256 indexed txId);
    event Approve(address indexed owner, uint256 indexed txId);
    event Execute(uint256 indexed txId);

    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public required;

    struct Transaction {{
        address to;
        uint256 value;
        bytes data;
        bool executed;
    }}

    Transaction[] public transactions;
    mapping(uint256 => mapping(address => bool)) public approved;

    modifier onlyOwner() {{
        require(isOwner[msg.sender], "Not owner");
        _;
    }}

    constructor(address[] memory _owners, uint256 _required) {{
        require(_owners.length > 0, "Owners required");
        require(_required > 0 && _required <= _owners.length, "Invalid required");

        for (uint256 i = 0; i < _owners.length; i++) {{
            address owner = _owners[i];
            require(owner != address(0), "Invalid owner");
            require(!isOwner[owner], "Owner not unique");

            isOwner[owner] = true;
            owners.push(owner);
        }}

        required = _required;
    }}

    receive() external payable {{
        emit Deposit(msg.sender, msg.value);
    }}

    function submit(address _to, uint256 _value, bytes calldata _data) external onlyOwner {{
        transactions.push(Transaction({{
            to: _to,
            value: _value,
            data: _data,
            executed: false
        }}));
        emit Submit(transactions.length - 1);
    }}

    function approve(uint256 _txId) external onlyOwner {{
        require(_txId < transactions.length, "Tx does not exist");
        require(!approved[_txId][msg.sender], "Tx already approved");

        approved[_txId][msg.sender] = true;
        emit Approve(msg.sender, _txId);
    }}

    function execute(uint256 _txId) external onlyOwner {{
        require(_txId < transactions.length, "Tx does not exist");
        require(!transactions[_txId].executed, "Tx already executed");
        require(_getApprovalCount(_txId) >= required, "Not enough approvals");

        Transaction storage transaction = transactions[_txId];
        transaction.executed = true;

        (bool success, ) = transaction.to.call{{value: transaction.value}}(transaction.data);
        require(success, "Tx failed");

        emit Execute(_txId);
    }}

    function _getApprovalCount(uint256 _txId) private view returns (uint256 count) {{
        for (uint256 i = 0; i < owners.length; i++) {{
            if (approved[_txId][owners[i]]) {{
                count += 1;
            }}
        }}
    }}
}}'''

    elif contract_type == "simple":
        name = params_dict.get("name", "SimpleStorage")

        code = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract {name} {{
    uint256 public value;
    address public owner;

    event ValueChanged(uint256 newValue);

    modifier onlyOwner() {{
        require(msg.sender == owner, "Not owner");
        _;
    }}

    constructor() {{
        owner = msg.sender;
    }}

    function setValue(uint256 _value) public onlyOwner {{
        value = _value;
        emit ValueChanged(_value);
    }}

    function getValue() public view returns (uint256) {{
        return value;
    }}
}}'''

    else:
        return json.dumps({
            "error": f"不支持的合约类型: {contract_type}",
            "supported_types": ["erc20", "erc721", "multisig", "simple"]
        }, ensure_ascii=False)

    return json.dumps({
        "contract_type": contract_type,
        "code": code,
        "params": params_dict
    }, ensure_ascii=False, indent=2)


def explain_contract(code: str) -> str:
    """
    解释智能合约的功能

    Args:
        code: Solidity 合约代码

    Returns:
        合约功能解释（JSON 格式）
    """
    analysis = {
        "contract_name": "",
        "contract_type": "未知",
        "inheritance": [],
        "state_variables": [],
        "functions": [],
        "events": [],
        "modifiers": [],
        "patterns": []
    }

    # 提取合约名称
    contract_match = re.search(r'contract\s+(\w+)', code)
    if contract_match:
        analysis["contract_name"] = contract_match.group(1)

    # 检测合约类型
    if 'ERC20' in code or 'IERC20' in code:
        analysis["contract_type"] = "ERC20 代币"
    elif 'ERC721' in code or 'IERC721' in code:
        analysis["contract_type"] = "ERC721 NFT"
    elif 'MultiSig' in code or 'multisig' in code.lower():
        analysis["contract_type"] = "多签钱包"

    # 提取继承
    inheritance_match = re.search(r'contract\s+\w+\s+is\s+([\w\s,]+)', code)
    if inheritance_match:
        analysis["inheritance"] = [x.strip() for x in inheritance_match.group(1).split(',')]

    # 提取状态变量
    state_vars = re.findall(r'(uint256|address|bool|mapping|string|bytes)\s+(public|private|internal)?\s*(\w+)', code)
    analysis["state_variables"] = [{"type": t, "visibility": v or "internal", "name": n} for t, v, n in state_vars[:5]]

    # 提取函数
    functions = re.findall(r'function\s+(\w+)\s*\([^)]*\)\s+(public|external|internal|private)', code)
    analysis["functions"] = [{"name": name, "visibility": vis} for name, vis in functions[:10]]

    # 提取事件
    events = re.findall(r'event\s+(\w+)', code)
    analysis["events"] = events[:5]

    # 提取修饰符
    modifiers = re.findall(r'modifier\s+(\w+)', code)
    analysis["modifiers"] = modifiers

    # 检测设计模式
    if 'onlyOwner' in code or 'owner' in code:
        analysis["patterns"].append("Ownable 模式")
    if 'paused' in code or 'whenNotPaused' in code:
        analysis["patterns"].append("Pausable 模式")
    if 'reentrancyGuard' in code or 'nonReentrant' in code:
        analysis["patterns"].append("ReentrancyGuard 模式")

    return json.dumps(analysis, ensure_ascii=False, indent=2)


def optimize_gas(code: str) -> str:
    """
    提供 Gas 优化建议

    Args:
        code: Solidity 合约代码

    Returns:
        Gas 优化建议（JSON 格式）
    """
    suggestions = []

    # 1. 检查 public 变量
    if re.search(r'(uint256|address|bool)\s+public\s+\w+', code):
        suggestions.append({
            "type": "存储优化",
            "issue": "public 状态变量会自动生成 getter 函数",
            "suggestion": "如果不需要外部访问，使用 private 或 internal",
            "gas_saved": "~2000 gas per deployment"
        })

    # 2. 检查循环
    if 'for' in code and 'length' in code:
        suggestions.append({
            "type": "循环优化",
            "issue": "在循环中重复读取 array.length",
            "suggestion": "将 length 缓存到局部变量",
            "gas_saved": "~100 gas per iteration"
        })

    # 3. 检查 string 使用
    if re.search(r'string\s+(public|private|internal)?\s*\w+', code):
        suggestions.append({
            "type": "数据类型优化",
            "issue": "string 类型 Gas 消耗较高",
            "suggestion": "如果字符串长度固定，考虑使用 bytes32",
            "gas_saved": "~1000 gas per operation"
        })

    # 4. 检查 external vs public
    public_funcs = len(re.findall(r'function\s+\w+\s*\([^)]*\)\s+public', code))
    if public_funcs > 0:
        suggestions.append({
            "type": "函数可见性优化",
            "issue": f"发现 {public_funcs} 个 public 函数",
            "suggestion": "如果函数只从外部调用，使用 external 代替 public",
            "gas_saved": "~500 gas per call"
        })

    # 5. 检查 uint256 vs uint8
    if 'uint8' in code or 'uint16' in code:
        suggestions.append({
            "type": "数据类型优化",
            "issue": "使用小于 256 位的整数类型",
            "suggestion": "除非打包存储，否则使用 uint256 更省 Gas",
            "gas_saved": "~100 gas per operation"
        })

    result = {
        "total_suggestions": len(suggestions),
        "suggestions": suggestions,
        "estimated_total_savings": f"~{len(suggestions) * 500} gas"
    }

    return json.dumps(result, ensure_ascii=False, indent=2)


# ============================================
# 工具定义（用于 LLM Function Calling）
# ============================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "security_check",
            "description": "检查 Solidity 智能合约代码的安全问题，包括重入攻击、整数溢出、访问控制等常见漏洞",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要检查的 Solidity 合约代码"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_contract",
            "description": "生成智能合约代码。支持的类型：erc20（ERC20代币）、erc721（NFT）、multisig（多签钱包）、simple（简单合约）",
            "parameters": {
                "type": "object",
                "properties": {
                    "contract_type": {
                        "type": "string",
                        "description": "合约类型：erc20, erc721, multisig, simple"
                    },
                    "params": {
                        "type": "string",
                        "description": "合约参数（JSON格式），如 {\"name\": \"MyToken\", \"symbol\": \"MTK\"}"
                    }
                },
                "required": ["contract_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "explain_contract",
            "description": "分析并解释智能合约的功能、结构、设计模式等",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要分析的 Solidity 合约代码"
                    }
                },
                "required": ["code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "optimize_gas",
            "description": "分析智能合约代码并提供 Gas 优化建议",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "要优化的 Solidity 合约代码"
                    }
                },
                "required": ["code"]
            }
        }
    }
]


# 工具注册表
AVAILABLE_TOOLS = {
    "security_check": security_check,
    "generate_contract": generate_contract,
    "explain_contract": explain_contract,
    "optimize_gas": optimize_gas
}
