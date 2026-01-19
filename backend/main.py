import os
import shutil
import uuid
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# [注意] 這裡引入了 func 用於計算統計數據
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel

# --- 1. 資料庫連線 (支援部署) ---

# 嘗試讀取雲端環境變數 (Render 會自動注入 DATABASE_URL)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # 如果在雲端 (Render 使用 PostgreSQL)
    # 修正 SQLAlchemy 的連線字串格式 (postgres:// -> postgresql://)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    # 如果在本地 (使用 MySQL)
    # ⚠️ 請確認這裡的 root:密碼@localhost:3306/資料庫名稱 是否正確
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/chocolate_shop"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. 資料庫模型 (Tables) ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    role = Column(String(20), default="member")
    email = Column(String(100))
    phone = Column(String(20))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text)
    category = Column(String(100))
    image_url = Column(String(500))

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    total_price = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="處理中")
    
    # 收件資訊欄位
    receiver_name = Column(String(50))
    receiver_phone = Column(String(20))
    receiver_address = Column(String(255))
    
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_name = Column(String(255))
    price = Column(Integer)
    quantity = Column(Integer)
    
    order = relationship("Order", back_populates="items")

# 自動建立資料表 (如果不存在的話)
Base.metadata.create_all(bind=engine)

# --- 3. FastAPI 初始化 ---
app = FastAPI()

# 設定圖片上傳目錄
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 掛載靜態檔案目錄 (讓前端可以讀取圖片)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# 設定 CORS (允許前端跨域請求)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 資料庫依賴函式
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 4. Pydantic 驗證模型 (Schemas) ---

class UserRegister(BaseModel):
    username: str
    password: str
    email: str | None = None
    phone: str | None = None

class LoginSchema(BaseModel):
    username: str
    password: str

class CartItemSchema(BaseModel):
    product_id: int
    name: str
    price: int
    quantity: int

class CheckoutSchema(BaseModel):
    username: str
    # 結帳時前端傳來的收件資訊
    receiver_name: str
    receiver_phone: str
    receiver_address: str
    items: List[CartItemSchema]

class OrderItemRead(BaseModel):
    product_name: str
    price: int
    quantity: int
    
    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    username: str
    total_price: int
    created_at: datetime
    status: str 
    
    # [關鍵] 確保 API 回傳這些欄位，前端才看得到
    receiver_name: str | None = None
    receiver_phone: str | None = None
    receiver_address: str | None = None
    
    items: List[OrderItemRead] = []
    
    class Config:
        from_attributes = True

# --- 5. API 路由 Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Choco Gemini API is running!"}

# 初始化管理員帳號
@app.get("/init_admin")
def init_admin(db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == "admin").first()
    if not existing:
        admin = User(username="admin", password="123456", role="admin", email="admin@test.com", phone="0900000000")
        db.add(admin)
        db.commit()
        return {"message": "Admin Created"}
    return {"message": "Admin Exists"}

# [後台] 儀表板統計數據
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    product_count = db.query(Product).count()
    order_count = db.query(Order).count()
    
    # 計算總營收 (使用 func.sum)
    total_revenue = db.query(func.sum(Order.total_price)).scalar() or 0
    
    return {
        "product_count": product_count,
        "order_count": order_count,
        "total_revenue": total_revenue
    }

# 會員註冊
@app.post("/api/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="密碼需大於6碼")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="帳號已存在")
    new_user = User(username=user.username, password=user.password, role="member", email=user.email, phone=user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Success", "username": new_user.username}

# 會員登入
@app.post("/api/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    if user.password != data.password: # type: ignore
        raise HTTPException(status_code=400, detail="帳號或密碼錯誤")
    return {"message": "Login OK", "token": "fake-jwt", "role": user.role, "username": user.username} # type: ignore

# 取得所有商品列表
@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# 取得單一商品
@app.get("/api/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="找不到該商品")
    return product

# [後台] 新增商品
@app.post("/api/products")
async def create_product(
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(None),
    category: str = Form("生巧克力"),
    image: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    image_url = ""
    
    if image:
        filename = image.filename or ""
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_location = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
            
        # 注意：這裡使用相對路徑或絕對路徑需視部署環境調整
        # 在 Render 上通常直接回傳相對路徑或完整 URL
        image_url = f"http://127.0.0.1:8000/uploads/{unique_filename}"
        
        # 如果已經部署，這裡可能需要改成前端能訪問的域名
        # 但為了簡單起見，我們暫時維持這樣，或使用相對路徑

    new_product = Product(
        name=name, 
        price=price, 
        description=description,
        category=category,
        image_url=image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# [後台] 更新商品
@app.put("/api/products/{product_id}")
async def update_product(
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(None),
    category: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="找不到商品")
    
    # 更新欄位 (加上 type: ignore 避免編輯器誤報)
    product.name = name # type: ignore
    product.price = price # type: ignore
    product.description = description # type: ignore
    product.category = category # type: ignore

    # 如果有上傳新圖片才更新
    if image:
        filename = image.filename or ""
        file_extension = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_location = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(image.file, file_object)
            
        product.image_url = f"http://127.0.0.1:8000/uploads/{unique_filename}" # type: ignore

    db.commit()
    db.refresh(product)
    return product

# [後台] 刪除商品
@app.delete("/api/products/{pid}")
def delete_product(pid: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == pid).first()
    if not p: raise HTTPException(404, "Not Found")
    db.delete(p)
    db.commit()
    return {"message": "Deleted"}

# 建立訂單 (結帳)
@app.post("/api/orders")
def create_order(order_data: CheckoutSchema, db: Session = Depends(get_db)):
    total = 0
    for item in order_data.items:
        total += item.price * item.quantity
    
    new_order = Order(
        username=order_data.username,
        total_price=total,
        status="處理中",
        # 寫入收件資訊
        receiver_name=order_data.receiver_name,
        receiver_phone=order_data.receiver_phone,
        receiver_address=order_data.receiver_address
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    for item in order_data.items:
        db_item = OrderItem(
            order_id=new_order.id,
            product_name=item.name,
            price=item.price,
            quantity=item.quantity
        )
        db.add(db_item)
    
    db.commit()
    return {"message": "訂單建立成功", "order_id": new_order.id, "total": total}

# [後台] 取得所有訂單
@app.get("/api/orders", response_model=List[OrderRead])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders

# [前台] 取得特定使用者的訂單
@app.get("/api/orders/user/{username}", response_model=List[OrderRead])
def get_user_orders(username: str, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.username == username).order_by(Order.created_at.desc()).all()
    return orders

# [後台] 更新訂單狀態
@app.put("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="找不到訂單")
    
    order.status = status # type: ignore
    
    db.commit()
    return {"message": "狀態更新成功", "status": order.status} # type: ignore