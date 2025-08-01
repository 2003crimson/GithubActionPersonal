#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewWorld Cloud 自动签到脚本
支持GitHub Actions自动化执行
"""

import requests
import json
import os
import sys
from datetime import datetime
import time

class NewWorldCheckin:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://neworld.cloud"
        
        # 设置通用请求头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        })
    
    def login(self):
        """用户登录"""
        login_url = f"{self.base_url}/auth/login"
        
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Referer": login_url,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        
        payload = {
            "code": "",
            "email": self.email,
            "passwd": self.password
        }
        
        try:
            response = self.session.post(login_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ret') == 1:
                print(f"[{datetime.now()}] 登录成功")
                return True
            else:
                print(f"[{datetime.now()}] 登录失败: {result.get('msg', '未知错误')}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] 登录请求失败: {str(e)}")
            return False
        except json.JSONDecodeError:
            print(f"[{datetime.now()}] 登录响应解析失败")
            return False
    
    def checkin(self):
        """执行签到"""
        checkin_url = f"{self.base_url}/user/checkin"
        
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        }
        
        try:
            response = self.session.post(checkin_url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ret') == 1:
                msg = result.get('msg', '签到成功')
                print(f"[{datetime.now()}] 签到成功: {msg}")
                return True
            else:
                msg = result.get('msg', '签到失败')
                print(f"[{datetime.now()}] 签到失败: {msg}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] 签到请求失败: {str(e)}")
            return False
        except json.JSONDecodeError:
            print(f"[{datetime.now()}] 签到响应解析失败")
            return False
    
    def run(self):
        """执行完整的签到流程"""
        print(f"[{datetime.now()}] 开始执行自动签到")
        
        # 登录
        if not self.login():
            print(f"[{datetime.now()}] 自动签到失败: 登录失败")
            return False
        
        # 等待一秒避免请求过快
        time.sleep(1)
        
        # 签到
        if self.checkin():
            print(f"[{datetime.now()}] 自动签到完成")
            return True
        else:
            print(f"[{datetime.now()}] 自动签到失败")
            return False

def main():
    """主函数"""
    # 从环境变量获取账号信息
    email = os.getenv('NEWORLD_EMAIL')
    password = os.getenv('NEWORLD_PASSWORD')
    
    if not email or not password:
        print("错误: 请设置环境变量 NEWORLD_EMAIL 和 NEWORLD_PASSWORD")
        sys.exit(1)
    
    # 执行签到
    checker = NewWorldCheckin(email, password)
    success = checker.run()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
