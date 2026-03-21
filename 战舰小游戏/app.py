import flask
from flask import request, jsonify
import hmac
import hashlib

app = flask.Flask(__name__)

# ========== 配置 ==========
SECRET_KEY = "my_super_secret_123"
# ==========================

user_gold = 0


def verify_signature(data):
    try:
        if not isinstance(data, dict):
            print("verify_signature: data is not dict")
            return False
        received_data = data.get("data", "")
        received_sig = data.get("signature", "")
        expected_sig = hmac.new(
            SECRET_KEY.encode(),
            received_data.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(received_sig, expected_sig)
    except Exception as e:
        print("Signature verification error:", e)
        return False


# ========== 页面路由 ==========
@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/game')
def game():
    return flask.render_template('game.html')


@app.route('/game_new')
def game_new():
    return flask.render_template('game.new.html')


@app.route('/game_beta')
def game_beta():
    return flask.render_template('game.beta.html')


# ========== 金币 API ==========
@app.route('/api/get_gold', methods=['POST'])
def get_gold():
    print("--- get_gold called ---")
    json_data = request.get_json()
    if not json_data:
        print("get_gold: no json data")
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        print("get_gold: invalid signature")
        return jsonify({"error": "Invalid signature"}), 403
    return jsonify({"gold": user_gold})


@app.route('/api/add_gold', methods=['POST'])
def add_gold():
    global user_gold
    print("--- add_gold called ---")
    json_data = request.get_json()
    if not json_data:
        print("add_gold: no json data")
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        print("add_gold: invalid signature")
        return jsonify({"error": "Invalid signature"}), 403
    amount = json_data.get("amount", 0)
    user_gold += amount
    print(f"add_gold: added {amount}, total {user_gold}")
    return jsonify({"gold": user_gold})


@app.route('/api/buy_torpedo', methods=['POST'])
def buy_torpedo():
    global user_gold
    print("--- buy_torpedo called ---")
    json_data = request.get_json()
    if not json_data:
        print("buy_torpedo: no json data")
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        print("buy_torpedo: invalid signature")
        return jsonify({"error": "Invalid signature"}), 403

    torpedo_type = json_data.get("type", "")
    price = 0
    success = False

    if torpedo_type == "normal":
        price = 3
        if user_gold >= price:
            user_gold -= price
            success = True
    elif torpedo_type == "super":
        price = 7
        if user_gold >= price:
            user_gold -= price
            success = True
    else:
        return jsonify({"success": False, "message": "未知鱼雷类型"}), 400

    if success:
        print(f"buy_torpedo: bought {torpedo_type}, remaining {user_gold}")
        return jsonify({"success": True, "gold": user_gold})
    else:
        return jsonify({"success": False, "message": "金币不足"}), 400


# ========== 启动服务器 ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)