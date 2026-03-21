import flask
from flask import request, jsonify
import hmac
import hashlib

app = flask.Flask(__name__)

# ========== 配置 ==========
SECRET_KEY = "battle_sim_2026_v1"
# ==========================

# 用 IP 地址作为账户，存金币
ip_gold = {}


def get_client_ip():
    """获取客户端 IP"""
    return request.remote_addr


def verify_signature(data):
    try:
        if not isinstance(data, dict):
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
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    ip = get_client_ip()
    gold = ip_gold.get(ip, 0)
    return jsonify({"gold": gold})


@app.route('/api/add_gold', methods=['POST'])
def add_gold():
    print("--- add_gold called ---")
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    amount = json_data.get("amount", 0)
    ip = get_client_ip()
    # 如果该 IP 没有记录，初始化为 0
    if ip not in ip_gold:
        ip_gold[ip] = 0
    ip_gold[ip] += amount
    print(f"add_gold: IP={ip} added {amount}, total {ip_gold[ip]}")
    return jsonify({"gold": ip_gold[ip]})


@app.route('/api/buy_torpedo', methods=['POST'])
def buy_torpedo():
    print("--- buy_torpedo called ---")
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No JSON data"}), 400
    if not verify_signature(json_data):
        return jsonify({"error": "Invalid signature"}), 403

    torpedo_type = json_data.get("type", "")
    price = 0
    success = False

    ip = get_client_ip()
    if ip not in ip_gold:
        ip_gold[ip] = 0

    if torpedo_type == "normal":
        price = 3
        if ip_gold[ip] >= price:
            ip_gold[ip] -= price
            success = True
    elif torpedo_type == "super":
        price = 7
        if ip_gold[ip] >= price:
            ip_gold[ip] -= price
            success = True
    else:
        return jsonify({"success": False, "message": "未知鱼雷类型"}), 400

    if success:
        print(f"buy_torpedo: IP={ip} bought {torpedo_type}, remaining {ip_gold[ip]}")
        return jsonify({"success": True, "gold": ip_gold[ip]})
    else:
        return jsonify({"success": False, "message": "金币不足"}), 400


# ========== 启动服务器 ==========
if __name__ == '__main__':
    print("🚀 战舰模拟器 Beta 模式已启动（IP 作为账户）")
    app.run(host='0.0.0.0', port=5009)