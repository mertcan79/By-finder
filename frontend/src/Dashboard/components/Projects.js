// Chakra imports
import {
  Flex,
  Icon,
  Table,
  Tbody,
  Text,
  Th,
  Thead,
  Tr,
  useColorModeValue,
} from "@chakra-ui/react";
// Custom components
import Card from "./Card/Card.js";
import CardHeader from "./Card/CardHeader.js";
import DashboardTableRow from "./Tables/DashboardTableRow";
import React from "react";


const Projects = ({ title, captions, data }) => {
  const textColor = useColorModeValue("gray.700", "white");

  return (
    <Card p='16px' overflowX={{ sm: "scroll", xl: "hidden" }}>
      <CardHeader p='12px 0px 28px 0px'>
        <Flex direction='column'>
          <Text fontSize='lg' color={textColor} fontWeight='bold' pb='.5rem'>
            {title}
          </Text>
        </Flex>
      </CardHeader>
      <Table variant='simple' color={textColor}>
        <Thead>
          <Tr my='.8rem' ps='0px'>
            {captions.map((caption, idx) => {
              return (
                <Th color='gray.400' key={idx} ps={idx === 0 ? "0px" : null}>
                  {caption}
                </Th>
              );
            })}
          </Tr>
        </Thead>
        <Tbody>
          {data.map((row) => {
            return (
              <DashboardTableRow
                name={row.name}
                rooms= {row.rooms}
                price={row.price}
                sqfts= {row.sqfts}
                quality= {row.quality}
                score= {row.score}
              />
            );
          })}
        </Tbody>
      </Table>
    </Card>
  );
};

export default Projects;
