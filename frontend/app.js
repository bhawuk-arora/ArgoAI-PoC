// Global variable to hold the chart instance
let myChart = null;

async function query() {
  let q = document.getElementById("query").value;
  const header = document.getElementById("output-header");
  const rawOutput = document.getElementById("rawOutput");
  
  header.innerHTML = "Querying...";
  rawOutput.innerText = "";
  
  try {
    // 1. Fetch data from the new intelligent endpoint
    let res = await fetch(`http://127.0.0.1:8000/query?q=${q}`);
    let data = await res.json();
    
    // Display raw data 
    rawOutput.innerText = JSON.stringify(data, null, 2);

    // Clear previous chart
    const canvas = document.getElementById('chartCanvas');
    if (myChart) {
      myChart.destroy();
    }
    
    // --- Visualization Logic based on AI Routing Mode ---
    
    if (data.mode === "SEMANTIC_SEARCH") {
      header.innerHTML = `✅ **Mode: Semantic Search (RAG)** - Found 5 relevant profiles for context.`;
      
      // Plot the first profile (Pressure vs. Temperature)
      const labels = data.results.map(r => r.pres);
      const temp_data = data.results.map(r => r.temp);
      
      myChart = new Chart(canvas.getContext('2d'), {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: `Temperature (°C) for best match (Pressure: dbar)`,
            data: temp_data,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          scales: {
            x: { title: { display: true, text: 'Pressure (dbar)' } },
            y: { title: { display: true, text: 'Temperature (°C)' }, reverse: true } // Reverse Y-axis for depth
          }
        }
      });
      
    } else if (data.mode === "NL_TO_SQL") {
      header.innerHTML = `✅ **Mode: NL-to-SQL Translation** - Executed SQL: <pre>${data.sql}</pre>`;

      // Plot the quantitative result (assuming it's MAX temp/salinity for simplicity)
      if (data.results && data.results.length > 0) {
        const result = data.results[0];
        // Find the result value and parameter name
        const valueKey = Object.keys(result).filter(k => k.endsWith('_value'))[0];
        const parameter = result.parameter.toUpperCase();
        const value = result[valueKey];
        
        myChart = new Chart(canvas.getContext('2d'), {
          type: 'bar',
          data: {
            labels: [parameter],
            datasets: [{
              label: valueKey.replace('_', ' ').toUpperCase(),
              data: [value],
              backgroundColor: 'rgba(255, 99, 132, 0.5)'
            }]
          },
          options: {
             scales: { y: { beginAtZero: true } }
          }
        });
      }
      
    } else {
      header.innerText = "Error: Could not determine query mode.";
    }
    
  } catch (error) {
    header.innerText = "Error fetching data from API. Is FastAPI running (Run `uvicorn main:app --reload` in your backend directory)? Check console for details.";
    rawOutput.innerText = `Fetch Error: ${error}`;
    console.error("API Fetch Error:", error);
  }
}

// Keeping legacy functions as placeholders but they are unused by the new HTML
async function semantic() { /* ... */ }
async function sql() { /* ... */ }