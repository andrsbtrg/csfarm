const urls = [barChartAllUrl, barChartDataUrl, rankingChartDataUrl];

Promise.all(urls.map(url => d3.json(url))).then(run);

function run(dataset) {
	if (barChartDataUrl === barChartAllUrl) {
		d3BarChart(dataset[0]);
		rankingChart(dataset[2]);
	} else {
		d3BarChart(dataset[0], dataset[1]);
		rankingChart(dataset[2]);
	}
};
