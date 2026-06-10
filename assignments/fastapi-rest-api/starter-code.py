from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

# In-memory store for example items
items: Dict[int, Item] = {
    1: Item(id=1, name="Notebook", description="A spiral notebook", price=4.99),
    2: Item(id=2, name="Pen", description="Blue ink pen", price=1.49),
}


@app.get("/items/", response_model=List[Item])
def list_items(q: Optional[str] = None):
    """Return all items, optionally filtering by query text."""
    values = list(items.values())
    if q:
        q_lower = q.lower()
        values = [item for item in values if q_lower in item.name.lower() or (item.description and q_lower in item.description.lower())]
    return values


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """Return a single item by ID or raise a 404 error."""
    item = items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/", response_model=Item, status_code=201)
def create_item(item: Item):
    """Create a new item and return it."""
    if item.id in items:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items[item.id] = item
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    """Update an existing item by ID."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item
