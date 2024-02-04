const urls = [barChartDataUrl];

Promise.all(urls.map(url => d3.json(url))).then(run);

function run(dataset) {
	d3BarChart(dataset[0]);
};
