import { FC } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';

interface InteractiveTableProps {
  rowData: any[];
  columnDefs: any[];
}

const InteractiveTable: FC<InteractiveTableProps> = ({ rowData, columnDefs }) => {
  const defaultColDef = {
    resizable: true,
    sortable: true,
    filter: true,
    wrapText: true,
    autoHeight: true,
  };

  const gridOptions = {
    enableRangeSelection: true,
    defaultColDef,
    suppressHorizontalScroll: false,
    columnDefs: columnDefs.map((col) =>
      col.field === 'document'
      ? { ...col, cellRenderer: (params: any) => params.value ? { __html: params.value } : '' }
      : col
    )
  };

  return (
    <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
      <AgGridReact
        rowData={rowData}
        gridOptions={gridOptions}
        pagination={true}
        paginationPageSize={10}
        domLayout='autoHeight'
      />
    </div>
  );
};

export default InteractiveTable;
