import streamlit as st
import random

st.set_page_config(page_title="MindMate - Mental Health Chatbot", page_icon="💬")
st.title("💬 MindMate - Your Mental Health Companion")
st.write("I'm here to talk. Just type how you're feeling. 💙")

# Predefined replies
sad_replies = [
    "I'm really sorry you're feeling this way. You're not alone. 🌧️",
    "It’s okay to feel sad sometimes. Let it out. 💙",
    "Even rainy days end eventually. 🌈",
    "You’re doing better than you think. 🤗",
    "Want to talk about what's making you sad?",
    "You have permission to rest. You're human. 🧠",
]

anxious_replies = [
    "Take a deep breath. You’ve got this. 🌬️",
    "Anxiety can be overwhelming. You're not alone.",
    "Let’s take it one step at a time. 🪜",
    "Try grounding yourself. 5 things you can see, 4 you can touch...",
    "You’re safe here. Want to share what's on your mind?",
]

stress_replies = [
    "It sounds like you’ve been under pressure. 🧠",
    "You don’t have to carry everything alone. 🤝",
    "Even taking 5 minutes to breathe can help. 💨",
    "I’m proud of you for opening up.",
    "What’s the heaviest thing on your mind right now?",
]

generic_replies = [
    "Tell me more about what you're feeling. 💭",
    "I’m listening. No judgment, just support. 🤗",
    "Let it out, I’m here for you.",
    "What do you feel like you need most right now?",
    "Thanks for trusting me with your thoughts.",
]

greeting_replies = [
    "Hey! How are you feeling today?",
    "Hi there! I’m here for you anytime. 😊",
    "Hello! Want to talk about anything?",
    "Hey, friend. You’re safe here. ❤️",
    "What's on your mind today?",
]

thank_you_replies = [
    "You're very welcome! Glad I could help. 💙",
    "Here anytime you need me. 😊",
    "Take care of yourself. You matter. 💖",
    "No problem at all, happy to help. 🌟",
    "Stay strong and kind to yourself. 🌼",
]

bye_replies = [
    "Take care of yourself. I'm always here. 👋",
    "Goodbye! Remember to breathe and rest. 🫶",
    "Hope you feel a little better. 💫",
    "Sending you peace and strength. ✨",
    "Bye for now! Come back whenever you want to talk. 🧠",
]

tips = [
    "Try journaling your thoughts for 5 minutes. ✍️",
    "Step outside for fresh air, even for a few minutes. 🌿",
    "Drink water and stretch a bit. 🧘",
    "Write down what you're grateful for. 🌟",
    "Listen to your favorite calming music. 🎵",
    "Speak kindly to yourself — you're trying. 💗",
]

# Message analyzer
def get_bot_reply(user_input):
    user_input = user_input.lower()

    if any(word in user_input for word in ["sad", "unhappy", "cry", "down", "blue", "hurt"]):
        return random.choice(sad_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

    elif any(word in user_input for word in ["anxious", "panic", "nervous", "scared", "afraid"]):
        return random.choice(anxious_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

    elif any(word in user_input for word in ["stress", "overwhelmed", "tired", "burned", "exhausted"]):
        return random.choice(stress_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

    elif any(word in user_input for word in ["hi", "hello", "hey"]):
        return random.choice(greeting_replies)

    elif "thank" in user_input:
        return random.choice(thank_you_replies)

    elif any(word in user_input for word in ["bye", "goodbye", "see you"]):
        return random.choice(bye_replies)

    else:
        return random.choice(generic_replies)

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box with form to prevent session state errors
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    bot_reply = get_bot_reply(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("MindMate", bot_reply))

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**👤 You:** {msg}")
    else:
        st.markdown(f"**🤖 MindMate:** {msg}")
