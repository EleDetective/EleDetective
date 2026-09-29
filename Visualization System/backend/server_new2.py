# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import sys
import os
sys.path.append('data')
from dataControl_new2 import DataControl

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 定义一个示例路由，用于向前端提供数据
@app.route('/api/data', methods=['GET'])
def get_data():
    # print(data_control.hierarchy)
    data = {"message": "Hello from Flask!", "data": data_control.get_hierarchy()}
    return jsonify(data)

@app.route('/api/data_ids', methods=['POST'])
def get_data_ids():
    content = request.json
    ids = content["ids"]
    tmp_hierarchy = data_control.get_hierarchy()
    new_hierarchy = {}
    for id in ids:
        new_hierarchy[id] = tmp_hierarchy[id]
    data = {"message": "Hello from Flask!", "data": new_hierarchy, "tot": len(tmp_hierarchy)}
    return jsonify(data)

@app.route('/api/score_edit', methods=['POST'])
def score_edit():
    content = request.json  # 获取前端发送的数据
    id = content["id"]
    box = content["box"]
    scale = content["scale"]
    result = data_control.score_edit(id, box, scale)

    return jsonify({"status": "success", "updated": result})

@app.route('/api/apply_edit', methods=['POST'])
def apply_edit():
    content = request.json  # 获取前端发送的数据
    edit_record = content["edit_record"]
    ids = content["ids"]
    result = data_control.apply_edit(edit_record, ids)

    return jsonify({"status": "success", "updated": result})

@app.route('/api/get_sample_influence', methods=['POST'])
def get_sample_influence():
    content = request.json  # 获取前端发送的数据
    id = content["id"]
    target_ids = content["target_ids"]
    print(id, target_ids)
    
    sample_influence, within_influence = data_control.get_sample_influence(id, target_ids)

    return jsonify({"status": "success", "sample_influence": sample_influence, "within_influence": within_influence})

@app.route('/api/get_sample_influence_bids', methods=['POST'])
def get_sample_influence_bids():
    content = request.json  # 获取前端发送的数据
    id = content["id"]
    bids = content["bids"]
    target_ids = content["target_ids"]
    
    sample_influence, within_influence = data_control.get_sample_influence_bids(id, bids, target_ids)

    return jsonify({"status": "success", "sample_influence": sample_influence, "within_influence": within_influence})
# # 接收前端数据并处理
# @app.route('/api/send', methods=['POST'])
# def receive_data():
#     content = request.json  # 获取前端发送的数据

#     return jsonify({"status": "success", "received": content})

if __name__ == '__main__':
    print("start")
    data_control = DataControl(with_text=True)
    # data_control = DataControl(with_text=True, use_prop=False)

    data_control.load_data(os.environ.get("ELEDETECTIVE_DATASET", "data/datasets/YOUR_DATASET"), model="dreamsim")

    
    print("done")
    app.run(host='127.0.0.1', port=int(os.environ.get("ELEDETECTIVE_BACKEND_PORT", "5102")), threaded=False)
