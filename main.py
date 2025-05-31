import streamlit as st
from scrape import scrape
from parse import extractContent, cleanBody, splitContent, llmParse

st.title("Web Scraper")

website = st.text_input("Enter website URL:")

if st.button("Scrape"):
    if website:
        st.write("Scraping the website...")
        response = scrape(website)
        result = cleanBody(extractContent(response))
        st.session_state.domContent = result
        with st.expander("View DOM content"):
            st.text_area("Scraped Content", result, height=400)
    else:
        st.warning("Please enter a website URL.")

if("domContent" in st.session_state):
    desc = st.text_area("Describe what you want to extract: ")
    
    if(st.button("Parse Content")):
        if desc:
            st.write("Parsing Content...")
            chunks = splitContent(st.session_state.domContent)
            llmResponse = llmParse(chunks, desc)
            st.write("LLM response", llmResponse)
