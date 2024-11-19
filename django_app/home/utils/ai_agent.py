from groq import Groq

key='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'

def analyze_code_with_llm(file_content,file_name):
    prompt=f"""
         Aalyze the following code for :
         - code style and formatting issues
         - potential bugs and errors
         - performance improvements
         - best practices
    
    File : {file_name}
    Content: {file_content}
    
    provide a detailed json output with structure"
    {{
            "issues":[
                {{
                "type":"<style|error|performance|best_practice>",
                "line": <line_number>,
                "description": "<description>",
                "suggestion": "<suggestion>"
            }}
            ]
    }}
    ```json
    """
    
    client = Groq(api_key=key)
    completion=client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{
            "role":"user",
            "content":prompt
        }],
        temperature=1,
        top_p=1,
    )
    
    return completion.choices[0].message.content