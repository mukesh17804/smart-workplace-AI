import streamlit as st
import pandas as pd
import nltk
import pyttsx3
from datetime import datetime, timedelta
import random

# Ensure nltk tokenizer data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

from nltk.tokenize import word_tokenize

# -----------------------------------------------------
# 🧠 Initialize
# -----------------------------------------------------
st.set_page_config(page_title="Smart Workplace AI Assistant", layout="wide")
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -----------------------------------------------------
# 🎯 Header
# -----------------------------------------------------
st.title("🤖 Smart Workplace AI Assistant")
st.subheader("AI-powered Intelligent Assistant for the Modern Office 🧠")
st.write("This AI Assistant reads your emails and chat messages (simulated), auto-detects meetings, tasks, and deadlines — and provides real-time insights & voice alerts.")

# -----------------------------------------------------
# 📧 Simulated Inputs
# -----------------------------------------------------
with st.expander("📩 Simulated Emails / Chat Messages"):
    sample_data = [
        "Meeting with Product Team scheduled at 3 PM tomorrow.",
        "Reminder: Submit project report by Friday evening.",
        "Can we reschedule our client discussion to next Monday?",
        "Prepare slides for AI workshop due by Wednesday.",
        "Budget review meeting today at 4 PM with Finance team."
    ]
    df = pd.DataFrame(sample_data, columns=["Inbox / Chat Messages"])
    st.table(df)

# -----------------------------------------------------
# 🔍 NLP Analyzer
# -----------------------------------------------------
def analyze_text(text):
    words = word_tokenize(text.lower())
    meeting_keywords = ["meeting", "schedule", "discussion", "call", "conference"]
    task_keywords = ["submit", "prepare", "complete", "send", "finish"]
    date_keywords = ["today", "tomorrow", "monday", "tuesday", "wednesday", "thursday", "friday"]

    analysis = {"Meetings": False, "Tasks": False, "Deadline": "N/A"}
    for w in words:
        if w in meeting_keywords:
            analysis["Meetings"] = True
        if w in task_keywords:
            analysis["Tasks"] = True
        if w in date_keywords:
            analysis["Deadline"] = w
    return analysis

# -----------------------------------------------------
# ⚙️ AI Processing
# -----------------------------------------------------
results = []
for msg in sample_data:
    info = analyze_text(msg)
    results.append({
        "Message": msg,
        "Meeting": "✅" if info["Meetings"] else "❌",
        "Task": "✅" if info["Tasks"] else "❌",
        "Deadline": info["Deadline"]
    })

results_df = pd.DataFrame(results)
st.markdown("### 📊 AI Analysis Results")
st.dataframe(results_df, use_container_width=True)

# -----------------------------------------------------
# 📅 Smart Scheduler
# -----------------------------------------------------
st.markdown("### 🗓️ Smart Meeting Scheduler")
today = datetime.now()
schedule_data = []

for index, row in results_df.iterrows():
    if row["Meeting"] == "✅":
        meet_time = today + timedelta(hours=random.randint(1, 48))
        schedule_data.append({
            "Event": row["Message"],
            "Scheduled Time": meet_time.strftime("%Y-%m-%d %H:%M")
        })

if schedule_data:
    st.success("Meetings automatically detected and scheduled ✅")
    st.table(schedule_data)
    speak("Meetings have been successfully scheduled.")
else:
    st.warning("No meetings detected.")

# -----------------------------------------------------
# 📈 Productivity Dashboard
# -----------------------------------------------------
st.markdown("### 📊 Productivity Dashboard")
meeting_count = results_df["Meeting"].value_counts().get("✅", 0)
task_count = results_df["Task"].value_counts().get("✅", 0)
progress = (task_count / len(results_df)) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Meetings Detected", meeting_count)
col2.metric("Tasks Identified", task_count)
col3.metric("Task Progress (%)", f"{progress:.2f}%")

# -----------------------------------------------------
# 📢 Voice Alert System
# -----------------------------------------------------
if progress >= 60:
    speak("Great work! Productivity is improving.")
else:
    speak("You have pending tasks. Please check your to-do list.")

# -----------------------------------------------------
# 💬 AI Chatbot
# -----------------------------------------------------
st.markdown("### 💬 Smart Workplace Chatbot")

user_input = st.text_input("Ask your assistant:", placeholder="e.g., Show my meetings for tomorrow")
if user_input:
    if "meeting" in user_input.lower():
        st.write("📅 You have meetings scheduled as shown above.")
        speak("Here are your scheduled meetings.")
    elif "task" in user_input.lower():
        st.write("🧾 You have pending tasks in your AI task tracker.")
        speak("Here are your pending tasks.")
    elif "hello" in user_input.lower():
        st.write("👋 Hello Mukesh! How can I assist you today?")
        speak("Hello Mukesh! How can I assist you today?")
    else:
        st.write("🤔 Sorry, I didn’t understand that. Try asking about meetings or tasks.")
        speak("Sorry, I didn’t understand that.")

# -----------------------------------------------------
# 🔁 Auto Refresh (Fixed)
# -----------------------------------------------------
st.button("🔄 Refresh Assistant", on_click=st.rerun)

# -----------------------------------------------------
# ✅ Footer
# -----------------------------------------------------
st.markdown("---")
st.caption("Developed by Mukesh Kanna — Smart Workplace AI Assistant 🧠 | Powered by Python + NLP + Streamlit")
