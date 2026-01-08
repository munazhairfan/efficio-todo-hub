from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from models.user import User
from schemas import TodoCreate, TodoUpdate, TodoResponse, TodoListResponse
from dependencies.db_deps import get_db_session
from dependencies.auth_deps import get_current_user
from services.todo_service import (
    create_todo_service,
    get_user_todos_service,
    get_todo_service,
    update_todo_service,
    delete_todo_service
)

router = APIRouter(
    prefix="/api/todos",
    tags=["todos"]
)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> TodoResponse:
    """
    Create a new todo item for the authenticated user.
    Implements POST /api/todos endpoint per contracts/api-contract.yaml
    # UI Component: TodoCreateForm -> Backend Endpoint: POST /api/todos
    # UI Component: TodoCreateForm -> Service: create_todo_service
    """
    return await create_todo_service(todo, current_user.id, db)


@router.get("/", response_model=TodoListResponse)
async def get_todos(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> TodoListResponse:
    """
    Get all todos for the authenticated user.
    Implements GET /api/todos endpoint per contracts/api-contract.yaml
    # UI Component: TodoListPage -> Backend Endpoint: GET /api/todos
    # UI Component: TodoListPage -> Service: get_user_todos_service
    # Expected by UI pattern: Returns list of todos for rendering in UI components
    """
    todos = await get_user_todos_service(current_user.id, db)
    return TodoListResponse(todos=todos)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> TodoResponse:
    """
    Get a specific todo by ID.
    Implements GET /api/todos/{id} endpoint per contracts/api-contract.yaml
    # UI Component: TodoDetailPage -> Backend Endpoint: GET /api/todos/{id}
    # UI Component: TodoDetailPage -> Service: get_todo_service
    """
    return await get_todo_service(todo_id, current_user.id, db)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: uuid.UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> TodoResponse:
    """
    Update a specific todo by ID.
    Implements PUT /api/todos/{id} endpoint per contracts/api-contract.yaml
    # UI Component: TodoUpdateForm -> Backend Endpoint: PUT /api/todos/{id}
    # UI Component: TodoUpdateForm -> Service: update_todo_service
    """
    return await update_todo_service(todo_id, todo_update, current_user.id, db)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session)
) -> None:
    """
    Delete a specific todo by ID.
    Implements DELETE /api/todos/{id} endpoint per contracts/api-contract.yaml
    # UI Component: TodoDeleteButton -> Backend Endpoint: DELETE /api/todos/{id}
    # UI Component: TodoDeleteButton -> Service: delete_todo_service
    """
    await delete_todo_service(todo_id, current_user.id, db)