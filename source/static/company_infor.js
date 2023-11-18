function checkAPIKey() {
    var apiKey = document.getElementById('api-key').value;
    if (!apiKey) {
        alert("Please enter your OpenAI API Key");
    } else {
        document.getElementById('insights-selection').style.display = 'block';
    }
}

/*
    * This function is called when the user clicks on the "Generate Insights" button.
    * It will fetch the company overview, income statement, balance sheet, cash flow, and news sentiment data.
    * It will then display the data on the page.
    * The data is fetched from the server, which in turn fetches the data from the OpenAI API.
    * The server will also perform some data processing and analysis.
    * The data is then sent back to the client, which will display the data on the page.
    * The data is displayed using the displayCompanyOverview, displayIncomeStatement, displayBalanceSheet, displayCashFlow, and displayNewsSentiment functions.
    * These functions are defined in the company_infor.js file.
*/
function generateInsights() {
    var tickerSymbol = document.getElementById('ticket-symbol').value;
    fetchCompanyOverview(tickerSymbol);
    fetchIncomeStatement(tickerSymbol);
    fetchBalanceSheet(tickerSymbol);
    fetchCashFlow(tickerSymbol);
    fetchNewsSentiment(tickerSymbol);
}

function fetchCompanyOverview(tickerSymbol) {
    const loadingMessage = document.getElementById('company-overview-loading-message');
    if (loadingMessage) {
        loadingMessage.classList.remove('hide'); // Show the loading message
    }
    fetch('/company_overview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: tickerSymbol })
    })
        .then(response => {
            if (!response.ok) {
                return Promise.reject('Failed to fetch');
            }
            return response.json();
        })
        .then(data => {
            displayCompanyOverview(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            if (loadingMessage) {
                loadingMessage.classList.add('hide'); // Hide the loading message
            }
        });
}

function displayCompanyOverview(data) {
    // Update DOM to display company overview data
    document.getElementById('company-overview').innerHTML = `
        <h2>Company Name: ${data.Name}</h2>
        <p>Description: ${data.Description}</p>
        <p>Symbol: ${data.Symbol}</p>
        <p>Asset Type: ${data.AssetType}</p>
        <p>CIK: ${data.CIK}</p>
        <p>Exchange: ${data.Exchange}</p>
        <p>Currency: ${data.Currency}</p>
        <p>Country: ${data.Country}</p>
        <p>Sector: ${data.Sector}</p>
        <p>Industry: ${data.Industry}</p>
        <p>Address: ${data.Address}</p>
        <p>Fiscal Year End: ${data.FiscalYearEnd}</p>
        <p>Latest Quarter: ${data.LatestQuarter}</p>
        <p>Market Capitalization: ${data.MarketCapitalization}</p>
    `;
}

function fetchIncomeStatement(tickerSymbol) {
    const loadingMessage = document.getElementById('income-statement-loading-message');
    if (loadingMessage) {
        loadingMessage.classList.remove('hide'); // Show the loading message
    }
    fetch('/income_statement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: tickerSymbol })
    })
        .then(response => {
            if (!response.ok) {
                return Promise.reject('Failed to fetch');
            }
            return response.json();
        })
        .then(data => {
            displayIncomeStatement(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            if (loadingMessage) {
                loadingMessage.classList.add('hide'); // Hide the loading message
            }
        });
}

function displayIncomeStatement(data) {

    function displayIncomeStatementMetrics(metrics) {
        const metricsElement = document.createElement('div');
        metricsElement.innerHTML = '<h2>Metrics</h2>';
        for (const metric in metrics) {
            const metricItem = document.createElement('p');
            metricItem.textContent = `${metric.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase())}: ${metrics[metric]}`;
            metricsElement.appendChild(metricItem);
        }
        return metricsElement;
    }

    function displayIncomeStatementChartData(chartData) {
        // Create a container for the chart
        const chartContainer = document.createElement('div');
        chartContainer.className = 'income-statement-chart-container';

        // Create a header element
        const header = document.createElement('h2');
        header.textContent = 'Chart Data';
        chartContainer.appendChild(header);

        // Create a separate div for the Plotly chart
        const plotlyDiv = document.createElement('div');
        plotlyDiv.className = 'income-statement-plotly-chart'; // Assign a class name
        chartContainer.appendChild(plotlyDiv);

        // Prepare the labels and data for Plotly.js
        const labels = chartData['dates'];
        const data = [];
        for (const key in chartData) {
            if (key !== 'dates') {
                data.push({
                    name: key.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase()),
                    x: labels,
                    y: chartData[key],
                    mode: 'lines',
                    line: { shape: 'linear' },
                    type: 'scatter'
                });
            }
        }

        // Create the layout object for the Plotly chart
        const layout = {
            title: 'Chart Data',
            xaxis: {
                title: 'Dates',
                tickvals: labels,
                ticktext: labels
            },
            yaxis: {
                title: 'Billion USD',
                zeroline: true
            },
            autosize: true
        };

        // Render the Plotly chart into the dedicated div
        Plotly.newPlot(plotlyDiv, data, layout);

        return chartContainer;
    }


    function displayIncomeStatementInsights(insights) {
        const insightsElement = document.createElement('div');
        insightsElement.innerHTML = '<h2>Insights</h2>';
        for (const insight in insights) {
            const insightItem = document.createElement('p');
            insightItem.textContent = `${insight.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase())}: ${insights[insight]}`;
            insightsElement.appendChild(insightItem);
        }

        return insightsElement;
    }

    const incomeStatementElement = document.getElementById('income-statement');

    if (!incomeStatementElement) {
        console.error("Income statement element not found.");
        return;
    }
    incomeStatementElement.innerHTML = '';
    incomeStatementElement.appendChild(displayIncomeStatementMetrics(data.metrics));
    incomeStatementElement.appendChild(document.createElement('hr'));
    incomeStatementElement.appendChild(displayIncomeStatementChartData(data.chart_data));
    incomeStatementElement.appendChild(document.createElement('hr'));
    incomeStatementElement.appendChild(displayIncomeStatementInsights(data.insights));
}

function fetchBalanceSheet(tickerSymbol) {
    const loadingMessage = document.getElementById('balance-sheet-loading-message');
    if (loadingMessage) {
        loadingMessage.classList.remove('hide'); // Show the loading message
    }

    fetch('/balance_sheet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: tickerSymbol })
    })
        .then(response => {
            if (!response.ok) {
                return Promise.reject('Failed to fetch');
            }
            return response.json();
        })
        .then(data => {
            displayBalanceSheet(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            if (loadingMessage) {
                loadingMessage.classList.add('hide'); // Hide the loading message
            }
        });
}

function displayBalanceSheet(data) {
    function displayBalanceSheetMetrics(metrics) {
        const metricsElement = document.createElement('div');
        metricsElement.innerHTML = '<h2>Metrics</h2>';
        for (const metric in metrics) {
            const metricItem = document.createElement('p');
            metricItem.textContent = `${metric.replace(/(^|_)(.)/g, (_, a, b) => (a ? ' ' : '') + b.toUpperCase())}: ${metrics[metric]}`;
            metricsElement.appendChild(metricItem);
        }

        return metricsElement;
    }

    function displayBalanceSheetChartData(chartData) {
        // Create a container for the entire balance sheet chart section
        const chartContainer = document.createElement('div');
        chartContainer.className = 'balance-sheet-chart-container'; // Assign class name
        chartContainer.innerHTML = '<h2>Balance Sheet Data</h2>';

        for (let key in chartData) {
            if (chartData.hasOwnProperty(key)) {
                // Create a container for each individual chart
                const chartDiv = document.createElement('div');
                chartDiv.className = 'individual-balance-plotly-chart'; // Assign class name
                chartContainer.appendChild(chartDiv);

                const labels = Object.keys(chartData[key]).map(key => key.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase()));;
                const data = [{
                    name: key.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase()),
                    x: labels,
                    y: Object.values(chartData[key]),
                    type: 'bar'
                }];

                // Create the layout object for the Plotly chart
                const layout = {
                    title: key.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase()),
                    xaxis: {
                        title: 'Categories',
                    },
                    yaxis: {
                        title: 'Billions USD',
                        zeroline: true
                    }
                };

                // Render the Plotly chart
                Plotly.newPlot(chartDiv, data, layout);
            }
        }

        return chartContainer;
    }


    function displayBalanceSheetInsights(insights) {
        const insightsElement = document.createElement('div');
        insightsElement.innerHTML = '<h2>Insights</h2>';
        for (const insight in insights) {
            const insightItem = document.createElement('p');
            insightItem.textContent = `${insight.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase())}: ${insights[insight]}`;
            insightsElement.appendChild(insightItem);
        }

        return insightsElement;
    }

    const balanceSheetElement = document.getElementById('balance-sheet');
    if (!balanceSheetElement) {
        console.error("Balance sheet element not found.");
        return;
    }

    balanceSheetElement.innerHTML = '';
    balanceSheetElement.appendChild(displayBalanceSheetMetrics(data.metrics));
    balanceSheetElement.appendChild(document.createElement('hr'));
    balanceSheetElement.appendChild(displayBalanceSheetChartData(data.chart_data));
    balanceSheetElement.appendChild(document.createElement('hr'));
    balanceSheetElement.appendChild(displayBalanceSheetInsights(data.insights));
}

function fetchCashFlow(tickerSymbol) {
    const loadingMessage = document.getElementById('cash-flow-loading-message');
    if (loadingMessage) {
        loadingMessage.classList.remove('hide'); // Show the loading message
    }
    fetch('/cash_flow', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: tickerSymbol })
    })
        .then(response => {
            if (!response.ok) {
                return Promise.reject('Failed to fetch');
            }
            return response.json();
        })
        .then(data => {
            displayCashFlow(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            if (loadingMessage) {
                loadingMessage.classList.add('hide'); // Hide the loading message
            }
        });
}

function displayCashFlow(data) {
    function displayCashFlowMetrics(metrics) {
        const metricsElement = document.createElement('div');
        metricsElement.innerHTML = '<h2>Metrics</h2>';
        for (const metric in metrics) {
            const metricItem = document.createElement('p');
            metricItem.textContent = `${metric.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase())}: ${metrics[metric]}`;
            metricsElement.appendChild(metricItem);
        }

        return metricsElement;
    }

    function displayCashFlowChartData(chartData) {
        const chartContainer = document.createElement('div');

        // Create a header element
        const header = document.createElement('h2');
        header.textContent = 'Cash Flow Chart Data';
        chartContainer.appendChild(header);

        // Create a separate div for the Plotly chart
        const plotlyDiv = document.createElement('div');
        plotlyDiv.className = 'individual-cash-flow-plotly-chart'; // Assign a class name
        chartContainer.appendChild(plotlyDiv);

        // Extract shared dates
        const labels = chartData.dates || [];

        // The traces array will store our dataset for the Plotly chart
        const traces = [];

        for (const key in chartData) {
            // We skip the dates key as it's not an actual section
            if (key !== "dates") {
                const section = chartData[key];

                // Check if the section data is an object and not a primitive value
                if (typeof section === 'object') {
                    const dataValues = Object.values(section);

                    // Create a trace for this section
                    const trace = {
                        x: labels,
                        y: dataValues,
                        name: key.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase()),
                        type: 'bar'
                    };

                    traces.push(trace);
                }
            }
        }

        const layout = {
            title: 'Grouped Cash Flow Data',
            xaxis: {
                title: 'Dates'
            },
            yaxis: {
                title: 'Billions USD',
                zeroline: true
            },
            barmode: 'group',
        };

        // Render the Plotly chart
        Plotly.newPlot(plotlyDiv, traces, layout);

        return chartContainer;
    }


    function displayCashFlowInsights(insights) {
        const insightsElement = document.createElement('div');
        insightsElement.innerHTML = '<h2>Insights</h2>';
        for (const insight in insights) {
            const insightItem = document.createElement('p');
            insightItem.textContent = `${insight.replace(/(^|_)(\w)/g, (_, p1, p2) => p1 ? ' ' + p2.toUpperCase() : p2.toUpperCase())}: ${insights[insight]}`;
            insightsElement.appendChild(insightItem);
        }

        return insightsElement;
    }

    const CashFlowElement = document.getElementById('cash-flow');
    if (!CashFlowElement) {
        console.error("Balance sheet element not found.");
        return;
    }

    CashFlowElement.innerHTML = '';
    CashFlowElement.appendChild(displayCashFlowMetrics(data.metrics));
    CashFlowElement.appendChild(document.createElement('hr'));
    CashFlowElement.appendChild(displayCashFlowChartData(data.chart_data));
    CashFlowElement.appendChild(document.createElement('hr'));
    CashFlowElement.appendChild(displayCashFlowInsights(data.insights));
}

function fetchNewsSentiment(tickerSymbol) {
    const loadingMessage = document.getElementById('news-sentiment-loading-message');
    if (loadingMessage) {
        loadingMessage.classList.remove('hide'); // Show the loading message
    }
    fetch('/new_sentiment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symbol: tickerSymbol })
    })
        .then(response => {
            if (!response.ok) {
                return Promise.reject('Failed to fetch');
            }
            return response.json();
        })
        .then(data => {
            displayNewsSentiment(data);
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            if (loadingMessage) {
                loadingMessage.classList.add('hide'); // Hide the loading message
            }
        });
}

function displayNewsSentiment(data) {
    const newsSentimentElement = document.getElementById('news-sentiment');

    if (data.mean_sentiment_class && data.news) {
        let sentimentHTML = `<h2>Overall Sentiment: ${data.mean_sentiment_class}</h2>`;
        sentimentHTML += '<table class="table table-striped">';
        sentimentHTML += '<thead><tr><th>Title</th><th>Source</th><th>Score (%)</th><th>Sentiment Label</th></tr></thead><tbody>';

        data.news.forEach(article => {
            const sentimentScorePercentage = (article.sentiment_score * 100).toFixed(2);
            let sentimentScoreClass = '';
            switch (article.sentiment_label) {
                case 'Bearish':
                    sentimentScoreClass = 'sentiment-bearish';
                    break;
                case 'Somewhat-Bearish':
                    sentimentScoreClass = 'sentiment-somewhat-bearish';
                    break;
                case 'Neutral':
                    sentimentScoreClass = 'sentiment-neutral';
                    break;
                case 'Somewhat-Bullish':
                    sentimentScoreClass = 'sentiment-somewhat-bullish';
                    break;
                case 'Bullish':
                    sentimentScoreClass = 'sentiment-bullish';
                    break;
                default:
                    sentimentScoreClass = '';
            }
            const source = new URL(article.url).hostname;
            sentimentHTML += `
                <tr>
                    <td><a href="${article.url}" target="_blank">${article.title}</a></td>
                    <td>${source}</td>
                    <td><span class="${sentimentScoreClass}">${sentimentScorePercentage}%</span></td>
                    <td>${article.sentiment_label}</td>
                </tr>`;
        });

        sentimentHTML += '</tbody></table>';
        newsSentimentElement.innerHTML = sentimentHTML;
    } else {
        newsSentimentElement.innerText = 'No sentiment data available';
    }
}