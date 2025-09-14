async function semantic() {
  let q = document.getElementById("query").value;
  let res = await fetch(`http://127.0.0.1:8000/semantic?q=${q}`);
  let data = await res.json();
  document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}

async function sql() {
  let q = document.getElementById("query").value;
  let res = await fetch(`http://127.0.0.1:8000/sql?q=${q}`);
  let data = await res.json();
  document.getElementById("output").innerText = JSON.stringify(data, null, 2);
}
