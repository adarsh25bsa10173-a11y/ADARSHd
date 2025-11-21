from tracker import add_habit, mark_done, show_todays_status, show_all_habits, delete_habit
from insights import view_stats
from visualizer import visualize

def main():
    while True:
        print("\n=== Habit Tracker ===\n")
        print("1. Add Habit")
        print("2. Mark Habit as Done")
        print("3. Show Today's Status")
        print("4. View Stats")
        print("5. Visualize Data")
        print("6. Show All Habits")
        print("7. Delete Habit")
        print("8. Exit")
        choice = input("\nChoose: ")
        print()
        match choice:
            case "1":
                habit = input("Enter habit name: ") 
                add_habit(habit.title())
            case "2":
                habit = input("Enter habit name: ")
                mark_done(habit.title())
            case "3":
                show_todays_status()
            case "4":
                view_stats()
            case "5":
                visualize()
            case "6":
                show_all_habits()
            case "7":
                habit = input("Which habit to remove? ")
                delete_habit(habit.title())
            case "8":
                print("Goodbye!")
                print("_________________________________________\n")
                break
            case _: 
                print("Invalid Choice!\n")
        input("Press Enter Key To Continue...")

if __name__ == "__main__":
    main()