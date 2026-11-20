document.querySelectorAll('.project video[autoplay]').forEach((video) => {
    video.play().catch(() => {});
});

document.querySelectorAll('.project-presentation').forEach((presentation) => {
    const video = presentation.querySelector('video');
    const play = presentation.querySelector('.project-presentation-play');
    play.hidden = false;
    play.addEventListener('click', () => {
        // Leave the media URL unassigned until the visitor explicitly plays it.
        if (!video.hasAttribute('src')) video.src = video.dataset.src;
        video.controls = true;
        video.play().catch(() => {});
    });
    video.addEventListener('play', () => { play.hidden = true; });
    video.addEventListener('pause', () => { play.hidden = false; });
    video.addEventListener('ended', () => { play.hidden = false; });
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
