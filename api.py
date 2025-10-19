from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_PATH = "discord_data.txt"

def load_raw_file(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def try_parse_json(raw):
    if raw is None:
        return None
    s = raw.strip()
    try:
        data = json.loads(s)
        if isinstance(data, dict) and "users" in data:
            return data["users"]
        if isinstance(data, list):
            return data
    except Exception:
        pass

    # Bazı JSON dosyalarında dış [] olmayabilir
    try:
        fixed = "[" + s.strip().strip(",") + "]"
        data2 = json.loads(fixed)
        if isinstance(data2, list):
            return data2
    except Exception:
        pass

    return None

def load_users():
    raw = load_raw_file(DATA_PATH)
    return try_parse_json(raw) or []

def find_user(qid):
    users = load_users()
    q = str(qid).strip()
    for u in users:
        if str(u.get("discord_id")) == q or str(u.get("id")) == q:
            return u
    return None

@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "message": "Kullanıcıyı görmek için /<discord_id> gir (örnek: /714099961549160508)"
    })

@app.route("/<string:qid>", methods=["GET"])
def get_user(qid):
    user = find_user(qid)
    if not user:
        return jsonify({"status": "error", "message": "❌ Discord ID bulunamadı"}), 404
    return jsonify(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
