selector_prompt = """
You are an expert web scraper. Given the following HTML content and a query, generate a {selector_type} selector that accurately extracts the information requested by the query. Must respond with only the selector string, without any additional text or explanation.
User Query: {query}
Selector Type: {selector_type}
HTML Content: 
{html}
"""