// frontend/src/components/InteractiveTable/index.tsx
import { FC, useState } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { ICellRendererParams, GridApi } from 'ag-grid-community';

interface InteractiveTableProps {
  rowData: any[];
  columnDefs: any[];
}

const truncateText = (text: string, maxLength: number) => {
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

const HtmlCellRenderer = (params: ICellRendererParams) => {
  return <span dangerouslySetInnerHTML={{ __html: params.value }} />;
};

const InteractiveTable: FC<InteractiveTableProps> = ({ rowData, columnDefs }) => {
  const [maxChars, setMaxChars] = useState(100); // Default max characters
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

  const gridOptions = {
    enableRangeSelection: true,
    defaultColDef,
    suppressHorizontalScroll: false,
    columnDefs: columnDefs.map((col) =>
      col.field === 'document'
      ? { ...col, cellRendererFramework: HtmlCellRenderer }
      : { ...col, valueFormatter: (params: any) => truncateText(params.value, maxChars) }
    ),
  };

  const onBtExport = () => {
    if (gridApi) {
      gridApi.exportDataAsCsv();
    }
  };

  const onGridReady = (params: any) => {
    setGridApi(params.api);
  };

  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
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
          gridOptions={gridOptions}
          pagination={true}
          paginationPageSize={10}
          domLayout='autoHeight'
          onGridReady={onGridReady}
        />
      </div>
    </div>
  );
};

export default InteractiveTable;
