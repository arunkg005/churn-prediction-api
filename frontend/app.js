const form = document.getElementById('predictionForm');
const statusText = document.getElementById('statusText');
const serviceText = document.getElementById('serviceText');
const apiUrlInput = document.getElementById('apiUrlInput');
const saveApiUrlButton = document.getElementById('saveApiUrl');
const loadDefaultsButton = document.getElementById('loadDefaults');
const loadSampleButton = document.getElementById('loadSample');
const submitButton = document.getElementById('submitButton');
const riskCard = document.getElementById('resultCard');
const suggestionsCard = document.getElementById('suggestionsCard');
const riskPercent = document.getElementById('riskPercent');
const riskLabel = document.getElementById('riskLabel');
const predictionText = document.getElementById('predictionText');
const riskMeter = document.getElementById('riskMeter');
const suggestionsList = document.getElementById('suggestionsList');

function resolveApiBaseUrl() {
  const configured = (window.__API_BASE_URL__ || '').trim();

  if (!configured) {
    return '';
  }

  return configured.replace(/\/$/, '');
}

let apiBaseUrl = resolveApiBaseUrl();
let predictUrl = apiBaseUrl ? `${apiBaseUrl}/predict` : '';

const sampleCustomer = {
  gender: 'Male',
  Partner: 'No',
  Dependents: 'No',
  PhoneService: 'Yes',
  MultipleLines: 'Yes',
  OnlineSecurity: 'No',
  OnlineBackup: 'No',
  DeviceProtection: 'No',
  TechSupport: 'No',
  StreamingTV: 'Yes',
  StreamingMovies: 'Yes',
  Contract: 'Month-to-month',
  PaperlessBilling: 'Yes',
  PaymentMethod: 'Electronic check',
  tenure: 5,
  MonthlyCharges: 95.2,
  TotalCharges: 476,
};

function clearCustomerInputs() {
  form.querySelectorAll('[data-field]').forEach((element) => {
    element.value = '';
  });
}

function applyCustomer(customer) {
  Object.entries(customer).forEach(([field, value]) => {
    const element = form.querySelector(`[data-field="${field}"]`);
    if (element) {
      element.value = String(value);
    }
  });
}

function resetResultState() {
  riskCard.dataset.riskClass = 'low';
  suggestionsCard.dataset.riskClass = 'low';
  riskPercent.textContent = '0.0%';
  riskLabel.textContent = 'Awaiting input';
  predictionText.textContent = 'Run a prediction to see the result.';
  riskMeter.style.width = '0%';
  suggestionsList.hidden = true;
  suggestionsList.innerHTML = '';
}

function gatherPayload() {
  const payload = {};

  new FormData(form).forEach((value, key) => {
    payload[key] = value;
  });

  payload.tenure = Number(payload.tenure);
  payload.MonthlyCharges = Number(payload.MonthlyCharges);
  payload.TotalCharges = Number(payload.TotalCharges);

  return payload;
}

function setStatus(message, state = 'idle') {
  statusText.textContent = message;

  if (state === 'idle') {
    statusText.removeAttribute('data-state');
    return;
  }

  statusText.dataset.state = state;
}

function setService(message, state = 'idle') {
  serviceText.textContent = message;

  if (state === 'error') {
    serviceText.style.color = 'var(--danger)';
    return;
  }

  serviceText.style.color = '';
}

function setBusyState(isBusy) {
  submitButton.disabled = isBusy;
  loadDefaultsButton.disabled = isBusy;
  loadSampleButton.disabled = isBusy;
  saveApiUrlButton.disabled = isBusy;
  apiUrlInput.disabled = isBusy;
  submitButton.textContent = isBusy ? 'Running...' : 'Run prediction';
}

function parseRiskPercent(value) {
  const numeric = Number(value);
  if (Number.isNaN(numeric)) {
    return 0;
  }

  return Math.max(0, Math.min(100, numeric));
}

function getRiskBand(percent) {
  if (percent >= 66) {
    return 'high';
  }

  if (percent >= 34) {
    return 'mid';
  }

  return 'low';
}

function buildSuggestions(customer, riskBand) {
  const suggestions = [];

  if (riskBand === 'high') {
    suggestions.push('Offer a retention call with a targeted discount or loyalty credit.');
  } else if (riskBand === 'mid') {
    suggestions.push('Proactively check in with the customer before the next billing cycle.');
  } else {
    suggestions.push('Keep the customer engaged with periodic value updates and service reminders.');
  }

  if (customer.Contract === 'Month-to-month') {
    suggestions.push('Encourage a one-year or two-year contract with a lower monthly rate.');
  }

  if (customer.PaymentMethod === 'Electronic check') {
    suggestions.push('Promote automatic payments to reduce billing friction.');
  }

  if (customer.PaperlessBilling === 'Yes') {
    suggestions.push('Send a billing walkthrough so the customer can track charges more clearly.');
  }

  if (customer.TechSupport === 'No' || customer.OnlineSecurity === 'No') {
    suggestions.push('Bundle support or security add-ons to increase perceived value.');
  }

  if (Number(customer.tenure) < 12) {
    suggestions.push('Strengthen onboarding with a 30/60/90-day follow-up plan.');
  }

  return suggestions.slice(0, 4);
}

function renderSuggestions(items) {
  suggestionsList.hidden = false;
  suggestionsList.innerHTML = '';

  items.forEach((item) => {
    const listItem = document.createElement('li');
    listItem.textContent = item;
    suggestionsList.appendChild(listItem);
  });
}

function updateSummary(result, customer) {
  const percent = parseRiskPercent(result.risk_percent);
  const riskBand = getRiskBand(percent);
  const conclusion = result.churn_prediction === 1 ? 'The customer is likely to churn.' : 'The customer is likely to stay.';

  riskCard.dataset.riskClass = riskBand;
  suggestionsCard.dataset.riskClass = riskBand;
  riskPercent.textContent = `${percent.toFixed(1)}%`;
  riskLabel.textContent = riskBand.charAt(0).toUpperCase() + riskBand.slice(1);
  predictionText.textContent = conclusion;
  riskMeter.style.width = `${percent}%`;
  renderSuggestions(buildSuggestions(customer, riskBand));

  riskCard.classList.remove('is-updated');
  void riskCard.offsetWidth;
  riskCard.classList.add('is-updated');
}

async function parseJsonSafely(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}

async function runPrediction() {
  if (!apiBaseUrl) {
    setStatus('Set and save the API URL first.', 'error');
    setService('API URL not configured', 'error');
    return;
  }

  if (!form.checkValidity()) {
    form.reportValidity();
    setStatus('Please complete all required fields.', 'error');
    return;
  }

  setBusyState(true);
  setStatus('Running prediction...');

  try {
    const response = await fetch(predictUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(gatherPayload()),
    });

    const data = await parseJsonSafely(response);

    if (!response.ok) {
      throw new Error(data.error || 'Prediction request failed.');
    }

    updateSummary(data, gatherPayload());
    setStatus('Prediction updated.', 'success');
    setService('Connected');
  } catch (error) {
    setStatus(error.message || 'Unable to get prediction.', 'error');
    setService('Connection failed', 'error');
  } finally {
    setBusyState(false);
  }
}

function saveApiUrl(url) {
  const nextUrl = url.trim().replace(/\/$/, '');

  if (!nextUrl) {
    window.localStorage.removeItem('apiBaseUrl');
    window.__API_BASE_URL__ = '';
    apiBaseUrl = '';
    predictUrl = '';
    setService('API URL not configured', 'error');
    setStatus('Enter an API URL and save it.', 'error');
    return;
  }

  window.localStorage.setItem('apiBaseUrl', nextUrl);
  window.__API_BASE_URL__ = nextUrl;
  apiBaseUrl = nextUrl;
  predictUrl = `${nextUrl}/predict`;
  setService(`API connected: ${nextUrl}`);
  setStatus('API URL saved.', 'success');
}

loadDefaultsButton.addEventListener('click', () => {
  clearCustomerInputs();
  resetResultState();
  setStatus('Fields cleared. Select your own values.', 'success');
});

loadSampleButton.addEventListener('click', () => {
  applyCustomer(sampleCustomer);
  setStatus('Sample loaded.');
});

saveApiUrlButton.addEventListener('click', () => {
  saveApiUrl(apiUrlInput.value || '');
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  await runPrediction();
});

apiUrlInput.value = apiBaseUrl;

clearCustomerInputs();
resetResultState();
setService(apiBaseUrl ? `API connected: ${apiBaseUrl}` : 'API URL not configured', apiBaseUrl ? 'idle' : 'error');
setStatus('Ready.');