import json

data = json.load(open("data.json", encoding="utf-8"))

html = """
<html>
<head>
<meta charset='UTF-8'>
<title>Ranking Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: Arial; padding: 20px; }
table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
th, td { border: 1px solid #ccc; padding: 6px; text-align: left; }
th { background: #eee; }
</style>
</head>
<body>

<h1>Ranking Dashboard</h1>

<h2>Ranking aktualny</h2>
<table id="ranking"></table>

<h2>Historia (wykres punktów)</h2>
<canvas id="historyChart" width="800" height="300"></canvas>

<script>
const data = """ + json.dumps(data) + """;

// --- Ranking aktualny ---
const ranking = data["Ranking"]; // nazwa zakładki z arkusza
let htmlTable = "<tr>";
ranking[0].forEach(h => htmlTable += "<th>" + h + "</th>");
htmlTable += "</tr>";

for (let i = 1; i < ranking.length; i++) {
  htmlTable += "<tr>";
  ranking[i].forEach(c => htmlTable += "<td>" + c + "</td>");
  htmlTable += "</tr>";
}

document.getElementById("ranking").innerHTML = htmlTable;

// --- Historia wykres ---
const history = data["Ranking Historia"]; // nazwa zakładki z arkusza
const labels = history.slice(1).map(r => r[0] + " " + r[1]); // Data + Godzina
const points = history.slice(1).map(r => Number(r[4]));      // kolumna Punkty

new Chart(document.getElementById("historyChart"), {
  type: 'line',
  data: {
    labels: labels,
    datasets: [{
      label: "Punkty",
      data: points,
      borderColor: "blue",
      fill: false
    }]
  }
});
</script>

</body>
</html>
"""

open("index.html", "w", encoding="utf-8").write(html)
