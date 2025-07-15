def render_chat_bubble(user_msg, bot_msg):
    return f"""
    <div class='chat-bubble user'><div>{user_msg}</div></div>
    <div class='chat-bubble bot'><div>{bot_msg}</div></div>
    """
