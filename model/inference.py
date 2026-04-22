import torch
from transformers import AutoModel, AutoTokenizer, pipeline
from model import TransformerModel

class ModelInference:
    def __init__(self, model_name_or_path, device=None, quantize=False):
        """
        初始化模型推理器
        :param model_name_or_path: 模型路径
        :param device: 设备，默认自动选择
        :param quantize: 是否使用量化
        """
        self.model_name_or_path = model_name_or_path
        
        # 自动选择设备
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        # 加载模型和分词器
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        
        # 量化选项
        if quantize:
            self.model = AutoModel.from_pretrained(model_name_or_path, torch_dtype=torch.float16)
            if torch.cuda.is_available():
                self.model = self.model.to(self.device)
                self.model = torch.quantization.quantize_dynamic(
                    self.model,
                    {torch.nn.Linear},  # 指定要量化的层
                    dtype=torch.qint8  # 量化为INT8
                )
        else:
            self.model = AutoModel.from_pretrained(model_name_or_path)
            if torch.cuda.is_available():
                self.model = self.model.to(self.device)
        
        # 构建Transformer模型
        self.transformer_model = TransformerModel(model_name_or_path)
        if torch.cuda.is_available():
            self.transformer_model = self.transformer_model.to(self.device)
        
        # 上下文管理
        self.context = []
    
    def generate(self, prompt, max_length=100, temperature=1.0, top_k=50, top_p=0.95, stream=False):
        """
        生成文本
        :param prompt: 提示文本
        :param max_length: 最大生成长度
        :param temperature: 温度参数
        :param top_k: Top-k采样参数
        :param top_p: Top-p采样参数
        :param stream: 是否流式生成
        :return: 生成的文本
        """
        # 添加上下文
        full_prompt = " ".join(self.context + [prompt])
        
        # 编码输入
        input_ids = self.tokenizer.encode(full_prompt, return_tensors="pt").to(self.device)
        
        if stream:
            # 流式生成
            return self._stream_generate(input_ids, max_length, temperature, top_k, top_p)
        else:
            # 普通生成
            generated_text = self.transformer_model.generate(
                input_ids,
                max_length=max_length,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p
            )
            
            # 更新上下文
            self.context.append(prompt)
            self.context.append(generated_text)
            # 限制上下文长度
            if len(self.context) > 10:
                self.context = self.context[-10:]
            
            return generated_text
    
    def _stream_generate(self, input_ids, max_length, temperature, top_k, top_p):
        """
        流式生成文本
        """
        self.transformer_model.eval()
        with torch.no_grad():
            for _ in range(max_length):
                outputs = self.transformer_model.forward(input_ids)
                # 获取最后一个token的logits
                next_token_logits = outputs[:, -1, :]
                
                # 温度缩放
                next_token_logits = next_token_logits / temperature
                
                # Top-k采样
                if top_k > 0:
                    values, indices = torch.topk(next_token_logits, top_k)
                    next_token_logits = torch.full_like(next_token_logits, -float('inf'))
                    next_token_logits.scatter_(1, indices, values)
                
                # Top-p采样
                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(next_token_logits, descending=True)
                    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                    # 移除累积概率超过top_p的token
                    sorted_indices_to_remove = cumulative_probs > top_p
                    # 保留至少一个token
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    indices_to_remove = sorted_indices[sorted_indices_to_remove]
                    next_token_logits[:, indices_to_remove] = -float('inf')
                
                # 采样下一个token
                next_token = torch.multinomial(torch.softmax(next_token_logits, dim=-1), num_samples=1)
                
                # 将新token添加到输入序列
                input_ids = torch.cat([input_ids, next_token], dim=-1)
                
                # 解码当前token
                current_token = self.tokenizer.decode(next_token[0], skip_special_tokens=True)
                yield current_token
                
                # 检查是否生成了结束符
                if next_token.item() == self.tokenizer.eos_token_id:
                    break
        
        # 解码完整序列
        generated_text = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
        
        # 更新上下文
        self.context.append(self.tokenizer.decode(input_ids[0][:len(self.tokenizer.encode(" ".join(self.context)))], skip_special_tokens=True))
        self.context.append(generated_text)
        # 限制上下文长度
        if len(self.context) > 10:
            self.context = self.context[-10:]
    
    def clear_context(self):
        """
        清空上下文
        """
        self.context = []
    
    def get_embedding(self, text):
        """
        获取文本的嵌入向量
        :param text: 输入文本
        :return: 嵌入向量
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
        return embedding

if __name__ == "__main__":
    # 测试推理器
    inference = ModelInference("model/pretrained/bge-base-zh-v1.5", quantize=True)
    
    # 普通生成
    print("普通生成:")
    result = inference.generate("你好，", max_length=50)
    print(result)
    
    # 流式生成
    print("\n流式生成:")
    for token in inference.generate("今天天气怎么样？", max_length=50, stream=True):
        print(token, end="", flush=True)
    print()
    
    # 测试上下文
    print("\n测试上下文:")
    result = inference.generate("我想去公园玩", max_length=50)
    print(result)
    
    # 清空上下文
    inference.clear_context()
    print("\n清空上下文后:")
    result = inference.generate("我想去公园玩", max_length=50)
    print(result)