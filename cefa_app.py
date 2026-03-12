import streamlit as st
import json
import random

st.set_page_config(page_title="CEFA Exam Trainer", page_icon="📊")

st.title("📊 CEFA Legal Exam Trainer")

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Session state
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.questions = []

# Start screen
if not st.session_state.started:

    st.write("Practice CEFA Legal exam questions.")

    if st.button("🚀 Start Exam"):
        st.session_state.started = True
        st.session_state.questions = random.sample(questions, len(questions))
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.rerun()

# Exam mode
else:

    q_list = st.session_state.questions
    q_index = st.session_state.q_index

    progress = q_index / len(q_list)
    st.progress(progress)

    if q_index < len(q_list):

        q = q_list[q_index]

        st.subheader(f"Question {q_index + 1} / {len(q_list)}")

        # biztosítjuk a sortöréseket az I., II., III., IV. soroknál
        formatted_question = q["question"].replace(" II.", "\n\nII.") \
                                          .replace(" III.", "\n\nIII.") \
                                          .replace(" IV.", "\n\nIV.")

        st.markdown(formatted_question)

        choice = st.radio(
            "Select your answer:",
            q["options"],
            key=f"q_{q_index}"
        )

        if st.button("Submit Answer"):

            user_index = q["options"].index(choice)

            if user_index == q["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1

            else:
                correct_index = q["answer"]
                correct_letter = chr(97 + correct_index)
                correct_text = q["options"][correct_index]

                st.error(f"❌ Wrong. Correct answer: {correct_letter}) {correct_text}")

                if q.get("explanation"):
                    st.write("Explanation:", q["explanation"])

            st.session_state.q_index += 1
            st.rerun()

    else:

        st.subheader("🎉 Exam Finished")

        score = st.session_state.score
        total = len(q_list)
        percent = round(score / total * 100, 1)

        st.write(f"Score: **{score} / {total}**")
        st.write(f"Result: **{percent}%**")

        if percent >= 70:
            st.success("✅ Passed!")
        else:
            st.error("❌ Try again")

        if st.button("🔄 Restart Exam"):
            st.session_state.started = False
            st.rerun()
