"""
Main entry point for the Todo In-Memory Console App.
"""
from .models import TaskList
from .cli import cli_add_task, cli_view_tasks, cli_update_task, cli_delete_task, cli_toggle_task_status


def display_menu():
    """
    Display the main menu options.
    """
    print("\n" + "="*40)
    print("         TODO APPLICATION")
    print("="*40)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Toggle Complete/Incomplete")
    print("6. Exit")
    print("="*40)


def get_menu_choice() -> str:
    """
    Get the user's menu choice.

    Returns:
        The user's menu choice as a string
    """
    return input("Select an option (1-6): ").strip()


def main():
    """
    Main application loop.
    """
    print("Welcome to the Todo In-Memory Console App!")

    task_list = TaskList()

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == '1':
            cli_add_task(task_list)
        elif choice == '2':
            cli_view_tasks(task_list)
        elif choice == '3':
            cli_update_task(task_list)
        elif choice == '4':
            cli_delete_task(task_list)
        elif choice == '5':
            cli_toggle_task_status(task_list)
        elif choice == '6':
            print("\nThank you for using the Todo App. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select a number between 1 and 6.")

        # Pause to let user see the result before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()