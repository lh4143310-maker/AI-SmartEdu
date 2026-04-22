import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("测试导入...")

# 测试核心模块
try:
    import uvicorn
    import fastapi
    import starlette
    print("✅ 核心Web模块导入成功")
except Exception as e:
    print(f"❌ 核心Web模块导入失败: {e}")

# 测试模型模块
try:
    import torch
    import transformers
    print("✅ 模型模块导入成功")
except Exception as e:
    print(f"❌ 模型模块导入失败: {e}")

# 测试配置模块
try:
    from config.config import MYSQL_CONFIG, NEO4J_CONFIG, WEB_STATIC_DIR, EMBEDDING_MODEL_PATH
    print("✅ 配置模块导入成功")
except Exception as e:
    print(f"❌ 配置模块导入失败: {e}")

# 测试后端模块
try:
    from backend.service import ChatService
    from backend.schemas import Question, Answer
    print("✅ 后端模块导入成功")
except Exception as e:
    print(f"❌ 后端模块导入失败: {e}")

# 测试工具模块
try:
    from tools.agent import get_agent
    from tools.entity.entity_alignment import EntityAlignment
    print("✅ 工具模块导入成功")
except Exception as e:
    print(f"❌ 工具模块导入失败: {e}")

# 测试依赖模块
try:
    from config.dependency import neo4j_driver, neo4j_schema, embedding_model
    print("✅ 依赖模块导入成功")
except Exception as e:
    print(f"❌ 依赖模块导入失败: {e}")

print("\n测试完成！")
