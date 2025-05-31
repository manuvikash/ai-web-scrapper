from bs4 import BeautifulSoup
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def extractContent(html):
    soup = BeautifulSoup(html, "html.parser")
    body = soup.body
    if(body):
        return str(body)
    else:
        return ""
    
def cleanBody(body):
    soup = BeautifulSoup(body, "html.parser")
    for trash in soup(["script", "style"]):
        trash.extract()

    cleaned = soup.get_text(separator="\n")
    cleaned = "\n".join(line.strip() for line in cleaned.splitlines() if line.strip())
    return cleaned

def splitContent(content, length = 6000):
    return[content[i : i+length] for i in range(0, len(content), length)]

model = OllamaLLM(model="llama3.2:1b")

def llmParse(chunks, desc):
    prompt = ChatPromptTemplate.from_template(template)
    print(prompt)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"Parsings batch: {i} of {len(chunks)}")
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": desc}
        )
        print(f"Parsed batch: {i} of {len(chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
