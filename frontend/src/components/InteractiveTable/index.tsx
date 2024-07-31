import React, { FC, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { ICellRendererParams, GridApi, GridReadyEvent } from 'ag-grid-community';

interface InteractiveTableProps {
  rowData: any[];
  columnDefs: any[];
  maxChars: number; // Add maxChars as a prop
}

const truncateText = (text: string, maxLength: number) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const HtmlCellRenderer = (params: ICellRendererParams) => {
  return <span dangerouslySetInnerHTML={{ __html: params.value }} />;
};

const InteractiveTable: FC<InteractiveTableProps> = ({ rowData, columnDefs, maxChars }) => {
  const [gridApi, setGridApi] = useState<GridApi | null>(null); // Define type for gridApi

  const defaultColDef = {
    resizable: true,
    sortable: true,
    filter: true,
    wrapText: true,
    autoHeight: true,
    cellStyle: {
      whiteSpace: 'normal',
      lineHeight: '1.2',
    },
  };

  const onBtExport = () => {
    if (gridApi) {
      const exportParams = {
        processCellCallback: (params: any) => {
          if (params.column.getColId() === 'document') {
            return params.value;
          }
          return params.value;
        },
      };
      gridApi.exportDataAsCsv(exportParams);
    }
  };

  const onGridReady = (params: GridReadyEvent) => {
    setGridApi(params.api);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <button onClick={onBtExport} style={{ marginLeft: '10px' }}>
          Export CSV
        </button>
      </div>
      <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs.map((col) =>
            col.field === 'document'
            ? { ...col, cellRendererFramework: HtmlCellRenderer }
            : { ...col, valueFormatter: (params: any) => truncateText(params.value, maxChars) }
          )}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={10}
          domLayout='autoHeight'
          onGridReady={onGridReady}
          enableRangeSelection={true}  // Enable range selection for clipboard functionality
        />
      </div>
    </div>
  );
};

export default InteractiveTable;
