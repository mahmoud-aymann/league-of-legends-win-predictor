const form = document.getElementById("predict-form");
const resultPlaceholder = document.getElementById("result-placeholder");
const resultView = document.getElementById("result-view");
const probabilityText = document.getElementById("probability-text");
const predictionText = document.getElementById("prediction-text");
const errorView = document.getElementById("error-view");
const prefillBtn = document.getElementById("prefill-btn");

const setLoading = (isLoading) => {
  const button = form.querySelector("button[type='submit']");
  button.disabled = isLoading;
  button.textContent = isLoading ? "Predicting..." : "Predict outcome";
};

const formatProbability = (value) => `${(value * 100).toFixed(1)}%`;

const getSamplePayload = () => {
  const ranges = {
    kills: [3, 20],
    deaths: [0, 15],
    assists: [2, 25],
    gold_earned: [5000, 25000],
    cs: [50, 350],
    wards_placed: [2, 15],
    wards_killed: [0, 10],
    damage_dealt: [5000, 60000],
  };

  return window.__FEATURE_ORDER__.reduce((acc, feature) => {
    const [min, max] = ranges[feature] ?? [0, 100];
    acc[feature] = Math.round(min + Math.random() * (max - min));
    return acc;
  }, {});
};

const fillForm = (values) => {
  Object.entries(values).forEach(([key, value]) => {
    const input = form.elements.namedItem(key);
    if (input) {
      input.value = value;
    }
  });
};

prefillBtn?.addEventListener("click", () => {
  fillForm(getSamplePayload());
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setLoading(true);
  errorView.hidden = true;
  resultPlaceholder.hidden = true;
  resultView.hidden = true;

  const formData = new FormData(form);
  const payload = {};
  for (const [key, value] of formData.entries()) {
    payload[key] = Number(value);
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Unexpected error");
    }

    probabilityText.textContent = formatProbability(data.win_probability);
    predictionText.textContent =
      data.prediction === 1
        ? "✅ Blue side is favored — lean into aggression."
        : "⚠️ Win rate below threshold — shift to safer objectives.";

    resultView.hidden = false;
  } catch (error) {
    errorView.textContent = error.message;
    errorView.hidden = false;
    resultPlaceholder.hidden = true;
    resultView.hidden = true;
  } finally {
    setLoading(false);
  }
});

