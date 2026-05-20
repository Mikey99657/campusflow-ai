# CampusFlow AI

校园 AI Agent 工作流平台 - 基于 Multi-Agent 的校园学习辅助系统

## 功能特性

- **多 Agent 调度**: Supervisor 模式自动路由任务到专业 Agent
- **代码生成**: Java 代码生成、分析、调试
- **实验报告**: 自动生成实验报告和学习总结
- **UML 分析**: UML 图生成和分析
- **长上下文管理**: 滑动窗口 + 自动摘要
- **可插拔模型**: 支持 MiMo / OpenAI / DeepSeek

## 技术栈

- **后端**: Python 3.12 + FastAPI + LangGraph + LangChain
- **前端**: React + Next.js + TailwindCSS
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **AI 模型**: MiMo API (兼容 OpenAI 格式)

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/campusflow-ai.git
cd campusflow-ai
```

### 2. 后端设置

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -e .

# 配置环境变量
copy ..\.env.example ..\.env
# 编辑 .env 文件，填入你的 API Key
```

### 3. 启动后端

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/docs 查看 API 文档

### 4. 前端设置

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000 使用应用

### 5. Docker 启动 (可选)

```bash
docker-compose up --build
```

## 项目结构

```
campusflow-ai/
├── backend/
│   ├── app/
│   │   ├── api/           # API 路由和 Schema
│   │   ├── agents/        # LangGraph Agent 系统
│   │   ├── core/          # 核心模块 (LLM, 上下文管理)
│   │   ├── db/            # 数据库模型
│   │   ├── services/      # 业务逻辑层
│   │   └── utils/         # 工具函数
│   └── pyproject.toml
├── frontend/
│   └── src/
│       ├── app/           # Next.js 页面
│       ├── components/    # React 组件
│       ├── hooks/         # 自定义 Hook
│       └── lib/           # 工具库
└── docker-compose.yml
```

## 添加新 Agent

只需 3 步:

1. 创建 `backend/app/agents/nodes/your_agent.py`
2. 添加提示词 `backend/app/agents/prompts/templates/your_agent.j2`
3. 在 `supervisor.py` 注册节点和边

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| LLM_PROVIDER | 模型提供者 | mimo |
| LLM_BASE_URL | API 地址 | - |
| LLM_API_KEY | API 密钥 | - |
| LLM_MODEL_NAME | 模型名称 | - |
| DATABASE_URL | 数据库连接 | sqlite:///./data/campusflow.db |

## License

MIT
