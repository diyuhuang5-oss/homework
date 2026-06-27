# 科技產品價格分析與預測戰情室

這是一個基於 Flask 開發的全端數據分析專案，旨在透過動態網頁爬蟲與數學衰減模型，追蹤並預測消費性電子產品（如 iPhone）的價格走勢。

## 📁 專案架構 (Project Architecture)

本專案採用前後端分離與微服務概念，架構如下：

*   **`app/` (前端與路由模組)**
    *   `__init__.py`: Flask 應用程式初始化
    *   `routes.py`: API 路由與頁面渲染控制
    *   `models.py`: SQLAlchemy 資料庫 ORM 模型設計
    *   `templates/index.html`: 戰情室儀表板前端 UI (基於 Bootstrap)
    *   `static/`: 存放動態生成的價格衰減預測曲線圖 (`.png`)
*   **`scraper/` (資料擷取模組)**
    *   `parsers.py` / `runner.py`: 結合 Selenium 實作的動態網頁爬蟲，負責突破電商防線抓取最新價格。
*   **`analysis/` (數學運算模組)**
    *   `decay_model.py`: 核心運算引擎。使用 SciPy (`curve_fit`) 與 NumPy，實作指數衰減數學模型，計算「衰減係數」與「預估底價」。
*   **根目錄執行檔**
    *   `run.py`: Flask 伺服器啟動入口，具備雲端 Port 自動適應功能。
    *   `init_db.py` / `generate_mock_data.py`: 資料庫初始化與歷史測試資料自動生成腳本。
    *   `requirements.txt`: 專案依賴套件清單。
    *   `科技產品價格分析戰情室_專題計畫書.pdf`: 本專案之完整企劃與研究方法說明。

## 🚀 部署環境

*   **開發環境:** Python 3.11.4
*   **資料庫:** SQLite / SQLAlchemy
*   **雲端託管:** Render (Web Service)