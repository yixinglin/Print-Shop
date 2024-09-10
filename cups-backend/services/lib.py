import cups 
import time
from typing import List
from pydantic import BaseModel
from utils import strutils


class PrintJob(BaseModel):
    printer_name: str
    filename: str  # filename in the history directory
    hash: str  # hash of the file in the history directory
    title: str = "Print Job"
    enabled_watermark: bool = False
    options: dict={}


def convert_doc_to_pdf():
    pass 

def convert_img_to_pdf():
    pass 
  
def print_jobs():
    print("Print Jobs")
    conn = cups.Connection()
    jobs = conn.getJobs()
    return jobs

def printer_status(printer):
    print("Printer Status")
    conn = cups.Connection()
    attrs = conn.getPrinterAttributes(printer)
    status = {}
    status['printer-state'] = attrs['printer-state']  # 3: idle, 4: printing, 5: stopped
    status['printer-state-message'] = attrs['printer-state-message']
    status['printer-state-reasons'] = attrs['printer-state-reasons']
    status['printer-type'] = attrs['printer-type']
    status['printer-is-accepting-jobs'] = attrs['printer-is-accepting-jobs']
    status['printer-info'] = attrs['printer-info']
    status['printer-location'] = attrs['printer-location']
    status['printer-make-and-model'] = attrs['printer-make-and-model']
    status['printer-uri-supported'] = attrs['printer-uri-supported']
    status['printer-op-policy'] = attrs['printer-op-policy']
    return status

def printer_attributes(printer):
    print("Printer Attributes")
    conn = cups.Connection()
    attrs = conn.getPrinterAttributes(printer)
    return attrs

def printer_attributes_brief(printer):
    print('Printer Brief Attributes ')
    conn = cups.Connection()
    attrs = conn.getPrinterAttributes(printer)
    brief = {}
    brief['printer-id'] = attrs['printer-id']
    brief['printer-uuid'] = attrs['printer-uuid']
    brief['printer-name'] = attrs['printer-name']
    brief['printer-info'] = attrs['printer-info']
    brief['printer-state'] = attrs['printer-state']
    brief['printer-state-message'] = attrs['printer-state-message']
    brief['printer-state-reasons'] = attrs['printer-state-reasons']
    brief['printer-uri-supported'] = attrs['printer-uri-supported']
    brief['printer-location'] = attrs['printer-location']
    brief['printer-name'] = attrs['printer-name']
    brief['print-scaling-supported'] = attrs['print-scaling-supported']
    brief['pdf-versions-supported'] = attrs['pdf-versions-supported']
    brief['orientation-requested-supported'] = attrs['orientation-requested-supported']
    brief['which-jobs-supported'] = attrs['which-jobs-supported']
    brief['job-settable-attributes-supported'] = attrs['job-settable-attributes-supported']  
    brief['printer-resolution-supported']   = attrs['printer-resolution-supported']
    brief['sides-supported'] = attrs['sides-supported']
    brief['cups-version'] = attrs['cups-version']
    brief['media-supported'] = attrs['media-supported']
    brief['document-format-supported'] = attrs['document-format-supported']
    return brief

def list_printers() -> List:
    print("List Printers")
    conn = cups.Connection()
    printers = []
    for k, v in conn.getPrinters().items():        
        if v['printer-is-shared'] == True:
            v['printer-name'] = k
            printers.append(v)
    return printers 


def create_job(printer_name: str, file_path: str, title: str, options: dict):
    # TODO: 打印加上水印功能
    print(f"Create Job ({title}) with options:\n{options}")
    print(f"File Path: {file_path}")
    conn = cups.Connection() 

    if options:
        # Remove empty fields
        options = {k: v for k, v in options.items() if not strutils.isEmptyString(v)}
        print(f"Options after removing empty fields: {options}")
    job_id = conn.printFile(printer_name, file_path, title, options)
    print("Job ID:", job_id)
    return job_id

def job_attributes(job_id):
    print(f"Job Attributes  ({job_id})")
    conn = cups.Connection()
    attrs = conn.getJobAttributes(job_id)
    return attrs

def cancel_job(job_id):
    print("Cancel Job")
    conn = cups.Connection()    
    conn.cancelJob(job_id)
    print("Job", job_id, "cancelled")   
    return job_id

def cancel_all_jobs():
    print("Cancel All Jobs")
    conn = cups.Connection()    
    jobs = conn.getJobs(which_jobs='all', requested_attributes=['job-id'], my_jobs=False)
    for job_id  in jobs:
        try:
            conn.cancelJob(job_id)
            print("Job", job_id, "cancelled")   
        except cups.IPPError:
            print("Job", job_id, "not found")   

def create_options(copies=1, sides='one-sided', 
                   collate=None, fit_to_page=None, 
                   page_ranges=None, landscape=None,  
                   print_color_mode = "monochrome", 
                   print_quality="normal", 
                   print_scaling=None, 
                   resolution="300",
                   page_set=None,
                   media='default'):
    options = {}
    options['copies'] = str(copies)  # number of copies to print
    options['sides'] = sides # 'one-sided', 'two-sided-long-edge', 'two-sided-short-edge', 'two-sided-short-edge-flip', 'two-sided-long-edge-flip'
    if collate:
        options['collate'] = collate # True or False, collate multiple copies of each page on a single sheet of paper
    if fit_to_page:
        options['fit-to-page'] = fit_to_page # True or False, fit the printable area to the page size
    if page_ranges:
        options['page-ranges'] = page_ranges # '1-5', '1,3,5'
    if page_set:
        options['page-set'] = page_set # 'first', 'last', 'even', 'odd', 'next', 'previous'
    if landscape:
        options['landscape'] = landscape # True or False, rotate the printable area 90 degrees
    options['media'] = media  # 'default', 'a4', 'a5', 'b5', 'legal', 'letter', 'executive', 'tabloid'
    options['print-color-mode'] = print_color_mode # monochrome, color
    options['print-quality'] = print_quality # draft, normal, high
    if print_scaling:
        options['print-scaling'] = print_scaling # auto, none, fill, fit
    options['printer-resolution'] = resolution # 300, 600, 1200, 2400
    return options

def test_query(printer):
    status = printer_status(printer)
    # print(status)
    printers = list_printers()
    for printer in printers:
        print(printer)


if __name__ == '__main__':
    # print_jobs()
    #test_query('Virtual_PDF_Printer')
    #printer_attributes_brief('Virtual_PDF_Printer')
    printer = 'Virtual_PDF_Printer'
    source = './doc/dhl.pdf'
    # options = create_options(copies=5, sides='one-sided', collate="false", 
    #                          fit_to_page='none', page_ranges="", landscape='false', 
    #                          print_color_mode='color', print_quality='normal', page_set='even', 
    #                        print_scaling='none', resolution='150dpi', media='b5')    
    options = create_options(resolution='300dpi', media='custom_1682.04x2380.9mm_1682.04x2380.9mm')    
    create_job(printer, source, 'Test Job', options)    
    for i in range(10):
        status = printer_status(printer)
        time.sleep(0.5)
        print(status['printer-state'])
    