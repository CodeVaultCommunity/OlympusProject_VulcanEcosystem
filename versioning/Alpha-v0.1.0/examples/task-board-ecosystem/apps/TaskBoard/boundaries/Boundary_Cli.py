"""CLI presentation calls prepared use cases and projects their data to JSON."""

import json
import sqlite3
import sys
from collections.abc import Callable

from apps.TaskBoard.entities.Entity_ActorContext import Entity_ActorContext
from apps.TaskBoard.entities.Entity_Task import Entity_Task
from apps.TaskBoard.usecases.TaskManagement.UseCase_CreateTask import UseCase_CreateTask
from apps.TaskBoard.usecases.TaskManagement.UseCase_ListTasks import UseCase_ListTasks
from apps.TaskBoard.usecases.TaskManagement.UseCase_CompleteTask import UseCase_CompleteTask


class Boundary_Cli:
    def __init__(self, create_task: UseCase_CreateTask, list_tasks: UseCase_ListTasks,
                 complete_task: UseCase_CompleteTask,
                 resolve_actor: Callable[[str | None], Entity_ActorContext | None]) -> None:
        self.create_task = create_task
        self.list_tasks = list_tasks
        self.complete_task = complete_task
        self.resolve_actor = resolve_actor

    def taskData(self, task: Entity_Task) -> dict[str, str | bool]:
        return {"task_id": task.getId(), "title": task.getTitle(), "completed": task.isCompleted()}

    def run(self, command: str, token: str | None, title: str | None = None,
            task_id: str | None = None) -> int:
        actor_context = self.resolve_actor(token)
        try:
            if command == "create":
                data = self.taskData(self.create_task.createTask(actor_context, title))
            elif command == "list":
                data = {"tasks": [self.taskData(task) for task in self.list_tasks.listTasks(actor_context)]}
            elif command == "complete":
                data = self.taskData(self.complete_task.completeTask(actor_context, task_id))
            else:
                raise ValueError("unknown_command")
        except PermissionError as error:
            print(json.dumps({"error": str(error)}), file=sys.stderr)
            return 3
        except ValueError as error:
            print(json.dumps({"error": str(error)}), file=sys.stderr)
            return 2
        except LookupError as error:
            print(json.dumps({"error": str(error)}), file=sys.stderr)
            return 4
        except (sqlite3.Error, OSError):
            print(json.dumps({"error": "storage_unavailable"}), file=sys.stderr)
            return 5
        print(json.dumps(data, ensure_ascii=False))
        return 0
