/* ================================================================
   SHE REPORT — Main JavaScript
   ================================================================ */

document.addEventListener('DOMContentLoaded', function() {

  // ── Mobile Nav Toggle ────────────────────────────────────────
  const toggle = document.querySelector('.nav-toggle');
  const nav    = document.querySelector('.navbar-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open'));
    });
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove('open');
      }
    });
  }

  // ── Active Nav Link ──────────────────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.navbar-nav a').forEach(link => {
    if (link.getAttribute('href') === currentPath ||
        (currentPath !== '/' && link.getAttribute('href') !== '/' && currentPath.startsWith(link.getAttribute('href')))) {
      link.classList.add('active');
    }
  });

  // ── Back to Top ──────────────────────────────────────────────
  const btn = document.getElementById('backToTop');
  if (btn) {
    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    });
    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Auto-dismiss Django messages ─────────────────────────────
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // ── Animate numbers on scroll ────────────────────────────────
  const counters = document.querySelectorAll('[data-count]');
  if (counters.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    counters.forEach(c => observer.observe(c));
  }

  function animateCounter(el) {
    const target  = parseInt(el.getAttribute('data-count'));
    const duration = 1800;
    const step     = 16;
    const increment = target / (duration / step);
    let current = 0;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) { current = target; clearInterval(timer); }
      el.textContent = Math.floor(current).toLocaleString('en-IN');
    }, step);
  }

  // ── Crime Trend Chart ────────────────────────────────────────
  const chartEl = document.getElementById('crimeTrendChart');
  if (chartEl && typeof Chart !== 'undefined') {
    const years  = JSON.parse(chartEl.getAttribute('data-years')  || '[]');
    const totals = JSON.parse(chartEl.getAttribute('data-totals') || '[]');
    new Chart(chartEl, {
      type: 'bar',
      data: {
        labels: years,
        datasets: [{
          label: 'Total Crimes Against Women',
          data: totals,
          backgroundColor: 'rgba(139,26,74,0.75)',
          borderColor: 'rgba(139,26,74,1)',
          borderWidth: 2,
          borderRadius: 6,
          hoverBackgroundColor: 'rgba(139,26,74,0.9)',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => `  ${ctx.parsed.y.toLocaleString('en-IN')} cases`
            }
          }
        },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#4A4A6A' } },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0,0,0,0.06)' },
            ticks: {
              color: '#4A4A6A',
              callback: val => val.toLocaleString('en-IN')
            }
          }
        }
      }
    });
  }

  // ── District Pie Chart ────────────────────────────────────────
  const pieEl = document.getElementById('crimeTypeChart');
  if (pieEl && typeof Chart !== 'undefined') {
    const labels = JSON.parse(pieEl.getAttribute('data-labels') || '[]');
    const values = JSON.parse(pieEl.getAttribute('data-values') || '[]');
    new Chart(pieEl, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: [
            '#8B1A4A','#B5446E','#2A9D8F','#F4A261','#1A2B4A','#E07B30','#6B1238'
          ],
          borderWidth: 2,
          borderColor: '#fff',
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { font: { size: 12 }, padding: 12, color: '#4A4A6A' }
          }
        }
      }
    });
  }

  // ── Smooth scroll for anchor links ───────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
