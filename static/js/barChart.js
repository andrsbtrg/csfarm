function d3BarChart(data) {
   // Declare the chart dimensions and margins.
   const width = 928;
   const height = 500;
   // Declare the x (horizontal position) scale.
   const x_scale = d3.scaleBand().range([0, width]).padding(0.1);
   const y_scale = d3.scaleLinear().range([height, 0]);

   const svg = d3.select("#barChart")
      .attr("width", width)
      .attr("height", height)

   x_scale.domain(data.map(d => d["x"]))
   y_scale.domain([0, d3.max(data, (d) => d["y"])]);

   svg.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("class", "bar")
      .attr("x", (d) => x_scale(d["x"]))
      .attr("y", (d) => y_scale(d["y"]))
      .attr("width", 20)
      .attr("height", (d) => height - y_scale(d["y"]));
}
