const API_URL = "http://127.0.0.1:8000";

const textInput = document.getElementById("textInput");
const charCount = document.getElementById("charCount");

textInput.addEventListener("input", () => {
    charCount.innerText = textInput.value.length;
});

function showLoader() {
    document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
    document.getElementById("loader").classList.add("hidden");
}

async function summarizeText() {

    const text = textInput.value;

    if (!text.trim()) {
        alert("Please enter some text");
        return;
    }

    showLoader();

    const formData = new FormData();
    formData.append("text", text);

    try {

        const response = await fetch(`${API_URL}/summarize-text/`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("output").innerText = data.summary;

    } catch (error) {

        document.getElementById("output").innerText =
            "Error generating summary";

    }

    hideLoader();
}

async function summarizePDF() {

    const file = document.getElementById("pdfFile").files[0];

    if (!file) {
        alert("Please upload a PDF");
        return;
    }

    showLoader();

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch(`${API_URL}/summarize-pdf/`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("output").innerText = data.summary;

    } catch (error) {

        document.getElementById("output").innerText =
            "Error processing PDF";

    }

    hideLoader();
}