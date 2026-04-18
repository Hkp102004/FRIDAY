from duckduckgo_search import DDGS

# Your personal news topics - gaming is priority!
NEWS_TOPICS = [
    {"topic": "gaming news", "label": "Gaming", "max_results": 5},
    {"topic": "AI technology news", "label": "AI & Tech", "max_results": 3},
    {"topic": "world news today", "label": "World News", "max_results": 2},
]

def get_topic_news(topic, max_results=3):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(topic, max_results=max_results))
            return results
    except Exception as e:
        return []

def get_full_briefing():
    briefing = "Good morning Harsh! Here's your news briefing!\n\n"
    
    for category in NEWS_TOPICS:
        results = get_topic_news(category["topic"], category["max_results"])
        if results:
            briefing += f"--- {category['label']} ---\n"
            for i, r in enumerate(results, 1):
                briefing += f"{i}. {r['title']}\n"
            briefing += "\n"
    
    return briefing

def get_gaming_news():
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news("gaming news", max_results=5))
            if results:
                response = "Latest gaming news:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"{i}. {r['title']}\n"
                return response
            return "Couldn't find gaming news right now!"
    except Exception as e:
        return f"News fetch failed: {str(e)}"

def get_ai_news():
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news("AI technology news", max_results=3))
            if results:
                response = "Latest AI and tech news:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"{i}. {r['title']}\n"
                return response
            return "Couldn't find AI news right now!"
    except Exception as e:
        return f"News fetch failed: {str(e)}"

def get_world_news():
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news("world news today", max_results=3))
            if results:
                response = "Latest world news:\n\n"
                for i, r in enumerate(results, 1):
                    response += f"{i}. {r['title']}\n"
                return response
            return "Couldn't find world news right now!"
    except Exception as e:
        return f"News fetch failed: {str(e)}"

if __name__ == "__main__":
    print(get_full_briefing())