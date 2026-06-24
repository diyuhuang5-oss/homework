import sys
import os
# 這兩行能確保 Python 執行時能正確找到父資料夾的 app 模組
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Product, PriceHistory
from parsers import get_pchome_price

def main():
    print("啟動【資料庫連線】與【價格爬蟲系統】...\n")
    
    # 1. 連線到我們剛剛建立的本地端資料庫
    engine = create_engine('sqlite:///local_test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 2. 定試驗目標
    brand = "Apple"
    model_name = "iPhone 14 Pro"
    
    try:
        # 3. 檢查資料庫裡是否已經有這款產品，如果沒有，就先建立產品主檔
        product = session.query(Product).filter_by(brand=brand, model_name=model_name).first()
        if not product:
            print(f"📌 資料庫內無此產品，正在建立主檔: {brand} {model_name}")
            product = Product(brand=brand, model_name=model_name)
            session.add(product)
            session.commit() # 先提交以取得 product.id
            
        # 4. 執行爬蟲抓取最新價格
        scraped_price = get_pchome_price(model_name)
        
        if scraped_price:
            # 5. 將字串價格轉換為浮點數，並寫入價格歷史表
            price_record = PriceHistory(
                product_id=product.id,
                platform="PChome",
                current_price=float(scraped_price)
            )
            session.add(price_record)
            session.commit() # 提交儲存！
            print(f"\n💾 成功！最新價格 $ {scraped_price} 已安全寫入資料庫。")
        else:
            print("\n⚠️ 未抓取到價格，本次不寫入資料庫。")
            
    except Exception as e:
        session.rollback() # 發生錯誤時撤銷所有資料庫操作，保護資料安全
        print(f"⚠️ 寫入資料庫時發生錯誤: {e}")
    finally:
        session.close() # 關閉資料庫連線
        print("\n資料庫連線已安全關閉。")

if __name__ == "__main__":
    main()