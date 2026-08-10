import os
import requests
import feedparser

print("Initializing RSS scraping routines...")
rss_feeds = [
    "https://techcrunch.com",
    "https://ycombinator.com"
]

collected_articles = []
for feed_url in rss_feeds:
    try:
        parsed_feed = feedparser.parse(feed_url)
        for entry in parsed_feed.entries[:5]:
            collected_articles.append(f"{entry.title}: {entry.description}")
    except Exception as e:
        print(f"Warning: Failed to fetch {feed_url} due to {e}")

aggregate_news_payload = "\n".join(collected_articles) if collected_articles else "No news data gathered today."

print("Connecting to Google AI Studio Gateway...")
api_token = os.environ.get("GEMINI_API_KEY")
if not api_token:
    print("Execution Error: GEMINI_API_KEY parameter is null.")
    exit(1)

endpoint_url = f"https://googleapis.com{api_token}"

instruction_prompt = f"""
You are an autonomous automated system-optimization agent.
Analyze the following tech text dump and isolate up to 2 distinct new technical terminologies, API modifications, or prompt architecture insights from today.
Format your output exactly as standard HTML table rows (tr) matching the predefined template.
Do not include any markdown format tags like ```html, backticks, or explanatory text. Return ONLY raw HTML rows.

Template Format:
<tr>
    <td class="p-4 font-mono font-bold text-indigo-600">Term Name (Acronym)</td>
    <td class="p-4 text-slate-600">Highly accurate, deterministic, technical definition formatted for semantic AI RAG extraction.</td>
    <td class="p-4 text-slate-500">Contextual origin summary from current news payload.</td>
</tr>

Input Data Stream:
{aggregate_news_payload}
"""

