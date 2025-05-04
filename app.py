from flask import Flask, render_template, request, send_from_directory
import requests
import json
import os
import pandas as pd

app = Flask(__name__)
API_KEY = 'bce309a4aceb4f70a8fa84490cb62d10'

def build_query(params):
    parts = []

    if params.get("keywords"): parts.append(params["keywords"])
    if params.get("from_user"): parts.append(f"from:{params['from_user']}")
    if params.get("to_user"): parts.append(f"to:{params['to_user']}")
    if params.get("mentions"): parts.extend([f"@{m.strip()}" for m in params["mentions"].split(',') if m.strip()])
    if params.get("since"): parts.append(f"since:{params['since']}")
    if params.get("until"): parts.append(f"until:{params['until']}")
    if params.get("min_retweets"): parts.append(f"min_retweets:{params['min_retweets']}")
    if params.get("min_faves"): parts.append(f"min_faves:{params['min_faves']}")
    if params.get("min_replies"): parts.append(f"min_replies:{params['min_replies']}")
    if params.get("lang"): parts.append(f"lang:{params['lang']}")

    return " ".join(parts)


def fetch_tweets(query, query_type, max_pages):
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": API_KEY}

    all_tweets = []
    cursor = None

    for page in range(int(max_pages)):
        params = {
            "queryType": query_type, 
            "query": query}

        if cursor:
            params["cursor"] = cursor

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        tweets = data.get("tweets", [])
        cursor = data.get("next_cursor")
        all_tweets.extend(tweets)

        if not cursor:
            break

    return all_tweets


def save_to_files(data, filename="tweets_data", folder="Output"):
    os.makedirs(folder, exist_ok=True)

    json_path = os.path.join(folder, f"{filename}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    if data:
        df = pd.json_normalize(data)
        excel_path = os.path.join(folder, f"{filename}.xlsx")
        df.to_excel(excel_path, index=False)

    return json_path, excel_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        inputs = request.form.to_dict()

        query = build_query(inputs)
        all_tweets = fetch_tweets(query, inputs.get("queryType"), inputs.get("max_pages"))
        json_path, excel_path = save_to_files(all_tweets)

        sample_tweets = []
        for t in all_tweets[:10]:  
            sample_tweets.append({
                "text": t.get("text", ""),
                "createdAt": t.get("createdAt", ""),
                "url": t.get("url", "#"),
                "author": {"name": t.get("author", {}).get("name", "Unknown")}
            })

        return render_template("index.html",
                               success=True,
                               json_file=os.path.basename(json_path),
                               excel_file=os.path.basename(excel_path),
                               tweets=sample_tweets)

    return render_template("index.html", success=False)


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("Output", filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
