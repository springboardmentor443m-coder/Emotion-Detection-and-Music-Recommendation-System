const API_URL = "http://127.0.0.1:5000/predict";

const fileInput = document.getElementById("fileInput");
const webcam = document.getElementById("webcam");
const preview = document.getElementById("preview");
const loader = document.getElementById("loader");
const emotionOutput = document.getElementById("emotion");
const songsDiv = document.getElementById("songs");
const statusOutput = document.getElementById("status");
const textMoodInput = document.getElementById("textMoodInput");
const textStatusOutput = document.getElementById("textStatus");
const historyList = document.getElementById("historyList");
const resultHeadline = document.getElementById("resultHeadline");
const resultSubtext = document.getElementById("resultSubtext");
const resultEmotionValue = document.getElementById("resultEmotionValue");
const resultSourceValue = document.getElementById("resultSourceValue");
const resultCountValue = document.getElementById("resultCountValue");
const tabButtons = Array.from(document.querySelectorAll(".tab-button"));
const tabPanels = Array.from(document.querySelectorAll(".tab-panel"));

let stream = null;
let selectedBlob = null;

function toggleTheme() {
    document.body.classList.toggle("dark");
}

function setActiveTab(tabName) {
    tabButtons.forEach((button) => {
        const isActive = button.dataset.tab === tabName;
        button.classList.toggle("is-active", isActive);
        button.setAttribute("aria-selected", String(isActive));
    });

    tabPanels.forEach((panel) => {
        panel.classList.toggle("is-active", panel.dataset.panel === tabName);
    });
}

function openFile() {
    fileInput.click();
}

fileInput.addEventListener("change", async (event) => {
    const [file] = event.target.files;

    if (!file) {
        return;
    }

    selectedBlob = file;
    preview.src = URL.createObjectURL(file);
    preview.hidden = false;
    statusOutput.textContent = `Ready to analyze: ${file.name}`;
});

async function startCamera() {
    if (stream) {
        return;
    }

    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        webcam.srcObject = stream;
        statusOutput.textContent = "Camera is on. Capture a frame when you're ready.";
    } catch (error) {
        statusOutput.textContent = "Camera access was blocked. Upload an image instead.";
        console.error(error);
    }
}

function stopCamera() {
    if (!stream) {
        return;
    }

    stream.getTracks().forEach((track) => track.stop());
    webcam.srcObject = null;
    stream = null;
}

function captureImage() {
    if (!stream || !webcam.videoWidth || !webcam.videoHeight) {
        statusOutput.textContent = "Start the camera first, then capture an image.";
        return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    canvas.getContext("2d").drawImage(webcam, 0, 0);

    canvas.toBlob((blob) => {
        if (!blob) {
            statusOutput.textContent = "Could not capture an image. Try again.";
            return;
        }

        selectedBlob = blob;
        preview.src = canvas.toDataURL("image/jpeg");
        preview.hidden = false;
        statusOutput.textContent = "Captured image ready for analysis.";
        stopCamera();
    }, "image/jpeg");
}

async function analyzeMood() {
    if (!selectedBlob) {
        statusOutput.textContent = "Upload or capture an image before analyzing.";
        return;
    }

    loader.classList.remove("hidden");
    emotionOutput.textContent = "";
    songsDiv.innerHTML = "";
    statusOutput.textContent = "Analyzing mood and fetching songs...";

    const formData = new FormData();
    formData.append("image", selectedBlob, "moodmate.jpg");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "The backend returned an error.");
        }

        emotionOutput.textContent = `Emotion: ${data.emotion}`;
        statusOutput.textContent = "Analysis complete.";
        changeBackground(data.emotion);
        updateResultSummary({
            emotion: data.emotion,
            source: "Image analysis",
            songs: data.songs || []
        });
        renderSongs(data.songs || []);
        await loadHistory();
        setActiveTab("results");
        stopCamera();
    } catch (error) {
        statusOutput.textContent = "Could not reach the backend. Check that Flask is running.";
        songsDiv.innerHTML = "";
        console.error(error);
        alert(error.message);
    } finally {
        loader.classList.add("hidden");
    }
}

async function analyzeTextMood() {
    const text = textMoodInput.value.trim();

    if (!text) {
        textStatusOutput.textContent = "Enter a message before analyzing text mood.";
        return;
    }

    loader.classList.remove("hidden");
    emotionOutput.textContent = "";
    songsDiv.innerHTML = "";
    textStatusOutput.textContent = "Reading your text and matching its mood...";

    try {
        const response = await fetch("http://127.0.0.1:5000/predict-text", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "The backend returned an error.");
        }

        emotionOutput.textContent = `Emotion: ${data.emotion}`;
        textStatusOutput.textContent = `Text mood analyzed using ${data.source.replace("_", " ")}.`;
        changeBackground(data.emotion);
        updateResultSummary({
            emotion: data.emotion,
            source: "Text analysis",
            songs: data.songs || []
        });
        renderSongs(data.songs || []);
        await loadHistory();
        setActiveTab("results");
    } catch (error) {
        textStatusOutput.textContent = "Could not analyze text mood. Check that Flask is running.";
        console.error(error);
        alert(error.message);
    } finally {
        loader.classList.add("hidden");
    }
}

function renderSongs(songs) {
    if (!songs.length) {
        songsDiv.innerHTML = "<p class=\"empty-state\">No songs found for this mood.</p>";
        return;
    }

    songsDiv.innerHTML = songs.map((song, index) => `
        <article class="song-card">
            <div class="song-card-top">
                <span class="song-index">${String(index + 1).padStart(2, "0")}</span>
                <span class="song-badge">${song.track_id ? "Spotify Track" : "Curated Match"}</span>
            </div>
            <div class="song-cover-shell">
                ${song.image ? `<img class="song-cover" src="${song.image}" alt="${song.title} cover">` : `<div class="song-cover song-cover-placeholder">${song.title.charAt(0)}</div>`}
            </div>
            <div class="song-copy">
                <h3>${song.title}</h3>
                <p class="song-artist">${song.artist}</p>
            </div>
            <div class="song-meta">
                <span class="song-meta-chip">${song.track_id ? "Embedded playback" : "Search ready"}</span>
                <span class="song-meta-chip">Mood matched</span>
            </div>
            <div class="song-actions">
            ${song.track_id ? `
            <div class="player-shell">
                <div class="player-header">
                    <span class="player-dot"></span>
                    <span>Now available to play</span>
                </div>
                <iframe
                    src="https://open.spotify.com/embed/track/${song.track_id}"
                    width="250"
                    height="152"
                    loading="lazy"
                    allow="encrypted-media">
                </iframe>
            </div>` : song.spotify_search_url
                ? `<a class="song-link" href="${song.spotify_search_url}" target="_blank" rel="noopener noreferrer">Open in Spotify</a>`
                : `<p class="song-source">Local recommendation</p>`}
            </div>
        </article>
    `).join("");
}

function updateResultSummary({ emotion, source, songs }) {
    if (!resultHeadline || !resultSubtext || !resultEmotionValue || !resultSourceValue || !resultCountValue) {
        return;
    }

    const count = songs.length;
    resultHeadline.textContent = `${emotion} mood detected. Recommendations are ready.`;
    resultSubtext.textContent = `This session used ${source.toLowerCase()} and returned ${count} curated ${count === 1 ? "track" : "tracks"} for the current mood.`;
    resultEmotionValue.textContent = emotion;
    resultSourceValue.textContent = source;
    resultCountValue.textContent = String(count);
}

function changeBackground(emotion) {
    const colors = {
        Happy: "linear-gradient(135deg, #f6d365, #fda085)",
        Sad: "linear-gradient(135deg, #4facfe, #00f2fe)",
        Angry: "linear-gradient(135deg, #f85032, #e73827)",
        Surprise: "linear-gradient(135deg, #f9d423, #ff4e50)",
        Fear: "linear-gradient(135deg, #5f72bd, #9b23ea)",
        Neutral: "linear-gradient(135deg, #667eea, #764ba2)"
    };

    document.body.style.background = colors[emotion] || colors.Neutral;
}

function renderHistory(items) {
    if (!historyList) {
        return;
    }

    if (!items.length) {
        historyList.innerHTML = "<p class=\"empty-state\">Your recent mood detections will appear here.</p>";
        return;
    }

    historyList.innerHTML = items.map((item) => `
        <article class="history-card">
            <div class="history-meta">
                <span class="history-badge">${item.input_type === "text" ? "Text" : "Image"}</span>
                <span class="history-time">${formatHistoryTime(item.created_at)}</span>
            </div>
            <h3>${item.emotion}</h3>
            <p>${item.input_text ? item.input_text : "Captured from facial expression analysis."}</p>
        </article>
    `).join("");
}

function formatHistoryTime(value) {
    if (!value) {
        return "Just now";
    }

    const normalized = value.includes("T") ? value : value.replace(" ", "T");
    const date = new Date(normalized);

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString([], {
        dateStyle: "medium",
        timeStyle: "short"
    });
}

async function loadHistory() {
    if (!historyList) {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/history");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not load history.");
        }

        renderHistory(data.history || []);
    } catch (error) {
        historyList.innerHTML = "<p class=\"empty-state\">History is unavailable right now.</p>";
        console.error(error);
    }
}

async function clearHistory() {
    if (!historyList) {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/history", {
            method: "DELETE"
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            throw new Error(data.error || "Could not clear history.");
        }

        renderHistory([]);
    } catch (error) {
        console.error(error);
        alert(error.message);
    }
}

window.toggleTheme = toggleTheme;
window.openFile = openFile;
window.startCamera = startCamera;
window.captureImage = captureImage;
window.analyzeMood = analyzeMood;
window.analyzeTextMood = analyzeTextMood;
window.loadHistory = loadHistory;
window.clearHistory = clearHistory;
window.addEventListener("beforeunload", stopCamera);
window.addEventListener("DOMContentLoaded", loadHistory);
tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
        setActiveTab(button.dataset.tab);
    });
});
