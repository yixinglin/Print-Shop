from fastapi import UploadFile, APIRouter
from schemas.cups import PrintJob
from schemas.basic import ResponseSuccess
from core.log import server_logger as logger
from services.CupsService import CupsPrintJobRequestService, CupsJobStatusService

job_router = APIRouter(prefix="/printjob")

# 3. 打印任务管理相关接口
@job_router.post("/create")
def create_print_job(job: PrintJob):
    # 创建一个新的打印任务，上传需要打印的文件，并指定要使用的打印机和打印选项（如页数、双面打印等）
    logger.info(job.dict())
    svc = CupsPrintJobRequestService()
    result = svc.add_print_job(job)
    return ResponseSuccess(message=f"Print job [{job.printer_name}:{job.filename}] created successfully",
                           data=result)

@job_router.delete("/cancel")
def cancel_print_job(job_id: str):
    # 取消指定的打印任务
    svc = CupsPrintJobRequestService()
    return svc.remove_print_job(job_id)


@job_router.get("/status")
def get_print_job_status(client_id: str, job_id: str):

    # 查询指定打印任务的状态，包括是否已打印、是否排队、是否发生错误等。
    svc = CupsJobStatusService()
    data = svc.query_print_job_status(client_id, job_id)
    return ResponseSuccess(message=f"Print job [{client_id}:{job_id}] status queried successfully",
                           data=data)

def get_user_jobs(user_id: str):
    #TODO 查询指定用户的所有打印任务
    pass

# 4. 任务队列与调度相关接口

def get_print_queue(printer_id: str):

    #TODO 查询指定打印机的任务队列，显示所有排队的打印任务以及其当前状态。
    pass

def dispatch_print_job(job_id: str, printer_id: str):


    #TODO 手动调度指定的打印任务到某个特定的打印机上执行（用于调度多个任务到不同的打印机）。
    pass

def requeue_failed_job(job_id: str):
    # TODO 将失败的打印任务重新加入队列并尝试再次执行。
    pass


# 5. 实时反馈与通知相关接口
def subscribe_print_updates():
    # TODO 用户通过WebSocket连接订阅实时打印任务状态更新，包括打印任务的进度、错误报告等。
    pass

def unsubscribe_print_updates():
    # TODO 用户取消订阅打印任务的实时更新。
    pass

def get_notification_settings(user_id: str):
    # TODO 获取用户的通知设置（如是否接收打印完成或错误通知）。
    pass

def update_notification_settings(user_id: str, settings: dict):
    # TODO 更新用户的通知设置。
    pass

