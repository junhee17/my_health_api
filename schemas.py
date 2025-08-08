from pydantic import BaseModel
from datetime import date
from typing import List

# APIでやり取りするデータの型を定義するファイル (スキーマ)

# --- 食事(Food)関連のスキーマ ---

# 食事データの基本的な形
class FoodBase(BaseModel):
    name: str
    calories: int

# 食事データを作成する際に受け取る形
class FoodCreate(FoodBase):
    pass

# DBから読み込んだり、APIのレスポンスとして返す際の形
class Food(FoodBase):
    id: int
    log_id: int

    class Config:
        from_attributes = True 

# --- 運動(Workout)関連のスキーマ ---

# 運動データの基本的な形
class WorkoutBase(BaseModel):
    name: str
    duration_minutes: int

# 運動データを作成する際に受け取る形
class WorkoutCreate(WorkoutBase):
    pass

# DBから読み込んだり、APIのレスポンスとして返す際の形
class Workout(WorkoutBase):
    id: int
    log_id: int

    class Config:
        from_attributes = True 

# --- 一日の記録(DailyLog)関連のスキーマ ---

# 一日の記録の基本的な形
class DailyLogBase(BaseModel):
    date: date

# 一日の記録を作成する際に受け取る形
class DailyLogCreate(DailyLogBase):
    pass

# DBから読み込んだり、APIのレスポンスとして返す際の形
# この場合、関連する食事と運動の記録も一緒に返す
class DailyLog(DailyLogBase):
    id: int
    foods: List[Food] = []
    workouts: List[Workout] = []

    class Config:
        from_attributes = True
