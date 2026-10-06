const searchInput = document.querySelector("#shipment-search");
const shipmentRows = [...document.querySelectorAll(".shipment-row")];
const visibleCount = document.querySelector("#visible-count");
const emptyState = document.querySelector("#empty-state");
const sampleNumberButton = document.querySelector(".sample-number");

if (sampleNumberButton) {
  sampleNumberButton.addEventListener("click", () => {
    const trackingNumberInput = document.querySelector("#tracking-number");
    trackingNumberInput.value = sampleNumberButton.dataset.trackingNumber;
    trackingNumberInput.form.requestSubmit();
  });
}

function filterShipments() {
  const query = searchInput.value.trim().toLowerCase();
  let visible = 0;

  for (const row of shipmentRows) {
    const matches = row.dataset.search.toLowerCase().includes(query);
    row.hidden = !matches;
    if (matches) visible += 1;
  }

  visibleCount.textContent = visible;
  emptyState.hidden = visible !== 0;
}

if (searchInput) {
  searchInput.addEventListener("input", filterShipments);
}

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && searchInput && !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)) {
    event.preventDefault();
    searchInput.focus();
  }
});