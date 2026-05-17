const queryApiUrl = new URLSearchParams(window.location.search).get('apiUrl');
const storedApiUrl = window.localStorage ? window.localStorage.getItem('apiBaseUrl') : '';

window.__API_BASE_URL__ = window.__API_BASE_URL__ || queryApiUrl || storedApiUrl || '';