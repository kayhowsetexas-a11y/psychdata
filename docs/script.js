const modeToggle = document.querySelector('.toggle-button');
const body = document.body;
const modeLabel = document.querySelector('.mode-label');

function setMode(mode) {
  if (mode === 'dark') {
    body.classList.add('dark-mode');
    body.classList.remove('light-mode');
    modeLabel.textContent = 'Dark mode';
    localStorage.setItem('site-mode', 'dark');
  } else {
    body.classList.add('light-mode');
    body.classList.remove('dark-mode');
    modeLabel.textContent = 'Light mode';
    localStorage.setItem('site-mode', 'light');
  }
}

modeToggle.addEventListener('click', () => {
  const nextMode = body.classList.contains('dark-mode') ? 'light' : 'dark';
  setMode(nextMode);
});

const storedMode = localStorage.getItem('site-mode') || 'light';
setMode(storedMode);

function renderCharts() {
  const lineCtx = document.getElementById('trendChart');
  const barCtx = document.getElementById('raceChart');
  const donutCtx = document.getElementById('careChart');

  new Chart(lineCtx, {
    type: 'line',
    data: {
      labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
      datasets: [
        {
          label: 'Depression prevalence',
          data: [24, 28, 22, 18, 15],
          borderColor: '#0f69ff',
          backgroundColor: 'rgba(15, 105, 255, 0.12)',
          tension: 0.35,
          fill: true,
          pointRadius: 4,
        },
        {
          label: 'Anxiety prevalence',
          data: [31, 29, 25, 20, 17],
          borderColor: '#14b8a6',
          backgroundColor: 'rgba(20, 184, 166, 0.14)',
          tension: 0.35,
          fill: true,
          pointRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          mode: 'index',
          intersect: false,
        },
        legend: {
          position: 'top',
        },
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false,
      },
      scales: {
        x: {
          grid: { display: false },
        },
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: ['White', 'American Indian/Alaska Native', 'Black/African American', 'Hispanic/Latino', 'Asian'],
      datasets: [
        {
          label: 'Access rate',
          data: [100, 82, 74, 68, 60],
          backgroundColor: '#5b95e8',
          borderRadius: 8,
          borderSkipped: false,
        },
      ],
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: {
        tooltip: { enabled: true },
        legend: { display: false },
      },
      scales: {
        x: {
          beginAtZero: true,
          max: 100,
          ticks: { stepSize: 25 },
          grid: { color: 'rgba(255, 255, 255, 0.12)' },
        },
        y: { grid: { display: false } },
      },
    },
  });

  new Chart(donutCtx, {
    type: 'doughnut',
    data: {
      labels: ['Workforce shortage', 'Adequate coverage', 'Expanding access'],
      datasets: [
        {
          data: [56, 28, 16],
          backgroundColor: ['#0f69ff', '#38bdf8', '#34d399'],
          hoverOffset: 10,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => `${context.label}: ${context.parsed}%`,
          },
        },
        legend: { position: 'bottom' },
      },
    },
  });
}

window.addEventListener('DOMContentLoaded', renderCharts);
