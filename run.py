import os
from app.routes import app

if __name__ == "__main__":
    print("正在啟動 Flask 伺服器...")
    
    # 這裡很關鍵：雲端上有分配 Port 就用雲端的，沒有（像是本地端）就預設用 5000
    port = int(os.environ.get("PORT", 5000))
    
    # host="0.0.0.0" 代表允許外網的所有人透過網址連線進來
    app.run(host="0.0.0.0", port=port)