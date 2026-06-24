from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# 建立 SQLAlchemy 的基底類別 (這個就是報錯說找不到的 Base)
Base = declarative_base()

class Product(Base):
    """產品主表：儲存硬體基本資訊"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)        
    model_name = Column(String(100), nullable=False)   
    
    prices = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(brand='{self.brand}', model_name='{self.model_name}')>"

class PriceHistory(Base):
    """價格歷史表：儲存爬蟲每日收集的動態數據"""
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    platform = Column(String(50), nullable=False)      
    current_price = Column(Numeric(10, 2), nullable=False) 
    scraped_at = Column(DateTime, default=datetime.now)    
    
    product = relationship("Product", back_populates="prices")

    def __repr__(self):
        return f"<PriceHistory(platform='{self.platform}', price={self.current_price})>"