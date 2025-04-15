import streamlit as st
import random
import speech_recognition as sr
from gtts import gTTS
import tempfile

# --- Helper Functions ---
def get_response(user_input):
    # Predefined responses with 50 possible replies
    responses = {
        "hi": ["Hello! How can I help you today?", "Hey there! How's it going?", "Hi! What's on your mind today?", "Greetings! How can I assist you?", "Hey! How are you feeling?"],
        "how are you": ["I'm doing great, thank you! How about you?", "I'm feeling good, thanks for asking!", "I'm well! How are you feeling today?", "I'm doing great, thanks for asking!", "All systems are go here! How are you doing?"],
        "sad": ["I'm really sorry you're feeling this way, but you're not alone. Want to talk about it?", "It's okay to feel sad sometimes. I'm here if you need me.", "I'm sorry you're feeling sad. Would you like some support or tips?", "Sadness is part of being human, and I'm here to listen if you want to share.", "It's tough to feel down. How can I help you feel better?"],
        "stressed": ["Stress is tough, but you can get through it. Focus on one thing at a time.", "Take a deep breath. Stress can be managed with small steps.", "Stress is temporary. You can do this! Let's break things down together.", "I know it's hard, but you are stronger than this stress. Let's take it one step at a time.", "Stay calm. Stress can be controlled with mindfulness and rest."],
        "motivated": ["You are capable of amazing things! Stay focused and keep going!", "Push through! Every step you take brings you closer to your goal.", "Believe in yourself! You have the strength to overcome anything.", "Never give up! You are closer to your goal than you think.", "You've got this! Keep moving forward, no matter how small the step."],
        "fitness": ["Exercise is key to both body and mind. Try to stay active every day!", "Fitness is a journey, not a destination. Start small and keep going!", "Exercise releases endorphins, making you feel better. Move your body regularly!", "A healthy body is essential for a healthy mind. Keep moving and stay strong.", "Take care of your body, it's the only place you have to live! Get active every day."],
        "hello": ["Hi there! How can I help you today?", "Hey! How’s it going?", "Hello, friend! What’s on your mind?", "Hi! I’m here to talk and listen.", "Hello, how are you doing today?"],
        "thank you": ["You're welcome! I'm always here for you.", "No problem! I'm glad I could help.", "Anytime! Let me know if you need anything else.", "You're welcome! Take care.", "Happy to help! Don’t hesitate to ask again."],
        "goodbye": ["Goodbye! Take care of yourself!", "See you soon! Stay strong!", "Goodbye! I’m always here if you need to talk.", "Take care! Remember, you are not alone.", "Wishing you the best! I’ll be here whenever you need me."],
        "bored": ["Boredom can be a sign to try something new. Want to explore something together?", "How about a quick break? Maybe try stretching or stepping outside.", "Try doing something creative, like drawing, reading, or even dancing!", "It's normal to feel bored sometimes. Let's come up with something fun to do!", "Why not start a new hobby? It might help with the boredom."],
        "angry": ["I'm sorry you're feeling angry. Would you like to share what's going on?", "Anger is a natural emotion. Take a deep breath, and let's talk about it.", "It’s okay to feel angry, but let’s try to calm down together. How can I help?", "Anger can be tough, but you have control over it. Let’s talk about it.", "Take a moment to breathe deeply. Would you like to talk about what made you angry?"],
        "confused": ["Feeling confused is okay. Let's work through it together.", "Confusion is temporary. Take it one step at a time, and you'll understand.", "I’m here to help! Tell me what’s on your mind, and we’ll sort it out.", "Don’t worry, confusion is part of the process. Let’s figure it out together.", "It’s normal to feel confused. Take your time, and let's talk it through."],
        "happy": ["I’m so glad to hear you're happy! What’s making you feel this way?", "That's wonderful! I’m so happy for you.", "Happy feelings are always welcome! What’s bringing you joy?", "It’s great to hear you’re feeling happy! Keep riding that wave of positivity.", "Happiness is contagious! Keep smiling and spreading good vibes."],
        "alone": ["I’m here with you, you’re not alone. Would you like to talk?", "It’s okay to feel alone sometimes. I’m here to listen whenever you need.", "Being alone can be tough, but know that I’m here for you.", "Sometimes it feels lonely, but you are never truly alone. I’m here for you.", "You might feel alone, but there are always people who care. I'm one of them."],
        "tired": ["Rest is important. Maybe it's time to take a break.", "Being tired is a sign to rest. It’s okay to take time for yourself.", "It’s okay to feel tired. Take a break and recharge.", "When you're tired, rest is key. Take it easy for a bit and come back stronger.", "Listen to your body. If you’re tired, it’s time to give yourself some rest."],
        "love": ["Love is a beautiful thing! It’s great to talk about what you care for.", "Love is powerful and can heal. I hope you’re surrounded by love.", "Love brings light to the darkest days. Let’s talk more about it.", "Love and kindness are essential for well-being. What’s on your heart?", "Love is a wonderful feeling, and I’m glad you’re thinking of it."],
        "hope": ["Hope is everything. Always keep hope alive, even in tough times.", "Hope keeps us going. I hope you find peace and strength today.", "Never lose hope! Every day brings a new possibility.", "Hope is the light that guides us through tough times. Keep believing.", "Hope is the fuel that powers our dreams. Stay hopeful!"],
        "grateful": ["Gratitude is a powerful feeling. What are you thankful for today?", "Gratitude makes everything brighter. Keep counting your blessings.", "Being grateful helps us stay positive. What are you grateful for?", "Gratitude is the key to happiness. Appreciate the little things.", "Grateful hearts are happy hearts. Take a moment to reflect on what you're thankful for."],
        "fear": ["It’s okay to be afraid. Let’s talk about what’s scaring you.", "Fear is a natural emotion. Take a deep breath and let’s face it together.", "Fear is temporary, but your strength is permanent. Let’s work through it.", "Feeling afraid is part of life, but together, we can conquer it.", "Fear can be overwhelming, but we can tackle it one step at a time."],
        "anxiety": ["Anxiety can be tough, but you don’t have to face it alone. Let’s talk.", "Breathe deeply. Anxiety can be managed with the right steps.", "Anxiety might feel strong, but you are stronger. We can handle it together.", "I’m here to help you calm your nerves. Let’s work through it step by step.", "Anxiety doesn’t define you. You are capable of overcoming it."],
        "calm": ["Let’s focus on staying calm together. Take deep breaths.", "Calm is the key to clarity. Let’s take a moment to relax.", "Relax and take a few deep breaths. You are in control.", "Calmness brings clarity. Let’s slow down and breathe.", "Stay calm. Everything will work out, step by step."],
        "peace": ["Peace begins with a deep breath. Let’s find your inner calm.", "Peace is what you deserve. Let’s focus on finding it together.", "Take a moment for peace. Relax and let go of your stress.", "Peace comes from within. Let’s focus on what calms your mind.", "In the midst of chaos, peace can still be found. Let’s search for it."],
        "grief": ["Grief is a heavy burden, but it’s okay to feel. Would you like to talk about it?", "It’s hard to deal with grief, but I’m here to listen whenever you're ready.", "Grief takes time to heal. Let’s take things slowly and talk it through.", "Grief is a part of life, and you don’t have to carry it alone. I'm here for you.", "It’s okay to feel grief. Take your time, and let’s share your feelings."],
        "recovery": ["Recovery is a journey. Take it one step at a time.", "Healing starts with small steps. You are doing great.", "Recovery takes time, but I’m here to support you every step of the way.", "Your strength is inspiring. Keep going with your recovery.", "Stay strong! Recovery is possible, and you’re on the right path."],
        "self-care": ["Self-care is important. Have you done something kind for yourself today?", "Remember to take care of yourself, both physically and mentally.", "Self-care isn’t selfish, it’s necessary. What can you do for yourself today?", "Treat yourself with kindness and respect. Self-care is vital for your well-being.", "Taking care of yourself helps you take care of others too. Make time for self-care."],
        "friends": ["Friends are a wonderful support system. Do you have someone to talk to?", "Having good friends is essential. Who’s your best friend?", "Friendship is a beautiful bond. Let’s cherish those we love.", "Friends lift us up when we’re down. Be sure to spend time with the people who care about you.", "Good friends make everything easier. Who are you spending time with today?"],
    }

    # Get the response based on user input and randomize it for variety
    response_list = responses.get(user_input.lower())
    if response_list:
        return random.choice(response_list)
    else:
        return "I'm here to listen, feel free to share more."

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
