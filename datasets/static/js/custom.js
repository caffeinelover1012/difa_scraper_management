document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', (e) => {
      const searchValue = e.target.value.toLowerCase();
      const tableRows = document.querySelectorAll('#datasetsTable tr');
      tableRows.forEach(row => {
        const datasetName = row.querySelector('td:nth-child(2)').textContent.toLowerCase();
        row.style.display = datasetName.includes(searchValue) ? '' : 'none';
      });
    });
  });
  