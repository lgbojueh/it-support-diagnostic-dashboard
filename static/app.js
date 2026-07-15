const refreshButton = document.getElementById("refresh-button");
const overallStatus = document.getElementById("overall-status");
const statusIndicator = document.getElementById("status-indicator");
const lastUpdated = document.getElementById("last-updated");
const resultsContainer = document.getElementById("diagnostic-results");

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function setProgress(id, value) {
  const progress = document.getElementById(id);
  const safeValue = Math.min(Math.max(Number(value), 0), 100);

  progress.style.width = `${safeValue}%`;

  if (safeValue >= 90) {
    progress.style.background = "#ff6577";
  } else if (safeValue >= 75) {
    progress.style.background = "#ffc857";
  } else {
    progress.style.background = "#47d7ff";
  }
}

function displaySystemInformation(system) {
  setText("cpu-usage", `${system.cpu_usage_percent}%`);
  setText("memory-usage", `${system.memory.used_percent}%`);
  setText("disk-usage", `${system.disk.used_percent}%`);

  setProgress("cpu-progress", system.cpu_usage_percent);
  setProgress("memory-progress", system.memory.used_percent);
  setProgress("disk-progress", system.disk.used_percent);

  setText(
    "operating-system",
    `${system.operating_system} ${system.os_version}`
  );

  setText("architecture", system.architecture);
  setText("cpu-cores", system.cpu_cores);
  setText("total-memory", `${system.memory.total_gb} GB`);
  setText("available-memory", `${system.memory.available_gb} GB`);
  setText("free-disk", `${system.disk.free_gb} GB`);
}

function displayNetworkInformation(network) {
  const connected = network.internet_connected;

  setText(
    "network-status",
    connected ? "Connected" : "Disconnected"
  );

  setText("hostname", network.hostname);
  setText("local-ip", network.local_ip);

  setText(
    "connectivity",
    connected ? "Internet available" : "Connection failed"
  );
}

function displayWarnings(warnings) {
  resultsContainer.innerHTML = "";

  warnings.forEach((warning) => {
    const item = document.createElement("div");

    item.className = `diagnostic-item ${warning.level}`;
    item.textContent = warning.message;

    resultsContainer.appendChild(item);
  });

  const hasCritical = warnings.some(
    (warning) => warning.level === "critical"
  );

  const hasWarning = warnings.some(
    (warning) => warning.level === "warning"
  );

  statusIndicator.className = "status-indicator";

  if (hasCritical) {
    overallStatus.textContent = "Critical issue detected";
    statusIndicator.classList.add("critical");
  } else if (hasWarning) {
    overallStatus.textContent = "Review recommended";
    statusIndicator.classList.add("warning");
  } else {
    overallStatus.textContent = "System is healthy";
    statusIndicator.classList.add("healthy");
  }
}

async function runDiagnostics() {
  refreshButton.disabled = true;
  refreshButton.textContent = "Running...";

  overallStatus.textContent = "Collecting system information";
  resultsContainer.innerHTML =
    '<p class="empty-message">Running diagnostic checks...</p>';

  try {
    const response = await fetch("/api/diagnostics");

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const report = await response.json();

    displaySystemInformation(report.system);
    displayNetworkInformation(report.network);
    displayWarnings(report.warnings);

    lastUpdated.textContent =
      `Updated ${new Date(report.generated_at).toLocaleString()}`;
  } catch (error) {
    console.error(error);

    overallStatus.textContent = "Diagnostic request failed";
    statusIndicator.className = "status-indicator critical";

    resultsContainer.innerHTML =
      '<p class="error-message">Unable to retrieve diagnostic information.</p>';
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = "Run Diagnostics";
  }
}

refreshButton.addEventListener("click", runDiagnostics);

runDiagnostics();