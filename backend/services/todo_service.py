"""
Todo Service Layer
Handles all todo-related business logic
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from models.todo import Todo
from models.user import User
from schemas import TodoCreate, TodoUpdate, TodoResponse


async def create_todo_service(todo_data: TodoCreate, user_id: uuid.UUID, db: AsyncSession) -> TodoResponse:
    """
    Service function to create a new todo
    # UI Component: TodoCreateForm -> Service: create_todo_service
    """
    # Create a new Todo instance with the user's ID
    db_todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        completed=todo_data.completed or False,
        user_id=user_id
    )

    # Add to database session and commit
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)

    return TodoResponse(
        id=db_todo.id,
        title=db_todo.title,
        description=db_todo.description,
        completed=db_todo.completed,
        created_at=db_todo.created_at,
        updated_at=db_todo.updated_at,
        user_id=db_todo.user_id
    )


async def get_user_todos_service(user_id: uuid.UUID, db: AsyncSession) -> List[TodoResponse]:
    """
    Service function to get all todos for a user
    # UI Component: TodoListPage -> Service: get_user_todos_service
    """
    # Query for todos belonging to the user
    result = await db.execute(
        select(Todo).where(Todo.user_id == user_id)
    )
    todos = result.scalars().all()

    # Convert to response format
    todo_responses = [
        TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            user_id=todo.user_id
        )
        for todo in todos
    ]

    return todo_responses


async def get_todo_service(todo_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession) -> TodoResponse:
    """
    Service function to get a specific todo by ID
    # UI Component: TodoDetailPage -> Service: get_todo_service
    """
    # Query for the specific todo that belongs to the user
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        user_id=todo.user_id
    )


async def update_todo_service(todo_id: uuid.UUID, todo_update: TodoUpdate, user_id: uuid.UUID, db: AsyncSession) -> TodoResponse:
    """
    Service function to update a specific todo by ID
    # UI Component: TodoUpdateForm -> Service: update_todo_service
    """
    # Query for the specific todo that belongs to the user
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )

    # Update fields if provided
    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.completed is not None:
        todo.completed = todo_update.completed

    # Commit changes to database - updated_at will be updated automatically by the model
    await db.commit()
    await db.refresh(todo)

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        user_id=todo.user_id
    )


async def delete_todo_service(todo_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession) -> None:
    """
    Service function to delete a specific todo by ID
    # UI Component: TodoDeleteButton -> Service: delete_todo_service
    """
    # Query for the specific todo that belongs to the user
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    )
    todo = result.scalar_one_or_none()

    if not todo:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or doesn't belong to user"
        )

    # Delete the todo
    await db.delete(todo)
    await db.commit()