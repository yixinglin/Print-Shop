import os
from typing import List
import requests
import client.lib as cupslib
import json

import client.rest as rest
from schemas.cups import PrintJob

# SERVER_URL = "http://localhost:634"  # 服务端地址
LOCAL_DOWNLOAD_PATH = "temp/client/jobs"  # 本地下载路径

os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)


class CupsClients:
    def __init__(self, client_id):
        self.client_id = client_id

    def register_printers(self):
        # Register printers to the server
        printers = cupslib.list_printers()
        attrs = []
        for p in printers:
            name = p['printer-name']
            a = cupslib.printer_attributes_brief(name)
            attrs.append(a)
        body = dict(
            client_id=self.client_id,
            attrs=attrs,
            total=len(attrs)
        )
        response = rest.register_cups_client(body)
        print("Register response:", response.text)

    def fetch_print_jobs(self) -> List[PrintJob]:
        # 从服务端获取任务（实际可能使用消息队列或REST API）
        resp = rest.fetch_all_requested_print_jobs()
        if resp.status_code == 200:
            jobs = resp.json()["jobs"]
            jobs = [PrintJob(**j) for j in jobs]
            jobs = [j for j in jobs if j.client_id == self.client_id]
        else:
            raise RuntimeError(f"Failed to fetch print jobs. Server response: {resp.status_code}")

        return jobs

    def delete_print_job(self, job_id):
        # 从服务端删除任务（实际可能使用消息队列或REST API）
        return rest.delete_requested_print_job(self.client_id, job_id)

    def download_file(self, file_url, job_id):
        response = requests.get(file_url)
        file_path = os.path.join(LOCAL_DOWNLOAD_PATH, f"{job_id}.pdf")
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path

    def execute_print_job(self, job_id, file_path, printer_id, options):
        try:
            # 连接CUPS
            # conn = cups.Connection()
            # printers = conn.getPrinters()
            printers = [dict(printer_id="local_printer", name="Local Printer", device_uri="lpd://localhost")]
            printer_id_list = [p["printer_id"] for p in printers]

            # 检查打印机是否存在
            if printer_id not in printer_id_list:
                raise Exception(f"Printer {printer_id} not found")

            # 报告状态：任务开始执行
            resp = self.report_job_status_to_server(job_id, "in_progress")

            # 执行打印
            print_options = {
                "copies": str(options.get("copies", 1)),
                "media": options.get("paper_size", "A4"),
                "sides": "two-sided-long-edge" if options.get("duplex") else "one-sided"
            }

            # conn.printFile(printer_id, file_path, "Print Job", print_options)
            print(f"Job {job_id} sent to printer {printer_id}")

            # 报告状态：任务成功完成
            self.report_job_status_to_server(job_id, "completed")
            return True
        except Exception as e:
            # 报告状态：任务失败
            self.report_job_status_to_server(job_id, "failed", error_message=str(e))
            print(f"Job {job_id} failed with error: {e}")
            return False

    # def report_job_status_to_server(self, job_id, status, error_message=None):
    #     status_data = {
    #         "job_id": job_id,
    #         "status": status,
    #         "error_message": error_message
    #     }
    #     try:
    #         response = requests.post(f"{SERVER_URL}/api/cups/task/notify_job_status", json=status_data)
    #         if response.status_code == 200:
    #             print(f"Successfully reported status {status} for job {job_id}")
    #         else:
    #             print(f"Failed to report status for job {job_id}. Server response: {response.status_code}")
    #             print(response.text)
    #     except Exception as e:
    #         print(f"Error reporting status: {e}")

    def run(self):
        pass
