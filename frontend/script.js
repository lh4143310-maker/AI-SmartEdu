// 前端交互逻辑

// 发送消息到后端
async function sendMessage() {
    const message = document.getElementById('message').value;
    if (!message.trim()) return;

    // 添加用户消息到聊天记录
    addMessage('user', message);
    document.getElementById('message').value = '';

    // 显示加载状态
    const loadingElement = document.createElement('div');
    loadingElement.id = 'loading';
    loadingElement.className = 'message assistant';
    loadingElement.innerHTML = '<div class="loading">正在思考...</div>';
    document.getElementById('chat').appendChild(loadingElement);
    scrollToBottom();

    try {
        // 发送请求到后端
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        // 处理流式响应
        if (response.ok) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullResponse = '';
            
            // 移除加载状态
            document.getElementById('chat').removeChild(loadingElement);
            
            // 创建助手消息元素
            const assistantMessage = document.createElement('div');
            assistantMessage.className = 'message assistant';
            document.getElementById('chat').appendChild(assistantMessage);

            // 处理流式数据
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                fullResponse += chunk;
                
                // 更新助手消息
                assistantMessage.innerHTML = marked.parse(purify.sanitize(fullResponse));
                scrollToBottom();
            }
        } else {
            throw new Error('请求失败');
        }
    } catch (error) {
        console.error('Error:', error);
        // 移除加载状态
        if (document.getElementById('loading')) {
            document.getElementById('chat').removeChild(loadingElement);
        }
        // 显示错误消息
        addMessage('assistant', '抱歉，处理请求时出现错误，请稍后再试。');
    }
}

// 添加消息到聊天记录
function addMessage(sender, text) {
    const chat = document.getElementById('chat');
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    
    if (sender === 'assistant') {
        messageElement.innerHTML = marked.parse(purify.sanitize(text));
    } else {
        messageElement.textContent = text;
    }
    
    chat.appendChild(messageElement);
    scrollToBottom();
}

// 滚动到聊天底部
function scrollToBottom() {
    const chat = document.getElementById('chat');
    chat.scrollTop = chat.scrollHeight;
}

// 绑定发送按钮事件
document.getElementById('send').addEventListener('click', sendMessage);

// 绑定回车键事件
document.getElementById('message').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// 初始化页面
window.onload = function() {
    addMessage('assistant', '你好！我是AI智教大模型，有什么可以帮助你的吗？');
};