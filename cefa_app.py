import streamlit as st
import json
import random

st.set_page_config(page_title="CEFA Exam Trainer", page_icon="🎓")

st.title("🎓 CEFA Practice")

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

    if "answered" not in st.session_state:
        st.session_state.answered = False

    progress = q_index / len(q_list)
    st.progress(progress)

    # VAN MÉG KÉRDÉS
    if q_index < len(q_list):

        q = q_list[q_index]

        st.subheader(f"Question {q_index + 1} / {len(q_list)}")

        formatted_question = q["question"].replace(" II.", "\n\nII.") \
                                          .replace(" III.", "\n\nIII.") \
                                          .replace(" IV.", "\n\nIV.")

        st.markdown(formatted_question)

        choice = st.radio(
            "Select your answer:",
            q["options"],
            key=f"q_{q_index}",
            disabled=st.session_state.answered
        )

        if not st.session_state.answered:

            if st.button("Submit Answer"):

                user_index = q["options"].index(choice)
                st.session_state.user_index = user_index
                st.session_state.answered = True
                st.rerun()

        if st.session_state.answered:

            user_index = st.session_state.user_index
            correct_index = q["answer"]

            correct_letter = chr(97 + correct_index)
            correct_text = q["options"][correct_index]


            if user_index == correct_index:
                st.success("✅ Correct!")

            if not st.session_state.score_added:
                st.session_state.score += 1
                st.session_state.score_added = True
            else:
                st.error(f"❌ Wrong. Correct answer: {correct_letter}) {correct_text}")

                if q.get("explanation"):
                    st.info(q["explanation"])

            if st.button("Next Question ➡️"):

                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.score_added = False
                st.rerun()

    # NINCS TÖBB KÉRDÉS
    else:

        st.subheader("🎉 Exam Finished")

        score = st.session_state.score
        total = len(q_list)
        percent = round(score / total * 100, 1)

        st.write(f"Score: **{score} / {total}**")
        st.write(f"Result: **{percent}%**")

        if percent >= 60:
            st.success("✅ Passed!")
        else:
            st.error("❌ Try again")

        if st.button("🔄 Restart Exam"):

            st.session_state.started = False
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.rerun()







