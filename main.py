from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database.database import engine
from database import models
import database.schemas as schemas
from database.database import get_db

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get('/start')
async def first_method():
    return 'hello, world'

@app.post('/users', response_model=schemas.User)
async def create_user(new_user: schemas.BaseUser, db: Session = Depends(get_db)):
    new_db_user = models.User(**new_user.dict())
    db.add(new_db_user)
    db.commit()
    db.flush()
    return new_db_user

@app.put('/users/{user_id}', response_model=schemas.User)
async def update_user(user_id: int,
                      new_user_data: schemas.UpdateUser,
                      db: Session = Depends(get_db)):
    db_user: models.User = db.query(models.User).get(user_id)

    if not db_user:
        raise HTTPException(400, "User not found, try again")

    if new_user_data.full_name and new_user_data.full_name != db_user.full_name:
        db_user.full_name = new_user_data.full_name

    if new_user_data.age and new_user_data.age != db_user.age:
        db_user.age = new_user_data.age

    if new_user_data.gender and new_user_data.gender != db_user.gender:
        db_user.gender = new_user_data.gender

    db.commit()
    db.flush()
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int,
                      db: Session = Depends(get_db)):

    db_user: models.User = db.query(models.User).get(user_id)

    if not db_user:
        raise HTTPException(400, "User not found, try again")

    db.delete(db_user)
    db.commit()

    return {"success": True}

@app.post("/user/add_car", response_model=schemas.User)
async def add_car_to_user(car_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = db.query(models.User).get(user_id)

    if not db_user:
        raise HTTPException(400, "user not found")

    db_car: models.Car = db.query(models.Car).get(car_id)

    if not db_car:
        raise HTTPException(400, "car not found")

    db_user.cars.append(db_car)

    db.flush()
    db.commit()

    return db_user

@app.post("/user/del_car", response_model=schemas.User)
async def add_car_to_user(car_id: int, user_id: int, db: Session = Depends(get_db)):
    db_user: models.User = db.query(models.User).get(user_id)

    if not db_user:
        raise HTTPException(400, "User not found")

    db_car: models.Car = db.query(models.Car).get(car_id)

    if not db_car:
        raise HTTPException(400, "car not found")

    db_user.cars.append(db_car)

    db.delete(db_car)
    db.commit()

    return db_user