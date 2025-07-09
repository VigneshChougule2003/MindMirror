document.addEventListener("DOMContentLoaded", () => {
  const uploadBtn = document.getElementById("upload-btn");
  const fileInput = document.getElementById("html-file");
  const resultBox = document.getElementById("result-box");
  const fileNameDisplay = document.getElementById("file-name");
  const toggle = document.getElementById("dark-toggle");
  const loader = document.getElementById("loader");
  const chartTypeButtons = document.querySelectorAll("#chart-controls button[data-type]");
  const downloadPDFBtn = document.getElementById("download-pdf");

  let chartType = "bar";
  let chart;

  // ✅ Apply dark mode on page load
  document.body.classList.toggle("dark-mode", toggle.checked);

  // 🌙 Dark mode toggle
  toggle.addEventListener("change", () => {
    document.body.classList.toggle("dark-mode", toggle.checked);
  });

  // 📂 Show selected file name
  fileInput.addEventListener("change", () => {
    fileNameDisplay.textContent = fileInput.files[0]?.name || "No file selected";
  });

  // 📊 Switch chart type
  chartTypeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      chartType = btn.dataset.type;
      if (window.lastSummary) renderChart(window.lastSummary);
    });
  });

  // 🚀 Upload and analyze
  uploadBtn.addEventListener("click", () => {
    const file = fileInput.files[0];
    if (!file) return alert("Please select your watch-history.html file.");

    const formData = new FormData();
    formData.append("file", file);

    loader.style.display = "flex";
    resultBox.textContent = "";

    fetch("/upload", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      loader.style.display = "none";
      if (data.result && data.summary) {
        resultBox.textContent = "🧠 Psychological Analysis:\n\n" + data.result;
        window.lastSummary = data.summary;
        renderChart(data.summary);
      } else {
        resultBox.textContent = "❌ " + (data.error || "Unexpected server response.");
      }
    })
    .catch(err => {
      loader.style.display = "none";
      resultBox.textContent = "❌ Upload or analysis failed.";
      console.error(err);
    });
  });

  // 📊 Render chart from summary
  function renderChart(summaryText) {
    const cleaned = summaryText.replace("User watched: ", "");
    const parts = cleaned.split(", ");
    const labels = [], data = [];

    for (let part of parts) {
      const match = part.match(/^(.*) \(([\d.]+)%\)$/);
      if (match) {
        labels.push(match[1]);
        data.push(parseFloat(match[2]));
      }
    }

    const ctx = document.getElementById("summary-chart").getContext("2d");
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
      type: chartType,
      data: {
        labels,
        datasets: [{
          label: "Content Distribution",
          data,
          backgroundColor: [
            "#9B6B9E", "#B19CD9", "#81C784", "#FFB74D",
            "#9575CD", "#4DB6AC", "#F06292", "#BA68C8"
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        animation: {
          animateRotate: true,
          animateScale: true
        },
        plugins: {
          legend: {
            position: "bottom"
          }
        }
      }
    });
  }

  // 📄 Download PDF with analysis + chart
  downloadPDFBtn.addEventListener("click", () => {
    if (!chart || !window.lastSummary) {
      alert("Please analyze first.");
      return;
    }

    const canvas = document.getElementById("summary-chart");
    const resultText = resultBox.textContent;

    html2canvas(canvas).then(canvasImage => {
      const { jsPDF } = window.jspdf;
      const pdf = new jsPDF();

      const chartImgData = canvasImage.toDataURL("image/png", 1.0);

      pdf.setFont("helvetica", "bold");
      pdf.setFontSize(16);
      pdf.text("MindMirror Psychological Report", 10, 15);

      pdf.setFontSize(12);
      pdf.setFont("helvetica", "normal");
      pdf.text("🧠 RAG-Based Mental Health Analysis:", 10, 30);
      const analysisLines = pdf.splitTextToSize(resultText.trim(), 180);
      pdf.text(analysisLines, 10, 38);

      const chartY = 38 + analysisLines.length * 6 + 10;
      pdf.text("📊 Content Consumption Summary:", 10, chartY);
      pdf.addImage(chartImgData, "PNG", 10, chartY + 5, 180, 100);

      const timestamp = new Date().toLocaleString();
      pdf.setFontSize(10);
      pdf.text(`Exported on: ${timestamp}`, 10, 290);

      pdf.save("MindMirror_Report.pdf");
    });
  });
});
