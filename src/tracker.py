import csv
import os
import pandas as pd
from datetime import date

HABITS_DATA = "data/habits.csv"

def initialize_csv():
    if not os.path.exists(HABITS_DATA):
        with open(HABITS_DATA, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "habits", "status"])

def add_habit(habit_name):
    initialize_csv()
    today = date.today().isoformat()
    with open(HABITS_DATA, mode="a", newline="") as f:
        writer = csv.writer(f);
        writer.writerow([today, habit_name, 0])
    print("✅ Habit \""+habit_name+"\" added for today.\n")

def mark_done(habit_name):
    today = date.today().isoformat()
    df = pd.read_csv(HABITS_DATA)
    if habit_name in df["habits"].values:
        if ((df["habits"] == habit_name) & (df["date"] == today)).any():
            df.loc[(df["habits"] == habit_name) & (df["date"] == today), "status"]=1
        else:
            new_row=pd.DataFrame([{"date": today, "habits": habit_name, "status": 1}])
            df=pd.concat([df, new_row], ignore_index=True)
        df.to_csv(HABITS_DATA, index=False)
        print("✅ Habit \""+habit_name+"\" marked done for "+today+"\n")
    else:
        print("❌ \""+habit_name+"\" does not exist.\nTry adding it first.\n")

def show_todays_status():
    today = date.today().isoformat()
    df=pd.read_csv(HABITS_DATA)
    status = df[df["date"]==today]
    row_index=[]
    for i in range(1, status.shape[0]+1):
        row_index.append(i)
    status.index=row_index
    print(status, "\n")

def show_all_habits():
    df=pd.read_csv(HABITS_DATA)
    df=df.drop_duplicates(subset="habits", keep="first")
    row_index=[]
    for i in range(1, df.shape[0]+1):
        row_index.append(i)
    df.index=row_index
    print(df[["habits", "date"]].rename(columns={"date": "date added"}), "\n")

def delete_habit(habit_name):
    df=pd.read_csv(HABITS_DATA)
    if habit_name in df["habits"].values:
        df=df[df["habits"] != habit_name]
        print("✅ \""+habit_name+"\" removed from list.\n")
        df.to_csv(HABITS_DATA, index=False)
    else:
        print("❌ \""+habit_name+"\" does not exist.\nTry adding it first.\n")