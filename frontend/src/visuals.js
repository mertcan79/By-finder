import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';

const SankeyDiagram = () => {
  const ref = useRef();

  useEffect(() => {
    const data = {
      nodes: [
        { name: 'Start' },
        { name: 'Price' },
        { name: 'Rooms' },
        { name: 'Quality' },
        { name: 'Distance' },
        { name: 'End' },
      ],
      links: [
        { source: 0, target: 1, value: Math.random() },
        { source: 1, target: 2, value: Math.random() },
        { source: 1, target: 3, value: Math.random() },
        { source: 2, target: 4, value: Math.random() },
        { source: 3, target: 4, value: Math.random() },
        { source: 4, target: 5, value: Math.random() },
      ],
    };

    const width = 600;
    const height = 600;

    const svg = d3
      .select(ref.current)
      .attr('width', width)
      .attr('height', height);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const sankeyGenerator = sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .extent([
        [1, 1],
        [width - 1, height - 5],
      ]);

    const sankeyData = sankeyGenerator(data);

    const link = svg
      .append('g')
      .selectAll('path')
      .data(sankeyData.links)
      .enter()
      .append('path')
      .attr('d', sankeyLinkHorizontal())
      .attr('stroke', (d) => color(d.source.name)) // Set color based on the source node
      .attr('stroke-width', (d) => Math.max(1, d.width))
      .attr('fill', 'none');

    const node = svg
      .append('g')
      .selectAll('rect')
      .data(sankeyData.nodes)
      .enter()
      .append('rect')
      .attr('x', (d) => d.x0)
      .attr('y', (d) => d.y0)
      .attr('height', (d) => d.y1 - d.y0)
      .attr('width', (d) => d.x1 - d.x0)
      .attr('fill', (d) => color(d.name)) // Set color based on the node name
      .append('title')
      .text((d) => `${d.name}\n${d.value}`);

    // Append text for nodes
    svg
      .append('g')
      .style('font', '10px sans-serif')
      .selectAll('text')
      .data(sankeyData.nodes)
      .join('text')
      .attr('x', (d) => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))
      .attr('y', (d) => (d.y1 + d.y0) / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', (d) => (d.x0 < width / 2 ? 'start' : 'end'))
      .text((d) => d.name);
  }, []);

  return <svg ref={ref} style={{ width: '100%', height: '600px', background: 'dark.800' }} />;

};

export default SankeyDiagram;
