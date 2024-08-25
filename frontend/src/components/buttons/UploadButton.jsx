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
    onPreview(file) {
      console.log('Preview:', file.name);
    },
    onRemove(file) {
      console.log('Remove:', file.name);
    },
    
  };

  return (
    <Upload {...props}>
      <Button icon={<UploadOutlined />}>Click to Upload</Button>
    </Upload>
  );
};

export default UploadButton;
