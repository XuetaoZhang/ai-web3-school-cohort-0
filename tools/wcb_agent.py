#!/usr/bin/env python3
"""
WCB Agent API 集成工具
用于与 Web3 Career Build 平台交互
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime

class WCBAgent:
    """Web3 Career Build Agent API 客户端"""

    def __init__(self):
        self.base_url = "https://web3career.build"
        self.api_key = os.environ.get("WEB3_CAREER_API_KEY")

        if not self.api_key:
            raise ValueError("WEB3_CAREER_API_KEY 环境变量未设置")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def call(self, procedure: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        调用 WCB Agent API

        Args:
            procedure: tRPC 过程名称，如 "users.getProfile"
            input_data: 输入参数（可选）

        Returns:
            API 响应结果
        """
        url = f"{self.base_url}/api/agent/call"
        payload = {
            "procedure": procedure,
            "input": input_data or {}
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "ok": False,
                "error": {
                    "code": "REQUEST_FAILED",
                    "message": str(e)
                }
            }

    def get_catalog(self) -> Dict[str, Any]:
        """获取 API 目录（可用的过程列表）"""
        url = f"{self.base_url}/api/agent/catalog"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "ok": False,
                "error": str(e)
            }

    # ========== 用户相关 ==========

    def get_profile(self) -> Dict[str, Any]:
        """获取个人资料"""
        return self.call("users.getProfile")

    def get_permissions(self) -> Dict[str, Any]:
        """获取我的权限"""
        return self.call("users.getMyPermissions")

    # ========== 任务相关 ==========

    def list_tasks(self, program_id: str, track_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取任务列表

        Args:
            program_id: 项目 ID
            track_id: 赛道 ID（可选）
        """
        input_data = {"programId": program_id}
        if track_id:
            input_data["trackId"] = track_id

        return self.call("tasks.listForLearner", input_data)

    def get_task_history(self) -> Dict[str, Any]:
        """获取任务历史"""
        return self.call("tasks.myTaskHistory")

    def submit_task_evidence(self, task_id: str, proof: str) -> Dict[str, Any]:
        """
        提交任务证明

        Args:
            task_id: 任务 ID
            proof: 证明链接（如 GitHub 链接）

        Returns:
            提交结果
        """
        return self.call("tasks.submitEvidence", {
            "taskId": task_id,
            "proof": proof
        })

    # ========== 活动相关 ==========

    def list_events(self, program_id: str, range_start: Optional[str] = None,
                   range_end: Optional[str] = None) -> Dict[str, Any]:
        """
        获取活动列表

        Args:
            program_id: 项目 ID
            range_start: 开始时间（ISO 8601 格式）
            range_end: 结束时间（ISO 8601 格式）
        """
        input_data = {"programId": program_id}
        if range_start:
            input_data["rangeStart"] = range_start
        if range_end:
            input_data["rangeEnd"] = range_end

        return self.call("events.listForLearner", input_data)

    def get_calendar(self) -> Dict[str, Any]:
        """获取公开日历"""
        return self.call("events.getCalendarPublic")

    # ========== 机会相关 ==========

    def list_opportunities(self) -> Dict[str, Any]:
        """浏览机会（Hackathon、项目等）"""
        return self.call("opportunities.list")

    def get_opportunity(self, opportunity_id: str) -> Dict[str, Any]:
        """获取机会详情"""
        return self.call("opportunities.getById", {"id": opportunity_id})

    def my_applications(self) -> Dict[str, Any]:
        """获取我的申请"""
        return self.call("opportunities.myApplications")


def main():
    """命令行工具入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python wcb_agent.py profile          # 获取个人资料")
        print("  python wcb_agent.py permissions      # 获取权限")
        print("  python wcb_agent.py tasks <program_id> [track_id]  # 获取任务列表")
        print("  python wcb_agent.py history          # 获取任务历史")
        print("  python wcb_agent.py events <program_id>  # 获取活动列表")
        print("  python wcb_agent.py opportunities    # 浏览机会")
        print("  python wcb_agent.py applications     # 我的申请")
        print("  python wcb_agent.py catalog          # 获取 API 目录")
        sys.exit(1)

    agent = WCBAgent()
    command = sys.argv[1]

    result = None

    if command == "profile":
        result = agent.get_profile()
    elif command == "permissions":
        result = agent.get_permissions()
    elif command == "tasks":
        if len(sys.argv) < 3:
            print("错误: 需要提供 program_id")
            sys.exit(1)
        program_id = sys.argv[2]
        track_id = sys.argv[3] if len(sys.argv) > 3 else None
        result = agent.list_tasks(program_id, track_id)
    elif command == "history":
        result = agent.get_task_history()
    elif command == "events":
        if len(sys.argv) < 3:
            print("错误: 需要提供 program_id")
            sys.exit(1)
        program_id = sys.argv[2]
        result = agent.list_events(program_id)
    elif command == "opportunities":
        result = agent.list_opportunities()
    elif command == "applications":
        result = agent.my_applications()
    elif command == "catalog":
        result = agent.get_catalog()
    else:
        print(f"未知命令: {command}")
        sys.exit(1)

    # 格式化输出
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
