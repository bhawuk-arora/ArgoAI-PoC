// Global variable to hold the chart instance
let myChart = null;

// Global Chart.js Defaults for Dark Theme
Chart.defaults.color = '#8b949e';
Chart.defaults.font.family = "'Inter', sans-serif";

async function query() {
  let q = document.getElementById("query").value;
  const header = document.getElementById("output-header");
  const rawOutput = document.getElementById("rawOutput");
  const canvas = document.getElementById('chartCanvas');
  const btnText = document.querySelector('.btn-text');
  const btnLoader = document.getElementById('btn-loader');
  
  // UI Loading State
  btnText.style.display = 'none';
  btnLoader.style.display = 'block';
  header.innerHTML = "<span style='color: var(--accent-cyan);'>Querying...</span>";
  rawOutput.innerText = "";
  if (myChart) {
    myChart.destroy(); // Clear previous chart
  }
  
  try {
    // 1. Fetch data from the new intelligent endpoint
    let res = await fetch(`/query?q=${encodeURIComponent(q)}`);
    let data = await res.json();
    
    // Display raw data 
    rawOutput.innerText = JSON.stringify(data, null, 2);

    // Common Chart Options for Dark Theme
    const darkThemeOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#f0f6fc' } }
        },
        scales: {
            x: { 
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#8b949e' }
            },
            y: { 
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#8b949e' }
            }
        }
    };

    // 2. Visualization Logic based on AI Routing Mode
    if (data.mode === "SEMANTIC_SEARCH") {
      header.innerHTML = `✅ <strong style="color:var(--accent-cyan)">Mode: Semantic Search (RAG)</strong> - Found relevant profiles for context.`;
      
      // Plot the first profile (Pressure vs. Temperature)
      const labels = data.results.map(r => r.pres);
      const temp_data = data.results.map(r => r.temp);
      
      let options = JSON.parse(JSON.stringify(darkThemeOptions));
      options.scales.x.title = { display: true, text: 'Pressure (dbar)', color: '#8b949e' };
      options.scales.y.title = { display: true, text: 'Temperature (°C)', color: '#8b949e' };
      options.scales.y.reverse = true; // Reverse Y-axis for depth visualization

      myChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: `Temperature (°C) for best match`,
            data: temp_data,
            borderColor: '#00f2fe',
            backgroundColor: 'rgba(0, 242, 254, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointBackgroundColor: '#4facfe',
            pointBorderColor: '#fff'
          }]
        },
        options: options
      });
      
    } else if (data.mode === "NL_TO_SQL") {
      header.innerHTML = `✅ <strong style="color:var(--accent-cyan)">Mode: NL-to-SQL Translation</strong> - Executed SQL: <code style="color:var(--accent-blue)">${data.sql}</code>`;

      // Plot the quantitative result
      if (data.results && data.results.length > 0) {
        const result = data.results[0];
        const valueKey = Object.keys(result).find(k => k === 'value');
        const parameter = result.parameter.toUpperCase();
        const value = result[valueKey];
        const aggregation = result.aggregation;
        
        let options = JSON.parse(JSON.stringify(darkThemeOptions));
        options.scales.y.title = { display: true, text: parameter, color: '#8b949e' };
        options.scales.y.beginAtZero = false;

        myChart = new Chart(canvas.getContext('2d'), {
          type: 'bar',
          data: {
            labels: [`${aggregation} ${parameter}`],
            datasets: [{
              label: `${aggregation} Result`,
              data: [value],
              backgroundColor: 'rgba(79, 172, 254, 0.7)',
              borderColor: '#00f2fe',
              borderWidth: 1,
              borderRadius: 4
            }]
          },
          options: options
        });
      }
      
    } else {
      header.innerText = "Error: Could not determine query mode.";
    }
    
  } catch (error) {
    header.innerHTML = "❌ <strong style='color:#ff6b6b'>Error fetching data from API.</strong> Check console for details.";
    rawOutput.innerText = `Fetch Error: ${error}`;
    console.error("API Fetch Error:", error);
  } finally {
      // Reset UI Loading State
      btnText.style.display = 'block';
      btnLoader.style.display = 'none';
  }
}

// Removed original semantic() and sql() functions as they are no longer used by index.html