import {
  Box,
  Button,
  Input,
  FormControl,
  FormLabel,
  Flex,
} from "@chakra-ui/react";
// import { globalStyles } from "./Dashboard/theme/styles"
import chakraTheme from "./Dashboard/theme/theme";
import Projects from "./Dashboard/components/Projects";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import React, { useEffect, useState, useRef } from "react";
import ChartStatistics from "./Dashboard/components/ChartStatistics";

function FindTab() {
  const [coordinates, setCoordinates] = useState([]);
  const [numFlats, setNumFlats] = useState(0);
  const [price, setPrice] = useState("");
  const [rooms, setRooms] = useState("");
  const [sqfts, setSqfts] = useState("");
  const [quality, setQuality] = useState("");
  const [tableData, setTableData] = useState([]);
  const [tableDataBayesian, setTableDataBayesian] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      // Fetch Traditional Results
      let response = await fetch(
        `http://localhost:8000/traditional_search?price=${price}&rooms=${rooms}&quality=${quality}&sqfts=${sqfts}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let data = await response.json();
      if (Array.isArray(data)) {
        setCoordinates(data);
        setNumFlats(data.length);
        const tableData = data.map((item, index) => ({
          id: index + 1,
          name: item.name,
          rooms: item.rooms,
          price: item.price,
          sqfts: item.sqfts,
          quality: item.quality,
        }));
        setTableData(tableData.slice(0, 10)); // Limit the table data to the top 10 items
      }

      let bayesian_response = await fetch(
        `http://localhost:8000/bayesian_search?price=${price}&rooms=${rooms}&quality=${quality}&sqfts=${sqfts}`
      );
      if (!bayesian_response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let bayesian_data = await bayesian_response.json();
      const tableDataBayesian = bayesian_data.map((item, index) => ({
        id: index + 1,
        name: item.name,
        rooms: item.rooms,
        price: item.price,
        sqfts: item.sqfts,
        quality: item.quality,
        score: item.score,
      }));
      setTableDataBayesian(tableDataBayesian.slice(0, 10));
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <Box>
      <Box width="33%" mx="auto" height="400px">
        <form onSubmit={handleSubmit}>
          <FormControl id="price">
            <FormLabel>Price Approximation</FormLabel>
            <Input
              bgColor="white"
              type="number"
              placeholder="Enter approximated price"
              onChange={(e) => setPrice(e.target.value)}
            />
          </FormControl>
          <FormControl id="rooms">
            <FormLabel>Number of Rooms Approximation</FormLabel>
            <Input
              bgColor="white"
              type="number"
              placeholder="Enter approximated number of rooms"
              onChange={(e) => setRooms(e.target.value)}
            />
          </FormControl>
          <FormControl id="sqfts">
            <FormLabel>Sqfts Approximation</FormLabel>
            <Input
              bgColor="white"
              type="number"
              placeholder="Enter approximated sqfts"
              onChange={(e) => setSqfts(e.target.value)}
            />
          </FormControl>
          <FormControl id="quality">
            <FormLabel>Quality</FormLabel>
            <Input
              bgColor="white"
              type="number"
              placeholder="Enter approximated quality (1 to 5)"
              onChange={(e) => setQuality(e.target.value)}
            />
          </FormControl>
          <Button colorScheme="teal" type="submit">
            Search
          </Button>
        </form>
      </Box>
      <Flex direction="row" justify="space-between" width="100%">
        <Box flex="1" margin="1">
          <Projects
            title={"Flats"}
            amount={price}
            captions={["Name", "Rooms", "Price", "Sqfts", "Quality"]}
            data={tableData}
          />
        </Box>
        <Box flex="1" margin="2">
          <Projects
            title={"Flats - Bayesian Way"}
            amount={price}
            captions={["Name", "Rooms", "Price", "Sqfts", "Quality"]}
            data={tableDataBayesian}
          />
        </Box>
      </Flex>
      <Box>
        <ChartStatistics
          title="Flats Found"
          amount={numFlats}
          percentage={(numFlats / 9000) * 100}
        />
      </Box>
      <Box>
        <MapContainer
          key={coordinates.toString()}
          center={[49.2827, -123.1207]}
          zoom={11}
          style={{ width: "100%", height: "400px" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {coordinates.map((coordinate, index) => (
            <Marker
              key={index}
              position={[
                Number(coordinate.latitude),
                Number(coordinate.longitude),
              ]}
            >
              <Popup>Flat Location</Popup>
            </Marker>
          ))}
        </MapContainer>
      </Box>
    </Box>
  );
}
export default FindTab;
