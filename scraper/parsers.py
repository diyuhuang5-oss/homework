from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_pchome_price(keyword):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    print(f"啟動瀏覽器，準備搜尋: {keyword} ...")
    driver = webdriver.Chrome(options=options)
    
    try:
        url = f"https://ecshweb.pchome.com.tw/search/v3.3/?q={keyword}"
        driver.get(url)
        
        print("網頁外框載入完畢，正在往下滾動以觸發價格顯示...")
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(3) 
        
        elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'value') or contains(@class, 'price')]")
        
        for el in elements:
            raw_text = el.text.strip().replace('$', '').replace(',', '')
            
            if raw_text.isdigit() and len(raw_text) >= 3:
                print(f"🎉 突破盲點！成功找到 {keyword} 的最新價格為: $ {raw_text}")
                return raw_text
                
        print("⚠️ 畫面上有價格，但程式沒有抓到，可能是網頁結構發生了重大改版。")
        driver.save_screenshot("error_screenshot_2.png")
        return None
        
    except Exception as e:
        print(f"⚠️ 發生錯誤: {e}")
        return None
        
    finally:
        driver.quit()
