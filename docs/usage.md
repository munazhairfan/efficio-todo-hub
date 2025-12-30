# Todo In-Memory Console App - Usage Guide

## Overview
The Todo In-Memory Console App is a simple command-line application that allows you to manage your tasks. All data is stored in memory, so tasks will be lost when the application exits.

## Features
- Add new tasks with titles and descriptions
- View all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete
- Simple and intuitive menu-driven interface

## Getting Started

### Prerequisites
- Python 3.x installed on your system

### Running the Application
1. Navigate to the project directory
2. Run the application using Python:
   ```bash
   python -m src.main
   ```
   Or if in the src directory:
   ```bash
   python main.py
   ```

## Using the Application

### Main Menu
When you start the application, you'll see the main menu with the following options:

```
========================================
         TODO APPLICATION
========================================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete/Incomplete
6. Exit
========================================
```

### Adding a Task
1. Select option `1` from the main menu
2. Enter the task title when prompted
3. Enter the task description (optional) when prompted
4. The application will confirm the task was added with its assigned ID

### Viewing Tasks
1. Select option `2` from the main menu
2. All tasks will be displayed with their status:
   - `[○]` indicates the task is incomplete
   - `[✓]` indicates the task is complete
3. Each task shows its ID, title, and description

### Updating a Task
1. Select option `3` from the main menu
2. Enter the ID of the task you want to update
3. Enter the new title (or press Enter to keep the current title)
4. Enter the new description (or press Enter to keep the current description)
5. The application will confirm the update

### Deleting a Task
1. Select option `4` from the main menu
2. Enter the ID of the task you want to delete
3. Confirm the deletion by typing `y` or `yes`
4. The application will confirm the deletion

### Toggling Task Status
1. Select option `5` from the main menu
2. Enter the ID of the task you want to toggle
3. The application will change the status from complete to incomplete or vice versa
4. The application will confirm the status change

### Exiting the Application
1. Select option `6` from the main menu
2. The application will exit

## Status Indicators
- `[○]` - Incomplete task
- `[✓]` - Complete task

## Example Workflow
```
Welcome to the Todo In-Memory Console App!

========================================
         TODO APPLICATION
========================================
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete/Incomplete
6. Exit
========================================
Select an option (1-6): 1

--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional): Need to buy milk, bread, and eggs

✓ Task added successfully with ID: 1

Press Enter to continue...
```

## Error Handling
- Invalid task IDs will result in an error message
- Empty task titles are not allowed
- Attempting to operate on non-existent tasks will show an appropriate error

## Project Structure
```
project/
├── src/                 # Source code
│   ├── main.py         # Application entry point
│   ├── models.py       # Task data model
│   ├── todo.py         # Task management logic
│   └── cli.py          # Command-line interface
├── tests/              # Unit tests
├── docs/               # Documentation
└── requirements.txt    # Python dependencies (if any)
```