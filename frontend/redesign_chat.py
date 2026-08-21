with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace chat window HTML with professional design
old_chat_html = '''<div class="chat-window" id="chatWindow">
        <div class="chat-header"><div style="display:flex;align-items:center;gap:8px;"><select id="chatMode" style="width:auto;margin:0;padding:4px 8px;font-size:11px;background:transparent;border:1px solid rgba(255,255,255,0.3);color:white;border-radius:4px;"><option value="general">AI Assistant</option><option value="support">DevPilot Support</option></select></div><span onclick="toggleChat()" style="cursor:pointer;">✕</span></div>
        <div class="chat-messages" id="chatMessages"><div class="chat-msg ai-msg">How can I help you with your code?</div></div>
        <div class="chat-input-area"><input type="text" id="chatInput" placeholder="Ask anything..." onkeypress="if(event.key===\'Enter\')sendChat()"><button onclick="sendChat()">Send</button></div>
    </div>'''

new_chat_html = '''<div class="chat-window" id="chatWindow">
        <div class="chat-header">
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:8px;height:8px;background:#16a34a;border-radius:50%;"></div>
                <span style="font-weight:500;">DevPilot Assistant</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <select id="chatMode" style="margin:0;padding:4px 8px;font-size:11px;background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:4px;font-family:var(--font);">
                    <option value="general">AI Mode</option>
                    <option value="support">Support</option>
                </select>
                <span onclick="toggleChat()" style="cursor:pointer;font-size:14px;color:var(--text-secondary);">✕</span>
            </div>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="chat-msg ai-msg">Hello. I can help you with code analysis, security scanning, or general programming questions.</div>
        </div>
        <div class="chat-input-area">
            <input type="text" id="chatInput" placeholder="Type a message..." onkeypress="if(event.key===\'Enter\')sendChat()">
            <button onclick="sendChat()" style="padding:7px 12px;font-size:12px;">Send</button>
        </div>
    </div>'''

content = content.replace(old_chat_html, new_chat_html)

# Update chat bot button to match professional theme
old_bot_btn = '<div class="chat-bot-btn" onclick="toggleChat()">✦</div>'
new_bot_btn = '<div class="chat-bot-btn" onclick="toggleChat()" title="Chat with DevPilot"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg></div>'
content = content.replace(old_bot_btn, new_bot_btn)

# Update chat CSS to match professional theme
old_chat_css = '''.chat-window { position:fixed; bottom:88px; right:24px; width:360px; height:480px; background:var(--surface); border:1px solid var(--border); border-radius:12px; display:none; flex-direction:column; z-index:999; overflow:hidden; box-shadow:var(--shadow-lg); }
        .chat-window.open { display:flex; }
        .chat-header { padding:16px; border-bottom:1px solid var(--border); font-weight:600; font-size:13px; display:flex; justify-content:space-between; align-items:center; }
        .chat-messages { flex:1; overflow-y:auto; padding:16px; }
        .chat-msg { padding:10px 12px; border-radius:8px; margin-bottom:8px; font-size:12px; line-height:1.6; max-width:85%; }
        .user-msg { background:var(--accent); color:white; margin-left:auto; border-bottom-right-radius:2px; }
        .ai-msg { background:var(--surface-hover); color:var(--text); border-bottom-left-radius:2px; }
        .chat-input-area { display:flex; gap:8px; padding:12px; border-top:1px solid var(--border); }
        .chat-input-area input { flex:1; margin:0; }
        .chat-input-area button { padding:8px 14px; font-size:12px; }'''

new_chat_css = '''.chat-window { position:fixed; bottom:88px; right:24px; width:380px; height:500px; background:var(--surface); border:1px solid var(--border); border-radius:10px; display:none; flex-direction:column; z-index:999; overflow:hidden; box-shadow:0 8px 32px rgba(0,0,0,0.15); }
        .chat-window.open { display:flex; animation:slideUp 0.2s ease; }
        @keyframes slideUp { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
        .chat-header { padding:12px 16px; border-bottom:1px solid var(--border); font-size:13px; display:flex; justify-content:space-between; align-items:center; background:var(--surface); }
        .chat-messages { flex:1; overflow-y:auto; padding:16px; background:var(--bg); }
        .chat-messages::-webkit-scrollbar { width:4px; }
        .chat-messages::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
        .chat-msg { padding:10px 14px; border-radius:8px; margin-bottom:8px; font-size:12.5px; line-height:1.6; max-width:85%; word-wrap:break-word; }
        .user-msg { background:var(--accent); color:white; margin-left:auto; border-bottom-right-radius:2px; }
        .ai-msg { background:var(--surface); color:var(--text); border:1px solid var(--border); border-bottom-left-radius:2px; }
        .chat-input-area { display:flex; gap:8px; padding:12px; border-top:1px solid var(--border); background:var(--surface); }
        .chat-input-area input { flex:1; margin:0; padding:8px 12px; font-size:12.5px; }
        .chat-input-area button { padding:7px 14px; font-size:12px; border-radius:6px; }'''

content = content.replace(old_chat_css, new_chat_css)

# Update chat bot button CSS
old_bot_css = '''.chat-bot-btn { position:fixed; bottom:24px; right:24px; width:52px; height:52px; background:var(--accent); border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:22px; z-index:1000; box-shadow:0 4px 16px rgba(79,70,229,0.3); transition:all 0.2s; }
        .chat-bot-btn:hover { transform:scale(1.05); box-shadow:0 6px 24px rgba(79,70,229,0.4); }'''

new_bot_css = '''.chat-bot-btn { position:fixed; bottom:24px; right:24px; width:48px; height:48px; background:var(--accent); border-radius:8px; display:flex; align-items:center; justify-content:center; cursor:pointer; z-index:1000; box-shadow:0 2px 8px rgba(79,70,229,0.3); transition:all 0.15s; }
        .chat-bot-btn:hover { background:var(--accent-hover); box-shadow:0 4px 12px rgba(79,70,229,0.4); }'''

content = content.replace(old_bot_css, new_bot_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Chatbot redesigned to match professional theme!")