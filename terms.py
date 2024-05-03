import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Function to generate outline
def generate_outline(keyword):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an expert in creating content outlines for retirement glossary pages. Your task is to generate a two-level content outline hierarchy based on the provided SERP data and keyword. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content. The outline should serve as a precise template for creating a glossary page that provides clear, direct information without editorializing."""
            },
            {
                "role": "user",
                "content": f"""Generate a two-level content outline for a retirement glossary page about '{keyword}'. Be unique and creative.     
                The outline should cover the main topics and subtopics related to '{keyword}', focusing on the information found in the SERP titles and snippets. Use a clear and concise structure, with main topics as level-1 items and subtopics as level-2 items. The outline should clearly delineate sections such as definitions, applications, why it is important, benefits, and frequently asked questions, focusing solely on factual content."""
            }
        ]
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
                1. Use clear and accessible language 2. Maintain a neutral and informative tone 3. Include sections like definition, usage, benefits, and related terms 4. Avoid editorial opinions and focus on factual information
                Use Markdown for formatting, with '#' for main titles and '##' for subtitles. Do not include conclusion paragraphs"""
            },
            {
                "role": "user",
                "content": f"""Create an informative retirement glossary page about '{keyword}'. Begin with an introduction that provides a clear overview of the topic. This article should not be opinionated.  that goes into detail on '{keyword}' and describes it in the context of a retirement glossary term. Your content should be similar and semantically related to the titles and snippets that are ranking on Page 1 now. Incorporate the following outline:
                Outline: {outline_text}
                The article should delve into a detailed breakdown of '{keyword}', maintaining a focus on content semantically related to the keyword. 
                Each H2 subheading should be followed by an NLP-friendly paragraph that answers the question and provides valuable insights. Try to stick to between 3-6 H2 headlines for each article. Ensure that the content is accessible, encouraging, and informative, while maintaining a friendly and reassuring tone.
                Use Markdown formatting, with '#' for the main title and '##' for subtitles. Do not include a conclusion paragraph or an FAQ section.
                The article should match the tone and language of the retirement planning industry, focusing on simplifying complex concepts, providing practical solutions, and educating readers on key aspects of the topic.
                """
            }
        ]
    )
    
    content_text = response.choices[0].message.content
    return content_text

# Streamlit app
st.title("Retirement Glossary Term Generator")
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
