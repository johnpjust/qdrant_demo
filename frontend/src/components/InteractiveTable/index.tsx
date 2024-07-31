import { FC } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

interface InteractiveTableProps {
  rowData: any[];
  columnDefs: any[];
}

const InteractiveTable: FC<InteractiveTableProps> = ({ rowData, columnDefs }) => {
  return (
    <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}> {/* Adjust height and width */}
      <AgGridReact
        rowData={rowData}
        columnDefs={columnDefs}
        pagination={true}
        paginationPageSize={10}
        domLayout='autoHeight'
      />
    </div>
  );
};

export default InteractiveTable;
