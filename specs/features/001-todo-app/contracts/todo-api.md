# Todo API Contracts

## Task Management Functions

### add_task(title: str, description: str = "") -> int
**Purpose**: Add a new task to the in-memory storage
**Input**:
- title (str): Task title (required, non-empty)
- description (str): Task description (optional)
**Output**: int - The ID of the newly created task
**Side Effects**: Task added to in-memory storage with 'completed' = False
**Error Cases**:
- ValueError if title is empty or None

### get_task(task_id: int) -> dict
**Purpose**: Retrieve a task by its ID
**Input**: task_id (int): Unique identifier of the task
**Output**: dict with keys: id, title, description, completed
**Error Cases**:
- KeyError if task_id does not exist

### update_task(task_id: int, title: str = None, description: str = None) -> bool
**Purpose**: Update task details by ID
**Input**:
- task_id (int): Unique identifier of the task
- title (str): New title (optional)
- description (str): New description (optional)
**Output**: bool - True if update successful, False otherwise
**Error Cases**:
- KeyError if task_id does not exist

### delete_task(task_id: int) -> bool
**Purpose**: Remove a task by ID
**Input**: task_id (int): Unique identifier of the task
**Output**: bool - True if deletion successful, False otherwise
**Error Cases**:
- KeyError if task_id does not exist

### mark_complete(task_id: int) -> bool
**Purpose**: Mark a task as complete
**Input**: task_id (int): Unique identifier of the task
**Output**: bool - True if marking successful, False otherwise
**Error Cases**:
- KeyError if task_id does not exist

### mark_incomplete(task_id: int) -> bool
**Purpose**: Mark a task as incomplete
**Input**: task_id (int): Unique identifier of the task
**Output**: bool - True if marking successful, False otherwise
**Error Cases**:
- KeyError if task_id does not exist

### get_all_tasks() -> list
**Purpose**: Retrieve all tasks
**Output**: list of task dictionaries with keys: id, title, description, completed

### get_completed_tasks() -> list
**Purpose**: Retrieve all completed tasks
**Output**: list of task dictionaries with keys: id, title, description, completed

### get_pending_tasks() -> list
**Purpose**: Retrieve all pending tasks
**Output**: list of task dictionaries with keys: id, title, description, completed