import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import ToolMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_neo4j import Neo4jVector,Neo4jGraph
from neo4j_graphrag.types import SearchType

from tools.agent import get_agent

from config.config import MYSQL_CONFIG, NEO4J_CONFIG, WEB_STATIC_DIR, EMBEDDING_MODEL_PATH, VECTOR_STORE_DIR, AGENT_WITH_MEMORY, AGENT_STREAM_OUTPUT
import logging

logger = logging.getLogger(__file__)




class ChatService:

    def __init__(self):
        import torch
        # 检查CUDA是否可用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embeddings = HuggingFaceEmbeddings(model_name = str(EMBEDDING_MODEL_PATH),model_kwargs = {"device": device}) 
        
        # 尝试连接Neo4j数据库
        try:
            self.neo4j_store = Neo4jGraph(
                url=NEO4J_CONFIG["uri"],
                username=NEO4J_CONFIG["auth"][0],
                password=NEO4J_CONFIG["auth"][1],
                database="neo4j"
            )
            self.agent = get_agent(self.neo4j_store.get_schema)
        except Exception as e:
            logger.warning(f"Neo4j数据库连接失败: {str(e)}")
            logger.warning("项目将在没有Neo4j的情况下运行，某些功能可能不可用")
            # 当Neo4j连接失败时，传递一个空的schema函数
            def empty_schema():
                return ""
            self.agent = get_agent(empty_schema)
        # 针对于每一个实体，维护一个Neo4jVector的实例，后面利用该实例来完成搜索

        # 仅用于演示，后面不使用neo4j所提供的索引进行检索
        # self.vector_stores = {
        #     "CourseInfo": Neo4jVector.from_existing_index(
        #         url=config.NEO4J_CONFIG["uri"],
        #         username = config.NEO4J_CONFIG['auth'][0],
        #         password = config.NEO4J_CONFIG['auth'][1],
        #         embedding=self.embeddings,
        #         index_name="CourseInfo_namevector_index",
        #         keyword_index_name="course_name_index",
        #         search_type=SearchType.HYBRID
        #     )
        # }

    def chat(self,user_query,session_id):
        """
        聊天入口，根据配置决定是否流式输出
        :param user_query:
        :param session_id:
        :return:
        """
        agent_config = {"configurable":{"thread_id":session_id}}
        # 流式输出
        if AGENT_STREAM_OUTPUT:
            for content_tuple in  self.agent.stream({"messages":[("user",user_query)]},config=agent_config,stream_mode="messages"):
                if isinstance(content_tuple[0],ToolMessage) or content_tuple[0].content == "":
                    continue
                yield content_tuple[0].content
        # 非流式输出
        else:
            result = self.agent.invoke({"messages":[("user",user_query)]},config=agent_config)
            yield result["messages"][-1].content




if __name__ == '__main__':
    pass





