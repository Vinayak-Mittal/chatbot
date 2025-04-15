import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

# --- Helper Functions ---
def get_response(user_input):
    # Predefined responses
    responses = {
        "hi": "Hello! How can I help you today?",
        "how are you": "I'm doing well, thank you for asking! How about you?",
        "sad": "I'm really sorry you're feeling this way, but remember, you're not alone. Talking about it can help!",
        "stressed": "It's okay to feel stressed sometimes. Take a deep breath and focus on one thing at a time.",
        "motivated": "You are stronger than you think! Keep pushing forward, and success will follow.",
        "fitness": "Remember, regular exercise is great for both the body and mind! Try to stay active every day."
    }

    return responses.get(user_input.lower(), "I'm here to listen, feel free to share more.")

def speak_response(response):
    # Convert the response to speech using gTTS
    tts = gTTS(text=response, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# --- Streamlit UI ---
st.title("MindMate - Your Mental Health Companion")
st.markdown("### Chat with me for support, motivation, and tips!")

# Chat history storage
if "history" not in st.session_state:
    st.session_state.history = []

# Input box and send button
user_input = st.text_input("Type your message here", "")

if user_input:
    response = get_response(user_input)
    
    # Store conversation history
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"MindMate: {response}")
    
    # Display chat history
    for message in st.session_state.history:
        st.write(message)

    # Output response as audio
    speak_response(response)

# --- Daily Motivation Button ---
if st.button('Get Daily Motivation'):
    motivation_quotes = [
        "Believe in yourself! The sky's the limit.",
        "Success doesn’t come from what you do occasionally, it comes from what you do consistently.",
        "Don't stop when you're tired. Stop when you're done.",
        "The only way to do great work is to love what you do."
    ]
    motivational_quote = motivation_quotes[st.session_state.history.count('You: motivated') % len(motivation_quotes)]
    st.write(f"**Motivation for today:** {motivational_quote}")

    # Output motivation as speech
    speak_response(motivational_quote)

# --- Fitness Tips Button ---
if st.button('Get Fitness Tip'):
    fitness_tips = [
        "Exercise daily for at least 30 minutes to keep your body and mind fit.",
        "Drinking enough water is crucial for overall health, especially before and after workouts.",
        "Don't forget to warm up before and cool down after your workout to avoid injury.",
        "Remember, consistency is key. A small workout every day is better than one big workout a week."
    ]
    fitness_tip = fitness_tips[st.session_state.history.count('You: fitness') % len(fitness_tips)]
    st.write(f"**Fitness Tip for today:** {fitness_tip}")

    # Output fitness tip as speech
    speak_response(fitness_tip)











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
