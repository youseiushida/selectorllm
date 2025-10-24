from litellm import completion
from typing import Literal
from src.selectorllm.prompt import selector_prompt

def getSelector(query: str, html: str, model: str, selector_type: Literal["css", "xpath"] = "css") -> str:
    prompt = selector_prompt.format(query=query, html=html, selector_type=selector_type)
    response = completion(
        model=model,
        messages=[{ "content": prompt,"role": "user"}]
    )
    return response.choices[0].message.content 
