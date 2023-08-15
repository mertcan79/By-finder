import {
  Box,
  ChakraProvider,
  VStack,
  Text,
  Flex,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
} from "@chakra-ui/react";
// import { globalStyles } from "./Dashboard/theme/styles"
import chakraTheme from "./Dashboard/theme/theme";
import Projects from "./Dashboard/components/Projects";
import { MapContainßer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import React, { useEffect, useState, useRef } from "react";
import ChartStatistics from "./Dashboard/components/ChartStatistics";
import AnalysisTab from "./Analysis";
import FindTab from "./Find";

const SearchPage = () => {
  return (
    <Box bg="lightblue">
      <ChakraProvider theme={chakraTheme} resetCss={true}>
        <VStack spacing={2} padding={1}>
          <Tabs variant="enclosed">
            <TabList mb="1em">
              <Tab>Find</Tab>
              <Tab>Analysis</Tab>
            </TabList>

            <Text fontSize="2xl">Flat Search</Text>

            <TabPanels>
              <TabPanel>
                <FindTab />
              </TabPanel>

              <TabPanel>
                <AnalysisTab />
              </TabPanel>
            </TabPanels>
          </Tabs>
        </VStack>
      </ChakraProvider>
    </Box>
  );
};

export default SearchPage;
