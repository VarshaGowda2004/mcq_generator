import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
import pandas as pd
import traceback    
from dotenv import load_dotenv
import streamlit as st

from mcq_generator.utils import read_file, get_table_data
from mcq_generator.logger import logging
from mcq_generator.mcqgenerator import generate_evaluate_chain
from langchain_community.callbacks import get_openai_callback


# Load JSON file
with open(r"C:\Users\varsh\mcq\response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

st.title("MCQ Generator using LangChain and OpenAI")

with st.form("user_input_form"):
    uploaded_file = st.file_uploader("Upload a PDF or Text file", type=["pdf", "txt"])
    number_of_mcqs = st.number_input("Number of MCQs to generate", min_value=1, max_value=20, value=5)
    subject = st.text_input("Subject for the MCQs")
    tone = st.selectbox("Complexity", ["simple", "moderate", "difficult"])
    submit_button = st.form_submit_button("Generate MCQs")

if submit_button and uploaded_file is not None and number_of_mcqs and subject and tone:
    with st.spinner("Processing..."):
        try:
            # Read the file content
            text = read_file(uploaded_file)
            st.write("File content successfully read.")

            # Count tokens
            with get_openai_callback() as cb:
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": number_of_mcqs,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

            print(f"Total tokens used: {cb.total_tokens}, Cost: {cb.total_cost}, Completion: {cb.completion_tokens}, Prompt: {cb.prompt_tokens}")

            if isinstance(response, dict):
                st.success("MCQs generated successfully!")
                quiz = response.get("quiz", "No quiz generated.")
                if quiz:
                    quiz_table_data = get_table_data(quiz)
                    if quiz_table_data:
                        df = pd.DataFrame(quiz_table_data)
                        df.index = df.index + 1
                        st.table(df)
                        st.text_area(label="Review", value=response.get("review", ""))
                    else:
                        st.error("Error in formatting table data.")
                else:
                    st.warning("No quiz content found in response.")
            else:
                st.warning("Response is not in expected format.")
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("An error occurred while processing the file.")
