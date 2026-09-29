from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product

from database import session , engine
import database_models
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")

def greet():
    return ("WElcome to he fast api class")

products= [
    Product(id=1, name="Phone", description= " a smartphone", price= 699.99, quantity= 50),
    Product(id=2, name="Laptop", description= " a smart PC", price= 1069.90, quantity= 90),
    Product(id=3, name="Pen", description= " a Blue Ink Pen", price= 9.09, quantity= 97),
    Product(id=4, name="Table", description= " a Wooden table", price= 100, quantity= 10),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count =db.query(database_models.Product).count
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()        

@app.get("/products")
def get_all_products(db: Session  = Depends(get_db)):
    db_product =  db.query(database_models.Product).all()
    return db_product

@app.get("/products/{id}")
def ge_product_by_id(id: int,db: Session  = Depends(get_db) ):
    db_product= db.query(database_models.Product).filter(database_models.Product.id ==id).first()
    if db_product:
        return db_product

    return "NOt found"


@app.post("/products")
def add_product(product: Product, db: Session  = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()

    return product

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session  = Depends(get_db)):
    db_product= db.query(database_models.Product).filter(database_models.Product.id ==id).first()
    if db_product:
        db_product.name= product.name
        db_product.description= product.description
        db_product.price= product.price
        db_product.quantity= product.quantity

        db.commit()
        return "Product added successfully!"
            
    else:
        return "Not found"
            

    

@app.delete("/products/{id}")
def delete_product(id: int, db: Session  = Depends(get_db)):

    db_product= db.query(database_models.Product).filter(database_models.Product.id ==id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return " Product deleted "
    else:
        return " not found"


        
