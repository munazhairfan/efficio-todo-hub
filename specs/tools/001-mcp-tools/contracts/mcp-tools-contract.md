# MCP Tools API Contract

## Overview
This document defines the contract for the Model Context Protocol (MCP) tools that allow AI agents to manage user tasks.

## add_task Tool

### Request
- **Method**: Function call (to be integrated with MCP protocol)
- **Input Parameters**:
  - `user_id` (string, required): The ID of the user requesting the operation
  - `title` (string, required): The title of the task to create
  - `description` (string, optional): Detailed description of the task

### Response
- **Success**:
  - `task_id` (integer): ID of the newly created task
  - `status` (string): "created"
  - `title` (string): Title of the created task
- **Error**:
  - Exception with descriptive error message

## list_tasks Tool

### Request
- **Method**: Function call (to be integrated with MCP protocol)
- **Input Parameters**:
  - `user_id` (string, required): The ID of the user requesting the operation
  - `status` (string, optional): Filter by status ("all", "pending", "completed")

### Response
- **Success**:
  - Array of task objects with properties:
    - `id` (integer): Task ID
    - `title` (string): Task title
    - `description` (string): Task description
    - `status` (string): Task status ("pending" or "completed")
    - `created_at` (string): Creation timestamp
- **Error**:
  - Exception with descriptive error message

## complete_task Tool

### Request
- **Method**: Function call (to be integrated with MCP protocol)
- **Input Parameters**:
  - `user_id` (string, required): The ID of the user requesting the operation
  - `task_id` (integer, required): The ID of the task to complete

### Response
- **Success**:
  - `task_id` (integer): ID of the completed task
  - `status` (string): "completed"
  - `title` (string): Title of the completed task
- **Error**:
  - Exception with descriptive error message

## delete_task Tool

### Request
- **Method**: Function call (to be integrated with MCP protocol)
- **Input Parameters**:
  - `user_id` (string, required): The ID of the user requesting the operation
  - `task_id` (integer, required): The ID of the task to delete

### Response
- **Success**:
  - `task_id` (integer): ID of the deleted task
  - `status` (string): "deleted"
  - `title` (string): Title of the deleted task
- **Error**:
  - Exception with descriptive error message

## update_task Tool

### Request
- **Method**: Function call (to be integrated with MCP protocol)
- **Input Parameters**:
  - `user_id` (string, required): The ID of the user requesting the operation
  - `task_id` (integer, required): The ID of the task to update
  - `title` (string, optional): New title for the task
  - `description` (string, optional): New description for the task

### Response
- **Success**:
  - `task_id` (integer): ID of the updated task
  - `status` (string): "updated"
  - `title` (string): Title of the updated task
- **Error**:
  - Exception with descriptive error message

## Common Error Responses

- **Authentication Error**: Raised when user_id doesn't match the task owner
- **Not Found Error**: Raised when task_id doesn't exist
- **Validation Error**: Raised when required parameters are missing or invalid