# selectorllm
Generate CSS/XPath selectors from natural language using LLMs.  Extract HTML data without writing selectors manually.

---

自然言語でHTMLセレクタを生成 - LLMによる自動抽出
## Usage
```python
from selectorllm.main import getSelector

html = """<html>...</html>"""
query = "Extract link texts."

selector = getSelector(
    query,
    html,
    model="openrouter/openai/gpt-5", # Any LiteLLM-compatible model name
    selector_type="css"               # "css" or "xpath"
)

print(selector)  # example: "body > div > a"
```