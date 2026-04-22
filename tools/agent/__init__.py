import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from .schema import CheckSyntaxError, EntityAlignmentList,Neo4jQueryParams,DocumentRetrievalParams
from .tools_def import check_syntax_error,neo4j_query,entity_alignment,document_retrieval
from .prompts import major_agent_system_prompt_template
from config.config import MYSQL_CONFIG, NEO4J_CONFIG, WEB_STATIC_DIR, EMBEDDING_MODEL_PATH, VECTOR_STORE_DIR, AGENT_WITH_MEMORY, AGENT_STREAM_OUTPUT




def get_agent(neo4j_schema):
    """
    创建agent
    :return:
    """
    # 构造LLM
    llm = ChatDeepSeek(
        model="deepseek-chat"
    )
    # 构造tools
    neo4j_query_tool = tool(neo4j_query, args_schema=Neo4jQueryParams)
    check_syntax_tool = tool(check_syntax_error,args_schema=CheckSyntaxError)
    entity_alignment_tool = tool(entity_alignment,args_schema=EntityAlignmentList)
    document_retrieval_tool = tool(document_retrieval, args_schema=DocumentRetrievalParams)

    # 构造记忆模块
    memory_saver = InMemorySaver() if AGENT_WITH_MEMORY else None

    # 创建Agent
    agent = create_agent(
        model=llm,
        tools=[neo4j_query_tool,check_syntax_tool,entity_alignment_tool,document_retrieval_tool],
        checkpointer=memory_saver,
        system_prompt=major_agent_system_prompt_template.format(neo4j_schema=neo4j_schema)
    )
    return agent