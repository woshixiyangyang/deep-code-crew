# Meal Party Recruitment System

English | [中文](#中文版本)

## Overview

A comprehensive **Meal Party Recruitment System** built with Python. This system enables users to create dining events, recruit participants, manage menus, handle costs, and collaborate through real-time chat functionality. Data is automatically synchronized with Google Sheets for persistent storage.

## Features

- ✨ **Room Management**: Create and manage meal party events
- 👥 **Participant Recruitment**: Invite and manage attendees
- 🍽️ **Menu Management**: Add, update, and track menu items
- 💬 **Real-time Chat**: Communicate with other participants
- 💰 **Cost Calculation**: Automatic cost splitting and management
- 📋 **Room Duplication**: Clone existing rooms for similar events
- ☁️ **Google Sheets Integration**: Automatic data backup and synchronization
- 📊 **Data Persistence**: Save and load room data locally

## Prerequisites

Before setting up the project, ensure you have:

- Python 3.7 or higher
- Google Cloud account with Sheets API enabled
- Service Account Credential File from Google Cloud Console

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/woshixiyangyang/deep-code-crew.git
cd deep-code-crew
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Configuration

### Google Sheets Setup

To integrate Google Sheets functionality, prepare the following:

- **Google Sheet ID**: Your target Google Sheet ID
- **Service Account Credential File**: JSON file containing authentication credentials

Set the environment variables:

```bash
export GOOGLE_SHEET_ID="YOUR_SHEET_ID"
export GOOGLE_CREDENTIALS_PATH="path/to/service_account.json"
```

## Usage

To run the application:

```bash
python3 main.py
```

The application will start and guide you through the menu options.

---

## Testing & Verification

### Test Users

The system was tested with the following participants:

- YING LAN
- 신동해 (Shin Dong-hae)
- WEN NUORAN
- 김연세 (Kim Yeon-se)

### Tested Features

- ✅ Room creation and management
- ✅ Participant recruitment and management
- ✅ Menu item management and editing
- ✅ Real-time chat messaging
- ✅ Recruitment completion workflow
- ✅ Automatic cost calculation and splitting
- ✅ Room duplication functionality
- ✅ Google Sheets data persistence (save/load)

---

## Security & Privacy

⚠️ **Important Note**: For security purposes, the following private files are **not** included in the repository:

- `service_account.json` - Google Cloud service account credentials
- `credentials.json` - OAuth credentials
- `local_storage.json` - Local user data

**Users must provide their own** credentials and configuration files. Never commit sensitive files to version control.

## Project Structure

```
deep-code-crew/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── [source files]      # Core application modules
```

## Contributing

This is a team project for Information Programming Deepening. Contributions and improvements are welcome!

## License

[Add your license information here]

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

## 中文版本

# 聚餐招募系统

## 项目简介

一个基于 Python 开发的综合**聚餐招募系统**。该系统允许用户创建聚餐活动、招募参与者、管理菜单、处理费用，并通过实时聊天功能进行协作。数据会自动与 Google Sheets 同步以实现持久化存储。

## 主要功能

- ✨ **房间管理**：创建并管理聚餐活动
- 👥 **参与者招募**：邀请和管理参与者
- 🍽️ **菜单管理**：添加、更新和跟踪菜单项
- 💬 **实时聊天**：与其他参与者进行交流
- 💰 **费用计算**：自动计算和分割费用
- 📋 **房间复制**：复制现有房间创建类似活动
- ☁️ **Google Sheets 集成**：自动数据备份和同步
- 📊 **数据持久化**：本地保存和加载房间数据

## 系统要求

- Python 3.7 或更高版本
- Google Cloud 账户（已启用 Sheets API）
- Google Cloud 服务账户凭证文件

## 安装步骤

1. **克隆仓库**：
```bash
git clone https://github.com/woshixiyangyang/deep-code-crew.git
cd deep-code-crew
```

2. **安装依赖**：
```bash
pip install -r requirements.txt
```

## 配置说明

### Google Sheets 配置

配置 Google Sheets 功能需要准备以下内容：

- **Google Sheet ID**：目标 Google Sheet 的 ID
- **Service Account 凭证文件**：包含身份验证凭证的 JSON 文件

设置环境变量：

```bash
export GOOGLE_SHEET_ID="YOUR_SHEET_ID"
export GOOGLE_CREDENTIALS_PATH="path/to/service_account.json"
```

## 使用方法

运行应用程序：

```bash
python3 main.py
```

应用程序将启动并引导您浏览菜单选项。

---

## 测试验证

### 测试用户

系统已由以下参与者进行测试：

- YING LAN
- 신동해
- WEN NUORAN
- 김연세

### 已验证的功能

- ✅ 房间创建和管理
- ✅ 参与者招募和管理
- ✅ 菜单项管理和编辑
- ✅ 实时聊天消息
- ✅ 招募完成工作流
- ✅ 自动费用计算和分割
- ✅ 房间复制功能
- ✅ Google Sheets 数据持久化（保存/加载）

---

## 安全与隐私

⚠️ **重要提示**：出于安全考虑，以下私密文件**不**包含在仓库中：

- `service_account.json` - Google Cloud 服务账户凭证
- `credentials.json` - OAuth 凭证
- `local_storage.json` - 本地用户数据

**用户必须提供自己的**凭证和配置文件。请勿将敏感文件提交到版本控制系统。

## 项目结构

```
deep-code-crew/
├── main.py              # 应用程序入口
├── requirements.txt     # Python 依赖项
├── README.md           # 本文件
└── [源代码文件]         # 核心应用模块
```

## 贡献

这是一个信息编程深化的团队项目。欢迎提出改进建议和贡献！

## 许可证

[添加您的许可证信息]

## 支持

如有问题或建议，请在仓库中提出 Issue。
