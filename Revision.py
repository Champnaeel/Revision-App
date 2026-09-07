from typing import Annotated
from autogen import AssistantAgent, UserProxyAgent
import streamlit as st
from pathlib import Path
from pypdf import PdfReader

api = st.secrets["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"]
st.title("Revision app")

messager = "You're a teacher to help students revise and improve on their weaknesses before their exams"

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm_config = {"model": "openai/gpt-oss-120b", "api_key": api, "api_type": "groq"}

assistant = AssistantAgent(
    llm_config=llm_config,
    name="Tutor1",
    system_message=messager
)

work_dir = Path("coding_workspace")
work_dir.mkdir(exist_ok=True)

user_proxy = UserProxyAgent(
    name="proxy",
    human_input_mode="ALWAYS",

    code_execution_config=False,
    max_consecutive_auto_reply=1
)


@assistant.register_for_llm(description="Read the pdf that the student sends you")
@user_proxy.register_for_execution()
def pdf_reader(pdf:Annotated[str,"The pdf link that the student sends you"]):
    Reader = PdfReader(pdf)



if prompt := st.chat_input("What do you want the agents to do?"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            chat_res = user_proxy.initiate_chat(
                assistant,
                message=prompt,
                max_turns=1
            )

            response = chat_res.summary
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})