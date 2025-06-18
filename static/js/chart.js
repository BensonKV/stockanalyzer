document.addEventListener('DOMContentLoaded', function () {
    const ticker = new URLSearchParams(window.location.search).get('ticker');
    const periodSelect = document.getElementById('periodSelect');
    const loadingEl = document.getElementById('loading');
    const errorEl = document.getElementById('error');
    const chartCanvas = document.getElementById('priceChart');
    let stockChart = null;

    function loadStockData(period = '1y') {
        // Show loading
        loadingEl.style.display = 'block';
        errorEl.style.display = 'none';
        chartCanvas.style.display = 'none';

        fetch(`/api/data/${ticker}?period=${period}`)
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.error || 'Failed to fetch data');
                }

                // Hide loading
                loadingEl.style.display = 'none';
                chartCanvas.style.display = 'block';

                const ctx = chartCanvas.getContext('2d');

                if (stockChart) {
                    stockChart.destroy();
                }

                stockChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.dates,
                        datasets: [
                            {
                                label: 'Stock Price',
                                data: data.prices,
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                fill: true,
                                tension: 0.1
                            },
                            {
                                label: 'SMA 20',
                                data: data.sma20,
                                borderColor: 'rgba(153, 102, 255, 1)',
                                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                fill: false,
                                tension: 0.1
                            },
                            {
                                label: 'SMA 50',
                                data: data.sma50,
                                borderColor: 'rgba(255, 159, 64, 1)',
                                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                fill: false,
                                tension: 0.1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'top',
                            },
                            tooltip: {
                                mode: 'index',
                                intersect: false,
                            }
                        },
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Price (USD)'
                                }
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching stock data:', error);
                loadingEl.style.display = 'none';
                errorEl.style.display = 'block';
                errorEl.textContent = error.message || 'An error occurred.';
            });
    }

    // Event listener for period selector
    periodSelect.addEventListener('change', function () {
        const selectedPeriod = this.value;
        loadStockData(selectedPeriod);
    });

    // Initial load
    loadStockData('1y');
});

