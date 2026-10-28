"""HTTP and a small browser UI adapt the same prepared operations used by the CLI."""

import json
import sqlite3
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote, urlsplit

from apps.TaskBoard.entities.Entity_Task import Entity_Task


class Boundary_Http(BaseHTTPRequestHandler):
    def __init__(self, *args, create_task, list_tasks, complete_task, resolve_actor,
                 instance_id="standalone", **kwargs):
        self.create_task = create_task
        self.list_tasks = list_tasks
        self.complete_task = complete_task
        self.resolve_actor = resolve_actor
        self.instance_id = instance_id
        super().__init__(*args, **kwargs)

    def taskData(self, task: Entity_Task) -> dict[str, str | bool]:
        return {"task_id": task.getId(), "title": task.getTitle(), "completed": task.isCompleted()}

    def sendData(self, status: int, data: dict) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(encoded)

    def readData(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 <= length <= 8192:
            raise ValueError("body_size_invalid")
        data = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(data, dict):
            raise ValueError("body_must_be_object")
        return data

    def resolveContext(self):
        authorization = self.headers.get("Authorization", "")
        token = authorization[7:] if authorization.startswith("Bearer ") else None
        return self.resolve_actor(token)

    def do_GET(self) -> None:
        # BaseHTTPRequestHandler requires this exact method name.
        path = urlsplit(self.path).path
        if path == "/health":
            self.sendData(200, {"app": "TaskBoard", "ready": True, "instance_id": self.instance_id})
        elif path == "/":
            encoded = self.renderPage().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
        elif path == "/tasks":
            try:
                tasks = self.list_tasks.listTasks(self.resolveContext())
                self.sendData(200, {"tasks": [self.taskData(task) for task in tasks]})
            except PermissionError:
                self.sendData(403, {"error": "forbidden"})
            except (sqlite3.Error, OSError):
                self.sendData(503, {"error": "storage_unavailable"})
        else:
            self.sendData(404, {"error": "route_not_found"})

    def do_POST(self) -> None:
        # A framework-mandated spelling, documented as a language/API adaptation.
        path = urlsplit(self.path).path
        try:
            data = self.readData()
            actor_context = self.resolveContext()
            if path == "/tasks":
                if set(data) != {"title"}:
                    raise ValueError("expected_title_only")
                task = self.create_task.createTask(actor_context, data["title"])
                self.sendData(201, self.taskData(task))
            elif path.startswith("/tasks/") and path.endswith("/complete"):
                if data:
                    raise ValueError("expected_empty_object")
                task_id = unquote(path[len("/tasks/"):-len("/complete")])
                if "/" in task_id:
                    raise ValueError("invalid_task_id")
                task = self.complete_task.completeTask(actor_context, task_id)
                self.sendData(200, self.taskData(task))
            else:
                self.sendData(404, {"error": "route_not_found"})
        except PermissionError:
            self.sendData(403, {"error": "forbidden"})
        except (ValueError, UnicodeDecodeError) as error:
            self.sendData(422, {"error": str(error)})
        except LookupError:
            self.sendData(404, {"error": "task_not_found"})
        except (sqlite3.Error, OSError):
            self.sendData(503, {"error": "storage_unavailable"})

    def log_message(self, format, *args) -> None:
        # The framework defines this override; request bodies/tokens are never logged.
        return

    def renderPage(self) -> str:
        return r'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vulcan · Task Board</title>
<style>
:root{color-scheme:dark;font:16px/1.6 system-ui,sans-serif;background:#0d1521;color:#e8edf4}
*{box-sizing:border-box}body{max-width:920px;margin:0 auto;padding:42px 24px}header{border-bottom:1px solid #2b3a4d;padding-bottom:24px}
.eyebrow{color:#f0ae72;font-size:12px;letter-spacing:.17em;text-transform:uppercase}h1{font-size:42px;line-height:1.2;margin:12px 0}
p{color:#b4c1d1}.bar,.entry,li{display:flex;gap:12px;align-items:center}.bar{margin-top:24px;flex-wrap:wrap}
label{font-size:13px;color:#b4c1d1}input,button{font:inherit;border-radius:8px;padding:10px 14px;border:1px solid #35465c}
input{background:#162131;color:inherit;min-width:0}button{background:#edaa70;color:#17202d;font-weight:650;cursor:pointer}
button.secondary{background:#1d2c40;color:#e8edf4}button:disabled{opacity:.5;cursor:default}.entry{margin:30px 0 16px}.entry input{flex:1}
ul{list-style:none;padding:0}li{padding:18px 16px;background:#162131;border:1px solid #28394f;margin:10px 0;border-radius:10px}
li span{flex:1;overflow-wrap:anywhere}.done span{text-decoration:line-through;color:#8b9aaf}.tag{font:12px/1.4 ui-monospace,monospace;color:#afc8dd}
#status{min-height:28px;color:#f0ae72}.note{font-size:13px;margin-top:30px}a{color:#f0ae72}@media(max-width:560px){h1{font-size:34px}.entry{flex-wrap:wrap}.entry input{width:100%;flex-basis:100%}}
</style>
<header><div class="eyebrow">Vulcan Architecture · Executable example</div><h1>Small tasks. Explicit contracts.</h1>
<p>One application core, two boundaries. This browser and the CLI share the same use cases and SQLite data.</p></header>
<div class="bar"><label for="token">Local demo token</label><input id="token" type="password" value="demo-editor" autocomplete="off"><button class="secondary" id="refresh">Refresh</button></div>
<form class="entry" id="create"><input id="title" maxlength="120" placeholder="What needs to be done?" required aria-label="Task title"><button>Create task</button></form>
<div id="status" role="status" aria-live="polite"></div><ul id="tasks"></ul>
<p class="note">Use <code>demo-editor</code> to create, read and complete. Use <code>demo-reader</code> to read only. These are fixed local demonstration identities, resolved by the server. Configure different values through the documented environment variables.</p>
<p class="tag">UC-TASK-001 · UC-TASK-002 · UC-TASK-003</p>
<script>
const statusNode=document.querySelector('#status'),listNode=document.querySelector('#tasks');
async function request(path,options={}){const response=await fetch(path,{...options,headers:{'Authorization':'Bearer '+document.querySelector('#token').value,'Content-Type':'application/json'}});const data=await response.json();if(!response.ok)throw Error(data.error||'request_failed');return data}
async function refreshTasks(){try{const data=await request('/tasks');listNode.replaceChildren();for(const task of data.tasks){const row=document.createElement('li'),title=document.createElement('span'),button=document.createElement('button');title.textContent=task.title;button.textContent=task.completed?'Completed':'Complete';button.disabled=task.completed;button.className='secondary';if(task.completed)row.className='done';button.onclick=async()=>{try{await request('/tasks/'+encodeURIComponent(task.task_id)+'/complete',{method:'POST',body:'{}'});await refreshTasks()}catch(error){statusNode.textContent=error.message}};row.append(title,button);listNode.append(row)}statusNode.textContent=data.tasks.length+' task(s)'}catch(error){statusNode.textContent=error.message}}
document.querySelector('#refresh').onclick=refreshTasks;
document.querySelector('#create').onsubmit=async(event)=>{event.preventDefault();try{await request('/tasks',{method:'POST',body:JSON.stringify({title:document.querySelector('#title').value})});document.querySelector('#title').value='';await refreshTasks()}catch(error){statusNode.textContent=error.message}};
refreshTasks();
</script></html>'''
