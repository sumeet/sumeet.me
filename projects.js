document.querySelectorAll('.project video').forEach((video) => {
    video.play().catch(() => {});
});
