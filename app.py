from flask import Flask, render_template, jsonify, request
import requests
import urllib.request
import ssl
import json
import os
import re

app = Flask(__name__)

# External Thirukkural REST API dataset URL
THIRUKKURAL_API_URL = "https://raw.githubusercontent.com/fizerkhan/thirukural/master/data/thirukural.json"

_cached_dataset = None

def fetch_thirukkural_data():
    """Fetch dataset from external Thirukkural REST API dataset with fallback mechanisms."""
    global _cached_dataset
    if _cached_dataset is not None:
        return _cached_dataset
    
    # 1. Try requests.get
    try:
        response = requests.get(THIRUKKURAL_API_URL, timeout=8, verify=False)
        if response.status_code == 200:
            _cached_dataset = response.json()
            return _cached_dataset
    except Exception as e:
        print(f"requests.get failed: {e}")

    # 2. Try urllib with unverified SSL context fallback
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.urlopen(THIRUKKURAL_API_URL, context=ctx, timeout=8)
        _cached_dataset = json.loads(req.read().decode('utf-8'))
        return _cached_dataset
    except Exception as e:
        print(f"urllib.request failed: {e}")

    return None

def get_kurals_list(data):
    if not data:
        return []
    if "kurals" in data:
        return data["kurals"]
    if "kural" in data:
        return data["kural"]
    return []

def fix_line_words(text, expected_count):
    """Normalize Thirukkural meter: Line 1 has 4 words (4 சீர்கள்), Line 2 has 3 words (3 சீர்கள்)."""
    if not text:
        return ""
    words = str(text).strip().split()
    while len(words) > expected_count:
        # Merge artificially split compound words (e.g. 'இல்வாழ்' + 'க்கை' -> 'இல்வாழ்க்கை')
        words[-2] = words[-2] + words[-1]
        words.pop()
    return " ".join(words)

def format_kural(item):
    kural_lines = item.get("kural", item.get("lines", []))
    meaning_obj = item.get("meaning", {})
    
    en_meaning = ""
    ta_meaning = ""
    if isinstance(meaning_obj, dict):
        en_meaning = meaning_obj.get("en", "")
        ta_meaning = meaning_obj.get("ta_mu_va", meaning_obj.get("ta", ""))
    elif isinstance(meaning_obj, str):
        en_meaning = meaning_obj

    # Format into exact traditional Thirukkural 2-line structure (Line 1: 4 words, Line 2: 3 words)
    if isinstance(kural_lines, list) and len(kural_lines) == 2:
        line1 = fix_line_words(kural_lines[0], 4)
        line2 = fix_line_words(kural_lines[1], 3)
    else:
        full_text = " ".join(kural_lines) if isinstance(kural_lines, list) else str(kural_lines)
        words = full_text.strip().split()
        if len(words) >= 7:
            line1 = fix_line_words(" ".join(words[:4]), 4)
            line2 = fix_line_words(" ".join(words[4:]), 3)
        else:
            line1 = full_text
            line2 = ""

    return {
        "number": item.get("number"),
        "paal": item.get("section", "அறத்துப்பால்"),
        "athikaram": item.get("chapter", ""),
        "kural": [line1, line2],
        "kural_text": f"{line1}\n{line2}",
        "meaning_en": en_meaning,
        "meaning_ta": ta_meaning
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search/number/<number>")
def search_number(number):
    try:
        num = int(number)
    except ValueError:
        return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 404

    data = fetch_thirukkural_data()
    kurals = get_kurals_list(data)
    if not kurals:
        return jsonify({"success": False, "message": "Unable to fetch data from Thirukkural API middleware."}), 500

    for item in kurals:
        if item.get("number") == num:
            return jsonify({"success": True, "data": format_kural(item)})

    return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 404

@app.route("/search/athikaram/<path:name>")
def search_athikaram(name):
    query = name.strip().lower()
    if not query:
        return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 400

    data = fetch_thirukkural_data()
    kurals = get_kurals_list(data)
    if not kurals:
        return jsonify({"success": False, "message": "Unable to fetch data from Thirukkural API middleware."}), 500

    matches = []
    for item in kurals:
        chapter = item.get("chapter", "").strip().lower()
        if query in chapter or chapter in query:
            matches.append(format_kural(item))

    if matches:
        return jsonify({"success": True, "data": matches[0], "total_matches": len(matches)})

    if query.isdigit():
        ath_num = int(query)
        start_kural = (ath_num - 1) * 10 + 1
        for item in kurals:
            if item.get("number") == start_kural:
                return jsonify({"success": True, "data": format_kural(item)})

    return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 404

@app.route("/search/title/<path:title>")
def search_title(title):
    query = title.strip().lower()
    if not query:
        return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 400

    data = fetch_thirukkural_data()
    kurals = get_kurals_list(data)
    if not kurals:
        return jsonify({"success": False, "message": "Unable to fetch data from Thirukkural API middleware."}), 500

    matches = []
    for item in kurals:
        k_lines = item.get("kural", item.get("lines", []))
        lines_str = " ".join(k_lines).lower() if isinstance(k_lines, list) else str(k_lines).lower()
        
        meaning_obj = item.get("meaning", {})
        meaning_en = meaning_obj.get("en", "").lower() if isinstance(meaning_obj, dict) else ""
        meaning_ta = meaning_obj.get("ta_mu_va", "").lower() if isinstance(meaning_obj, dict) else ""
        chapter = item.get("chapter", "").lower()
        
        if query in lines_str or query in meaning_en or query in meaning_ta or query in chapter:
            matches.append(format_kural(item))

    if matches:
        return jsonify({"success": True, "data": matches[0], "total_matches": len(matches)})

    return jsonify({"success": False, "message": "No matching Kural was found. Please verify the Kural Number, Athikaram, or Title."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
