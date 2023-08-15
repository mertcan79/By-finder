const d3Container = useRef(null);

const nodes = [
    { id: "Price" },
    { id: "Sqft" },
    { id: "Rooms" },
    { id: "Distance" },
    { id: "Quality" },
];

const links = [
    { source: "Price", target: "Sqft", influence: 0.7 },
    { source: "Price", target: "Rooms", influence: 0.5 },
    { source: "Price", target: "Distance", influence: 0.6 },
    { source: "Price", target: "Quality", influence: 0.8 },
    { source: "Quality", target: "Sqft", influence: 0.7 },
];

useEffect(() => {
    if (nodes && links && d3Container.current) {
        const svg = d3.select(d3Container.current);

        // Clear the SVG before rendering
        svg.selectAll("*").remove();

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).distance(200))
            .force("charge", d3.forceManyBody().strength(-400))  // Adjust to make graph bigger
            .force("center", d3.forceCenter(svg.node().parentElement.clientWidth / 2, svg.node().parentElement.clientHeight / 2));

        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .style("stroke", "#aaa")
            .style("stroke-dasharray", ("3, 3"))
            .style("stroke-width", d => Math.sqrt(d.influence) * 10);

        const linkText = svg.append("g")
            .selectAll("text")
            .data(links)
            .enter().append("text")
            .attr("font-size", "16px")  // Bigger font size
            .attr("fill", "yellow")  // Change color to yellow
            .text(d => d.influence);

        const node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 30)  // Bigger nodes
            .attr("fill", "blue")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        const nodeText = svg.append("g")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("font-size", "18px")  // Bigger font size
            .attr("fill", "white")
            .text(d => d.id);

        simulation.nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);

        function ticked() {
            link.attr("x1", function (d) { return d.source.x; })
                .attr("y1", function (d) { return d.source.y; })
                .attr("x2", function (d) { return d.target.x; })
                .attr("y2", function (d) { return d.target.y; });

            linkText.attr("x", function (d) { return (d.source.x + d.target.x) / 2; })
                .attr("y", function (d) { return (d.source.y + d.target.y) / 2; });

            node.attr("cx", function (d) { return d.x; })
                .attr("cy", function (d) { return d.y; });

            nodeText.attr("x", function (d) { return d.x; })
                .attr("y", function (d) { return d.y; });
        }

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }
}, [nodes, links]);