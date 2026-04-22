import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer

class TransformerModel(nn.Module):
    def __init__(self, model_name_or_path, hidden_size=768, num_layers=12, num_heads=12, dropout=0.1):
        super(TransformerModel, self).__init__()
        # 加载预训练模型
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModel.from_pretrained(model_name_or_path)
        
        # Decoder-only结构
        self.decoder_layer = nn.TransformerDecoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dropout=dropout
        )
        self.decoder = nn.TransformerDecoder(
            self.decoder_layer,
            num_layers=num_layers
        )
        
        # 输出层
        self.fc = nn.Linear(hidden_size, self.tokenizer.vocab_size)
    
    def forward(self, input_ids, attention_mask=None):
        # 获取编码器输出
        encoder_outputs = self.model(input_ids, attention_mask=attention_mask).last_hidden_state
        
        # 构建目标序列（这里使用输入序列作为目标序列，实际应用中可能不同）
        tgt = input_ids
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(tgt.size(1)).to(input_ids.device)
        
        # 解码器前向传播
        decoder_outputs = self.decoder(tgt, encoder_outputs, tgt_mask=tgt_mask)
        
        # 输出层
        outputs = self.fc(decoder_outputs)
        
        return outputs
    
    def generate(self, input_ids, max_length=100, temperature=1.0, top_k=50, top_p=0.95):
        """生成文本"""
        self.eval()
        with torch.no_grad():
            for _ in range(max_length):
                outputs = self.forward(input_ids)
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
                
                # 检查是否生成了结束符
                if next_token.item() == self.tokenizer.eos_token_id:
                    break
        
        # 解码生成的序列
        generated_text = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
        return generated_text

if __name__ == "__main__":
    # 测试模型
    model = TransformerModel("model/pretrained/bge-base-zh-v1.5")
    input_text = "你好，"
    input_ids = model.tokenizer.encode(input_text, return_tensors="pt")
    generated_text = model.generate(input_ids, max_length=50)
    print("生成的文本:", generated_text)