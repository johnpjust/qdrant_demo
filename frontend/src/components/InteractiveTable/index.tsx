import { FC, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { GridApi, GridReadyEvent } from 'ag-grid-community';

interface InteractiveTableProps {
  rowData: any[];
  columnDefs: any[];
  maxChars: number; // Add maxChars as a prop
  setMaxChars: (value: number) => void; // Add setMaxChars as a prop
}

const truncateText = (text: string, maxLength: number) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const InteractiveTable: FC<InteractiveTableProps> = ({ rowData, columnDefs, maxChars, setMaxChars }) => {
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
        allColumns: true, // Export all columns
        onlySelected: false, // Export all rows
        processCellCallback: (params: any) => {
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
      <div style={{ marginBottom: '10px', textAlign: 'center' }}> {/* Center the max characters box */}
        <label>
          Max Characters:
          <input
            type="number"
            value={maxChars}
            onChange={(e) => setMaxChars(Number(e.target.value))}
            style={{ marginLeft: '10px', width: '50px' }}
          />
        </label>
        <button onClick={onBtExport} style={{ marginLeft: '10px' }}>
          Export CSV
        </button>
      </div>
      <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
        <AgGridReact
          rowData={rowData}
          columnDefs={columnDefs.map((col) =>
            col.field === 'document'
            ? { ...col, valueFormatter: (params: any) => truncateText(params.value, maxChars) }
            : { ...col, valueFormatter: (params: any) => truncateText(params.value, maxChars) }
          )}
          defaultColDef={defaultColDef}
          pagination={true}
          paginationPageSize={10}
          domLayout='autoHeight'
          onGridReady={onGridReady}
          enableRangeSelection={true}  // Enable range selection for clipboard functionality
          suppressCopySingleCellRanges={false}  // Allow copying
        />
      </div>
    </div>
  );
};

export default InteractiveTable;
