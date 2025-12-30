# Data Model for Todo In-Memory Python Console App

## Task Entity

### Fields
- **id**: int - Unique identifier for the task (auto-generated)
- **title**: str - Title/description of the task (required)
- **description**: str - Detailed description of the task (optional, can be empty)
- **completed**: bool - Completion status (default: False)

### Validation Rules
- **id**: Must be unique within the task list, auto-incrementing
- **title**: Must not be empty or None
- **description**: Can be empty string but not None
- **completed**: Boolean value only (True/False)

### State Transitions
- **Incomplete → Complete**: When user marks task as complete
- **Complete → Incomplete**: When user marks task as incomplete

## Task List Entity

### Fields
- **tasks**: list - Collection of Task objects
- **next_id**: int - Next available ID for new tasks (auto-incrementing)

### Operations
- **add_task**: Add a new task to the list
- **get_task**: Retrieve a task by ID
- **update_task**: Update task details by ID
- **delete_task**: Remove a task by ID
- **mark_complete**: Mark a task as complete by ID
- **mark_incomplete**: Mark a task as incomplete by ID
- **get_all_tasks**: Retrieve all tasks
- **get_completed_tasks**: Retrieve only completed tasks
- **get_pending_tasks**: Retrieve only pending tasks