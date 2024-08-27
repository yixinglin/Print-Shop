import React from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const UploadButton = ({url}) => {
  const props = {
    name: 'file',
    multiple: true, // 支持多文件上传
    action: url, // # 'http://192.168.8.10:634/history/upload/', // 文件上传的服务端URL
    onChange(info) {
      if (info.file.status === 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        console.log(`${info.file.name} file uploaded successfully`);
        // refresh the page to show the uploaded file
        window.location.reload();
      } else if (info.file.status === 'error') {
        const errorMsg = info.file.response?.detail || `${info.file.name} file upload failed.`;
        message.error(`Error: ${errorMsg}. File ${info.file.name}  upload failed. `);        
      }
    },

    beforeUpload(file) {
      const isPDF = file.type === 'application/pdf';
      if (!isPDF) {
        message.error(`${file.name} is not a PDF file.`);
      }
      return isPDF || Upload.LIST_IGNORE;
    },

    onPreview(file) {
      console.log('Preview:', file.name);
    },
    onRemove(file) {
      console.log('Remove:', file.name);
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files);
    },
    
  };
  
  return (
    <Upload {...props} >
      <Button icon={<UploadOutlined />}>Click to Upload</Button>
      {/* <p style={styles.upload_drag_icon}>
          <UploadOutlined />
      </p>
      <p style={styles.upload_text}>Click or drag file to this area to upload</p>
      <p>Support for a single or bulk upload. Only PDF files are allowed.</p> */}
    </Upload>
  );
};

// const styles = {
//   upload_drag_icon: {
//     border: '1px solid #d9d9d9',
//     borderRadius: 4,
//     padding: '20px',
//     textAlign: 'center',
//     color: '#999',
//     cursor: 'pointer',
//     width: '100%',
//     height: '100%',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//     margin: '10px 0',
//   },

//   upload_text: {  
//     margin: '10px 0',
//     color: '#999',
//     fontSize: '14px',
//     textAlign: 'center',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//     height: '100%',
//     width: '100%',
//     cursor: 'pointer',
//     border: '1px solid #d9d9d9',
//     borderRadius: 4,
//     padding: '20px',
//   }
// }

export default UploadButton;
