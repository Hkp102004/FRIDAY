from duckduckgo_search import DDGS

def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                response = f"Here's what I found about {query}:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"{i}. {r['title']}\n{r['body']}\n\n"
                return response
            return f"Couldn't find anything about {query}!"
    except Exception as e:
        return f"Search failed: {str(e)}"

def get_news(topic="gaming"):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(topic, max_results=5))
            if results:
                response = f"Latest {topic} news:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"{i}. {r['title']}\n{r['body']}\n\n"
                return response
            return f"Couldn't find news about {topic}!"
    except Exception as e:
        return f"News fetch failed: {str(e)}"

def search_youtube(query):
    try:
        import webbrowser
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Opening YouTube search for {query}!"
    except Exception as e:
        return f"Couldn't open YouTube: {str(e)}"

def open_website(url):
    try:
        import webbrowser
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening {url}!"
    except Exception as e:
        return f"Couldn't open website: {str(e)}"