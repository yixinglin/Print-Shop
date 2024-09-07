# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
# from fastapi.responses import HTMLResponse
# import json
# from typing import List
#
#
# # WebSocket管理类
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#     async def send_task(self, websocket: WebSocket, task: dict):
#         await websocket.send_text(json.dumps(task))
#
#     async def broadcast_task(self, task: dict):
#         for connection in self.active_connections:
#             await self.send_task(connection, task)
#
# manager = ConnectionManager()
#
# ws_router = APIRouter(prefix="/ws")
#
# task_queue = []
#
# # WebSocket连接端点
# @ws_router.websocket("/ws/pycups")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             # 等待客户端请求
#             data = await websocket.receive_text()
#             # 这里可以根据客户端发来的信息，做出响应处理
#             print(f"Received from client: {data}")
#             # 模拟从队列中派发任务
#             if task_queue:
#                 task = task_queue.pop(0)
#                 await manager.send_task(websocket, task)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         print("Client disconnected")
#
#
# # 模拟添加任务接口
# @ws_router.post("/add_task")
# async def add_task(printer_id: str, file_url: str, options: dict):
#     # 模拟任务生成
#     new_task = {
#         "job_id": "job_" + str(len(task_queue) + 1),
#         "printer_id": printer_id,
#         "file_url": file_url,
#         "options": options
#     }
#     task_queue.append(new_task)
#     # 当有新的任务时广播给所有连接的客户端
#     if manager.active_connections:
#         await manager.broadcast_task(new_task)
#     return {"message": "Task added and broadcasted"}