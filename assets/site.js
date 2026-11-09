const filters = document.querySelector('.publication-filters');
if (filters) {
  filters.hidden = false;
  const papers = [...document.querySelectorAll('#publication-list .publication')];
  filters.addEventListener('click', event => {
    const button = event.target.closest('[data-filter]');
    if (!button) return;
    for (const item of filters.querySelectorAll('button')) {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    }
    for (const paper of papers) {
      paper.hidden = button.dataset.filter !== 'all' && paper.dataset.author !== button.dataset.filter;
    }
    const count = papers.filter(paper => !paper.hidden).length;
    document.querySelector('#publication-count').textContent = document.documentElement.lang.startsWith('zh') ? `已显示 ${count} 篇论文。` : `${count} ${count === 1 ? 'publication' : 'publications'} shown.`;
  });
}
const printButton = document.querySelector('.print-button');
if (printButton) {
  printButton.hidden = false;
  printButton.addEventListener('click', () => window.print());
}

// Keep language links stable before a click, including the current section.
function updateLanguageLinks() {
  for (const link of document.querySelectorAll('.language-switch a')) {
    link.hash = window.location.hash;
  }
}
updateLanguageLinks();
window.addEventListener('hashchange', updateLanguageLinks);
