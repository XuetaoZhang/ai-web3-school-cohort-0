# 权限升级方案：从只读到写入

本文档描述如何安全地为 MCP 服务器添加写入工具，包括权限管理、用户确认、授权撤销和审计机制。

## 设计原则

1. **最小权限原则**: 默认只读，写入需要明确授权
2. **显式确认**: 危险操作需要用户确认
3. **可撤销性**: 所有授权都可以撤销
4. **完整审计**: 所有写入操作都有审计日志
5. **细粒度控制**: 不同操作有不同的权限级别

## 权限级别

### Level 0: 只读（当前实现）
- `search_docs(query)` - 搜索文档
- `get_file(path)` - 读取文件

### Level 1: 安全写入
需要用户一次性确认，低风险操作：
- `create_file(path, content)` - 创建新文件
- `append_to_file(path, content)` - 追加内容到文件末尾

### Level 2: 修改操作
需要每次确认，中等风险：
- `update_file(path, content)` - 覆盖文件内容
- `rename_file(old_path, new_path)` - 重命名文件

### Level 3: 危险操作
需要每次确认 + 二次确认，高风险：
- `delete_file(path)` - 删除文件
- `delete_directory(path)` - 删除目录

## 实现方案

### 1. 权限配置文件

创建 `src/permissions.py`:

```python
from enum import Enum
from pathlib import Path
from typing import Dict, Set
import json

class PermissionLevel(Enum):
    READ_ONLY = 0
    SAFE_WRITE = 1
    MODIFY = 2
    DANGEROUS = 3

class PermissionManager:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.permissions: Dict[str, PermissionLevel] = {}
        self.granted_operations: Set[str] = set()
        self.load_permissions()
    
    def load_permissions(self):
        """从配置文件加载权限设置"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                data = json.load(f)
                self.granted_operations = set(data.get("granted_operations", []))
    
    def save_permissions(self):
        """保存权限设置到配置文件"""
        with open(self.config_file, 'w') as f:
            json.dump({
                "granted_operations": list(self.granted_operations)
            }, f, indent=2)
    
    def request_permission(self, operation: str, level: PermissionLevel, 
                          details: Dict) -> bool:
        """请求执行操作的权限"""
        # Level 0 (只读) 总是允许
        if level == PermissionLevel.READ_ONLY:
            return True
        
        # Level 1 (安全写入) 一次性授权
        if level == PermissionLevel.SAFE_WRITE:
            if operation in self.granted_operations:
                return True
            return self._prompt_user_once(operation, details)
        
        # Level 2 (修改) 每次确认
        if level == PermissionLevel.MODIFY:
            return self._prompt_user_each_time(operation, details)
        
        # Level 3 (危险) 每次确认 + 二次确认
        if level == PermissionLevel.DANGEROUS:
            return self._prompt_user_dangerous(operation, details)
        
        return False
    
    def _prompt_user_once(self, operation: str, details: Dict) -> bool:
        """一次性授权提示"""
        print(f"\n⚠️  Permission Request: {operation}")
        print(f"Details: {json.dumps(details, indent=2)}")
        print("This operation will be allowed for the rest of the session.")
        response = input("Allow this operation? (yes/no): ").lower()
        
        if response == 'yes':
            self.granted_operations.add(operation)
            self.save_permissions()
            return True
        return False
    
    def _prompt_user_each_time(self, operation: str, details: Dict) -> bool:
        """每次确认提示"""
        print(f"\n⚠️  Confirmation Required: {operation}")
        print(f"Details: {json.dumps(details, indent=2)}")
        response = input("Proceed with this operation? (yes/no): ").lower()
        return response == 'yes'
    
    def _prompt_user_dangerous(self, operation: str, details: Dict) -> bool:
        """危险操作二次确认"""
        print(f"\n🚨 DANGEROUS OPERATION: {operation}")
        print(f"Details: {json.dumps(details, indent=2)}")
        print("This operation cannot be undone!")
        
        response1 = input("Are you sure? (yes/no): ").lower()
        if response1 != 'yes':
            return False
        
        response2 = input("Type the operation name to confirm: ")
        return response2 == operation
    
    def revoke_permission(self, operation: str):
        """撤销操作权限"""
        if operation in self.granted_operations:
            self.granted_operations.remove(operation)
            self.save_permissions()
            return True
        return False
    
    def revoke_all(self):
        """撤销所有权限"""
        self.granted_operations.clear()
        self.save_permissions()
```

### 2. 写入工具实现

在 `src/write_tools.py` 中实现写入工具：

```python
from pathlib import Path
from typing import Dict
from .config import is_path_allowed
from .logger import logger, log_tool_call
from .permissions import PermissionLevel, PermissionManager

permission_manager = PermissionManager(Path("config/permissions.json"))

async def create_file(path: str, content: str) -> str:
    """创建新文件"""
    file_path = Path(path)
    
    # 安全检查
    if not is_path_allowed(file_path):
        raise PermissionError(f"Path not allowed: {path}")
    
    if file_path.exists():
        raise FileExistsError(f"File already exists: {path}")
    
    # 请求权限
    if not permission_manager.request_permission(
        "create_file",
        PermissionLevel.SAFE_WRITE,
        {"path": path, "size": len(content)}
    ):
        raise PermissionError("Operation denied by user")
    
    # 执行操作
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    
    logger.info(f"Created file: {path}")
    return f"✓ File created: {path}\n📏 Size: {len(content)} characters"

async def update_file(path: str, content: str) -> str:
    """更新文件内容"""
    file_path = Path(path)
    
    # 安全检查
    if not is_path_allowed(file_path):
        raise PermissionError(f"Path not allowed: {path}")
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # 读取旧内容用于备份
    old_content = file_path.read_text(encoding='utf-8')
    
    # 请求权限
    if not permission_manager.request_permission(
        "update_file",
        PermissionLevel.MODIFY,
        {
            "path": path,
            "old_size": len(old_content),
            "new_size": len(content)
        }
    ):
        raise PermissionError("Operation denied by user")
    
    # 创建备份
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    backup_path.write_text(old_content, encoding='utf-8')
    
    # 执行操作
    file_path.write_text(content, encoding='utf-8')
    
    logger.info(f"Updated file: {path} (backup: {backup_path})")
    return f"✓ File updated: {path}\n💾 Backup: {backup_path}"

async def delete_file(path: str) -> str:
    """删除文件"""
    file_path = Path(path)
    
    # 安全检查
    if not is_path_allowed(file_path):
        raise PermissionError(f"Path not allowed: {path}")
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    # 请求权限（危险操作）
    if not permission_manager.request_permission(
        "delete_file",
        PermissionLevel.DANGEROUS,
        {"path": path, "size": file_path.stat().st_size}
    ):
        raise PermissionError("Operation denied by user")
    
    # 执行操作
    file_path.unlink()
    
    logger.warning(f"Deleted file: {path}")
    return f"✓ File deleted: {path}"
```

### 3. 审计日志增强

在 `src/audit.py` 中实现详细的审计日志：

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

class AuditLogger:
    def __init__(self, audit_file: Path):
        self.audit_file = audit_file
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_operation(self, operation: str, details: Dict[str, Any], 
                     success: bool, error: str = None):
        """记录操作到审计日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "success": success,
            "error": error
        }
        
        with open(self.audit_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_recent_operations(self, limit: int = 100) -> list:
        """获取最近的操作记录"""
        if not self.audit_file.exists():
            return []
        
        with open(self.audit_file) as f:
            lines = f.readlines()
            return [json.loads(line) for line in lines[-limit:]]
    
    def get_operations_by_type(self, operation: str) -> list:
        """获取特定类型的操作记录"""
        if not self.audit_file.exists():
            return []
        
        with open(self.audit_file) as f:
            return [
                json.loads(line) for line in f
                if json.loads(line)["operation"] == operation
            ]
```

### 4. 管理命令

创建 `src/manage.py` 用于权限管理：

```python
import argparse
from pathlib import Path
from .permissions import PermissionManager
from .audit import AuditLogger

def main():
    parser = argparse.ArgumentParser(description="Manage MCP server permissions")
    subparsers = parser.add_subparsers(dest='command')
    
    # 列出权限
    subparsers.add_parser('list', help='List granted permissions')
    
    # 撤销权限
    revoke_parser = subparsers.add_parser('revoke', help='Revoke a permission')
    revoke_parser.add_argument('operation', help='Operation to revoke')
    
    # 撤销所有权限
    subparsers.add_parser('revoke-all', help='Revoke all permissions')
    
    # 查看审计日志
    audit_parser = subparsers.add_parser('audit', help='View audit log')
    audit_parser.add_argument('--limit', type=int, default=20, 
                            help='Number of recent entries to show')
    audit_parser.add_argument('--operation', help='Filter by operation type')
    
    args = parser.parse_args()
    
    pm = PermissionManager(Path("config/permissions.json"))
    audit = AuditLogger(Path("logs/audit.log"))
    
    if args.command == 'list':
        print("Granted permissions:")
        for op in pm.granted_operations:
            print(f"  - {op}")
    
    elif args.command == 'revoke':
        if pm.revoke_permission(args.operation):
            print(f"✓ Revoked permission: {args.operation}")
        else:
            print(f"✗ Permission not found: {args.operation}")
    
    elif args.command == 'revoke-all':
        pm.revoke_all()
        print("✓ All permissions revoked")
    
    elif args.command == 'audit':
        if args.operation:
            entries = audit.get_operations_by_type(args.operation)
        else:
            entries = audit.get_recent_operations(args.limit)
        
        for entry in entries:
            status = "✓" if entry["success"] else "✗"
            print(f"{status} {entry['timestamp']} - {entry['operation']}")
            print(f"   Details: {entry['details']}")
            if entry.get('error'):
                print(f"   Error: {entry['error']}")

if __name__ == '__main__':
    main()
```

## 使用示例

### 授权写入操作

```bash
# 首次使用 create_file 时会提示
python -m src.server

# 在客户端调用
result = await session.call_tool("create_file", {
    "path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/test.md",
    "content": "# Test\nThis is a test file."
})

# 提示：
# ⚠️  Permission Request: create_file
# Details: {
#   "path": "/Users/zhangxuetao/ai-web3-school-cohort-0/daily/test.md",
#   "size": 30
# }
# This operation will be allowed for the rest of the session.
# Allow this operation? (yes/no): yes
```

### 撤销权限

```bash
# 列出所有授权
python -m src.manage list

# 撤销特定权限
python -m src.manage revoke create_file

# 撤销所有权限
python -m src.manage revoke-all
```

### 查看审计日志

```bash
# 查看最近 20 条操作
python -m src.manage audit

# 查看所有删除操作
python -m src.manage audit --operation delete_file

# 查看最近 100 条操作
python -m src.manage audit --limit 100
```

## 安全检查清单

在添加写入工具前，确保：

- [ ] 所有路径都经过白名单验证
- [ ] 危险操作需要二次确认
- [ ] 所有操作都有审计日志
- [ ] 权限可以随时撤销
- [ ] 修改操作会创建备份
- [ ] 错误消息不泄露敏感信息
- [ ] 用户确认提示清晰明确
- [ ] 配置文件权限正确（600）

## 最佳实践

1. **渐进式授权**: 从只读开始，根据需要逐步添加写入权限
2. **最小化范围**: 只授权必要的操作，不要一次性授权所有写入
3. **定期审计**: 定期检查审计日志，发现异常操作
4. **备份策略**: 修改操作前自动创建备份
5. **权限过期**: 考虑添加权限过期机制（如 24 小时后自动撤销）

## 未来改进

1. **基于角色的访问控制 (RBAC)**: 不同用户有不同的权限级别
2. **操作限流**: 限制单位时间内的写入操作次数
3. **文件版本控制**: 集成 Git 自动提交修改
4. **远程审计**: 将审计日志发送到远程服务器
5. **权限模板**: 预定义的权限配置模板（开发/生产环境）
