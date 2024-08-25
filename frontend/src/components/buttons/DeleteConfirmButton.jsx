import React from 'react';
import { Popconfirm, Button } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

const ConfirmButton = ({
  buttonText = "Confirm",   // 默认按钮文字
  confirmText = "Yes",      // 确认按钮文字
  cancelText = "No",        // 取消按钮文字
  popconfirmTitle = "Are you sure?", // Popconfirm 的标题
  popconfirmDescription = "Do you want to proceed?", // Popconfirm 的描述
  handleConfirm, // 确认回调函数
  danger = false, // 是否是危险按钮
}) => {
  return (
    <Popconfirm
      title={popconfirmTitle}
      description={popconfirmDescription}
      onConfirm={handleConfirm}
      icon={<QuestionCircleOutlined style={{ color: danger ? 'red' : 'blue' }} />}
      okText={confirmText}
      cancelText={cancelText}
    >
      <Button danger={danger}>{buttonText}</Button>
    </Popconfirm>
  );
};

export default ConfirmButton;
