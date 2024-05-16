import streamlit as st
from openai import OpenAI
import os
import re
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

def extract_keywords(data):
    lines = data.split('\n')
    keywords = []
    for line in lines:
        # Remove leading quotation marks and numbered text
        line = re.sub(r'^\d+\.\s*', '', line)  # Remove leading numbers followed by a dot and space
        line = line.strip("\"")  # Remove leading and trailing quotation marks
        if line:
            keywords.append(line)
    return keywords

def generate_seo_content(keyword):
    prompt = f"You are a content marketing specialist that understands user intent. Generate related keywords, SEO questions, and long-tail queries for the keyword to be used for an SEO-friendly article: {keyword}."
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    data = response.choices[0].message.content
    keywords = extract_keywords(data)
    return keywords


def generate_section_from_openai(keyword, user_prompt):
    context = ""
    for key, value in st.session_state.article.items():
        if value:
            context += f"\n\n{key.capitalize()}:\n{value}"

    prompt = f"Based on the keyword '{keyword}' and following the additional context provided, generate the required content to produce a portion of a a retirement glossary term SEO page. Be strict in following the prompt. {user_prompt} {context}"
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable content creator specializing in SEO-optimized articles. Use these inputs to construct a complete SEO-friendly Retirement Glossary Term page. Do not be editorial. Be more fact-based and terse. We just want to talk about the target keyword from the context of a dictionary term. Use sentence case for all headlines."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    
    return response.choices[0].message.content


st.header("Retirement Glossary Generator v3")

# Input for keyword
keyword = st.text_input("Enter the main keyword for the article:")

# Generate SEO data
if st.button("Generate SEO Data"):
    if keyword:
        keywords = generate_seo_content(keyword)
        st.session_state.keywords = keywords
        st.write("Keywords, SEO Questions, and Long-Tail Queries:", keywords)
    else:
        st.error("Please enter a keyword.")

# Text area for user to input the content
user_prompt = st.text_area("""Enter your prompt for generating the content. Include the keywords manually as needed.
\n\nFor Example, include this text at the beginning of each of your prompts: 
\n\nIntroduction: Please write the introductory portion of the article. Use these headlines to establish an introduction and general overview of the topic.""", height=300)

# Generate content based on the user prompt
if st.button("Generate Content"):
    if keyword and user_prompt:
        content = generate_section_from_openai(keyword, user_prompt)
        # Add the generated content to the article in session storage
        st.session_state.article[len(st.session_state.article) + 1] = content
        st.markdown("**Generated Content:**")
        st.write(content)
    else:
        st.error("Please ensure a keyword and prompt are provided.")

# Display the entire article so far
if st.button("Show Entire Article"):
    for key, value in st.session_state.article.items():
        if value:
            st.write(value)



    # # Sidebar for style reference
    # with st.sidebar:
    #     st.header("Style Reference")
    #     st.write("Use the following sample as a guideline for writing style:")
    #     st.code("401(k): A type of retirement plan that's sponsored by an employer. "
    #             "While 401(k) plan details differ between employers, they often include "
    #             "tax advantages and employee contributions that are deducted from your paycheck.")




    # Manual outline input
    # outline_input = st.text_area("Paste your outline here:", height=300, key="outline")
    # if outline_input:
        # st.session_state.outline = outline_input  # Save the manually entered outline

    # # Display the manually entered outline if it exists
    # if st.session_state.outline:
    #     st.markdown("**Outline:**")
    #     st.write(st.session_state.outline)



    # if 'outline' not in st.session_state:
    #     st.session_state.outline = ""

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
