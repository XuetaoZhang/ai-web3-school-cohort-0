// SPDX-License-Identifier: MIT
pragma solidity ^0.7.0;

/**
 * 这是一个有安全漏洞的合约示例
 * 用于演示常见的智能合约安全问题
 */

contract VulnerableContract {
    mapping(address => uint256) public balances;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // 漏洞 1: 缺少访问控制
    function setOwner(address newOwner) public {
        owner = newOwner;
    }

    // 漏洞 2: 重入攻击
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // 先转账，后更新状态 - 重入攻击风险！
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balances[msg.sender] = 0;
    }

    // 漏洞 3: tx.origin 使用
    function withdrawAll() public {
        require(tx.origin == owner, "Not owner");
        payable(owner).transfer(address(this).balance);
    }

    // 漏洞 4: 未检查的外部调用
    function callExternal(address target, bytes memory data) public {
        target.call(data);  // 返回值未检查
    }

    // 漏洞 5: 整数溢出（Solidity < 0.8.0）
    function deposit() public payable {
        balances[msg.sender] += msg.value;  // 可能溢出
    }

    // 漏洞 6: 时间戳依赖
    function isLucky() public view returns (bool) {
        return block.timestamp % 2 == 0;
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}
