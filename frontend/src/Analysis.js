import React, { useState, useEffect } from "react";
import { ChakraProvider, Box, Select } from "@chakra-ui/react";
import Plot from "react-plotly.js";

function AnalysisTab() {
  const [feature, setFeature] = useState("SearchPrice");
  const [data, setData] = useState([]);

  const handleDistribution = async () => {
    try {
      let response = await fetch(
        `http://localhost:8000/get_data?feature=${feature}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let fetchedData = await response.json();
      setData(fetchedData);
    } catch (error) {
      console.error("There was an error fetching the data", error);
    }
  };

  // Call handleDistribution when the feature changes
  useEffect(() => {
    handleDistribution();
  }, [feature]);

  return (
    <Box>
      <Select
        placeholder="Select feature"
        onChange={(e) => setFeature(e.target.value)}
      >
        <option value="SearchPrice">Search Price</option>
        <option value="SearchSqft">Search Sqft</option>
        <option value="SearchQuality">Search Quality</option>
        <option value="SearchRooms">Search Rooms</option>

        <option value="Price">Flat Price</option>
        <option value="Sqft">Flat Sqft</option>
        <option value="Quality">Flat Quality</option>
        <option value="Rooms">Flat Rooms</option>
      </Select>
      <Plot
        key={feature}
        data={[
          {
            x: data.x,
            y: data.y,
            type: "line",
            mode: "lines",
          },
        ]}
        layout={{ title: "KDE Plot" }}
      />
    </Box>
  );
}

export default AnalysisTab;
