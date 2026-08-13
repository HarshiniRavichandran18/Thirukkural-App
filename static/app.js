/* ==========================================================================
   ROYAL THIRUKKURAL EXPLORER — CLIENT APP LOGIC
   Vanilla JavaScript for Page Transitions, Dynamic Search & Manuscript Rendering
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const pages = {
    1: document.getElementById('page-1'),
    2: document.getElementById('page-2'),
    3: document.getElementById('page-3')
  };

  const btnExplore = document.getElementById('btn-explore');
  const btnBackToHome = document.getElementById('btn-back-to-home');
  const btnBackToSearch = document.getElementById('btn-back-to-search');
  const btnSearchAnother = document.getElementById('btn-search-another');

  const segmentBtns = document.querySelectorAll('.segment-btn');
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const inputLabel = document.getElementById('input-label');
  const searchSpinner = document.getElementById('search-spinner');
  const errorCard = document.getElementById('error-card');

  const displayPaal = document.getElementById('display-paal');
  const displayAthikaram = document.getElementById('display-athikaram');
  const displayNumber = document.getElementById('display-number');
  const displayLine1 = document.getElementById('display-line1');
  const displayLine2 = document.getElementById('display-line2');
  const displayMeaningEn = document.getElementById('display-meaning-en');

  let currentSearchType = 'number';

  const searchConfig = {
    number: {
      placeholder: 'Enter Kural Number (1–1330)',
      label: 'Kural Number (1–1330)'
    },
    athikaram: {
      placeholder: 'Enter Athikaram Name (e.g. கடவுள் வாழ்த்து)',
      label: 'Athikaram Name'
    },
    title: {
      placeholder: 'Enter Kural Title or Keyword',
      label: 'Kural Title / Keyword'
    }
  };

  function navigateToPage(pageNumber) {
    Object.keys(pages).forEach(key => {
      if (parseInt(key) === pageNumber) {
        pages[key].classList.add('active');
      } else {
        pages[key].classList.remove('active');
      }
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (btnExplore) {
    btnExplore.addEventListener('click', () => {
      hideErrorCard();
      navigateToPage(2);
      searchInput.focus();
    });
  }

  if (btnBackToHome) {
    btnBackToHome.addEventListener('click', () => {
      hideErrorCard();
      navigateToPage(1);
    });
  }

  if (btnBackToSearch) {
    btnBackToSearch.addEventListener('click', () => {
      navigateToPage(2);
      searchInput.focus();
    });
  }

  if (btnSearchAnother) {
    btnSearchAnother.addEventListener('click', () => {
      searchInput.value = '';
      hideErrorCard();
      navigateToPage(2);
      searchInput.focus();
    });
  }

  segmentBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      segmentBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      currentSearchType = btn.getAttribute('data-type');
      const config = searchConfig[currentSearchType];

      if (config) {
        searchInput.placeholder = config.placeholder;
        inputLabel.textContent = config.label;
        searchInput.value = '';
        hideErrorCard();
        searchInput.focus();
      }
    });
  });

  if (searchForm) {
    searchForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const query = searchInput.value.trim();
      if (!query) return;

      hideErrorCard();
      showSpinner();

      try {
        let endpoint = '';
        if (currentSearchType === 'number') {
          endpoint = `/search/number/${encodeURIComponent(query)}`;
        } else if (currentSearchType === 'athikaram') {
          endpoint = `/search/athikaram/${encodeURIComponent(query)}`;
        } else if (currentSearchType === 'title') {
          endpoint = `/search/title/${encodeURIComponent(query)}`;
        }

        const response = await fetch(endpoint);
        const json = await response.json();

        hideSpinner();

        if (response.ok && json.success && json.data) {
          renderManuscript(json.data);
          navigateToPage(3);
        } else {
          showErrorCard(json.message || 'No matching Kural was found. Please verify the Kural Number, Athikaram, or Title.');
        }
      } catch (err) {
        console.error('Fetch error:', err);
        hideSpinner();
        showErrorCard('No matching Kural was found. Please verify the Kural Number, Athikaram, or Title.');
      }
    });
  }

  function renderManuscript(kuralData) {
    displayPaal.textContent = kuralData.paal || 'அறத்துப்பால்';
    displayAthikaram.textContent = kuralData.athikaram || '';
    displayNumber.textContent = `குறள் ${kuralData.number}`;

    const lines = kuralData.kural || [];
    displayLine1.textContent = lines[0] || '';
    displayLine2.textContent = lines[1] || '';

    const englishMeaning = kuralData.meaning_en || '';
    displayMeaningEn.textContent = englishMeaning ? `“${englishMeaning}”` : '';
  }

  function showSpinner() {
    if (searchSpinner) searchSpinner.classList.add('visible');
  }

  function hideSpinner() {
    if (searchSpinner) searchSpinner.classList.remove('visible');
  }

  function showErrorCard(msg) {
    if (errorCard) errorCard.classList.add('visible');
  }

  function hideErrorCard() {
    if (errorCard) errorCard.classList.remove('visible');
  }
});
