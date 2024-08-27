import React, { useEffect, useState } from 'react';
import { fetch_list_history_files, delete_file, delete_all_files, get_download_file_url } from '../rest/printer.js';
import HistoryFileList from '../components/HistoryFileList.jsx';
import { message } from "antd";
import { useNavigate } from 'react-router-dom';


function Home() {
  const navigate = useNavigate(); // 使用 useNavigate 钩子进行导航
  const [files, setFiles] = useState([]);
  const [totalSize, setTotalSize] = useState("0");

  function messagePopup(text) {
    message.info(text);
  }

  function errorPopup(text) {
    message.error(text);
  }


  useEffect(() => {
    // fetch history files
    fetch_list_history_files()
      .then(response => {
        // messagePopup("Successfully fetched history files");
        setFiles(response.data.files);
        setTotalSize(response.data.total_size);
      })
      .catch(error => errorPopup(`Error fetching history files: ${error}`));
  }, []);


  // 处理打印操作
  const handlePrint = (record) => {
    console.log('Print:', record.filename);
    navigate('/create-job', { state: { file: record } }) // 跳转并传递文件数据
  };

  const handleDownload = (record) => {
    const url = get_download_file_url(record.filename)
    console.log('Download:', url);
    window.open(url, '_blank');
  }

  const handleAdd = () => {
    errorPopup(`Add. 尚未实现此功能.`);
  }

  const handleEmpty = () => {
    // errorPopup(`Empty. 尚未实现此功能.`);
    delete_all_files()
      .then(response => {
        messagePopup("All files deleted");
        setFiles([]);
        setTotalSize("0");
      })
      .catch(error => errorPopup(`Error deleting all files: ${error}`));
  }


  // 处理删除操作
  const handleDelete = (record) => {
    console.log(`Delete: ${record.filename}`);
    delete_file(record.filename)
      .then(response => {
        messagePopup(`File deleted [${record.filename}]`);
        // 更新文件列表
        setFiles(files.filter(file => file.filename !== record.filename));
      })
      .catch(error => messagePopup(`Error deleting file: ${error}`,));
  };

  return (
    <div style={{ fontFamily: "arial, calibri, sans-serif" }}>
      <h1>  𓍢ִ໋🌷͙֒₊˚*ੈ♡⸝⸝🪐༘⋆ </h1>
      <h1>HOME</h1>
      <p><strong>💡 Note</strong>: Please convert your files to <span style={{ color: "red" }}>PDF</span> before printing.</p>
      <HistoryFileList
        files={files}
        totalSize={totalSize}
        handlePrint={handlePrint}
        handleDownload={handleDownload}
        handleEmpty={handleEmpty}
        handleAdd={handleAdd}
        handleDelete={handleDelete} />
    </div>
  )
}

export default Home;