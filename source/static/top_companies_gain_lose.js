// Function to fetch data from your API
async function fetchTopCompaniesData() {
    try {
        const response = await fetch('/get_top_companies_gain_lose');
        if (!response.ok) {
            console.error('Failed to fetch data: ', response.status);
            return null;
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data: ', error);
        return null;
    }
}

// Function to create the animation
function createAnimation(data) {
    // Get the existing div element
    const tickerDiv = document.getElementById('top_gain_lose');

    // Create div elements for gainers and losers
    const gainersDiv = document.createElement('div');
    const losersDiv = document.createElement('div');
    spaceBetween = ". . .     |     . . ."

    // Format the data
    if (data.top_gainers) {
        gainersDiv.innerHTML = data.top_gainers.slice(0, 10).map(g => `<span style="color: ${getColor(g.change_percentage, true)}">${g.ticker} ${g.change_percentage}</span>`).join(spaceBetween);
    }
    if (data.top_losers) {
        losersDiv.innerHTML = data.top_losers.slice(0, 10).map(l => `<span style="color: ${getColor(l.change_percentage, false)}">${l.ticker} ${l.change_percentage}</span>`).join(spaceBetween);
    }

    // Append the div elements to the tickerDiv
    tickerDiv.appendChild(gainersDiv);
    tickerDiv.appendChild(losersDiv);

    // Set the styles and animations
    gainersDiv.style.animation = 'marquee-right 50s linear infinite';
    losersDiv.style.animation = 'marquee-left 50s linear infinite';
}

// Function to get color based on change percentage
function getColor(changePercentage, isGainer) {
    const value = Math.abs(parseFloat(changePercentage));
    const intensity = Math.min(value / 10, 1); // Normalize to [0, 1]
    return isGainer ? `rgba(0, 255, 0, ${intensity})` : `rgba(255, 0, 0, ${intensity})`;
}

// Define the keyframes for the marquee animations
const styleSheet = document.styleSheets[0];
styleSheet.insertRule(`
    @keyframes marquee-right {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
`, styleSheet.cssRules.length);
styleSheet.insertRule(`
    @keyframes marquee-left {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
`, styleSheet.cssRules.length);

// Fetch the data and create the animation
fetchTopCompaniesData().then(data => {
    if (data) {
        createAnimation(data);
    }
});
