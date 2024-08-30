import React, { useState } from 'react';
import { Table, Pagination, Button, Space, Input, Flex } from 'antd';
import { PrinterOutlined, DeleteOutlined, SearchOutlined, EyeOutlined } from '@ant-design/icons';
import UploadDragger from './buttons/UploadDragger';
import DeleteConfirmButton from './buttons/DeleteConfirmButton';
import { get_upload_file_url } from '../rest/printer'

const HistoryFileList = ({ files, totalSize, handlePrint, handleDelete, handleDownload,
  handleAdd, handleEmpty }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [searchText, setSearchText] = useState('');

  const columns = [
    {
      title: 'Created At',
      dataIndex: 'create_at',
      key: 'create_at',
      width: 200,
    },
    {
      title: 'Filename',
      dataIndex: 'filename',
      key: 'filename',
    },
    {
      title: 'Size',
      dataIndex: 'size',
      key: 'size',
      width: 150,
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 150,
      render: (text, record) => (
        <Space size="middle">
          <Button
            type="primary"
            icon={<PrinterOutlined />}
            onClick={() => { handlePrint ? handlePrint(record) : null }}
          />
          <Button
            icon={<EyeOutlined />}
            onClick={() => { handleDownload ? handleDownload(record) : null }}
          />
          <Button
            danger
            icon={<DeleteOutlined />}
            onClick={() => { handleDelete ? handleDelete(record) : null }}
          />
        </Space>
      ),
    },
  ];

  // 处理页码和每页条目数变化
  const handlePageChange = (page, size) => {
    setCurrentPage(page);
    setPageSize(size);
    // Scroll to top of page  
    window.scrollTo(0, 0);
  };

  // 处理搜索输入变化
  const handleSearch = (e) => {
    setSearchText(e.target.value);
    setCurrentPage(1); // 搜索时重置到第一页
  };

  // 过滤文件列表
  const filteredFiles = files.filter(file =>
    file.filename.toLowerCase().includes(searchText.toLowerCase())
  );

  const resetSearchKeyword = () => {
    setSearchText('');
    setCurrentPage(1);
  }

  // 计算当前页的数据
  const paginatedFiles = filteredFiles.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <div>
      <Flex  gap="large" wrap style={{ marginBottom: '10px' }} >        
        <Input
          placeholder="Search by filename"
          prefix={<SearchOutlined />}
          value={searchText}
          onChange={handleSearch}
          style={{ width: '300px' }}
        />
        <Button type="primary" onClick={() => { resetSearchKeyword ? resetSearchKeyword() : null }} >Reset</Button>

        <DeleteConfirmButton
          buttonText="Remove All Files"
          popconfirmTitle="Remove All Files"
          popconfirmDescription="Are you sure you want to remove all files?"
          confirmText="Yes, delete all"
          cancelText="No"
          handleConfirm={() => { handleEmpty ? handleEmpty() : null }}
          danger
        />

        <span>Total Size: {totalSize}</span>
        {/* <span>Files: {filteredFiles.length}</span> */}
      </Flex >
      <UploadDragger url={get_upload_file_url()} />
      <Table
        columns={columns}
        dataSource={paginatedFiles}  // 使用分页后的数据
        pagination={false}  // 关闭默认分页
        rowKey="filename"
        cellFontSizeSM={10}
      />
      <Pagination
        current={currentPage}
        pageSize={pageSize}
        total={filteredFiles.length}  // 使用过滤后的数据长度
        onChange={handlePageChange}
        showSizeChanger
        pageSizeOptions={['10', '25', '50', '100']}
        showTotal={(total) => `Total ${total} items`}
      />

    </div>
  );
};



export default HistoryFileList;
