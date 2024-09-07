import time
from typing import List
from fastapi import HTTPException
import utils.StrUtil as str_util
from core.db import RedisDataManager
from core.log import server_logger as logger
from schemas.cups import PrintJob, PrinterRegistration, JobStatusUpdate


class CupsPrinterService:

    def __init__(self):
        """
        管理打印机客户端注册信息
        """
        self.redis_manager = RedisDataManager()
        self.namespace = "CUPS_PRINTERS"

    def register_printer_client(self, reg: PrinterRegistration):
        time_to_live_sec = 3600
        self.redis_manager.set_json(f"{self.namespace}:{reg.client_id}",
                                    reg.dict(), time_to_live_sec=time_to_live_sec)
        data = {"client_id": reg.client_id,
                "message": f"Printer registered for client [{reg.client_id}].",
                "created_at": str_util.current_time(),
                "expires": time_to_live_sec
                }
        return data

    def query_all_printer_client(self):
        keys = self.redis_manager.get_keys_with_prefix(f"{self.namespace}:*")
        logger.info(f"Found clients: {len(keys)}.")
        clients = []
        for key in keys:
            reg = self.redis_manager.get_json(key)
            clients.append(PrinterRegistration(**reg))
        data = {
            "clients": clients,
            "total": len(clients)
        }
        return data

    def query_printer_client(self, client_id):
        reg = self.redis_manager.get_json(f"{self.namespace}:{client_id}")
        if reg is None:
            return HTTPException(status_code=404, detail="Client not found or no printers registered.")
        return PrinterRegistration(**reg)



class CupsPrintJobRequestService:

    def __init__(self):
        """
        管理打印任务
        """
        self.redis_manager = RedisDataManager()
        self.namespace = "PRINT_JOB_REQ"

    def query_print_job(self, job_id: str) -> PrintJob:
        key = f"{self.namespace}:{job_id}"
        res = self.redis_manager.get_json(key)
        if res is None:
            return None
        return PrintJob(**res)

    def query_all_print_jobs(self) -> dict:
        keys = self.redis_manager.get_keys_with_prefix(f"{self.namespace}:*")
        logger.info(f"Found print jobs: {len(keys)}.")
        print_jobs: List[PrintJob] = []
        for key in keys:
            job_attrs = self.redis_manager.get_json(key)
            if job_attrs is not None:
                print_jobs.append(PrintJob(**job_attrs))
        return {
            "jobs": print_jobs,
            "total": len(print_jobs)
        }

    def add_print_job(self, print_job: PrintJob):
        job_id = time.time() * 1000
        job_id = str(int(job_id))
        key = f"{self.namespace}:{job_id}"
        time_to_live_sec = 3600 * 24 * 14  # 14 days
        print_job.id = job_id
        self.redis_manager.set_json(key, print_job.dict(), time_to_live_sec=time_to_live_sec)
        return {
            "job_id": job_id,
            "client_id": print_job.client_id,
            "message": f"Print job {job_id} added.",
            "expires": time_to_live_sec,
            "created_at": str_util.current_time(),
        }

    def remove_print_job(self, job_id: str):
        key = f"{self.namespace}:{job_id}"
        self.redis_manager.delete(key)
        return {
            "job_id": job_id,
            "message": f"Print job {job_id} deleted."
        }




class CupsJobStatusService:

    def __init__(self):
        """
        管理打印任务状态
        """
        self.redis_manager = RedisDataManager()
        self.namespace = "CUPS_JOB_STATUS"

    def query_print_job_status(self, client_id: str, job_id: str) -> JobStatusUpdate:
        redis_manager = RedisDataManager()
        key = f"{self.namespace}:{client_id}:{job_id}"
        print(key)
        res = redis_manager.get_json(key)
        if res is None:
            return None
        return JobStatusUpdate(**res)

    def update_print_job_status(self, update: JobStatusUpdate):
        key = f"{self.namespace}:{update.client_id}:{update.job_id}"
        self.redis_manager.set_json(key, update.dict(), time_to_live_sec=3600)
        return {"message": f"Print job [{key}] inserted."}

    def notify_job_status(self, update: JobStatusUpdate):
        job_id = update.job_id
        print_job_status = self.query_print_job_status(job_id)
        # 确保任务存在
        if print_job_status is None:
            raise HTTPException(status_code=404, detail="Job not found")

        # 更新任务状态
        # print_job_status["status"] = update.status
        # print_job_status = update
        #
        # if update.status == "failed" and update.error_message:
        #     print_job_status["error_message"] = update.error_message

        # 更新任务状态
        print_job_status = update
        self.update_print_job_status(print_job_status.job_id, print_job_status.dict())

        # 如果需要，可以根据状态采取不同的操作，如通知用户
        if print_job_status.status == "completed":
            print(f"Job {job_id} completed successfully.")
        elif print_job_status.status == "failed":
            print(f"Job {job_id} failed with error: {print_job_status.error_message}")

        return {"message": f"Status of job {job_id} updated to {print_job_status.status}"}
