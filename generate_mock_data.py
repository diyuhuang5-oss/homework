from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Product, PriceHistory
from datetime import datetime, timedelta
import random
import math

engine = create_engine('sqlite:///local_test.db')
Session = sessionmaker(bind=engine)
session = Session()

# 確保產品存在
product = session.query(Product).filter_by(brand="Apple", model_name="iPhone 14 Pro").first()
if not product:
    product = Product(brand="Apple", model_name="iPhone 14 Pro")
    session.add(product)
    session.commit()

# 清除舊的價格紀錄，避免重複執行時資料大亂
session.query(PriceHistory).filter_by(product_id=product.id).delete()

# 設定數學模型的基礎參數
launch_price = 34900
min_price = 12000
true_k = 0.04  # 真實的衰減係數（我們要讓接下來的數學模型去猜這個數字）

# 從 24 個月前開始模擬
start_date = datetime.now() - timedelta(days=30 * 24)

print("正在製造 24 個月的歷史價格軌跡（包含市場隨機雜訊）...")

for month in range(25):
    target_date = start_date + timedelta(days=30 * month)
    
    # 這是冷卻定律的理論公式
    theoretical_price = min_price + (launch_price - min_price) * math.exp(-true_k * month)
    
    # 模擬現實生活中的市場波動（隨機上下浮動 200~800 元）
    noise = random.randint(-600, 600)
    final_price = round(theoretical_price + noise, -2) # 四捨五入到百位數
    
    # 寫入資料庫
    record = PriceHistory(
        product_id=product.id,
        platform="PChome",
        current_price=final_price,
        scraped_at=target_date
    )
    session.add(record)

session.commit()
session.close()
print("🎉 模擬數據注入成功！金庫內已累積兩年的時間序列資料。")