import osimport requestsimport feedparser

print("Initializing RSS scraping routines...")rss_feeds = [
    "https://techcrunch.com",
    "https://ycombinator.com"
]
collected_articles = []for feed_url in rss_feeds:
    parsed_feed = feedparser.parse(feed_url)
    for entry in parsed_feed.entries[:5]:
        collected_articles.append(f"{entry.title}: {entry.description}")
aggregate_news_payload = "\n".join(collected_articles)

print("Connecting to Google AI Studio Gateway...")api_token = os.environ.get("GEMINI_API_KEY")if not api_token:
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

Input Data Stream:{aggregate_news_payload}"""
request_body = {"contents": [{"parts": [{"text": instruction_prompt}]}]}api_response = requests.post(endpoint_url, json=request_body)parsed_response = api_response.json()extracted_html_rows = parsed_response['candidates'][0]['content']['parts'][0]['text'].strip()

print("Injecting new data matrices into target asset index.html...")with open("index.html", "r", encoding="utf-8") as target_file:
    file_buffer = target_file.read()
target_injection_anchor = '<tbody id="dynamic-glossary-target" class="divide-y divide-slate-100">'if target_injection_anchor in file_buffer:
    modified_html_payload = file_buffer.replace(target_injection_anchor, target_injection_anchor + "\n" + extracted_html_rows)
    with open("index.html", "w", encoding="utf-8") as write_file:
        write_file.write(modified_html_payload)
    print("Index structural updates compiled successfully.")else:
    print("Execution Error: ID target anchor not found inside current DOM ecosystem.")
    exit(1)
