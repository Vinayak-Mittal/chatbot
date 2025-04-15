import streamlit as st
import random
import speech_recognition as sr
import pyttsx3
import os

# Set page config
st.set_page_config(page_title="MindMate - Mental Health Chatbot", page_icon="🧠", layout="centered")

# Inject CSS for custom theme
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #0f1117;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        input, .stTextInput>div>div>input {
            background-color: #1c1f26;
            color: white;
        }
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #357ABD;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #E5E5E5;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 MindMate")
st.markdown("### Your Mental Health Companion - Now with Voice Support 🎙️")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Predefined replies
sad_replies = [
    "I'm really sorry you're feeling this way. You're not alone. 🌧️",
    "Even rainy days end eventually. 🌈",
    "Let it out. You’re not weak for feeling sad. 💙",
    "You're not a burden. You're a human being. 🤗"
]
anxious_replies = [
    "Take a deep breath. You’ve got this. 🌬️",
    "Let’s take it one step at a time. 🪜",
    "Ground yourself. 5 things you see, 4 you touch...",
    "Even your worst days only last 24 hours. ⏳"
]
stress_replies = [
    "Under pressure? Let’s unload it together. 💼",
    "You don’t have to do it all at once. 🧠",
    "Pause. Breathe. You’re allowed to rest. 🧘",
    "What’s stressing you out the most?"
]
generic_replies = [
    "Tell me more. I'm here to listen. 👂",
    "You are strong for sharing. 💪",
    "Your feelings matter. 🫶",
    "Let’s talk it through. What’s up?"
]
greeting_replies = [
    "Hi there! How are you doing today?",
    "Hello! What’s on your mind? 😊",
    "Hey friend, want to talk about anything?",
]
thank_you_replies = [
    "You're welcome. You’re doing great. 💙",
    "Glad I could help. Take care. 😊"
]
bye_replies = [
    "Goodbye! Be kind to yourself. 👋",
    "Take care! I’m here anytime. ❤️"
]
tips = [
    "Try journaling your thoughts. ✍️",
    "Step outside for 5 mins. Fresh air helps. 🌿",
    "Drink water. Stretch a bit. 🧘",
    "Play calming music. 🎵"
]
motivational_quotes = [
    "You are braver than you believe. 💪",
    "Tough times don’t last. You do. 🌟",
    "Your story isn’t over yet. ✍️"
]
fitness_tips = [
    "Walk for 10 minutes daily. 🚶",
    "Stretch every hour. 🧘‍♂️",
    "Hydrate with 2-3L water daily. 💧",
]

# Analyzer
def get_bot_reply(user_input):
    ui = user_input.lower()
    if any(x in ui for x in ["sad", "cry", "depressed", "hurt"]):
        return random.choice(sad_replies) + "\n💡 Tip: " + random.choice(tips)
    elif any(x in ui for x in ["anxious", "panic", "scared", "worried"]):
        return random.choice(anxious_replies) + "\n💡 Tip: " + random.choice(tips)
    elif any(x in ui for x in ["stress", "tired", "burned", "overworked"]):
        return random.choice(stress_replies) + "\n💡 Tip: " + random.choice(tips)
    elif any(x in ui for x in ["hi", "hello", "hey"]):
        return random.choice(greeting_replies)
    elif "thank" in ui:
        return random.choice(thank_you_replies)
    elif any(x in ui for x in ["bye", "goodbye"]):
        return random.choice(bye_replies)
    else:
        return random.choice(generic_replies)

# Voice Input Button
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        try:
            audio = r.listen(source, timeout=5)
            user_voice_input = r.recognize_google(audio)
            st.success(f"You said: {user_voice_input}")
            return user_voice_input
        except sr.UnknownValueError:
            st.error("Couldn't understand. Try again.")
        except sr.RequestError:
            st.error("Speech Recognition service unavailable.")
    return ""

# Buttons
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    if st.button("🌟 Daily Motivation"):
        quote = random.choice(motivational_quotes)
        st.success(f"Quote: _{quote}_")
        speak(quote)

with col3:
    if st.button("💪 Fitness Tip"):
        tip = random.choice(fitness_tips)
        st.info(f"Fitness Tip: {tip}")
        speak(tip)

# Input Methods
st.markdown("### Talk to me 💬")
col4, col5 = st.columns([3, 1])
with col4:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type something...")
        submit = st.form_submit_button("Send")
with col5:
    if st.button("🎤 Voice Input"):
        user_input = voice_input()
        if user_input:
            submit = True

if submit and user_input:
    bot_reply = get_bot_reply(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("MindMate", bot_reply))
    speak(bot_reply)

# Display Chat History
st.markdown("---")
st.subheader("📜 Chat History")
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧍 You:** {msg}")
    else:
        st.markdown(f"**🤖 MindMate:** {msg}")
















# import streamlit as st
# import random

# st.set_page_config(page_title="MindMate - Mental Health Chatbot", page_icon="💬")
# st.title("💬 MindMate - Your Mental Health Companion")
# st.write("I'm here to talk. Just type how you're feeling. 💙")

# # Predefined replies
# sad_replies = [
#     "I'm really sorry you're feeling this way. You're not alone. 🌧️",
#     "It’s okay to feel sad sometimes. Let it out. 💙",
#     "Even rainy days end eventually. 🌈",
#     "You’re doing better than you think. 🤗",
#     "Want to talk about what's making you sad?",
#     "You have permission to rest. You're human. 🧠",
# ]

# anxious_replies = [
#     "Take a deep breath. You’ve got this. 🌬️",
#     "Anxiety can be overwhelming. You're not alone.",
#     "Let’s take it one step at a time. 🪜",
#     "Try grounding yourself. 5 things you can see, 4 you can touch...",
#     "You’re safe here. Want to share what's on your mind?",
# ]

# stress_replies = [
#     "It sounds like you’ve been under pressure. 🧠",
#     "You don’t have to carry everything alone. 🤝",
#     "Even taking 5 minutes to breathe can help. 💨",
#     "I’m proud of you for opening up.",
#     "What’s the heaviest thing on your mind right now?",
# ]

# generic_replies = [
#     "Tell me more about what you're feeling. 💭",
#     "I’m listening. No judgment, just support. 🤗",
#     "Let it out, I’m here for you.",
#     "What do you feel like you need most right now?",
#     "Thanks for trusting me with your thoughts.",
# ]

# greeting_replies = [
#     "Hey! How are you feeling today?",
#     "Hi there! I’m here for you anytime. 😊",
#     "Hello! Want to talk about anything?",
#     "Hey, friend. You’re safe here. ❤️",
#     "What's on your mind today?",
# ]

# thank_you_replies = [
#     "You're very welcome! Glad I could help. 💙",
#     "Here anytime you need me. 😊",
#     "Take care of yourself. You matter. 💖",
#     "No problem at all, happy to help. 🌟",
#     "Stay strong and kind to yourself. 🌼",
# ]

# bye_replies = [
#     "Take care of yourself. I'm always here. 👋",
#     "Goodbye! Remember to breathe and rest. 🫶",
#     "Hope you feel a little better. 💫",
#     "Sending you peace and strength. ✨",
#     "Bye for now! Come back whenever you want to talk. 🧠",
# ]

# tips = [
#     "Try journaling your thoughts for 5 minutes. ✍️",
#     "Step outside for fresh air, even for a few minutes. 🌿",
#     "Drink water and stretch a bit. 🧘",
#     "Write down what you're grateful for. 🌟",
#     "Listen to your favorite calming music. 🎵",
#     "Speak kindly to yourself — you're trying. 💗",
# ]

# # Message analyzer
# def get_bot_reply(user_input):
#     user_input = user_input.lower()

#     if any(word in user_input for word in ["sad", "unhappy", "cry", "down", "blue", "hurt"]):
#         return random.choice(sad_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

#     elif any(word in user_input for word in ["anxious", "panic", "nervous", "scared", "afraid"]):
#         return random.choice(anxious_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

#     elif any(word in user_input for word in ["stress", "overwhelmed", "tired", "burned", "exhausted"]):
#         return random.choice(stress_replies) + "\n\n💡 *Tip:* " + random.choice(tips)

#     elif any(word in user_input for word in ["hi", "hello", "hey"]):
#         return random.choice(greeting_replies)

#     elif "thank" in user_input:
#         return random.choice(thank_you_replies)

#     elif any(word in user_input for word in ["bye", "goodbye", "see you"]):
#         return random.choice(bye_replies)

#     else:
#         return random.choice(generic_replies)

# # Chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Input box with form to prevent session state errors
# with st.form(key="chat_form", clear_on_submit=True):
#     user_input = st.text_input("You:")
#     submit_button = st.form_submit_button("Send")

# if submit_button and user_input:
#     bot_reply = get_bot_reply(user_input)
#     st.session_state.chat_history.append(("You", user_input))
#     st.session_state.chat_history.append(("MindMate", bot_reply))

# # Display chat history
# for sender, msg in st.session_state.chat_history:
#     if sender == "You":
#         st.markdown(f"**👤 You:** {msg}")
#     else:
#         st.markdown(f"**🤖 MindMate:** {msg}")
