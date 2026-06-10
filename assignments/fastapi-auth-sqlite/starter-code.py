"""Starter FastAPI app with JWT auth and SQLite persistence.

Run with:
    uvicorn starter-code:app --reload

This is a minimal example intended for educational use.
"""

from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# --- Config (change SECRET_KEY for production) ---
SECRET_KEY = "change-this-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Database setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./fastapi_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")


Base.metadata.create_all(bind=engine)

# --- Security utils ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Pydantic schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0


class ItemRead(ItemCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# --- FastAPI app ---
app = FastAPI(title="FastAPI JWT + SQLite Example")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


# --- Auth endpoints ---
@app.post("/auth/register", response_model=UserRead)
def register(user_in: UserCreate, db=Depends(get_db)):
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user_in.password)
    user = User(username=user_in.username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# --- Protected item endpoints ---
@app.post("/items/", response_model=ItemRead)
def create_item(item_in: ItemCreate, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    item = Item(title=item_in.title, description=item_in.description, price=item_in.price, owner_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/", response_model=List[ItemRead])
def read_items(q: Optional[str] = None, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    query = db.query(Item).filter(Item.owner_id == current_user.id)
    if q:
        ql = f"%{q}%"
        query = query.filter(Item.title.ilike(ql))
    return query.all()


@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(item_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item_in: ItemCreate, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = item_in.title
    item.description = item_in.description
    item.price = item_in.price
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, current_user: User = Depends(get_current_user), db=Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return None
