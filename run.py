from app.routes import app

if __name__ == "__main__":
    print("準備啟動 Flask 本地端伺服器...")
    # 開啟 debug 模式，這樣你修改程式碼時伺服器會自動重新載入
    app.run(debug=True, port=5000)