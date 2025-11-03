document.addEventListener("DOMContentLoaded", function() {
    const iframe = document.getElementById('allure-frame');

    iframe.onload = function() {
        try {
        if (iframe.contentWindow.location.hash) {
            iframe.contentWindow.location.href = iframe.contentWindow.location.href.split('#')[0];
            return;
        }

        const iframeBody = iframe.contentWindow.document.body;
        const pageBody = document.body;
        let isWideMode = false;

        const toggleWideMode = () => {
            const shouldBeWide = !!iframe.contentWindow.document.querySelector('[data-testid="split-layout"]');
            if (shouldBeWide !== isWideMode) {
            isWideMode = shouldBeWide;
            pageBody.classList.toggle('wide-mode', isWideMode);
            }
        };

        const observer = new MutationObserver(() => {
            requestAnimationFrame(toggleWideMode);
        });

        const config = { childList: true, subtree: true };
        observer.observe(iframeBody, config);

        toggleWideMode();

        } catch (e) {
        console.error("Could not access iframe content for resizing. This might be a cross-origin security error.", e);
        iframe.style.height = '85vh';
        }
    };
});
