# WCB Agent API 集成工具

自动化与 Web3 Career Build 平台的交互，简化日常学习流程。

## 📋 功能

### 1. WCB Agent 客户端 (`wcb_agent.py`)

基础 API 客户端，支持所有 WCB Agent API 功能：

- **用户相关**：获取个人资料、权限
- **任务相关**：获取任务列表、任务历史、提交证明
- **活动相关**：获取活动列表、日历
- **机会相关**：浏览 Hackathon、项目机会

### 2. 每日学习助手 (`daily_helper.py`)

自动化日常学习流程：

- **早晨简报**：获取今日任务、活动、机会
- **提交证明**：一键提交学习成果（GitHub 链接 + 学习笔记）
- **任务历史**：查看已完成的任务

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 设置 API Key

已在 `~/.bash_profile` 中配置：

```bash
export WEB3_CAREER_API_KEY="your-secret-key"
```

重新加载配置：

```bash
source ~/.bash_profile
```

### 3. 测试连接

```bash
cd ~/ai-web3-school-cohort-0/tools
python wcb_agent.py profile
```

## 📖 使用指南

### 基础 API 调用

```bash
# 获取个人资料
python3 wcb_agent.py profile

# 获取权限
python3 wcb_agent.py permissions

# 获取任务列表
python3 wcb_agent.py tasks <program_id> [track_id]

# 获取任务历史
python3 wcb_agent.py history

# 获取活动列表
python3 wcb_agent.py events <program_id>

# 浏览机会
python3 wcb_agent.py opportunities

# 我的申请
python3 wcb_agent.py applications

# 获取 API 目录
python3 wcb_agent.py catalog
```

### 每日学习助手

#### 早晨简报

每天开始学习前，获取今日任务和活动：

```bash
python3 daily_helper.py briefing <program_id>
```

示例：
```bash
python3 daily_helper.py briefing cohort-0
```

输出：
```
============================================================
🌅 早安！今日学习简报
============================================================

📋 个人资料
------------------------------------------------------------
姓名: 张学涛
邮箱: your-email@example.com

📝 待完成任务
------------------------------------------------------------
⏳ 1. Day 4: Context 学习与实践
   描述: 完成 Context 章节阅读并提交学习笔记
   截止: 2026-05-21

📅 今日活动
------------------------------------------------------------
🎯 Office Hours
   时间: 2026-05-21T14:00:00.000Z
   地点: Zoom

🚀 最新机会
------------------------------------------------------------
💡 AI × Web3 Hackathon
   参与 AI × Web3 主题黑客松，赢取奖金...
============================================================
```

#### 提交学习成果

完成每日学习后，提交证明：

```bash
python3 daily_helper.py submit <task_id> <date>
```

示例：
```bash
python3 daily_helper.py submit task-123 2026-05-21
```

**重要**：提交前会显示待提交内容，需要你确认：

```
============================================================
📤 准备提交任务证明
============================================================

任务 ID: task-123
日期: 2026-05-21

证明内容:
------------------------------------------------------------
📚 学习笔记: https://github.com/XuetaoZhang/ai-web3-school-cohort-0/blob/main/daily/2026-05-21.md
✅ 打卡草稿: https://github.com/XuetaoZhang/ai-web3-school-cohort-0/blob/main/daily/checkin-draft-2026-05-21.md
📦 GitHub Repo: https://github.com/XuetaoZhang/ai-web3-school-cohort-0
------------------------------------------------------------

确认提交？(y/n):
```

输入 `y` 确认提交，输入 `n` 取消。

#### 查看任务历史

```bash
python3 daily_helper.py history
```

## 🔧 在 Python 代码中使用

```python
from wcb_agent import WCBAgent

# 初始化客户端
agent = WCBAgent()

# 获取个人资料
profile = agent.get_profile()
print(profile)

# 获取任务列表
tasks = agent.list_tasks(program_id="cohort-0")
print(tasks)

# 提交任务证明
result = agent.submit_task_evidence(
    task_id="task-123",
    proof="https://github.com/XuetaoZhang/ai-web3-school-cohort-0/blob/main/daily/2026-05-21.md"
)
print(result)
```

## 🔐 安全注意事项

1. **API Key 保护**
   - ✅ 存储在环境变量中
   - ✅ 不写入代码、README、聊天记录
   - ✅ 不提交到公开 repo

2. **写入操作确认**
   - 所有写入操作（提交任务、更新资料）都需要先展示内容并获得确认
   - `daily_helper.py` 已内置确认机制

3. **权限范围**
   - API Key 继承创建者的权限
   - 无法执行超出权限范围的操作

## 📚 API 文档

完整 API 文档：https://web3career.build/llms.txt

## 🛠️ 故障排查

### 问题：API Key 未设置

```bash
# 检查环境变量
echo $WEB3_CAREER_API_KEY

# 如果为空，重新加载配置
source ~/.bash_profile
```

### 问题：请求失败（UNAUTHORIZED）

- 检查 API Key 是否正确
- 检查 API Key 是否已被删除
- 检查是否有足够的权限

### 问题：网络连接失败

- 检查网络连接
- 检查是否需要代理

## 📝 示例工作流

### 每日学习流程

```bash
# 1. 早晨：获取今日简报
python3 daily_helper.py briefing cohort-0

# 2. 学习：完成今日任务
# ... 阅读 Handbook、动手实践、写学习笔记 ...

# 3. 提交：推送代码到 GitHub
cd ~/ai-web3-school-cohort-0
git add -A
git commit -m "Day 4 完成"
git push origin main

# 4. 提交证明到 WCB 平台
python3 daily_helper.py submit task-123 2026-05-21

# 5. 查看历史
python3 daily_helper.py history
```

## 🎯 下一步

- [ ] 添加自动生成打卡内容功能
- [ ] 集成到 GitHub Actions，自动提交
- [ ] 添加进度统计和可视化
- [ ] 支持批量提交多个任务
