import React, { useEffect, useState } from 'react';
import { fetch_printers, post_create_job, get_printer_status_ws_listener_url , 
    fetch_printer_attributes, get_cups_admin_url, get_download_file_url } from '../rest/printer.js';
import PrinterList from '../components/PrinterList';
import PrintJobForm from '../components/forms/PrintJobForm';
import PDFViewer from '../components/PDFViewer.jsx';
import { message, Select, Flex } from 'antd';
import { useLocation } from 'react-router-dom';
import { saveToLocalStorage, restoreFromLocalStorage } from "../core/storage"
import { useNavigate } from 'react-router-dom';


const { Option } = Select;

function CreateJobView() {
    const location = useLocation();
    const { file } = location.state || {}; // 获取传递过来的任务    
    console.log("CreateJobView", file);
    const [formKey, setFormKey] = useState(0);
    const [printers, setPrinters] = useState([]);
    const [currentPrinter, setCurrentPrinter] = useState({});
    const [currentPrinterAttrs, setCurrentPrinterAttrs] = useState(null);

    function messagePopup(text) {
        message.info(text);
    }

    function errorPopup(text) {
        message.error(text);
    }

    useEffect(() => {
        // fetch printers
        const wss = [];
        fetch_printers()
            .then(response => {
                const printers_ = response.data.printers;
                // console.log(printers_);
                setPrinters(printers_);
                if (printers_.length > 0) {
                    setCurrentPrinter(printers_[0]);
                }
                printers_.forEach(p => {
                    const ws = buildWsConnection(p);
                    wss.push(ws);
                  }
                )
                    
            }
            )
            .catch(error => errorPopup(`Error fetching printers: ${error}`));
        // 当组件卸载时关闭WebSocket连接
        return () => {
            console.log("Unmounting CreateJobView");
            // Close WebSocket connections
            wss.forEach(ws => ws.close());
        };  
        
    }, []);


    const handleClickPrinterCard = (
        (printer_) => {
            console.log("Selected printer:", printer_);
            const printerName = printer_.name;
            const pri = printers.filter(p => p["printer-name"] === printerName)[0];

            fetch_printer_attributes(printerName)
                .then(response => {
                    // console.log("Printer Attributes:", response.data);
                    setCurrentPrinter(pri);
                    setCurrentPrinterAttrs(response.data["printer_attributes"]);
                    setFormKey(formKey + 1)
                    // Scroll to top of page                    
                })
                .catch(error => errorPopup('Error fetching printer attributes:', error));
        }
    );

    const buildWsConnection = (printer_) => {
        // This function builds a WebSocket connection to the printer server
        // In order to receive real-time updates on the printer status
        console.log("Building WS Connection for printer:", printer_);
        const printerName = printer_['printer-name'];
        const ws = new WebSocket(`${get_printer_status_ws_listener_url(printerName)}`);
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          handleReceivePrinterMessage(data);        
        };
    
        ws.onclose = () => {
          console.log('WebSocket connection closed');
        };
    
        ws.onerror = (error) => {
          console.log('WebSocket error:', error);
        };
        return ws;
    }

    const handleReceivePrinterMessage = (printer_) => {
        // This function is called when a message is received from the printer server
        // We can use this to update the printer status in real-time
        // console.log("Printer Message:", printer_);
        // Update printer status in real-time
        setPrinters((prevPrinters) =>
            prevPrinters.map((printer) =>
            printer['printer-name'] === printer_['printer-name']
                ? { ...printer, ...printer_ } // 更新对应打印机的状态
                : printer
            )
        );

        // TODO: Update print job status in real-time

    }

    /*
     printOptions: {
         {
              "EPSON_XP-6000": {
                   "pageRange": "1-5",
                   "copies": "1",
                   "paperSize": "iso_a4_210x297mm",
                   "printScaling": "auto",
                   "pageSet": "1-5",
                   "colorMode": "color"
              }            
     }
    */

    const saveFormValuesToLocalStorage = (formValues) => {      
        var printerName = currentPrinter['printer-name'];  
        var data = restoreFromLocalStorage("print_job_options");
        if (!data) {
            data = { 'printOptions': {} }
        }
        data['printOptions'][printerName] = formValues;
        saveToLocalStorage("print_job_options", data);
        console.log("Saved form values to local storage: ", data);
    };

    const restoreFormValuesFromLocalStorage = () => {
        var printerName = currentPrinter['printer-name'];
        const data = restoreFromLocalStorage("print_job_options");
        console.log("data: ", printerName, data);
        var formValues = null;
                
        if (data && data['printOptions']  && data['printOptions'][printerName]) {
            formValues = data['printOptions'][printerName];
            formValues.copies = 1;
            formValues.pageSet = "all";
            formValues.pageRange = null;
            formValues.title = file.file_name;
        }

        return formValues;
    };

    const onFinish = (formValues) => {
        console.log('Form Values (Submit):', formValues);
        const options = {
            "page-ranges": formValues.pageRange,
            "copies": `${formValues.copies}`,
            "media": formValues.paperSize,
            "print-scaling": formValues.printScaling,
            "page-set": formValues.pageSet,
            "print-color-mode": formValues.colorMode
        }

        const printerName = currentPrinter['printer-name'];
        const jobDetails = {
            printer_name: printerName,
            filename: file.file_name,
            hash: file.file_hash,
            title: formValues.title,
            options: options
        };

        saveFormValuesToLocalStorage(formValues);
        window.scrollTo(0, 0);
        const detailsStr = JSON.stringify(jobDetails);
        post_create_job(JSON.parse(detailsStr))
            .then(response => {
                messagePopup(`Print job created: ${response.data.job_id}`);
            })
            .catch(error => errorPopup(`Error creating print job: ${error}`));
    };

    const initForm = (() => {               
        var formValues = restoreFormValuesFromLocalStorage();
        console.log("initForm: ", formValues);
        if (formValues === null) {
            formValues = {
                paperSize: "iso_a4_210x297mm",
                copies: 1,
                colorMode: "monochrome",
                printScaling: "auto",
                pageSet: "all",
            }
        }

        var mediaSizes = currentPrinterAttrs ? currentPrinterAttrs['media-supported'] : ["a4", "b5"];
        // Sort by name 
        const formOptions = {
            mediaSizes: mediaSizes,
            colorModes: ["color", "monochrome"],
        }
        // console.log("Form Data:", formData);
        // console.log("Form Options:", formOptions);
        
        return <PrintJobForm
            key_={formKey}
            title={file.file_name}
            formValues={formValues}
            formOptions={formOptions}
            onFinish={onFinish}
        />
    })


    if (!file) {
        return (<div>
            <h2>Oops!</h2>
            <p>No file selected. Please go back to the <a href="/">home</a> page
                and start with a file to print.
            </p>
        </div>
        )
    }

    return (
        <div style={{ fontFamily: "arial, calibri, sans-serif" }}>
            <h1>🌊✮ ⋆ 🦈｡ * ⋆｡</h1>
            <h1> New Print Job </h1>
            <p>💡 Please select a printer</p>
            <div style={styles.printlist_container}>
                <PrinterList printers={printers} handleClickCard={handleClickPrinterCard} />
            </div>

            <p style={styles.selected_printer}>🖨️【{currentPrinter['printer-name']}】 📌【{file.file_name}】 </p>
    
            <Flex wrap justify="left" gap="large" >
                <div style={{ minWidth: '300px' }}>
                    {currentPrinterAttrs ? initForm() : null}
                </div>
                <div>
                    {file && currentPrinterAttrs ? <PDFViewer url={get_download_file_url(file.file_hash)}
                        width="680px" height="600" title="📃 Document" /> : null}
                </div>                            
            </Flex>            

            <a href="/jobs">All Print Jobs</a>
            <br /> <br />
            <a href={get_cups_admin_url()} target="_blank">CUPS Admin</a>
        </div>
    );

}

// 示例数据
const exampleJobs = [
    {
      job_id: 1,
      number_of_documents: 3,
      job_media_progress: "50%",
      copies: 2,
      media: "A4",
      page_set: "all",
      print_color_mode: "color",
      print_scaling: "fit",
      time_at_creation: "2024-08-25 12:30:00",
      job_state: "printing",
      job_state_reasons: ["none"],
      document_name_supplied: "example1.pdf",
    },
    {
      job_id: 2,
      number_of_documents: 1,
      job_media_progress: "100%",
      copies: 1,
      media: "A3",
      page_set: "all",
      print_color_mode: "monochrome",
      print_scaling: "none",
      time_at_creation: "2024-08-25 13:00:00",
      job_state: "completed",
      job_state_reasons: ["completed-successfully"],
      document_name_supplied: "example2.pdf",
    },
    // 其他示例任务
  ];

const styles = {
    selected_printer: {
        fontFamily: "Arial",
        fontSize: "18px",
        fontWeight: "bold",
        color: "blue",
        padding: "10px",
        margin: "10px 0"
    },

    printlist_container: {
        margin: "10px",
        border: "1px dashed #ccc",
        borderRadius: "5px",
        width: "100%",
    }
}

export default CreateJobView;
