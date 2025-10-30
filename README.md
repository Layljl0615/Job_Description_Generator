# Django ChatGPT Project

一个基于 Django 和 OpenAI API 的智能聊天应用，支持用户认证和对话历史管理。

## 功能特性

- 🤖 **AI 对话**：集成 OpenAI GPT-3.5-turbo 模型，实现智能对话
- 👤 **用户认证**：完整的用户注册、登录、登出功能
- 📝 **对话历史**：保存和查看个人对话记录
- 🔒 **隐私保护**：每个用户只能查看自己的对话历史
- 🗑️ **记录管理**：支持删除历史对话记录

## 技术栈

- **后端框架**：Django 4.2.25
- **数据库**：SQLite3
- **AI 服务**：OpenAI API (gpt-3.5-turbo)
- **前端**：Bootstrap 5 + Django Templates
- **Python 版本**：Python 3.9+

## 环境要求

- Python 3.9 或更高版本
- pip (Python 包管理器)
- OpenAI API Key

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/Layljl0615/Job_Description_Generator.git
cd Job_Description_Generator
```

### 2. 创建虚拟环境

```bash
python3.9 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install django==4.2.25
pip install openai==2.6.1
pip install python-dotenv
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ **重要**：请将 `your_openai_api_key_here` 替换为您的真实 OpenAI API 密钥。

### 5. 数据库迁移

```bash
python manage.py migrate
```

### 6. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器

```bash
python manage.py runserver
```

服务器启动后，访问 http://127.0.0.1:8000/

## 使用说明

### 注册账号

1. 访问首页，点击导航栏的 "Register" 按钮
2. 填写用户名、邮箱和密码
3. 注册成功后会自动登录

### 开始对话

1. 登录后在首页的输入框中输入问题
2. 点击 "Submit" 按钮
3. AI 会生成回复并显示在页面上

### 查看历史记录

1. 点击导航栏的 "Past Questions" 按钮
2. 查看所有历史对话
3. 可以点击 "Delete" 删除不需要的记录

## 项目结构

```
Django_ChatGPT/
├── chatbot/                 # 主应用
│   ├── migrations/         # 数据库迁移文件
│   ├── templates/          # HTML 模板
│   │   ├── base.html      # 基础模板
│   │   ├── home.html      # 主页
│   │   ├── login.html     # 登录页
│   │   ├── register.html  # 注册页
│   │   ├── past.html      # 历史记录页
│   │   └── navbar.html    # 导航栏
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   └── urls.py            # URL 路由
├── chatgpt/                # 项目配置
│   ├── settings.py        # Django 设置
│   └── urls.py            # 主 URL 配置
├── manage.py              # Django 管理脚本
├── .env                   # 环境变量（不包含在 git 中）
├── .gitignore            # Git 忽略文件
└── README.md             # 项目说明文档
```

## 数据模型

### Past 模型

存储用户的对话历史：

- `user`: 外键关联到 Django User 模型
- `prompt`: 用户的问题
- `response`: AI 的回复
- `created_at`: 创建时间戳

## 安全注意事项

- ✅ API 密钥通过环境变量管理，不会提交到 Git
- ✅ 数据库文件 `db.sqlite3` 已添加到 `.gitignore`
- ✅ 用户密码使用 Django 内置的安全加密
- ✅ 所有对话功能都需要登录才能访问

## 开发注意事项

### 更新 views.py 以使用环境变量

确保 `chatbot/views.py` 中的 OpenAI 客户端从环境变量读取 API 密钥：

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
```

### 依赖管理

如果添加了新的依赖，建议创建 `requirements.txt`：

```bash
pip freeze > requirements.txt
```

其他开发者可以通过以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

## 故障排除

### 问题 1：OpenAI API 错误

确保：
- `.env` 文件存在且包含有效的 API 密钥
- API 密钥有足够的额度
- 网络连接正常

### 问题 2：数据库错误

运行迁移命令：
```bash
python manage.py migrate
```

### 问题 3：静态文件无法加载

运行以下命令收集静态文件：
```bash
python manage.py collectstatic
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目仅供学习和研究使用。

## 联系方式

- GitHub: [@Layljl0615](https://github.com/Layljl0615)
- 项目仓库: [Job_Description_Generator](https://github.com/Layljl0615/Job_Description_Generator)

---

⭐ 如果这个项目对您有帮助，欢迎给个 Star！
