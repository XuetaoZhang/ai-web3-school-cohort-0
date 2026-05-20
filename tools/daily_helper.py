#!/usr/bin/env python3
"""
每日学习助手
自动化日常学习流程：获取任务、提交证明、查看活动
"""

import os
import sys
from datetime import datetime, timedelta
from wcb_agent import WCBAgent

class DailyHelper:
    """每日学习助手"""

    def __init__(self):
        self.agent = WCBAgent()
        self.repo_url = "https://github.com/XuetaoZhang/ai-web3-school-cohort-0"

    def morning_briefing(self, program_id: str):
        """
        早晨简报：获取今日任务和活动

        Args:
            program_id: 项目 ID
        """
        print("=" * 60)
        print("🌅 早安！今日学习简报")
        print("=" * 60)
        print()

        # 1. 获取个人资料
        print("📋 个人资料")
        print("-" * 60)
        profile_result = self.agent.get_profile()
        if profile_result.get("ok"):
            profile = profile_result.get("result", {})
            print(f"姓名: {profile.get('name', 'N/A')}")
            print(f"邮箱: {profile.get('email', 'N/A')}")
        else:
            print(f"❌ 获取失败: {profile_result.get('error', {}).get('message')}")
        print()

        # 2. 获取任务列表
        print("📝 待完成任务")
        print("-" * 60)
        tasks_result = self.agent.list_tasks(program_id)
        if tasks_result.get("ok"):
            tasks = tasks_result.get("result", [])
            if tasks:
                for i, task in enumerate(tasks, 1):
                    status = "✅" if task.get("completed") else "⏳"
                    print(f"{status} {i}. {task.get('title', 'N/A')}")
                    if task.get("description"):
                        print(f"   描述: {task.get('description')}")
                    if task.get("deadline"):
                        print(f"   截止: {task.get('deadline')}")
                    print()
            else:
                print("暂无任务")
        else:
            print(f"❌ 获取失败: {tasks_result.get('error', {}).get('message')}")
        print()

        # 3. 获取今日活动
        print("📅 今日活动")
        print("-" * 60)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        events_result = self.agent.list_events(
            program_id,
            today.isoformat(),
            tomorrow.isoformat()
        )
        if events_result.get("ok"):
            events = events_result.get("result", [])
            if events:
                for event in events:
                    print(f"🎯 {event.get('title', 'N/A')}")
                    print(f"   时间: {event.get('startTime', 'N/A')}")
                    if event.get('location'):
                        print(f"   地点: {event.get('location')}")
                    print()
            else:
                print("今日无活动")
        else:
            print(f"❌ 获取失败: {events_result.get('error', {}).get('message')}")
        print()

        # 4. 获取机会
        print("🚀 最新机会")
        print("-" * 60)
        opportunities_result = self.agent.list_opportunities()
        if opportunities_result.get("ok"):
            opportunities = opportunities_result.get("result", [])
            if opportunities:
                for opp in opportunities[:3]:  # 只显示前 3 个
                    print(f"💡 {opp.get('title', 'N/A')}")
                    if opp.get('description'):
                        print(f"   {opp.get('description')[:100]}...")
                    print()
            else:
                print("暂无新机会")
        else:
            print(f"❌ 获取失败: {opportunities_result.get('error', {}).get('message')}")

        print("=" * 60)

    def submit_daily_work(self, task_id: str, date: str):
        """
        提交每日学习成果

        Args:
            task_id: 任务 ID
            date: 日期（YYYY-MM-DD）

        Returns:
            提交结果预览（需要用户确认）
        """
        # 构建证明链接
        daily_note_url = f"{self.repo_url}/blob/main/daily/{date}.md"
        checkin_draft_url = f"{self.repo_url}/blob/main/daily/checkin-draft-{date}.md"

        proof_text = f"""
📚 学习笔记: {daily_note_url}
✅ 打卡草稿: {checkin_draft_url}
📦 GitHub Repo: {self.repo_url}
        """.strip()

        print("=" * 60)
        print("📤 准备提交任务证明")
        print("=" * 60)
        print()
        print(f"任务 ID: {task_id}")
        print(f"日期: {date}")
        print()
        print("证明内容:")
        print("-" * 60)
        print(proof_text)
        print("-" * 60)
        print()

        # 返回待提交的数据，等待用户确认
        return {
            "task_id": task_id,
            "proof": proof_text
        }

    def confirm_and_submit(self, submission_data: dict):
        """
        确认并提交

        Args:
            submission_data: 提交数据
        """
        result = self.agent.submit_task_evidence(
            submission_data["task_id"],
            submission_data["proof"]
        )

        if result.get("ok"):
            print("✅ 提交成功！")
            return True
        else:
            error = result.get("error", {})
            print(f"❌ 提交失败: {error.get('message', 'Unknown error')}")
            return False

    def check_task_history(self):
        """查看任务历史"""
        print("=" * 60)
        print("📊 任务历史")
        print("=" * 60)
        print()

        result = self.agent.get_task_history()
        if result.get("ok"):
            history = result.get("result", [])
            if history:
                for item in history:
                    status = "✅" if item.get("completed") else "⏳"
                    print(f"{status} {item.get('taskTitle', 'N/A')}")
                    print(f"   提交时间: {item.get('submittedAt', 'N/A')}")
                    if item.get('proof'):
                        print(f"   证明: {item.get('proof')[:80]}...")
                    print()
            else:
                print("暂无历史记录")
        else:
            print(f"❌ 获取失败: {result.get('error', {}).get('message')}")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python daily_helper.py briefing <program_id>")
        print("    # 获取今日简报")
        print()
        print("  python daily_helper.py submit <task_id> <date>")
        print("    # 提交每日学习成果（需要确认）")
        print()
        print("  python daily_helper.py history")
        print("    # 查看任务历史")
        print()
        print("示例:")
        print("  python daily_helper.py briefing cohort-0")
        print("  python daily_helper.py submit task-123 2026-05-21")
        sys.exit(1)

    helper = DailyHelper()
    command = sys.argv[1]

    if command == "briefing":
        if len(sys.argv) < 3:
            print("错误: 需要提供 program_id")
            sys.exit(1)
        program_id = sys.argv[2]
        helper.morning_briefing(program_id)

    elif command == "submit":
        if len(sys.argv) < 4:
            print("错误: 需要提供 task_id 和 date")
            sys.exit(1)
        task_id = sys.argv[2]
        date = sys.argv[3]

        # 显示待提交内容
        submission_data = helper.submit_daily_work(task_id, date)

        # 等待用户确认
        confirm = input("\n确认提交？(y/n): ").strip().lower()
        if confirm == 'y':
            helper.confirm_and_submit(submission_data)
        else:
            print("❌ 已取消提交")

    elif command == "history":
        helper.check_task_history()

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
