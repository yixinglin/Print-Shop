"""
接口定义了CUPS打印机和服务器之间的通信，包括：
1. 注册打印机，（查询，更新，删除）
2. 更新打印机状态，（查询，更新）
3. 获取新任务 （查询）
4. 报告任务状态

"""

from fastapi import APIRouter, HTTPException

from schemas.cups import PrintJob
from services.CupsService import CupsJobStatusService, JobStatusUpdate, CupsPrinterService, PrinterRegistration, \
    CupsPrintJobRequestService


task_router = APIRouter(prefix="/cups/task", tags=["CUPS Manager"])


# =============== Client Registration API ==
# 注册新的打印机客户端
@task_router.post("/register/printer-cli")
def register_printer_client(reg: PrinterRegistration):
    """
    注册新的打印机客户端
    """
    svc = CupsPrinterService()
    return svc.register_printer_client(reg)

# 获取已注册打印机的客户端信息
@task_router.get("/register/printer-cli/{client_id}")
def get_registered_printer_client(client_id: str):
    """
    获取已注册打印机的客户端信息
    :param client_id:
    :return: List[PrinterRegistration]
    """
    svc = CupsPrinterService()
    return svc.query_printer_client(client_id)

# 获取所有已注册的打印机客户端信息
@task_router.get("/register/printer-cli")
def get_all_registered_printer_clients():
    svc = CupsPrinterService()
    return svc.query_all_printer_client()


# == Print Job Request ==
# 获得所有新任务
@task_router.get("/jobs")
def get_all_requested_jobs():
    """
    获取所有新任务
    :return: List[PrintJob]
    """
    svc = CupsPrintJobRequestService()
    jobs = svc.query_all_print_jobs()
    return jobs

@task_router.delete("/jobs")
def delete_job(job_id):
    svc = CupsPrintJobRequestService()
    return svc.remove_print_job(job_id)


# 更新一个任务的状态
@task_router.post("/jobs/update-one")
def update_job_status(update: JobStatusUpdate):
    svc = CupsJobStatusService()
    return svc.update_print_job_status(update)



# @task_router.get("/jobs")
# def get_job_status(client_id: str, job_id: str):
#     svc = CupsJobStatusService()
#     return svc.query_print_job_status(client_id, job_id)


# 报告任务状态的API
@task_router.post("/notify/job_status")
def notify_job_status(update: JobStatusUpdate):
    svc = CupsJobStatusService()
    return svc.notify_job_status(update)


