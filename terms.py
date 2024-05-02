import streamlit as st
from openai import OpenAI
import serpapi
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPAPI_KEY = os.getenv('SERPAPI_KEY')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client = OpenAI()

def fetch_serp_data(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY
    }
    
    search = serpapi.search(params)
    results = search.get_dict()
    
    if "organic_results" not in results:
        print(f"No organic results found for keyword: {keyword}")
        return None
    
    organic_results = results["organic_results"]
    related_questions = results.get("related_questions", [])
    
    titles = [result["title"] for result in organic_results[:5] if "title" in result]
    snippets = [result["snippet"] for result in organic_results[:5] if "snippet" in result]
    questions = [question["question"] for question in related_questions if "question" in question]
    
    serp_data = {
        "keyword": keyword,
        "titles": titles,
        "snippets": snippets,
        "related_questions": questions
    }
    
    print("SERP Data Collected From SERPAPI")
    print(serp_data)
    return serp_data

def generate_outline(keyword, serp_data):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in creating content outlines for retirement glossary pages. Your task is to generate a two-level content outline hierarchy based on the provided SERP data and keyword. The outline should clearly delineate sections such as definitions, applications, benefits, and frequently asked questions, focusing solely on factual content. The outline should serve as a precise template for creating a glossary page that provides clear, direct information without editorializing."""
            }               
,
            {
                "role": "user",
                "content": f"""Generate a two-level content outline for a retirement glossary page about '{keyword}'. Be unique and creative. Use the following SERP data as inspiration:
                
                Titles: {serp_data['titles']}
                Snippets: {serp_data['snippets']}
                
                The outline should cover the main topics and subtopics related to '{keyword}', focusing on the information found in the SERP titles and snippets. Use a clear and concise structure, with main topics as level-1 items and subtopics as level-2 items. Follow the format and structure of the BambooHR article on "360 Degree Survey" as a reference."""
            }
        ]
    )
    
    return response.choices[0].message.content.strip()

def generate_content(keyword, serp_data):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a content generation assistant, tasked with creating SEO-optimized glossary entries. Write informative content that simplifies complex financial concepts of retirement planning. The content should:
                1. Use clear and accessible language 2. Maintain a neutral and informative tone 3. Include sections like definition, usage, benefits, and related terms 4. Avoid editorial opinions and focus on factual information
                Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Do not include conclusion paragraphs or FAQ sections."""
            }
,
            {
                "role": "user",
                "content": f"""Create an informative retirement glossary page about '{keyword}'. Begin with an introduction that provides a clear overview of the topic. This article should not be very opinionated that goes into detail on '{keyword}' and describes it in the context of a retirement glossary term. Your content should be similar and semantically related to the titles and snippets that are ranking on Page 1 now. Incorporate the following titles and snippets in a non-plagiarizing, semantically related way:
                Titles: {serp_data['titles']}
                Snippets: {serp_data['snippets']}
                The article should delve into a detailed breakdown of '{keyword}', maintaining a focus on content semantically related to the keyword. Use the provided titles and snippets to create relevant H2 subheadings in the form of questions.
                Each H2 subheading should be followed by an NLP-friendly paragraph that answers the question and provides valuable insights. Try to stick to between 3-6 H2 headlines for each article. Ensure that the content is accessible, encouraging, and informative, while maintaining a friendly and reassuring tone.
                Use Markdown formatting, with '#' for the main title and '##' for subtitles. Do not include a conclusion paragraph or an FAQ section.
                The article should match the tone and language of the retirement planning industry, focusing on simplifying complex concepts, providing practical solutions, and educating readers on key aspects of the topic.
                """
            }
        ]
    )
    
    return response.choices[0].message.content

st.title("Content Generator")

keyword = st.text_input("Enter a keyword:")

if st.button("Generate Outline"):
    if keyword:
        serp_data = fetch_serp_data(keyword)
        if serp_data:
            outline = generate_outline(keyword, serp_data)
            st.subheader("Generated Outline")
            outline_text = st.text_area("Edit the outline if needed:", value=outline, height=200)
            
            if st.button("Generate Article"):
                content = generate_content(outline_text, keyword, serp_data)
                st.subheader("Generated Article")
                st.markdown(content)
        else:
            st.warning(f"No organic results found for keyword: {keyword}")
    else:
        st.warning("Please enter a keyword.")