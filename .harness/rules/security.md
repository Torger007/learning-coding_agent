---
name: security-rules
description: L2 安全规范。定义沙箱参数、敏感信息处理、禁止事项。
version: "2.0"
---

# 安全规范

## 1. 沙箱执行（强制参数）

```yaml
# Docker Compose 安全配置
services:
  code-runner:
    image: python:3.12-slim
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    security_opt:
      - no-new-privileges:true
    read_only: true
    network_mode: none
    tmpfs:
      - /tmp:noexec,nosuid,size=100m
    stop_grace_period: 5s
```

- **执行超时**: 30 秒（硬限制）
- **CPU**: 最多 1 核
- **内存**: 最多 512MB
- **网络**: 默认完全隔离
- **文件系统**: 根目录只读，`/tmp` 临时可写

## 2. 危险代码检测（执行前扫描）

必须检测:
- 危险模块导入: `os`, `subprocess`, `sys`, `shutil`, `socket`, `urllib`, `pickle`, `ctypes`
- 危险函数: `eval`, `exec`, `compile`, `__import__`, `open`, `input`
- 危险模式: `rm -rf /`, `dd if=.*of=/dev/`, `mkfs`, `while True: pass`

实现位置: `backend/app/services/code_execution.py`（ DangerousCodeDetector 类）

## 3. 敏感信息

- **禁止硬编码**: API Key、密码、Token、数据库连接字符串
- **正确做法**: 环境变量 / 系统密钥管理 / 配置文件（`.env` 加入 `.gitignore`）
- **日志脱敏**: 任何日志中不得出现完整 API Key

## 4. 绝对禁止

- `eval()` 执行用户输入（沙箱内也不行，除非完全隔离）
- `os.system()` / `subprocess` 执行不受信任命令
- 生产环境开启调试模式
- 反序列化不受信任数据
