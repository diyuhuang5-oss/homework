import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Product, PriceHistory
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt  # 新增：引入畫圖套件

# 1. 數學模型函數
def decay_formula(t, k, p_min):
    p_launch = 34900
    return p_min + (p_launch - p_min) * np.exp(-k * t)

def analyze_product_decay():
    engine = create_engine('sqlite:///local_test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    records = session.query(PriceHistory).order_by(PriceHistory.scraped_at).all()
    
    if not records:
        print("資料庫內沒有足夠的數據可以分析。")
        return
        
    t_data = np.arange(len(records))
    y_data = np.array([float(r.current_price) for r in records])
    
    print(f"📊 成功自資料庫讀取 {len(y_data)} 筆價格紀錄，開始運算與繪圖...")
    
    try:
        popt, pcov = curve_fit(decay_formula, t_data, y_data, p0=[0.02, 15000])
        best_k, best_p_min = popt
        
        print("\n================ 數學模型分析報告 ================")
        print(f"📈 擬合成功！衰減係數 k = {best_k:.4f}, 底價 P_min = ${best_p_min:.0f}")
        print("==================================================")
        
        # ---------------- 視覺化繪圖區塊 ----------------
        # 設定圖片大小與解析度
        plt.figure(figsize=(10, 6), dpi=100)
        
        # 畫出真實數據 (散佈圖點點)
        plt.scatter(t_data, y_data, color='red', label='Historical Price (Data with Noise)', alpha=0.6)
        
        # 產生一條平滑的預測曲線 (從第 0 個月畫到第 30 個月)
        t_smooth = np.linspace(0, 30, 100)
        y_predict = decay_formula(t_smooth, best_k, best_p_min)
        
        # 畫出數學模型曲線 (藍色實線)
        plt.plot(t_smooth, y_predict, color='blue', linewidth=2, 
                 label=f'Fitted Decay Curve ($k$={best_k:.3f})')
        
        # 標示出市場底價的水平虛線
        plt.axhline(y=best_p_min, color='green', linestyle='--', alpha=0.5, 
                    label=f'Estimated Min Price (${best_p_min:.0f})')
        
        # 設定圖表的標題與座標軸標籤
        plt.title('iPhone 14 Pro Price Decay Model (Simulated)')
        plt.xlabel('Months Since Launch')
        plt.ylabel('Price (TWD)')
        
        # 加上網格與圖例
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.legend()
        
        # 存檔成圖片，而不是直接顯示 (確保沒有圖形介面的環境也能跑)
        plt.savefig('decay_curve.png', bbox_inches='tight')
        print("\n📸 圖表繪製完成！請查看專案資料夾下的 'decay_curve.png'")
        
    except Exception as e:
        print(f"數學模型計算或繪圖失敗: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    analyze_product_decay()