import { useState } from 'react';
import {
  Button,
  Container,
  TextInput,
  Loader,
  Box,
  Image,
  SegmentedControl,
  Text,
} from "@mantine/core";
import { IconSearch } from "@tabler/icons-react";
import { useStyles } from "./style";
import useMountedState from "@/hooks/useMountedState";
import { useGetSearchResult } from "@/hooks/useGetSearchResult";
import { getHotkeyHandler } from "@mantine/hooks";
import DemoSearch from "../DemoSearch";
import InteractiveTable from "../InteractiveTable";

export function Main() {
  const { classes } = useStyles();
  const [query, setQuery] = useMountedState("");
  const [maxChars, setMaxChars] = useState(100); // Default max characters
  const [numResults, setNumResults] = useState(5); // Default number of results
  const { data, error, loading, getSearch, resetData } = useGetSearchResult();
  const [isNeural, setIsNeural] = useMountedState(true);

  const handleSubmit = () => {
    if (query) {
      getSearch(query, isNeural, numResults);
    }
  };

  const onClickFindSimilar = (data: string) => {
    if (data) {
      resetData();
      setQuery(data);
      getSearch(data, isNeural, numResults);
    }
  };

  // Prepare data for the table
  const rowData = data?.result || [];
  const columnDefs = [
    { headerName: "Homepage URL", field: "homepage_url" },
    { headerName: "Alt", field: "alt" },
    { headerName: "Logo URL", field: "logo_url" },
    { headerName: "City", field: "city" },
    { headerName: "Document", field: "document" },
    { headerName: "Name", field: "name" },
  ];

  return (
    <Container className={classes.wrapper} size="100%"> {/* Use full width */}
      <Container p={0} size={600} className={classes.controls}>
        <SegmentedControl
          radius={30}
          data={[
            { label: "Neural", value: "neural" },
            { label: "Text", value: "text" },
          ]}
          onChange={(value) => {
            setIsNeural(value === "neural");
            resetData();
            query && getSearch(query, value === "neural", numResults);
          }}
          size="md"
          color="Primary.2"
          className={classes.control}
          value={isNeural ? "neural" : "text"}
        />
        <TextInput
          radius={30}
          size="md"
          icon={<IconSearch color="#102252" />}
          placeholder="Enter a query"
          rightSection={
            <Button
              className={classes.inputRightSection}
              radius={30}
              size="md"
              variant="filled"
              color="Primary.2"
              onClick={handleSubmit}
            >
              Search
            </Button>
          }
          rightSectionWidth={"6rem"}
          className={classes.inputArea}
          value={query}
          required
          onChange={(event) => setQuery(event.currentTarget.value)}
          onKeyDown={getHotkeyHandler([["Enter", handleSubmit]])}
        />
      </Container>

      <DemoSearch handleDemoSearch={onClickFindSimilar} />
      <Container className={classes.viewResult} size="100%"> {/* Use full width */}
        {loading ? (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Loader size="xl" color="Primary.2" variant="bars" />
          </Box>
        ) : error ? (
          <Box
            sx={{
              width: "100%",
              display: "flex",
              justifyContent: "center",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Image maw={240} src="./error.gif" alt="No results found." />

            <Text size="lg" color="dimmed">
              Error ```typescript
              Error: {error}
            </Text>
          </Box>
        ) : (
          <InteractiveTable
            rowData={rowData}
            columnDefs={columnDefs}
            maxChars={maxChars}
            setMaxChars={setMaxChars}
            numResults={numResults} // Pass numResults to the table component
            setNumResults={setNumResults} // Pass setNumResults to the table component
          />
        )}
      </Container>
    </Container>
  );
}
