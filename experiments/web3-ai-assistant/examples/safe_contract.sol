// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * 这是一个安全的合约示例
 * 展示了正确的安全实践
 */

contract SafeContract {
    mapping(address => uint256) public balances;
    address public owner;
    bool private locked;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier nonReentrant() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }

    constructor() {
        owner = msg.sender;
    }

    // ✅ 正确：有访问控制
    function transferOwnership(address newOwner) public onlyOwner {
        require(newOwner != address(0), "Invalid address");
        address previousOwner = owner;
        owner = newOwner;
        emit OwnershipTransferred(previousOwner, newOwner);
    }

    // ✅ 正确：防重入攻击
    function withdraw() public nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        // 先更新状态，再转账 - Checks-Effects-Interactions 模式
        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        emit Withdrawal(msg.sender, amount);
    }

    // ✅ 正确：使用 msg.sender 而不是 tx.origin
    function withdrawAll() public onlyOwner {
        uint256 balance = address(this).balance;
        (bool success, ) = payable(owner).call{value: balance}("");
        require(success, "Transfer failed");
    }

    // ✅ 正确：检查外部调用返回值
    function callExternal(address target, bytes memory data) public onlyOwner returns (bool) {
        (bool success, ) = target.call(data);
        require(success, "External call failed");
        return success;
    }

    // ✅ 正确：Solidity 0.8.0+ 自动检查溢出
    function deposit() public payable {
        require(msg.value > 0, "No value sent");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    // ✅ 正确：避免关键逻辑依赖时间戳
    function getBalance(address user) public view returns (uint256) {
        return balances[user];
    }

    receive() external payable {
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }
}
