import flask
from flask import request, jsonify
import hmac
import hashlib
import time

app = flask.Flask(__name__)

# ========== 配置 ==========
SECRET_KEY = "my_super_secret_123"  # 密钥，不要泄露给前端
# ==========================

# 简单存储金币（演示用全局变量，重启会重置；生产环境请用数据库）
user_gold = 0


def verify_signature(data):
    """
    验证 HMAC-SHA256 签名
    前端应发送 JSON: { "data": "...", "signature": "..." }
    其中 data 是字符串化的业务数据（如 "add_gold:1" 或 "buy_torpedo:normal"）
    """
    try:
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
    json_data = request.get_json()
    if not json_data or not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    return jsonify({"gold": user_gold})


@app.route('/api/add_gold', methods=['POST'])
def add_gold():
    json_data = request.get_json()
    if not json_data or not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    amount = json_data.get("amount", 0)
    global user_gold
    user_gold += amount
    return jsonify({"gold": user_gold})


@app.route('/api/buy_torpedo', methods=['POST'])
def buy_torpedo():
    json_data = request.get_json()
    if not json_data or not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    torpedo_type = json_data.get("type", "")  # 'normal' 或 'super'
    global user_gold

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
        return jsonify({"success": True, "gold": user_gold})
    else:
        return jsonify({"success": False, "message": "金币不足"}), 400


# ========== 启动服务器 ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)