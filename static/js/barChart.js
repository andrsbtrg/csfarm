const width = 600;
const height = 480;
const margin = { top: 20, right: 30, bottom: 55, left: 70 }

function d3BarChart(data, otherData) {
   // Declare the chart dimensions and margins.
   // const x_scale = d3.scaleBand().range([0, width]).padding(0.1);
   // const y_scale = d3.scaleLinear().range([height, 0]);
   const x_scale = d3
      .scaleBand()
      .range([margin.left, width - margin.right])
      .padding(0.1);

   const y_scale = d3.scaleLinear()
      .range([height - margin.bottom, margin.top]);

   const svg = d3.select("#barChart")
      .attr("width", width)
      .attr("height", height)

   x_scale.domain(data.map(d => d["date"]))
   y_scale.domain([0, d3.max(data, (d) => d["prod"])]);

   const x_axis = d3.axisBottom(x_scale)
   const y_axis = d3.axisLeft(y_scale)
   svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(x_axis)

   svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(y_axis);

   svg.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("class", "bar")
      .attr("x", (d) => x_scale(d["date"]))
      .attr("y", (d) => y_scale(d["prod"]))
      .attr("width", 50)
      .attr("height", (d) => height - (margin.bottom) - y_scale(d["prod"]));

   if (otherData != null) {
      svg.selectAll("rect")
         .data(otherData)
         .join("rect")
         .attr("class", "bar-2")
         .attr("x", (d) => x_scale(d["date"]))
         .attr("y", (d) => y_scale(d["prod"]))
         .attr("width", 50)
         .attr("height", (d) => height - (margin.bottom) - y_scale(d["prod"]));
   }
}

function rankingChart(data) {
   // Declare the chart dimensions and margins.
   // const x_scale = d3.scaleBand().range([0, width]).padding(0.1);
   // const y_scale = d3.scaleLinear().range([height, 0]);
   const x_scale = d3
      .scaleBand()
      .range([margin.left, width - margin.right])
      .padding(0.1);

   const y_scale = d3.scaleLinear()
      .range([height - margin.bottom, margin.top]);

   const svg = d3.select("#rankingChart")
      .attr("width", width)
      .attr("height", height)

   x_scale.domain(data.map(d => d["name"]))
   y_scale.domain([0, d3.max(data, (d) => d["avg"])]);

   const x_axis = d3.axisBottom(x_scale)
   const y_axis = d3.axisLeft(y_scale)
   svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(x_axis)

   svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(y_axis);

   svg.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("class", "bar-2")
      .attr("x", (d) => x_scale(d["name"]))
      .attr("y", (d) => y_scale(d["avg"]))
      .attr("width", 50)
      .attr("height", (d) => height - (margin.bottom) - y_scale(d["avg"]));
}
