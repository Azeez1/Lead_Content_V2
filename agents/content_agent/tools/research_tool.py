"""Simple research tool used by content agents."""

def perform_web_research(query: str, num_results: int = 3) -> list:
    """Mock web search returning a list of result summaries."""
    print(f"Performing research for: {query} (mocked, returning {num_results} results)")
    mock_results = [
        {"title": f"Result 1 for {query}", "snippet": "This is a summary of the first search result.", "url": "http://example.com/result1"},
        {"title": f"Result 2 for {query}", "snippet": "Detailed information can be found here regarding {query}.", "url": "http://example.com/result2"},
        {"title": f"Result 3 for {query}", "snippet": "Another perspective on {query}.", "url": "http://example.com/result3"},
    ]
    return mock_results[:num_results]
