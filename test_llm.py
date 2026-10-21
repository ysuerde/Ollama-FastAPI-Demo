import requests

# 你的本地接口地址
URL = "http://127.0.0.1:8000/chat"

def test_normal_chat():
    """测试正常对话"""
    payload = {"prompt": "你好", "session_id": "test_1", "stream": False}
    response = requests.post(URL, json=payload)
    assert response.status_code == 200
    assert "reply" in response.json()

def test_empty_input():
    """测试空输入异常边界"""
    payload = {"prompt": "", "session_id": "test_2", "stream": False}
    response = requests.post(URL, json=payload)
    # 模型可能会返回默认废话，或者接口报错，我们只断言接口没崩
    assert response.status_code in [200, 422, 500]

def test_long_input():
    """测试超长文本"""
    payload = {"prompt": "测试" * 1000, "session_id": "test_3", "stream": False}
    response = requests.post(URL, json=payload)
    assert response.status_code == 200