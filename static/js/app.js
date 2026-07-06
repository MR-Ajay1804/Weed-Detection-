const fileInput = document.getElementById("fileInput");
const uploadZone = document.getElementById("uploadZone");
const uploadForm = document.getElementById("uploadForm");
const predictButton = document.getElementById("predictButton");
const resetButton = document.getElementById("resetButton");
const previewCard = document.getElementById("previewCard");
const imagePreview = document.getElementById("imagePreview");
const previewName = document.getElementById("previewName");
const fileText = document.getElementById("fileText");
const particleCanvas = document.getElementById("particleCanvas");

const validImageTypes = ["image/jpeg", "image/png"];

function showSelectedFile(file) {
  if (!file) {
    return;
  }

  if (!validImageTypes.includes(file.type)) {
    fileText.textContent = "Please select a JPG or PNG image.";
    return;
  }

  const previewUrl = URL.createObjectURL(file);
  imagePreview.src = previewUrl;
  previewName.textContent = file.name;
  fileText.textContent = file.name;
  previewCard.classList.remove("is-hidden");
}

function resetForm() {
  uploadForm.reset();
  previewCard.classList.add("is-hidden");
  imagePreview.removeAttribute("src");
  previewName.textContent = "";
  fileText.textContent = "or press Enter to browse JPG or PNG files";
  predictButton.disabled = false;
  uploadForm.classList.remove("is-loading");
  predictButton.querySelector(".btn-text").textContent = "Predict Image";
}

fileInput?.addEventListener("change", (event) => {
  showSelectedFile(event.target.files[0]);
});

uploadZone?.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    fileInput.click();
  }
});

["dragenter", "dragover"].forEach((eventName) => {
  uploadZone?.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadZone.classList.add("is-dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  uploadZone?.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadZone.classList.remove("is-dragover");
  });
});

uploadZone?.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (!file) {
    return;
  }

  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  fileInput.files = dataTransfer.files;
  showSelectedFile(file);
});

uploadForm?.addEventListener("submit", () => {
  predictButton.disabled = true;
  uploadForm.classList.add("is-loading");
  predictButton.querySelector(".btn-text").textContent = "Analyzing...";
});

resetButton?.addEventListener("click", resetForm);

function resizeParticleCanvas() {
  particleCanvas.width = window.innerWidth;
  particleCanvas.height = window.innerHeight;
}

function startParticles() {
  if (!particleCanvas) {
    return;
  }

  const context = particleCanvas.getContext("2d");
  const particles = Array.from({ length: 70 }, () => ({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    size: Math.random() * 2 + 1,
    speed: Math.random() * 0.45 + 0.15,
    alpha: Math.random() * 0.45 + 0.15,
  }));

  function draw() {
    context.clearRect(0, 0, particleCanvas.width, particleCanvas.height);

    particles.forEach((particle) => {
      particle.y -= particle.speed;
      if (particle.y < -8) {
        particle.y = window.innerHeight + 8;
        particle.x = Math.random() * window.innerWidth;
      }

      context.fillStyle = `rgba(103, 232, 165, ${particle.alpha})`;
      context.fillRect(particle.x, particle.y, particle.size, particle.size);
    });

    requestAnimationFrame(draw);
  }

  resizeParticleCanvas();
  draw();
}

window.addEventListener("resize", resizeParticleCanvas);
startParticles();

window.addEventListener("load", () => {
  const results = document.getElementById("results");
  if (results) {
    results.scrollIntoView({ behavior: "smooth", block: "center" });
  }
});
