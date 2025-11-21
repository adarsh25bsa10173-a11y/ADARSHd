import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from insights import show_completion_rates

HABITS_DATA = "data/habits.csv"

def visualize():
    while True:
        print("\nVisualize Stats : ")
        print("1. Completion Rates")
        print("2. Habit Progress")
        print("3. Daily Completion")
        print("4. Go Back")
        choice = input("\nChoose: ")
        print()
        match choice:
            case "1":
                plot_completion_rates()
            case "2":
                plot_habit_progress()
            case "3":
                plot_activity_trend()
            case "4":
                break
            case _:
                print("Invalid Choice!")
        input("\nPress Enter Key To Continue...")

def plot_completion_rates():
    df=show_completion_rates()["Completion Rate"]
    plt.figure("Habit Completion Rates Chart")
    df.plot(kind="barh", color="skyblue")
    plt.title("Habit Completion Rates (%)")
    plt.xlabel("Completion Rate")
    plt.ylabel("Habit")
    plt.tight_layout()
    plt.show()

def plot_habit_progress():
    df=pd.read_csv(HABITS_DATA);
    habit_name = input("Enter a Habit to view its progress : ").title()
    if habit_name in df["habits"].values:
        df = df[(df["habits"] == habit_name) & (df["status"] == 1)]
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        streaks=[1]
        for i in range(1, len(df)):
            if (df.loc[i, "date"] - df.loc[i-1, "date"]).days == 1:
                streaks.append(1)
            else:
                streaks.append(-1)
        x = np.arange(len(streaks))
        y = np.cumsum(streaks)
        plt.figure(habit_name+"Progress Chart")
        plt.plot(x, y, linestyle='-', linewidth=1)
        plt.title("Progressive Line Chart")
        plt.xlabel("Day")
        plt.ylabel(habit_name)
        plt.yticks([])
        plt.grid(True)
        plt.show()
    else:
        print("\n\""+habit_name+"\" does not exist.\nTry adding it first.\n")

def plot_activity_trend():
    df=pd.read_csv(HABITS_DATA)
    df=df.groupby("date")["status"].sum()
    plt.figure("Activity Chart")
    plt.plot(df.index, df.values, linestyle='-', linewidth=1)
    plt.title("Progressive Line Chart")
    plt.xlabel("Day")
    plt.ylabel("No. of Habits Marked")
    plt.xticks(df.index[::30], rotation=90)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
