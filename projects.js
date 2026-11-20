document.querySelectorAll('.project video[autoplay]').forEach((video) => {
    video.play().catch(() => {});
});

document.querySelectorAll('.project-presentation').forEach((presentation) => {
    presentation.addEventListener('toggle', () => {
        if (!presentation.open) presentation.querySelector('video').pause();
    });
});

const playgrounds = [...document.querySelectorAll('.project-playground')];
window.addEventListener('message', (event) => {
    if (event.origin !== location.origin || event.data?.type !== 'rejectsynth:resize') return;
    const frame = playgrounds.find((candidate) => candidate.contentWindow === event.source);
    const height = event.data.height;
    if (frame && Number.isFinite(height)) frame.height = Math.ceil(Math.max(340, Math.min(1000, height)));
});

const stopOffscreen = new IntersectionObserver((entries) => {
    for (const entry of entries) {
        if (!entry.isIntersecting) entry.target.contentWindow?.postMessage({ type: 'rejectsynth:stop' }, location.origin);
    }
});
playgrounds.forEach((frame) => stopOffscreen.observe(frame));
