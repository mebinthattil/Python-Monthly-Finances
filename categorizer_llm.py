import ollama
def categorize(company_name):
    response = ollama.chat(model='categorizer_llm', messages=[
    {
        'role': 'user',
        'content': company_name,
    },
    ])
    return(response['message']['content'])
