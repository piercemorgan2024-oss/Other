const apiStatus = document.querySelector("#api-status");

async function loadStatus() {
  try {
    const response = await fetch("http://127.0.0.1:8000/");

    if (!response.ok) {
      throw new Error("Unable to reach backend");
    }

    const data = await response.json();
    apiStatus.textContent = data.message;
  } catch (error) {
    apiStatus.textContent = "Backend offline. Start the API to continue.";
  }
}

loadStatus();
