import {
  Avatar,
  AvatarGroup,
  Flex,
  Icon,
  Progress,
  Td,
  Text,
  Tr,
  useColorModeValue,
} from "@chakra-ui/react";
import React from "react";

function DashboardTableRow(props) {
  const { name, rooms, price, sqfts, quality } = props;
  const textColor = useColorModeValue("gray.900", "white");
  return (
    <Tr>
      <Td minWidth={{ sm: "250px" }} pl="0px">
        <Flex align="center" py=".8rem" minWidth="100%" flexWrap="nowrap">
          <Text
            fontSize="md"
            color={textColor}
            fontWeight="bold"
            minWidth="100%"
          >
            {name}
          </Text>
        </Flex>
      </Td>

      <Td>
        <Text fontSize="md" color={textColor} fontWeight="bold" pb=".5rem">
          {rooms}
        </Text>
      </Td>
      <Td>
        <Flex direction="column">
          <Text
            fontSize="md"
            color="teal.300"
            fontWeight="bold"
            pb=".2rem"
          >{`${price}`}</Text>
          <Progress
            colorScheme={price === 100 ? "teal" : "cyan"}
            size="xs"
            value={price}
            borderRadius="15px"
          />
        </Flex>
      </Td>
      <Td>
      <Text fontSize="md" color={textColor} fontWeight="bold" pb=".5rem">
          {sqfts}
        </Text>
      </Td>
      <Td>
      <Text fontSize="md" color={textColor} fontWeight="bold" pb=".5rem">
          {quality}
        </Text>
        </Td>
    </Tr>
  );
}

export default DashboardTableRow;
