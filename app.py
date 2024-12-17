#Fined Tuned Version of the code.

import streamlit as st
import google.generativeai as genai

# API Key Configuration
GOOGLE_API_KEY = "AIzaSyAW_TEQlzUQnpEtfZMvs45McmCXnwQw7RQ"
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initialization
model = genai.GenerativeModel("gemini-pro")


def generate_sql_query(user_input):
    """
    Generate SQL query using the AI model.
    """
    template = """
        Create a SQL query based on the following prompt:
        '''
        {text_input}
        '''
        I just want a SQL query.
    """
    formatted_template = template.format(text_input=user_input)
    response = model.generate_content(formatted_template)
    return response.text.replace("```", "").strip()


def generate_expected_output(sql_query):
    """
    Generate expected tabular output for the SQL query.
    """
    template = """
        What would be the expected response of this SQL query Snippet:
        '''
        {sql_query}
        '''
        Provide a sample vertical tabular response with no explanation.
    """
    formatted_template = template.format(sql_query=sql_query)
    response = model.generate_content(formatted_template)
    return response.text.strip()


def generate_explanation(sql_query):
    """
    Generate explanation for the SQL query.
    """
    template = """
        Explain this SQL query:
        '''
        {sql_query}
        '''
        Provide the simplest explanation possible.
    """
    formatted_template = template.format(sql_query=sql_query)
    response = model.generate_content(formatted_template)
    return response.text.strip()


def main():
    st.set_page_config(page_title="SQL Query Generator 🌐", page_icon=":robot", layout="centered")
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>SQL Query Generator 🌐</h1>
            <h3>Transform Plain English into SQL Queries</h3>
            <p>This tool helps you generate SQL queries with expected outputs and clear explanations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input Section
    text_input = st.text_area(
        "Enter your query in plain English here:",
        placeholder="Example: Get all employees earning more than $5000 in the Sales department.",
    )

    submit = st.button("Generate SQL Query 🚀")

    if submit:
        if not text_input.strip():
            st.error("Please enter a valid query in plain English!")
        else:
            with st.spinner("Generating SQL Query, Expected Output, and Explanation..."):
                try:
                    # Step 1: Generate SQL Query
                    sql_query = generate_sql_query(text_input)

                    # Step 2: Generate Expected Output
                    expected_output = generate_expected_output(sql_query)

                    # Step 3: Generate Explanation
                    explanation = generate_explanation(sql_query)

                    # Display Results in Sections
                    with st.expander("📝 SQL Query", expanded=True):
                        st.code(sql_query, language="sql")

                    with st.expander("📊 Expected Output", expanded=False):
                        st.text(expected_output)

                    with st.expander("💡 Explanation", expanded=False):
                        st.markdown(explanation)

                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
