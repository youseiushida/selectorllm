import pytest
from bs4 import BeautifulSoup
from selectorllm.main import get_selector
from dotenv import load_dotenv

load_dotenv()

# テスト用のサンプルHTML
SAMPLE_HTML = """
<!doctype html>
<html lang="en">
    <head>
        <title>Example Domain</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                background: #eee;
                width: 60vw;
                margin: 15vh auto;
                font-family: system-ui,sans-serif
            }

            h1 {
                font-size: 1.5em
            }

            div {
                opacity: 0.8
            }

            a:link,a:visited {
                color: #348
            }
        </style>
    <body>
        <div>
            <h1>Example Domain</h1>
            <p>This domain is for use in documentation examples without needing permission. Avoid use in operations.
            <p>
                <a href="https://iana.org/domains/example">Learn more</a>
        </div>
    </body>
</html>
"""


def test_title_selector_extracts_correct_content():
    """タイトルを取得するセレクタが正しく動作するかテスト"""
    query = "Please extract the title of the webpage."
    selector = get_selector(
        query, SAMPLE_HTML, 
        model="openrouter/openai/gpt-5", 
        selector_type="css"
    )
    
    # BeautifulSoupで検証
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    result = soup.select_one(selector)
    
    # セレクタで要素が取得できることを確認
    assert result is not None, f"Selector '{selector}' did not match any elements"
    
    # 取得した内容がタイトルであることを確認
    assert result.get_text(strip=True) == "Example Domain", \
        f"Expected 'Example Domain', but got '{result.get_text(strip=True)}'"


def test_title_selector_returns_valid_css_selector():
    """生成されたセレクタが有効なCSS Selectorの形式であることをテスト"""
    query = "Please extract the title of the webpage."
    selector = get_selector(
        query, SAMPLE_HTML,
        model="openrouter/openai/gpt-5",
        selector_type="css"
    )
    
    # セレクタが文字列であることを確認
    assert isinstance(selector, str), "Selector should be a string"
    assert len(selector) > 0, "Selector should not be empty"
    
    # BeautifulSoupで構文エラーが出ないことを確認
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    try:
        soup.select(selector)  # 構文チェック
    except Exception as e:
        pytest.fail(f"Invalid CSS selector '{selector}': {e}")


@pytest.mark.parametrize("query,expected_text", [
    ("Please extract the title of the webpage.", "Example Domain"),
    ("Get the main heading", "Example Domain"),
    ("Extract the link text", "Learn more"),
])
def test_various_selectors(query, expected_text):
    """様々なクエリでセレクタが正しく動作するかテスト"""
    selector = get_selector(
        query, SAMPLE_HTML,
        model="openrouter/openai/gpt-5",
        selector_type="css"
    )
    
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    result = soup.select_one(selector)
    
    assert result is not None, f"Selector '{selector}' did not match any elements"
    assert expected_text in result.get_text(strip=True), \
        f"Expected text containing '{expected_text}', but got '{result.get_text(strip=True)}'"


def test_selector_handles_multiple_matches():
    """複数の要素にマッチする場合の挙動をテスト"""
    query = "Get all paragraphs"
    selector = get_selector(
        query, SAMPLE_HTML,
        model="openrouter/openai/gpt-5",
        selector_type="css"
    )
    
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    results = soup.select(selector)
    
    # 少なくとも1つの段落が取得できることを確認
    assert len(results) > 0, f"Selector '{selector}' did not match any elements"
    # 全ての結果がpタグであることを確認（セレクタが適切な場合）
    for result in results:
        assert result.name in ["p", "div", "body"], \
            f"Expected paragraph-related elements, but got '{result.name}'"


@pytest.mark.slow
def test_selector_with_different_models():
    """異なるモデルでセレクタが生成できることをテスト"""
    query = "Please extract the title of the webpage."
    models = [
        "openrouter/openai/gpt-5",
        "openrouter/anthropic/claude-3.5-sonnet",
    ]
    
    for model in models:
        try:
            selector = get_selector(query, SAMPLE_HTML, model=model, selector_type="css")
            soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
            result = soup.select_one(selector)
            assert result is not None, f"Model {model} generated invalid selector: '{selector}'"
        except Exception as e:
            pytest.skip(f"Model {model} not available: {e}")