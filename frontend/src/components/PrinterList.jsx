import PrinterCard from './PrinterCard';

import { Flex } from 'antd';

const PrinterList = ({printers, handleClickCard}) => {
  return (
    <Flex wrap gap="small">
             {printers.map((printer, index) => (
        <PrinterCard index={index} 
          handleClick={handleClickCard}
          printer={ {
              'name': printer['printer-name'],
              'alias': printer['printer-info'],
              'state_message': printer['printer-state-message'],
              'state_reasons': printer['printer-state-reasons'],
              'state': printer['printer-state'],
          }
        } />
      ))}
    </Flex>
  );


};

export default PrinterList;
