
import {
  ClockCircleOutlined,
  CloseCircleOutlined,
  ExclamationCircleOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import { Divider, Flex, Tag } from 'antd';



const PrinterCard = ({index, printer, handleClick }) => {    
  const printerName = printer.name;
  
  const cardStyle = {
    ...styles.card,
    backgroundColor: getCardColor(getStatusName(printer.state)),
  };


  return (
    <div style={cardStyle} onClick={() => { handleClick ? handleClick(printer) : null }}>            
      <h3>{getStatusEmoji(printer.state)} {printerName}</h3>
      <p><strong>Alias:</strong> {printer.alias}</p>
      <p><strong>Status:</strong> {createStatusTag(printer.state)}</p>      
      <p><strong>Message:</strong> {printer.state_message}</p>
      <p><strong>Reasons:</strong> {printer.state_reasons.join(', ')}</p>
    </div>
  );
};


const getCardColor = (state) => {
  switch (state) {
    case 'Idle':
      return '#d4edda'; // 绿色背景，表示空闲状态
    case 'Printing':
      return '#cce5ff'; // 蓝色背景，表示打印中
    case 'Stopped':
      return '#f8d7da'; // 红色背景，表示错误
    default:
      return '#fefefe'; // 默认灰白色背景
  }
};

const getStatusName = (state) => {
  switch (state) {
    case 4:
      return "Printing";
    case 3:
      return "Idle";
    case 5:
      return "Stopped";
    default:
      return "Unknown";
  }
};

const getStatusEmoji = (state) => {
  switch (state) {
    case 4:
      return "🖨️";
    case 3:
      return "😴";
    case 5:
      return "⛔️";
    default:
      return "❓";
  };
}


const createStatusTag = (status) => {
  switch (status) {
    case 4:
      return <Tag icon={<SyncOutlined  spin />} color="processing">Printing</Tag>;
    case 3:
      return <Tag icon={<ClockCircleOutlined  />} color="success">Idle</Tag>;
    case 5:
      return <Tag icon={<CloseCircleOutlined />} color="error">Stopped</Tag>;
    default:
      return <Tag icon={<ExclamationCircleOutlined />} color="warning">Unknown</Tag>;
  }
}


const styles = {
  card: {
    fontFamily: 'Arial, sans-serif',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    padding: '10px',
    margin: '10px',
    textAlign: 'left',
    boxShadow: '6px 6px 7px rgba(0, 0, 0, 0.5)',
    // width: 'calc(25% - 32px)', // 调整宽度以适应每行四张卡片
    boxSizing: 'border-box',
    width: '250px',
  },
};

export default PrinterCard;
