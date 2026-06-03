// Account dropdown menu (Tailwind: toggle `hidden` + `flex`).
const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdownMenu.classList.toggle("hidden");
    dropdownMenu.classList.toggle("flex");
  });
  // Close when clicking outside.
  document.addEventListener("click", (e) => {
    if (!dropdownMenu.contains(e.target) && !dropdownButton.contains(e.target)) {
      dropdownMenu.classList.add("hidden");
      dropdownMenu.classList.remove("flex");
    }
  });
}

// Avatar upload live preview.
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file && photoPreview) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll the chat thread to the latest message.
const conversationThread = document.querySelector("[data-chat-scroll]");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

// Flash message popup: close on click, and auto-dismiss after 4s.
const popupMessage = document.getElementById("popup-message");
if (popupMessage) {
  const hidePopup = () => popupMessage.classList.add("hidden");
  const closeBtn = popupMessage.querySelector("[data-close-modal]");
  if (closeBtn) closeBtn.addEventListener("click", hidePopup);
  setTimeout(hidePopup, 4000);
}
