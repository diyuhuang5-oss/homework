from flask import Flask, jsonify, render_template
from app.models import Product, PriceHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import numpy as np
from scipy.optimize import curve_fit

# 初始化 Flask 應用程式
app = Flask(__name__)

# 將數學公式移到這裡供 API 使用
def decay_formula(t, k, p_min):
    p_launch = 34900
    return p_min + (p_launch - p_min) * np.exp(-k * t)

# 設定網站首頁 (確保整個檔案只有這個 home 函數)
@app.route('/')
def home():
    return render_template('index.html')

# 設定分析 API 的網址路由 (允許動態帶入品牌與型號)
@app.route('/api/analyze/<brand>/<model_name>')
def analyze_price(brand, model_name):
    engine = create_engine('sqlite:///local_test.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 1. 查詢產品是否存在
        product = session.query(Product).filter_by(brand=brand, model_name=model_name).first()
        if not product:
            return jsonify({"status": "error", "message": "資料庫中找不到該產品"})

        # 2. 撈取歷史價格
        records = session.query(PriceHistory).filter_by(product_id=product.id).order_by(PriceHistory.scraped_at).all()
        
        if len(records) < 5:
             return jsonify({"status": "error", "message": "數據不足，無法進行數學擬合"})

        # 3. 執行數學分析
        t_data = np.arange(len(records))
        y_data = np.array([float(r.current_price) for r in records])

        popt, _ = curve_fit(decay_formula, t_data, y_data, p0=[0.02, 15000])
        best_k, best_p_min = popt
        
        future_month = 30
        predicted_price = decay_formula(future_month, best_k, best_p_min)

        # 4. 將計算結果打包成 JSON 格式回傳
        return jsonify({
            "status": "success",
            "data": {
                "brand": brand,
                "model": model_name,
                "analysis": {
                    "decay_coefficient_k": round(best_k, 4),
                    "estimated_minimum_price": round(best_p_min, 0),
                    "predicted_price_month_30": round(predicted_price, 0)
                },
                "data_points_used": len(records)
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        session.close()