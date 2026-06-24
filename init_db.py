from app.models import Base
from sqlalchemy import create_engine

def init_database():
    print("準備建立資料庫與資料表結構...")
    
    # 指定建立一個名為 local_test.db 的本地端資料庫檔案
    engine = create_engine('sqlite:///local_test.db', echo=True)
    
    # 這行指令會讀取 models.py 裡面的設定，並實際在資料庫中把表單建立出來
    Base.metadata.create_all(engine)
    
    print("\n🎉 資料庫建置完成！請檢查左側資料夾是否多出了一個 'local_test.db' 檔案。")

if __name__ == "__main__":
    init_database()