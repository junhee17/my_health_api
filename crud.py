from sqlalchemy.orm import Session
from datetime import date

# 他のファイルで作成したモデルとスキーマをインポートする。
import models, schemas

# --- 照会関連の関数 ---

# 日付でその日の記録があるか探す関数
def get_daily_log_by_date(db: Session, log_date: date):
    return db.query(models.DailyLog).filter(models.DailyLog.date == log_date).first()

# --- 作成関連の関数 ---

# 日付に該当する記録がなければ、新しく作成する関数
def create_daily_log(db: Session, log_date: date):
    db_log = models.DailyLog(date=log_date)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# 見つけてきた「一日の記録」に食事の情報を追加する関数
def create_food_for_log(db: Session, food: schemas.FoodCreate, log_id: int):
    # .model_dump()で受け取ったデータを展開する (Pydantic V2 推奨)
    db_food = models.Food(**food.model_dump(), log_id=log_id)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

# 見つけてきた「一日の記録」に運動の情報を追加する関数
def create_workout_for_log(db: Session, workout: schemas.WorkoutCreate, log_id: int):
    # .model_dump()で受け取ったデータを展開する (Pydantic V2 推奨)
    db_workout = models.Workout(**workout.model_dump(), log_id=log_id)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

# --- 削除関連の関数 ---

# IDで食事を探して削除する関数
def delete_food_by_id(db: Session, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()

    # データがあれば削除を実行する
    if db_food:
        db.delete(db_food)
        db.commit()
    
    return db_food

# --- 更新関連の関数 ---

# IDで食事を探し、新しい情報で内容を更新する関数
def update_food_by_id(db: Session, food_id: int, food_update: schemas.FoodCreate):
    db_food = db.query(models.Food).filter(models.Food.id == food_id).first()

    # データがあれば内容を更新する
    if db_food:
        update_data = food_update.model_dump()
        db_food.name = update_data['name']
        db_food.calories = update_data['calories']
        db.commit()
        db.refresh(db_food)
        
    return db_food