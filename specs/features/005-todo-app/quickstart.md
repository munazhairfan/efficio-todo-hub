# Quickstart Guide: Todo In-Memory Python Console App

## Getting Started

### Prerequisites
- Python 3.x installed
- WSL 2 (if using Linux subsystem)

### Running the Application
1. Navigate to the project directory
2. Run `python src/main.py`
3. Follow the console prompts to interact with the todo application

### Basic Usage
- Launch the application to see the main menu
- Select options by entering the corresponding number
- Follow prompts to enter task details
- Use the application to add, view, update, delete, and mark tasks

### Project Structure
```
project/
├── src/
│   ├── main.py          # Application entry point
│   ├── todo.py          # Task management logic
│   ├── models.py        # Task data model
│   └── cli.py           # Command-line interface
├── tests/               # Unit tests
└── docs/                # Documentation
```

### Development Setup
1. Clone the repository
2. Ensure Python 3.x is installed
3. Run the application with `python src/main.py`
4. Run tests with `python -m pytest tests/`