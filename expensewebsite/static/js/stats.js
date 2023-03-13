const renderChart = (data, labels) => {
    const ctx = document.getElementById("myChart");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "# of Votes",
                    data: data.concat(0),
                    borderWidth: 1,
                    backgroundColor: "rgb(255, 99, 132)",
                    borderColor: "rgb(255, 99, 132)",
                },
            ],
        },
        options: {
            title: {
                display: true,
                text: "Expenses per category"
            },
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
}

const getChartData = () => {
    fetch('/expense-category-summary')
    .then(res => res.json())
    .then((result) => {
        console.log("result", result);
        const category_data = result.expense_category_data;
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
        console.log("lab", labels, "dataa", data);
        renderChart(data, labels)
    })
}

document.onload = getChartData();

