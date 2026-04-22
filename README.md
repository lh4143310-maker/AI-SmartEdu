# AI智教大模型项目

## 项目介绍

AI智教大模型项目是一个基于大语言模型的智能教育系统，专为教育场景设计。该项目结合了知识图谱技术和大语言模型能力，为用户提供智能的教育辅助服务。

### 项目目标

- 提供智能的教育问答服务
- 利用知识图谱增强回答的准确性和可靠性
- 结合RAG技术，融合结构化数据和非结构化知识，生成丰富自然的回答
- 实现实体识别和对齐，提高系统理解能力
- 构建一个易于理解和扩展的AI教育助手

### 适合人群

- 大模型初学者
- 教育技术开发者
- 对AI+教育感兴趣的研究人员
- 希望了解知识图谱与大语言模型结合应用的开发者

## 项目结构详解

### 核心目录结构

```
AI智教大模型/
├── model/              # 模型层【大模型核心架构与推理实现】
│   ├── pretrained/     # 预训练模型【开源基座、微调权重、LoRA/QLoRA适配权重】
│   ├── model.py        # 模型定义【Transformer架构、Decoder-only结构、注意力机制、模型组网代码】
│   └── inference.py    # 模型推理【推理加速、FP16/INT8量化、流式生成、上下文管理】
├── backend/            # 后端服务【大模型服务化部署】
│   ├── app.py          # Web应用入口【FastAPI接口、服务启动、路由注册】
│   ├── service.py      # 业务逻辑【对话管理、RAG检索、Prompt编排、多轮会话】
│   ├── schemas.py      # 数据模型【请求/响应结构体、对话消息格式、参数校验】
│   └── __init__.py
├── frontend/           # 前端界面【大模型交互可视化】
│   ├── templates/      # 页面模板【对话页面、参数配置页HTML模板】
│   │   ├── index.html
│   │   ├── marked.min.js
│   │   └── purify.min.js
│   └── script.js       # 交互逻辑【前端请求后端、流式对话渲染、交互事件】
├── data/               # 数据处理【大模型语料与微调数据工程】
│   ├── raw/            # 原始数据【通用语料、垂直领域对话数据、知识库原文】
│   ├── processed/      # 处理后数据【数据清洗、分词、Token化、微调数据集】
│   ├── vectorstore/    # 向量存储【ChromaDB向量库文件】
│   ├── data_prepare.py # 数据准备脚本【数据集构建、Prompt模板生成、向量库入库】
│   ├── document_ingestion.py # 文档导入脚本【RAG增强：课程文档导入ChromaDB】
│   ├── db_utils.py     # 数据库工具函数
│   └── __init__.py
├── config/             # 配置管理【大模型与服务参数管控】
│   ├── config.py       # 配置文件【模型路径、推理参数、服务端口、向量库配置】
│   ├── dependency.py   # 依赖管理【数据库连接、模型加载等】
│   ├── requirements.txt# 依赖管理【PyTorch、Transformers、FastAPI、向量数据库依赖】
│   └── __init__.py
├── tools/              # 工具模块【大模型增强能力】
│   ├── agent/          # 智能代理【ReAct框架、工具调用、任务规划、多Agent协作】
│   │   ├── __init__.py
│   │   ├── prompts.py  # 提示词模板
│   │   ├── schema.py   # 数据模型定义
│   │   └── tools_def.py# 工具函数定义
│   └── entity/         # 实体处理【NER实体识别、知识图谱、实体链接、槽位提取】
│       ├── __init__.py
│       ├── entity_alignment.py          # 实体对齐实现
│       └── entity_extractor_model_base.py# 实体提取模型基础类
└── README.md           # 项目文档【部署教程、使用说明、模型选型、接口文档】
```

### 必备组件说明

| 组件名称 | 是否必备 | 作用 | 详细说明 |
|---------|---------|------|----------|
| model目录 | 是 | 模型层 | 包含模型定义和推理实现 |
| backend目录 | 是 | 后端服务 | 提供Web接口，处理用户请求 |
| frontend目录 | 是 | 前端界面 | 提供用户交互界面 |
| data目录 | 是 | 数据处理 | 包含数据文件和处理脚本 |
| config目录 | 是 | 配置管理 | 管理所有配置信息，包括数据库连接等 |
| tools目录 | 是 | 工具模块 | 包含智能代理和实体处理功能 |

## 技术栈详解

### 后端技术

| 技术 | 版本 | 用途 | 重要性 |
|------|------|------|--------|
| Python | 3.10+ | 主要开发语言 | 必备 |
| FastAPI | 最新版 | Web框架 | 必备 |
| Uvicorn | 最新版 | ASGI服务器 | 必备 |
| MySQL | 8.0+ | 关系型数据库（实际使用 MySQL80 服务） | 必备 |
| Neo4j | 5.0+ | 图数据库（配合 APOC 插件使用） | 必备 |
| LangChain | 最新版 | LLM应用框架 | 必备 |
| DeepSeek | 最新版 | 大语言模型（API调用） | 必备 |
| BGE-base-zh-v1.5 | 最新版 | 文本嵌入模型（本地部署，CPU运行） | 必备 |
| ChromaDB | 最新版 | 向量数据库（RAG文档存储） | 必备 |
| PyTorch | 1.10+ | 深度学习框架 | 必备 |
| sentence-transformers | 最新版 | 句子嵌入库 | 必备 |
| cryptography | 最新版 | MySQL连接依赖 | 必备 |
| itsdangerous | 最新版 | Session管理依赖 | 必备 |

### 实际部署配置

#### MySQL 配置
- **服务名**: MySQL80
- **默认密码**: `123456`
- **数据库**: smart_edu
- **字符集**: utf8mb4

#### Neo4j 配置
- **版本**: Neo4j Desktop 2.x
- **APOC插件**: 已安装（2026.03.1-core）
- **认证**: neo4j/abc123456
- **注意**: APOC插件用于获取schema信息，启用后知识图谱功能完整

#### 模型配置
- **嵌入模型**: BGE-base-zh-v1.5（本地加载）
- **运行设备**: CPU（自动检测，无CUDA时回退到CPU）
- **大语言模型**: DeepSeek API（在线调用）

### 前端技术

| 技术 | 用途 | 重要性 |
|------|------|--------|
| HTML | 页面结构 | 必备 |
| JavaScript | 交互逻辑 | 必备 |
| Marked.js | Markdown解析 | 可选 |
| Purify.js | HTML净化 | 可选 |

### 核心组件关系

### 组件依赖关系

```
┌─────────────────┐     ┌─────────────────┐
│   前端界面      │────>│  FastAPI后端    │
└─────────────────┘     └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  ChatService    │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │    LangChain    │
                        │     Agent       │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼───────┐    ┌───────────▼───────────┐   ┌───────▼───────┐
│ 实体对齐工具   │    │     DeepSeek LLM      │   │ 文档检索工具   │
└───────┬───────┘    │   (回答生成与决策)     │   └───────┬───────┘
        │            └───────────┬───────────┘           │
        │                        │                        │
┌───────▼───────┐    ┌───────────▼───────────┐   ┌───────▼───────┐
│ Cypher检查工具 │    │   结构化数据查询       │   │  向量数据库    │
└───────┬───────┘    │      (Neo4j)          │   │  (ChromaDB)   │
        │            │   - 精确课程信息       │   │  - 课程介绍    │
┌───────▼───────┐    │   - 章节、价格等       │   │  - 背景知识    │
│  Neo4j查询工具 │    └───────────────────────┘   └───────────────┘
└───────┬───────┘
        │
┌───────▼───────┐
│   知识图谱     │
│    Neo4j      │
└───────────────┘
```

### 数据流向

1. **用户输入** → 前端界面 → FastAPI后端
2. **后端处理** → ChatService → LangChain Agent
3. **Agent决策** → 分析问题，确定检索策略
4. **并行检索** → 
   - 结构化数据查询：实体对齐 → Cypher检查 → Neo4j查询（精确数据）
   - 非结构化知识检索：文档检索 → ChromaDB（背景知识）
5. **结果融合** → DeepSeek 综合两类数据生成自然语言回答
6. **回答返回** → Agent → ChatService → 前端界面 → 用户

## 详细组件说明

### 1. 模型层（/model）

**作用**：包含模型定义和推理实现。

**结构**：
- **pretrained/**：预训练模型
  - `bge-base-zh-v1.5/`：中文预训练嵌入模型，用于将文本转换为向量表示

- **model.py**：模型定义
  - 实现了Transformer架构
  - Decoder-only结构
  - 注意力机制
  - 模型组网代码

- **inference.py**：模型推理
  - 推理加速
  - FP16/INT8量化
  - 流式生成
  - 上下文管理

### 2. 后端服务层（/backend）

**作用**：提供Web服务接口，处理用户请求。

**结构**：
- **app.py**：FastAPI应用入口
  - 定义路由和聊天服务接口
  - 会话管理
  - 静态文件服务

- **service.py**：聊天服务实现
  - 对话管理
  - RAG检索
  - Prompt编排
  - 多轮会话

- **schemas.py**：数据模型定义
  - 请求/响应结构体
  - 对话消息格式
  - 参数校验

### 3. 前端界面层（/frontend）

**作用**：提供用户交互界面。

**结构**：
- **templates/**：页面模板
  - `index.html`：主页面
  - `marked.min.js`：Markdown解析库
  - `purify.min.js`：HTML净化库

- **script.js**：交互逻辑
  - 前端请求后端
  - 流式对话渲染
  - 交互事件处理

### 4. 数据处理层（/data）

**作用**：处理数据准备和数据库操作。

**结构**：
- **raw/**：原始数据
  - `doccano_ext.jsonl`：Doccano标注工具导出的数据
  - `edu.sql`：教育相关的数据库脚本

- **processed/**：处理后数据
  - 数据清洗、分词、Token化、微调数据集

- **data_prepare.py**：数据准备脚本
  - 数据集构建
  - Prompt模板生成
  - 向量库入库

- **document_ingestion.py**：文档数据导入脚本（RAG增强）
  - 从MySQL提取课程介绍、章节信息
  - 生成嵌入向量并导入ChromaDB
  - 支持文档检索测试

- **db_utils.py**：数据库工具函数

### 5. 配置管理层（/config）

**作用**：管理所有配置信息和依赖。

**结构**：
- **config.py**：配置文件
  - 模型路径
  - 推理参数
  - 服务端口
  - 向量库配置
  - 数据库连接配置

- **dependency.py**：依赖管理
  - 数据库连接初始化（MySQL、Neo4j）
  - 模型加载（Embedding模型）
  - ChromaDB客户端和文档集合初始化（RAG增强）

- **requirements.txt**：Python依赖管理
  - PyTorch
  - Transformers
  - FastAPI
  - 向量数据库依赖

### 6. 工具模块层（/tools）

**作用**：提供智能代理和实体处理功能。

**结构**：
- **agent/**：智能代理模块
  - `__init__.py`：模块初始化，创建Agent实例
  - `prompts.py`：提示词模板，定义Agent的行为
  - `schema.py`：数据模型定义
  - `tools_def.py`：工具函数定义
    - 实体对齐工具
    - Cypher检查工具
    - Neo4j查询工具
    - 文档检索工具（RAG增强）

- **entity/**：实体处理模块
  - `entity_alignment.py`：实体对齐实现
  - `entity_extractor_model_base.py`：实体提取模型基础类

## 核心功能详解

### 1. 智能聊天功能

**功能说明**：基于大语言模型的对话系统，支持教育相关问题的智能回答。

**实现原理**：
1. **用户输入处理**：接收用户的问题
2. **实体提取**：从问题中提取关键实体
3. **实体对齐**：将提取的实体与知识图谱中的实体进行匹配
4. **并行检索**：
   - **结构化数据查询**：根据对齐的实体生成Cypher查询语句，从Neo4j获取精确数据（课程列表、章节、价格等）
   - **非结构化知识检索**：使用文档检索工具从ChromaDB获取背景知识（课程介绍、知识点解释等）
5. **结果融合**：DeepSeek LLM综合结构化数据和非结构化知识，生成自然、丰富的回答
6. **回答返回**：将生成的回答流式返回给用户

**核心代码**：
- `backend/service.py`：聊天服务实现
- `tools/agent/__init__.py`：Agent创建和管理
- `tools/agent/tools_def.py`：工具函数定义

### 2. 实体对齐功能

**功能说明**：将用户查询中的实体与知识图谱中的实体进行匹配。

**实现原理**：
1. **实体提取**：从用户查询中提取实体
2. **混合搜索**：结合全文搜索和向量搜索
   - 全文搜索：处理精确匹配
   - 向量搜索：处理语义相似性
3. **结果排序**：根据匹配度对结果进行排序
4. **实体替换**：将用户查询中的实体替换为知识图谱中的标准实体

**核心代码**：
- `tools/entity/entity_alignment.py`：实体对齐实现
- `tools/agent/tools_def.py`：entity_alignment工具函数

### 3. 知识图谱查询功能

**功能说明**：使用Neo4j图数据库存储和查询教育领域知识。

**实现原理**：
1. **Cypher生成**：根据用户问题生成Cypher查询语句
2. **语法检查**：检查Cypher语句的语法正确性
3. **查询执行**：执行Cypher查询，获取知识图谱数据
4. **结果处理**：处理查询结果，提取有用信息

**核心代码**：
- `tools/agent/tools_def.py`：neo4j_query和check_syntax_error工具函数

### 4. 混合搜索功能

**功能说明**：结合全文搜索和向量搜索，提高查询准确性。

**实现原理**：
1. **文本嵌入**：使用BGE模型将查询文本转换为向量
2. **向量搜索**：在向量索引中查找相似实体
3. **全文搜索**：在全文索引中查找匹配实体
4. **结果融合**：将两种搜索结果融合，计算综合得分
5. **结果排序**：根据综合得分对结果进行排序

**核心代码**：
- `tools/agent/tools_def.py`：hybrid_search_query函数

### 5. RAG增强检索功能（新增）

**功能说明**：结合结构化数据查询和非结构化知识检索，生成更丰富、自然的回答。

**实现原理**：
1. **双路检索**：
   - **结构化数据**：从Neo4j知识图谱查询精确数据（课程、章节、价格等）
   - **非结构化知识**：从ChromaDB向量库检索背景知识（课程介绍、概念解释等）
2. **结果融合**：DeepSeek LLM综合两类信息，生成连贯的自然语言回答
3. **优势**：
   - 结构化数据保证准确性
   - 非结构化知识增加解释性和丰富度
   - 回答更贴近人类表达方式

**核心代码**：
- `tools/agent/tools_def.py`：`document_retrieval` 函数
- `data/document_ingestion.py`：文档导入脚本
- `config/dependency.py`：ChromaDB初始化

**使用步骤**：
1. **导入文档数据**：
   ```bash
   python data/document_ingestion.py --ingest
   ```
2. **测试文档检索**：
   ```bash
   python data/document_ingestion.py --search "Java课程学什么" --top_k 3
   ```

### 6. 模型推理功能

**功能说明**：提供模型推理和文本生成能力。

**实现原理**：
1. **模型加载**：加载预训练模型
2. **推理加速**：使用FP16/INT8量化加速推理
3. **流式生成**：支持流式文本生成
4. **上下文管理**：维护对话上下文

**核心代码**：
- `model/model.py`：模型定义
- `model/inference.py`：模型推理实现

## 环境配置详细步骤

### 1. 系统环境准备

**步骤**：
1. 安装Python 3.10或更高版本
2. 安装MySQL 8.0或更高版本
3. 安装Neo4j 5.0或更高版本
4. 安装CUDA 11.7或更高版本（用于GPU加速）

### 2. Python依赖安装

**步骤**：
1. **进入项目目录**
   ```bash
   cd AI智教大模型
   ```

2. **创建虚拟环境**
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

3. **激活虚拟环境**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **安装依赖**
   ```bash
   pip install -r config/requirements.txt
   ```

### 3. 数据库配置

**MySQL配置**：
1. **创建数据库**
   ```sql
   CREATE DATABASE smart_edu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **导入数据**
   ```bash
   mysql -u root -p smart_edu < data/raw/edu.sql
   ```

3. **配置连接信息**
   编辑 `config/config.py` 文件：
   ```python
   MYSQL_CONFIG = {
       "host": "localhost",
       "port": 3306,
       "user": "root",
       "password": "123456",  # 默认密码，可根据实际情况修改
       "database": "smart_edu"
   }
   ```
   
   **注意**：项目默认使用的 MySQL 密码为 `123456`，已在 `config/config.py` 中配置。如果你的 MySQL 密码不同，请修改该文件。

**Neo4j配置**：
1. **启动Neo4j服务**
   ```bash
   # Windows
   neo4j start
   
   # Linux/Mac
   sudo service neo4j start
   ```

2. **访问Neo4j浏览器**
   打开 http://localhost:7474，默认用户名/密码：neo4j/neo4j

3. **修改密码**
   首次登录时，系统会提示修改密码

4. **配置连接信息**
   编辑 `config/config.py` 文件：
   ```python
   NEO4J_CONFIG = {
       "uri": "neo4j://localhost",
       "auth": ("neo4j", "abc123456")
   }
   ```

### 4. 模型配置

**嵌入模型**：
- 确保 `model/pretrained/bge-base-zh-v1.5/` 目录存在
- 该模型用于将文本转换为向量表示

**大语言模型**：
- 项目默认使用DeepSeek模型
- 确保你有DeepSeek的API访问权限
- 可以在 `tools/agent/__init__.py` 中修改模型配置

## 项目运行详细步骤

### 1. 导入文档数据（RAG增强功能）

**步骤**：
1. **进入项目目录**
   ```bash
   cd AI智教大模型
   ```

2. **导入课程文档到向量库**
   ```bash
   python data/document_ingestion.py --ingest
   ```
   这将从MySQL提取课程介绍、章节信息，并导入ChromaDB向量库

3. **（可选）测试文档检索**
   ```bash
   python data/document_ingestion.py --search "Java课程学什么" --top_k 3
   ```

### 2. 启动后端服务

**步骤**：
1. **确保文档数据已导入**

2. **启动FastAPI服务**
   ```bash
   python backend/app.py
   ```

3. **验证服务启动**
   服务将在 http://localhost:8000 启动
   可以通过访问 http://localhost:8000/docs 查看API文档

### 3. 访问前端界面

**步骤**：
1. **打开浏览器**
2. **访问地址**：http://localhost:8000
3. **开始使用**：在聊天框中输入教育相关问题，系统会智能回答

## 系统状态验证

### 启动成功标志

查看后端日志，确认以下信息：

```
✅ Neo4j数据库连接成功！
✅ Neo4j schema获取成功！      # APOC插件正常工作
✅ 嵌入模型加载成功！使用设备: cpu
✅ 文档集合加载成功！
✅ ChatDeepSeek初始化成功！
✅ EntityAlignment初始化成功！
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 数据验证

**MySQL数据检查**：
```bash
python -c "import pymysql; conn=pymysql.connect(host='localhost',user='root',password='123456',database='smart_edu'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM course_info'); print(f'课程数量: {cursor.fetchone()[0]}'); conn.close()"
```

**ChromaDB数据检查**：
```bash
python data/document_ingestion.py --search "Java" --top_k 3
```

### 功能测试

在聊天界面输入以下问题测试：
- "有哪些编程课程？" - 测试课程列表查询
- "Java基础课程学什么？" - 测试课程详情查询
- "Redis是讲什么的？" - 测试RAG文档检索

## 核心API接口详解

### 1. 聊天接口

**接口信息**：
- **路径**：`/chat`
- **方法**：POST
- **请求体**：
  ```json
  {
    "message": "数学课程有哪些章节？"
  }
  ```
- **响应**：流式文本响应，返回AI的回答

**使用示例**：
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "数学课程有哪些章节？"}'
```

### 2. 主页接口

**接口信息**：
- **路径**：`/`
- **方法**：GET
- **响应**：重定向到前端界面

**使用示例**：
```bash
curl http://localhost:8000/
```

## 项目架构深度解析

### 1. 架构设计理念

**设计原则**：
- **模块化**：将功能拆分为独立的模块，便于维护和扩展
- **松耦合**：模块之间通过明确的接口通信，减少依赖
- **可扩展性**：支持添加新功能和替换组件
- **性能优化**：针对大模型推理和数据库查询进行优化

### 2. 核心模块详解

**Backend模块**：
- **功能**：提供Web服务接口，处理用户请求
- **实现**：基于FastAPI框架，支持异步处理
- **关键组件**：
  - `app.py`：FastAPI应用入口，定义路由
  - `service.py`：聊天服务，处理聊天逻辑
  - `schemas.py`：数据模型，定义请求和响应结构

**Agent模块**：
- **功能**：智能决策中心，协调各工具的调用
- **实现**：基于LangChain的Agent机制
- **关键组件**：
  - `__init__.py`：创建Agent实例
  - `tools_def.py`：定义工具函数
  - `prompts.py`：定义Agent的提示词

**Entity模块**：
- **功能**：处理实体识别和对齐
- **实现**：基于Neo4j和嵌入模型
- **关键组件**：
  - `entity_alignment.py`：实体对齐实现

**Model模块**：
- **功能**：模型定义和推理
- **实现**：基于PyTorch和Transformers
- **关键组件**：
  - `model.py`：模型定义
  - `inference.py`：推理实现

### 3. 数据流详解

**用户查询流程**：
1. 用户在前端界面输入问题
2. 前端将问题发送到 `/chat` 接口
3. Backend模块接收请求，创建会话
4. ChatService调用Agent处理问题
5. Agent分析问题，提取实体
6. Agent调用实体对齐工具，匹配知识图谱中的实体
7. Agent生成Cypher查询语句
8. Agent调用语法检查工具，验证Cypher语句
9. Agent调用Neo4j查询工具，执行查询
10. Agent根据查询结果生成回答
11. ChatService将回答流式返回给前端
12. 前端显示回答给用户

## 常见问题与故障排除

### 1. 服务启动失败

**可能原因**：
- 端口8000被占用
- 数据库连接失败
- 模型路径配置错误
- 依赖包缺失或版本冲突

**解决方案**：
- **端口被占用**：
  ```bash
  # Windows
  netstat -ano | findstr :8000
  taskkill /PID <进程ID> /F
  ```

- **数据库连接失败**：
  - 检查MySQL80服务是否运行：`Get-Service MySQL80`
  - 检查Neo4j是否启动（通过Neo4j Desktop）
  - 验证密码：MySQL默认`123456`，Neo4j默认`abc123456`

- **依赖包缺失**：
  ```bash
  # 安装cryptography（MySQL连接需要）
  pip install cryptography
  
  # 安装itsdangerous（Session管理需要）
  pip install itsdangerous
  ```

- **模型路径配置错误**：
  - 确保 `model/pretrained/bge-base-zh-v1.5/` 目录存在

### 2. MySQL数据导入问题

**问题**：PowerShell不支持`mysql < file.sql`重定向语法

**解决方案**：
使用Python脚本导入：
```bash
python import_course_data.py
```

### 3. Neo4j APOC插件问题

**问题**：启动时提示`Could not use APOC procedures`

**解决方案**：
1. 打开Neo4j Desktop
2. 找到你的数据库项目
3. 点击Plugins选项卡
4. 安装/启用APOC插件
5. 重启Neo4j服务

### 4. CUDA/GPU相关问题

**问题**：`Torch not compiled with CUDA enabled`

**解决方案**：
系统已配置为自动检测CUDA，如无GPU则自动使用CPU运行，无需额外配置。

### 5. 向量模型加载问题

**问题**：嵌入模型加载失败

**检查项**：
- 确认`model/pretrained/bge-base-zh-v1.5/`目录存在
- 确认模型文件完整（包含config.json、pytorch_model.bin等）
- 检查PyTorch版本兼容性

### 2. 回答不准确

**可能原因**：
- 知识图谱数据不完整
- 实体对齐失败
- 大语言模型参数设置不当
- Cypher查询语句错误

**解决方案**：
- **知识图谱数据不完整**：
  - 补充知识图谱数据
  - 确保实体和关系的完整性

- **实体对齐失败**：
  - 检查实体对齐算法
  - 调整嵌入模型参数

- **大语言模型参数设置**：
  - 调整温度参数（temperature）
  - 调整最大生成长度（max_tokens）

- **Cypher查询语句错误**：
  - 检查Cypher语法
  - 确保查询语句符合知识图谱结构

### 3. 响应速度慢

**可能原因**：
- 模型推理时间长
- 数据库查询效率低
- 网络延迟
- 服务器性能不足

**解决方案**：
- **模型推理时间长**：
  - 使用GPU加速
  - 优化模型参数
  - 考虑使用更轻量级的模型

- **数据库查询效率低**：
  - 创建适当的索引
  - 优化Cypher查询语句
  - 考虑使用缓存机制

- **网络延迟**：
  - 确保网络连接稳定
  - 考虑使用本地模型

- **服务器性能不足**：
  - 增加服务器内存
  - 使用更强大的CPU/GPU

## 项目维护与扩展

### 1. 数据更新

**知识图谱更新**：
1. **添加新实体**：
   ```cypher
   CREATE (c:Course {name: '新课程', description: '课程描述'})
   ```

2. **添加新关系**：
   ```cypher
   MATCH (c:Course {name: '数学'}), (ch:Chapter {name: '代数'})
   CREATE (c)-[:HAS_CHAPTER]->(ch)
   ```

3. **批量导入**：
   - 使用Neo4j的`neo4j-admin import`工具
   - 使用Cypher的`LOAD CSV`语句

**模型更新**：
1. **嵌入模型更新**：
   - 下载最新版本的BGE模型
   - 更新配置文件中的模型路径

2. **大语言模型更新**：
   - 在 `tools/agent/__init__.py` 中修改模型配置
   - 考虑使用性能更好的模型

### 2. 功能扩展

**添加新工具**：
1. 在 `tools/agent/tools_def.py` 中定义新工具函数
2. 在 `tools/agent/schema.py` 中定义工具参数模型
3. 在 `tools/agent/__init__.py` 中注册新工具

**添加新功能**：
1. **添加新的API接口**：在 `backend/app.py` 中添加新路由
2. **添加新的前端功能**：修改 `frontend/templates/index.html`
3. **添加新的数据处理逻辑**：在 `data` 模块中添加新功能
4. **添加新的模型功能**：在 `model` 模块中添加新功能

### 3. 性能优化

**数据库优化**：
- **创建索引**：
  ```cypher
  CREATE INDEX course_name_index FOR (c:Course) ON (c.name)
  CREATE VECTOR INDEX CourseInfo_namevector_index FOR (c:Course) ON (c.name_embedding) 
  OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}}
  ```

- **优化查询**：
  - 使用参数化查询
  - 避免全图扫描
  - 合理使用限制和排序

**代码优化**：
- **缓存机制**：
  - 缓存频繁查询的结果
  - 使用Redis等缓存系统

- **并行处理**：
  - 使用异步IO
  - 并行处理多个查询

- **资源管理**：
  - 合理使用连接池
  - 及时释放资源

## 初学者指南

### 1. 学习路径

**阶段一：环境搭建**
- 安装Python和必要的依赖
- 配置MySQL和Neo4j数据库
- 启动项目并验证服务

**阶段二：核心概念理解**
- 理解大语言模型的基本原理
- 学习知识图谱的概念和应用
- 了解LangChain框架的使用
- 熟悉FastAPI框架的使用

**阶段三：功能开发**
- 尝试修改提示词，观察Agent行为变化
- 添加新的工具函数
- 扩展知识图谱数据
- 测试不同的模型参数

**阶段四：性能优化**
- 分析系统瓶颈
- 尝试不同的优化策略
- 测试优化效果

### 2. 学习资源

**官方文档**：
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Neo4j官方文档](https://neo4j.com/docs/)
- [LangChain官方文档](https://docs.langchain.com/)
- [Hugging Face官方文档](https://huggingface.co/docs/)
- [PyTorch官方文档](https://pytorch.org/docs/)

**教程资源**：
- [尚硅谷大模型项目实战课程](https://www.atguigu.com/)
- [Neo4j图数据库教程](https://neo4j.com/graphacademy/)
- [LangChain入门教程](https://python.langchain.com/docs/get_started/introduction)

**社区支持**：
- [GitHub Issues](https://github.com/issues)
- [Stack Overflow](https://stackoverflow.com/)
- [Neo4j社区](https://community.neo4j.com/)

### 3. 实践建议

**从小规模开始**：
- 先使用小规模的知识图谱数据
- 逐步添加功能和数据

**实验不同模型**：
- 尝试不同的大语言模型
- 比较不同嵌入模型的效果

**监控和调试**：
- 使用日志记录系统行为
- 监控性能指标
- 调试工具调用过程

**文档和注释**：
- 为代码添加详细的注释
- 记录实验结果和发现
- 分享经验和最佳实践

## 项目实际架构特点

### 1. RAG增强架构（已实现）

本项目采用**双路检索 + LLM生成**的RAG架构：

```
用户问题
    ↓
┌─────────────────┐
│   DeepSeek      │ ← 意图理解
│   Agent决策     │
└────────┬────────┘
         ↓
┌────────┴────────┐
│   并行检索       │
├─────────────────┤
│ Neo4j图谱查询   │ ← 精确结构化数据
│ ChromaDB检索    │ ← 非结构化文档知识
└────────┬────────┘
         ↓
┌─────────────────┐
│  结果融合生成    │ ← DeepSeek生成自然语言回答
└─────────────────┘
```

**核心优势**：
- 结构化数据保证准确性（课程价格、章节等）
- 非结构化知识增强解释性（课程介绍、背景）
- LLM生成自然流畅的回答

### 2. 实体对齐机制

使用**同义词表 + 向量检索**实现实体对齐：
- 先查MySQL同义词-标准词映射表
- 未命中则使用ChromaDB向量相似度检索
- 自动将用户输入对齐到系统标准实体

### 3. 提示词工程优化

针对客服场景优化提示词：
- **禁止暴露技术细节**：不显示"查询"、"对齐"等过程
- **直接回答问题**：先给核心答案，再补充推荐
- **自然对话风格**：像真人客服一样交流

## 项目未来发展

### 1. 功能增强

- **多模态支持**：添加图像、音频等多模态输入
- **个性化学习**：根据用户历史行为提供个性化推荐
- **智能评估**：自动评估用户学习进度和掌握程度
- **多语言支持**：扩展到多语言教育场景
- **语音交互**：添加语音输入和输出功能

### 2. 技术升级

- **模型优化**：使用更先进的大语言模型
- **知识图谱扩展**：构建更全面的教育知识图谱
- **性能提升**：优化系统架构，提高响应速度
- **部署优化**：支持容器化部署和云服务
- **微服务架构**：将系统拆分为独立的微服务

### 3. 应用场景扩展

- **K12教育**：针对中小学教育场景优化
- **高等教育**：支持大学课程和专业知识
- **职业教育**：提供职业技能培训和认证
- **终身学习**：支持成人教育和持续学习
- **企业培训**：支持企业内部培训和知识管理

## 总结

AI智教大模型项目是一个结合了大语言模型和知识图谱技术的智能教育系统，为用户提供智能的教育辅助服务。项目采用模块化设计，易于理解和扩展，适合大模型初学者学习和实践。

通过本项目，你可以：
- 了解大语言模型的应用方法
- 学习知识图谱的构建和查询
- 掌握LangChain框架的使用
- 实践AI+教育的具体应用
- 熟悉大模型项目的完整架构

希望本项目能够帮助你入门大模型应用开发，为教育技术的发展贡献力量！

---

**注意**：本项目仅供学习和研究使用，请勿用于商业用途。

---

**项目结构说明**：
本项目采用标准的大模型项目架构，分为以下几个主要层次：
- **模型层（model）**：负责模型定义和推理
- **后端层（backend）**：负责Web服务和业务逻辑
- **前端层（frontend）**：负责用户界面和交互
- **数据层（data）**：负责数据处理和存储
- **配置层（config）**：负责配置管理
- **工具层（tools）**：负责提供各种工具功能

这种分层架构使得项目结构清晰、易于维护和扩展，符合大模型项目的最佳实践。
