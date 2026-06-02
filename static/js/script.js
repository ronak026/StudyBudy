const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".room__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

// Flash message popup: close on click, and auto-dismiss after 4s.
const popupMessage = document.getElementById("popup-message");
if (popupMessage) {
  const hidePopup = () => popupMessage.classList.remove("show");
  const closeBtn = popupMessage.querySelector("[data-close-modal]");
  if (closeBtn) closeBtn.addEventListener("click", hidePopup);
  setTimeout(hidePopup, 4000);
}