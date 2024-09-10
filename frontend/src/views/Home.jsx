import React, { useEffect, useState } from 'react';
import { fetch_list_history_files, delete_file, delete_all_files, get_download_file_url, restore_file } from '../rest/printer.js';
import HistoryFileList from '../components/HistoryFileList.jsx';
import { message } from "antd";
import { useNavigate } from 'react-router-dom';


function Home() {
  const navigate = useNavigate(); // 使用 useNavigate 钩子进行导航
  const [files, setFiles] = useState([]);
  const [includeArchived, setIncludeArchived] = useState(false);
  const [totalSize, setTotalSize] = useState(0);

  function messagePopup(text) {
    message.info(text);
  }

  function errorPopup(text) {
    message.error(text);
  }


  useEffect(() => {
    // fetch history files
    fetch_list_history_files({include_archived: includeArchived})
      .then(response => {        
        let files_ = response.data.files;
        // Add key to each file object to avoid warning
        files_.forEach((file, index) => {
          file.key = index.toString();  // convert index to str
        });
        setFiles(() => files_);
        setTotalSize(response.data.total_size);
      })
      .catch(error => errorPopup(`Error fetching history files: ${error}`));
  }, [includeArchived]);


  // 处理打印操作
  const handlePrint = (record) => {
    console.log('Print:', record.file_name);
    navigate('/create-job', { state: { file: record } }) // 跳转并传递文件数据
  };

  const handleDownload = (record) => {
    const url = get_download_file_url(record.file_hash, true, false);
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
    console.log(`Delete: ${record.file_name}`);
    delete_file(record.file_hash)
      .then(response => {
        messagePopup(`File deleted [${record.file_name}]`);
        // 更新文件列表
        // setFiles(files.filter(file => file.file_name !== record.file_name));
        record.archived=true;
        setFiles(files.map(file => file.file_name === record.file_name ? record : file));
      })
      .catch(error => messagePopup(`Error deleting file: ${error}`,));
  };

  const handleRestore = (record) => {
    console.log(`Restore: ${record.file_name}`);
    // 实现恢复文件功能    
    restore_file(record.file_hash)
     .then(response => {
        messagePopup(`File restored [${record.file_name}]`);
        record.archived=false;
        setFiles(files.map(file => file.file_name === record.file_name ? record : file));
      }
     ).catch(error => errorPopup(`Error restoring file: ${error}`));

  }

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
        handleArchiveIncluded={() => setIncludeArchived(!includeArchived)}
        handleDelete={handleDelete} 
        handleRestore={handleRestore}/>
    </div>
  )
}

export default Home;