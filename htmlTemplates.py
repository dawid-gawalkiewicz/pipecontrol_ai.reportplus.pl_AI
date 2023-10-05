css = '''
<style>
.main {
height: 100vh;
}
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.block-container  {
padding: 0.2rem;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
footer, #MainMenu {
display: none;
}

[data-testid="InputInstructions"] {
    display: flex;
    flex-direction: column;
    height: 100%;
    min-height: 60vh;
    justify-content: space-between;
    border: 1px solid rgba(0, 0, 0, 0.1);
}

.chat-window {
    margin-bottom: 120px;
    overflow-y: auto;
}
.stTextInput {
    position: fixed;
    bottom: 0;
    z-index: 1000;
    background: black;
}
.stTextInput, .stMarkdown {
    margin-bottom: 1rem;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="/img/robot.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="/img/client.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
