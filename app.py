import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="AI Software Engineering Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Software Engineering Agent")
st.write("Analyze a repository and get suggested code changes.")

repo_url = st.text_input(
    "Repository",
    value="https://github.com/DoEhab/pay_service"
)

task = st.text_area(
    "What do you want to change?",
    placeholder="Example: Add idempotency support to the payment creation endpoint.",
    height=150
)

if st.button("🔍 Analyze & Suggest Changes", type="primary"):

    if not task.strip():
        st.warning("Please enter a task.")
    else:
        with st.spinner("Analyzing repository..."):

            try:
                result = run_agent(repo_url, task)

                st.success("Analysis completed!")

                st.subheader("Suggested Changes")
                st.markdown(result)

            except Exception as e:
                st.error(f"Error: {e}")