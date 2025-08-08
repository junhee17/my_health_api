from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

# 自作のPythonファイルをインポートする
import models, schemas, crud
from database import SessionLocal, engine

# データベースにテーブルを作成する
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# DBセッションを管理するための依存性注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- APIエンドポイント ---

@app.post("/logs/{log_date}/foods/", response_model=schemas.Food)
def create_food_for_date(log_date: date, food: schemas.FoodCreate, db: Session = Depends(get_db)):
    # 該当の日付の記録があるか探し、なければ新しく作成する
    db_log = crud.get_daily_log_by_date(db, log_date=log_date)
    if db_log is None:
        db_log = crud.create_daily_log(db, log_date=log_date)
    
    return crud.create_food_for_log(db=db, food=food, log_id=db_log.id)

@app.post("/logs/{log_date}/workouts/", response_model=schemas.Workout)
def create_workout_for_date(log_date: date, workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    # 該当の日付の記録があるか探し、なければ新しく作成する
    db_log = crud.get_daily_log_by_date(db, log_date=log_date)
    if db_log is None:
        db_log = crud.create_daily_log(db, log_date=log_date)
        
    return crud.create_workout_for_log(db=db, workout=workout, log_id=db_log.id)

@app.get("/logs/{log_date}/", response_model=schemas.DailyLog)
def read_log(log_date: date, db: Session = Depends(get_db)):
    db_log = crud.get_daily_log_by_date(db, log_date=log_date)
    
    # 記録がない場合は404エラーではなく、空のデータを返す仕様にした
    if db_log is None:
        return schemas.DailyLog(date=log_date, id=-1, foods=[], workouts=[])
        
    return db_log

@app.delete("/foods/{food_id}", response_model=schemas.Food)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    db_food = crud.delete_food_by_id(db, food_id=food_id)
    
    # 削除するデータが見つからなかった場合は、404エラーを返す
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
        
    return db_food

@app.put("/foods/{food_id}", response_model=schemas.Food)
def update_food(food_id: int, food: schemas.FoodCreate, db: Session = Depends(get_db)):
    db_food = crud.update_food_by_id(db, food_id=food_id, food_update=food)
    
    # 更新するデータが見つからなかった場合は、404エラーを返す
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
        
    return db_food