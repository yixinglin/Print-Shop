from client.cups_cli import CupsClients
from core.config import load_client_config
from core.config import client_config as config

print(config)
print(config.logging)
print(config.logging.level)


def round():
    # 初始化: 创建CUPS客户端,
    client_id = "client-1"
    print(f"Initializing CUPS client: {client_id}...")
    cups_client = CupsClients(client_id)
    cups_client.register_printers()

    # 获取打印任务, by client_id
    print_jobs = cups_client.fetch_print_jobs()
    total_jobs = len(print_jobs)
    done_jobs = 0
    print("#Jobs: ", total_jobs)

    for i, job in enumerate(print_jobs):
        print(f"\n[{i+1}] New print job: ")
        print(job)
        print("Downloading file...")
        print("Executing print job...")
        success = True
        if success:
            done_jobs += 1
            # cups_client.delete_print_job(job['id'])
            print(f"Job [{done_jobs}/{total_jobs}] executed successfully!")



    # 下载文件
    # file_path = download_file(print_job["file_url"], print_job["job_id"])
    # file_path = "temp/client/jobs/sample-job-id.pdf"
    #
    # # 执行打印
    # success = cups_client.execute_print_job(print_jobs["job_id"], file_path, print_job["printer_id"], print_job["options"])
    #

    # print(f"Job [{done_jobs}/{total_jobs}] executed successfully!")


# 模拟pycups客户端的主程序
if __name__ == "__main__":
    round()
