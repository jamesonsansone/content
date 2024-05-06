import streamlit as st
from openai import OpenAI
import serpapi
import os
from dotenv import load_dotenv

load_dotenv()
  
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
#SERPAPI_KEY = os.getenv('SERPAPI_KEY')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

# def fetch_serp_data(keyword):
#     search = serpapi.search({
#         "engine": "google",
#         "q": keyword,
#         "api_key": os.getenv('SERPAPI_KEY')
#     })
    
#     try:
#         results = search.get_dict()  # This should work if the library and API key are correctly set up
#     except Exception as e:
#         print("Error retrieving data from SERPAPI:", e)
#         return None
#     if "organic_results" not in results:
#         print(f"No organic results found for keyword: {keyword}")
#         return None
    
#     organic_results = results['organic_results']
#     related_questions = results.get('related_questions', [])
    
#     titles = [result['title'] for result in organic_results[:5] if 'title' in result]
#     snippets = [result['snippet'] for result in organic_results[:5] if 'snippet' in result]
#     questions = [question['question'] for question in related_questions if 'question' in question]
    
#     serp_data = {
#         "keyword": keyword,
#         "titles": titles,
#         "snippets": snippets,
#         "related_questions": questions
#     }
    
#     print("SERP Data Collected From SERPAPI")
#     print(serp_data)
#     return serp_data

# Function to generate outline
def generate_outline(keyword):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": f"""You are an expert in creating content outlines for retirement glossary pages. Your task is to generate a two-level content outline hierarchy based on the provided '{keyword}'. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content. You are writing this article on behalf of Human Interest, a 401(k) retirement plan provider."""
            },
            {
                "role": "user",
                "content": f"""Generate a two-level content outline for a retirement glossary page about '{keyword}'. Be unique and creative.     
                The outline should cover the main topics and subtopics related to '{keyword}', focusing on the information found in the SERP titles and snippets. Use a clear and concise structure, with main topics as level-1 items and subtopics as level-2 items. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content."""
            }
        ],
        max_tokens=2000
    )

    outline_text = response.choices[0].message.content
    return outline_text

# Function to generate content
def generate_content(keyword, outline_text):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a content generation assistant, tasked with creating SEO-optimized glossary entries. Write informative content that simplifies complex financial concepts of retirement planning. The content should:
                1. Use clear and accessible language 2. Maintain a neutral and informative tone 3. Include sections like definition, usage, benefits, and related terms 4. Avoid editorial opinions and focus on factual information 6. Do not include conclusion paragraphs 7. Write headlines in sentence case. """
            },
            {
                "role": "user",
                "content": f"""Create an informative, SEO-friendly retirement glossary page about '{keyword}'. Begin with an introduction that provides a clear overview of the topic. This article should not be opinionated.  The article should go into detail on '{keyword}' and describe the '{keyword}'in the context of a retirement glossary term. Make sure to follow the following rules: Your content should use full and complete sentences to expand upon the outline listed below. Use Natural Language processing to write complete semantically related sentences. Ensure that the content is accessible, encouraging, and informative, while maintaining a friendly and reassuring tone. The article should match the tone and language of the retirement planning industry, focusing on simplifying complex concepts, providing practical solutions, and educating readers on key aspects of the topic. Do not include conclusion paragraphs. Write headlines in sentence case. Use the outline below to understand what content we would like you to write about:
                Outline: {outline_text}

                """
            }
        ],
        max_tokens=3000,#add tokens here
        temperature=0.0,


    )
    
    content_text = response.choices[0].message.content
    return content_text

# Streamlit app
st.title("Retirement Glossary Term Generator | Updated")
keyword = st.text_input("Enter a keyword:")        

# Text area for outline text
outline_text = st.text_area("Paste your outline here:", height=400)

# Button to generate article
if st.button("Generate Article"):
    if keyword and outline_text:
        # Generate content based on keyword and outline
        content_text = generate_content(keyword, outline_text)
        # Display generated article
        st.subheader("Generated Article")
        st.markdown(content_text)
    else:
        st.warning("Please enter a keyword and paste your outline.")
elif st.button("Generate Outline"):
    if keyword:
        # Generate outline
        outline_text = generate_outline(keyword)
        # Display generated outline
        st.subheader("Generated Outline")
        outline_text = st.text_area("Edit the outline if needed:", value=outline_text, height=400)
    else:
        st.warning("Please enter a keyword.")