document.querySelectorAll('.project video[autoplay]').forEach((video) => {
    video.play().catch(() => {});
});

document.querySelectorAll('.project-presentation').forEach((presentation) => {
    presentation.addEventListener('toggle', () => {
        if (!presentation.open) presentation.querySelector('video').pause();
    });
});
