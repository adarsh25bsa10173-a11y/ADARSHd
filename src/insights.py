import csv
import pandas as pd
from datetime import date

HABITS_DATA = "data/habits.csv"

def view_stats():
    while True:
        print("\nView Stats : ")
        print("1. Streaks")
        print("2. Completion Rates")
        print("3. Best and Worst Habits")
        print("4. Summary")
        print("5. Go Back")
        choice = input("\nChoose: ")
        print()
        match choice:
            case "1":
                print("🔥Your Streaks : \n")
                print(show_streaks())
            case "2":
                print("✅ Your Completion Rates : \n")
                print(show_completion_rates())
            case "3":
                show_best_worst()
            case "4":
                show_summary()
            case "5":
                break
            case _:
                print("Invalid Choice!")
        input("\nPress Enter Key To Continue...")

def show_streaks():
    df=pd.read_csv(HABITS_DATA)
    streaks={}
    for habits, data in df.groupby("habits"):
        data = data.sort_values("date")
        current_streak = best_streak = 0
        prev_date = None
        for _, row in data.iterrows():
            d = pd.to_datetime(row["date"]).date()
            if row["status"] == 1:
                if prev_date and (d - prev_date).days == 1:
                    current_streak += 1
                else:
                    current_streak = 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0
            prev_date = d
        streaks[habits] = {
            "Current": current_streak,
            "Longest": best_streak
        }
    return pd.DataFrame(streaks).T

def show_completion_rates():
    completion_rates = {}
    df=pd.read_csv(HABITS_DATA)
    today = date.today()
    grouped_df=df.groupby("habits")
    for habit, data in grouped_df:
        start_date = pd.to_datetime(data["date"]).min().date()
        days = (today-start_date).days
        completion_rate = round((data["date"].nunique() / days) * 100, 2)
        completion_rates[habit] = {
            "Start Date": start_date.isoformat(),
            "Days Missed": days-data["date"].nunique(),
            "Completion Rate": completion_rate
        }
    return pd.DataFrame(completion_rates).T

def show_best_worst():
    streaks=show_streaks()
    completion_rates=show_completion_rates()
    df=completion_rates.join(streaks)
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    today = pd.to_datetime(date.today())
    df["Total Days"] = (today - df["Start Date"]).dt.days
    df["Score"] = (
        (df["Completion Rate"] / 1.4)
        + ((df["Current"] * 100 / df["Total Days"]) / 2)
        + ((df["Longest"] * 100 / df["Total Days"]) / 4)
    )
    df["Score"] = round(pd.to_numeric(df["Score"], errors="coerce"), 2)
    best_habit = df.loc[df["Score"].idxmax()]
    worst_habit = df.loc[df["Score"].idxmin()]
    print("\n🏆 Best Habit: ", best_habit.name)
    print("   Start Date          ", best_habit["Start Date"].date())
    print("   Completion Rate     ", best_habit["Completion Rate"])
    print("   Current Streak      ", best_habit["Current"])
    print("   Longest Streak      ", best_habit["Longest"])
    print("   Days Missed         ", best_habit["Days Missed"])
    print("   Score               ", best_habit["Score"])
    print("   \n💤 Worst Habit: ", worst_habit.name)
    print("   Start Date          ", worst_habit["Start Date"].date())
    print("   Completion Rate     ", worst_habit["Completion Rate"])
    print("   Current Streak      ", worst_habit["Current"])
    print("   Longest Streak      ", worst_habit["Longest"])
    print("   Days Missed         ", worst_habit["Days Missed"])
    print("   Score               ", worst_habit["Score"])

def show_summary():
    print("--- Summary ---")
    print("\n🔥Your Streaks : \n")
    print(show_streaks())
    print("\n✅ Your Completion Rates : \n")
    print(show_completion_rates())
    show_best_worst()