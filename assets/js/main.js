document.addEventListener("DOMContentLoaded", function() {
  const iframe = document.getElementById('allure-frame');
  const fullscreenBtn = document.getElementById('fullscreen-btn');

  if (iframe) {
    iframe.onload = function() {
      let lastHeight = 0;
      let retries = 15; // Try for ~7.5 seconds

      const resizeInterval = setInterval(() => {
        try {
          const currentHeight = iframe.contentWindow.document.body.scrollHeight;

          if (currentHeight > 0 && currentHeight === lastHeight) {
            iframe.style.height = currentHeight + 'px';
            clearInterval(resizeInterval);
          } else {
            lastHeight = currentHeight;
          }

          if (--retries <= 0) {
            console.warn("Could not auto-determine iframe height. It may be incorrect.");
            clearInterval(resizeInterval);
          }
        } catch (e) {
          console.error("Error resizing iframe:", e);
          clearInterval(resizeInterval);
        }
      }, 500); // Check every 500ms
    };
  }

  if (fullscreenBtn) {
    fullscreenBtn.addEventListener('click', function() {
      document.body.classList.toggle('focus-mode');
    });
  }
});