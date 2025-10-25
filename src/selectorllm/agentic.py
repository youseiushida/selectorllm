from litellm import completion
from typing import Literal, TypedDict
from src.selectorllm.prompt import selector_prompt
class SelectorState(TypedDict):
    query: str
    html: str
    model: str
    selector_type: Literal["css", "xpath"]
    selector: str
    feedback: str
    results: list[str]

def get_selector_agentic(query: str, html: str, model: str, selector_type: Literal["css", "xpath"] = "css") -> str:
    try: 
        from langgraph.graph import StateGraph, START, END
        from langgraph.types import RetryPolicy
        import bs4

    except ImportError:
        raise ImportError(
            "This feature requires additional dependencies. / この機能には追加の依存関係が必要です:\n"
            "  pip install selectorllm[agentic]"
        )
    def generate_selector(state: SelectorState):
        pass

    def check_selector(state: SelectorState):
        pass

    def regenerate_selector(state: SelectorState):
        pass
    
    def should_continue(state: SelectorState):
        pass
    selector_graph_builder = StateGraph(SelectorState)
    selector_graph_builder.add_node("generate_selector", generate_selector)
    selector_graph_builder.add_node("check_selector", check_selector)
    selector_graph_builder.add_node("regenerate_selector", regenerate_selector)

    selector_graph_builder.add_edge(START,"generate_selector")
    selector_graph_builder.add_edge("generate_selector","check_selector")
    selector_graph_builder.add_conditional_edges("check_selector",should_continue)
    selector_graph_builder.add_edge("regenerate_selector","check_selector")

    selector_graph=selector_graph_builder.compile()
    initial_state = SelectorState(
        query=query,
        html=html,
        model=model,
        selector_type=selector_type,
        selector="",
        feedback="",
        results=[]
    )
    selector = selector_graph.invoke(
        initial_state,
    )
    return selector["selector"]