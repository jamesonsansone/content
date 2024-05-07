import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

if 'article' not in st.session_state:
    st.session_state.article = {
        'introduction': None,
        'benefits': None,
        'FAQ': None
    }
    
# Add a new section dynamically
new_section_name = st.text_input("Add a new section (e.g., 'Risks'):")
if st.button("Add Section"):
    if new_section_name and new_section_name not in st.session_state.article:
        st.session_state.article[new_section_name] = None
        st.success(f"Section '{new_section_name}' added.")
    else:
        st.error("Please enter a unique section name.")

# Input for keyword
keyword = st.text_input("Enter the main keyword for the article:")

# Manual outline input
outline_input = st.text_area("Paste your outline here:", height=300, key="outline")
if outline_input:
    st.session_state.outline = outline_input  # Save the manually entered outline

# Display the manually entered outline if it exists
if st.session_state.outline:
    st.markdown("**Outline:**")
    st.write(st.session_state.outline)

# Dynamic dropdown that includes any added sections
section_options = list(st.session_state.article.keys())
section_key = st.selectbox("Choose the section to generate", options=section_options)
section_prompt = st.text_area(f"Enter your prompt for the {section_key} section:", height=300)

# Generate content for the selected section
if st.button(f"Generate {section_key.capitalize()}"):
    if keyword and section_prompt:
        content = generate_section_from_openai(section_key, keyword, section_prompt)
        st.session_state.article[section_key] = content
        st.markdown(f"**{section_key.capitalize()} Section:**")
        st.write(content)
    else:
        st.error("Please ensure a keyword and prompt are provided.")

# Display the entire article so far
if st.button("Show Entire Article"):
    for key, value in st.session_state.article.items():
        if value:
            st.subheader(f"{key.capitalize()} Section:")
            st.write(value)

# Sidebar for style reference
with st.sidebar:
    st.header("Style Reference")
    st.write("Use the following sample as a guideline for writing style:")
    st.code("401(k): A type of retirement plan that's sponsored by an employer. "
            "While 401(k) plan details differ between employers, they often include "
            "tax advantages and employee contributions that are deducted from your paycheck.")

# # def fetch_serp_data(keyword):
# #     search = serpapi.search({
# #         "engine": "google",
# #         "q": keyword,
# #         "api_key": os.getenv('SERPAPI_KEY')
# #     })
    
# #     try:
# #         results = search.get_dict()  # This should work if the library and API key are correctly set up
# #     except Exception as e:
# #         print("Error retrieving data from SERPAPI:", e)
# #         return None
# #     if "organic_results" not in results:
# #         print(f"No organic results found for keyword: {keyword}")
# #         return None
    
# #     organic_results = results['organic_results']
# #     related_questions = results.get('related_questions', [])
    
# #     titles = [result['title'] for result in organic_results[:5] if 'title' in result]
# #     snippets = [result['snippet'] for result in organic_results[:5] if 'snippet' in result]
# #     questions = [question['question'] for question in related_questions if 'question' in question]
    
# #     serp_data = {
# #         "keyword": keyword,
# #         "titles": titles,
# #         "snippets": snippets,
# #         "related_questions": questions
# #     }
    
# #     print("SERP Data Collected From SERPAPI")
# #     print(serp_data)
# #     return serp_data

# # Function to generate outline
# def generate_outline(keyword):
#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": f"""You are an expert in creating content outlines for retirement glossary pages. Your task is to generate a two-level content outline hierarchy based on the provided '{keyword}'. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content. You are writing this article on behalf of Human Interest, a 401(k) retirement plan provider."""
#             },
#             {
#                 "role": "user",
#                 "content": f"""Generate a two-level content outline for a retirement glossary page about '{keyword}'. Be unique and creative.     
#                 The outline should cover the main topics and subtopics related to '{keyword}', focusing on the information found in the SERP titles and snippets. Use a clear and concise structure, with main topics as level-1 items and subtopics as level-2 items. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content."""
#             }
#         ],
#         max_tokens=2000
#     )

#     outline_text = response.choices[0].message.content
#     return outline_text

# # Function to generate content
# def generate_content(keyword, outline_text):
#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """You are a content generation assistant, tasked with creating SEO-optimized glossary entries. Write informative content that simplifies complex financial concepts of retirement planning. The content should:
#                 1. Use clear and accessible language 2. Maintain a neutral and informative tone 3. Include sections like definition, usage, benefits, and related terms 4. Avoid editorial opinions and focus on factual information 6. Do not include conclusion paragraphs 7. Write headlines in sentence case. """
#             },
#             {
#                 "role": "user",
#                 "content": f"""Create an informative, SEO-friendly retirement glossary page about '{keyword}'. Begin with an introduction that provides a clear overview of the topic. This article should not be opinionated.  The article should go into detail on '{keyword}' and describe the '{keyword}'in the context of a retirement glossary term. Make sure to follow the following rules: Your content should use full and complete sentences to expand upon the outline listed below. Use Natural Language processing to write complete semantically related sentences. Ensure that the content is accessible, encouraging, and informative, while maintaining a friendly and reassuring tone. The article should match the tone and language of the retirement planning industry, focusing on simplifying complex concepts, providing practical solutions, and educating readers on key aspects of the topic. Do not include conclusion paragraphs. Write headlines in sentence case. Use the outline below to understand what content we would like you to write about:
#                 Outline: {outline_text}

#                 """
#             }
#         ],
#         max_tokens=3000,#add tokens here
#         temperature=0.0,


#     )
    
#     content_text = response.choices[0].message.content
#     return content_text
