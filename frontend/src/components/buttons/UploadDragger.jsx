import React from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

function UploadDragger({ url }) {
  const props = {
    name: 'file',
    multiple: true, // 支持多文件上传
    action: url, // 文件上传的服务端URL
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

  const { Dragger } = Upload;

  return (
    <Dragger {...props}>
      {/* <Button icon={<UploadOutlined />}>Click to Upload</Button> */}
      <p style={styles.upload_drag_icon}>
        <UploadOutlined />
      </p>
      <p style={styles.upload_text}>Click or drag file to this area to upload</p>
      <p style={styles.upload_hint}>Support for a single or bulk upload. Only PDF files are allowed.</p>
    </Dragger>
  );
}

const styles = {
  upload_drag_icon: {
    borderRadius: 4,
    fontSize: 70,
    padding: '10px',
    textAlign: 'center',
    color: '#999',
    cursor: 'pointer',
    width: '100%',
    height: '50px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    margin: '1px 0',
  },

  upload_text: {  
    margin: '10px 0',
    color: '#888',
    fontSize: '16px',
    textAlign: 'center',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '1px',
    width: '100%',
    cursor: 'pointer',
    borderRadius: 4,
    padding: '1px',
  },

  upload_hint: {
    margin: '1px 0',
    color: '#999',
    fontSize: '13px',
    textAlign: 'center',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
    width: '100%',
    cursor: 'pointer',
    borderRadius: 4,
    padding: '10px',
  }
}

export default UploadDragger;
