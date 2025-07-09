const BASE_URL = 'https://4b3d-54-242-46-203.ngrok-free.app';

const ctx = document.createElement('canvas');
ctx.id = 'chart';
document.getElementById('output').prepend(ctx);

function renderChart(summary) {
  const labels = Object.keys(summary);
  const data = Object.values(summary);

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Viewing Category %',
        data: data,
        backgroundColor: [
          '#66bb6a', '#42a5f5', '#ffa726', '#ab47bc', '#26c6da', '#ef5350', '#8d6e63', '#d4e157'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: {
          display: true,
          text: 'Top Watched Categories (%)'
        }
      }
    }
  });
}

document.getElementById('upload-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('file');
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  const uploadBtn = e.target.querySelector('button');
  uploadBtn.disabled = true;
  uploadBtn.innerText = 'Uploading...';

  try {
    const res = await fetch(`${BASE_URL}/upload`, {
      method: 'POST',
      body: formData
    });

    const result = await res.json();
    alert(result.message || 'Upload completed.');
  } catch (err) {
    alert('Upload failed. Check server logs.');
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.innerText = 'Upload';
  }
});

document.getElementById('analyze-btn').addEventListener('click', async () => {
  const analyzeBtn = document.getElementById('analyze-btn');
  const resultBox = document.getElementById('result');
  const loader = document.getElementById('loader');

  analyzeBtn.disabled = true;
  analyzeBtn.innerText = 'Analyzing...';
  resultBox.textContent = '';
  loader.style.display = 'block';

  try {
    const res = await fetch(`${BASE_URL}/analyze`, {
      method: 'POST'
    });
    const data = await res.json();

    if (data.summary) {
      renderChart(data.summary);
    }

    resultBox.textContent = data.analysis || 'No analysis returned.';
  } catch (err) {
    resultBox.textContent = 'Error fetching analysis.';
  } finally {
    loader.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = 'Analyze Mental Health';
  }
});
