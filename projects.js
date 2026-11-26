document.querySelectorAll('.project video[autoplay]').forEach((video) => {
    video.play().catch(() => {});
});

document.querySelectorAll('.project-presentation').forEach((presentation) => {
    const play = presentation.querySelector('.project-presentation-play');
    play.hidden = false;
    if (presentation.dataset.embed) {
        const link = presentation.querySelector('.project-presentation-link');
        const start = () => {
            const frame = document.createElement('iframe');
            frame.src = `${presentation.dataset.embed}?autoplay=1&rel=0`;
            frame.title = link.querySelector('img').alt;
            frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
            frame.allowFullscreen = true;
            frame.referrerPolicy = 'strict-origin-when-cross-origin';
            link.replaceWith(frame);
            play.hidden = true;
            frame.focus();
        };
        play.addEventListener('click', start, { once: true });
        link.addEventListener('click', (event) => {
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            play.click();
        });
        return;
    }
    const video = presentation.querySelector('video');
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
    if (frame && Number.isFinite(height)) frame.height = Math.ceil(Math.max(340, height));
});

const stopOffscreen = new IntersectionObserver((entries) => {
    for (const entry of entries) {
        if (!entry.isIntersecting) entry.target.contentWindow?.postMessage({ type: 'rejectsynth:stop' }, location.origin);
    }
});
playgrounds.forEach((frame) => stopOffscreen.observe(frame));

document.querySelectorAll('.source-files').forEach((files) => {
    function showDefinition(target) {
        const pad = target.closest('pre');
        const inset = pad.clientTop + parseFloat(getComputedStyle(pad).paddingTop);
        pad.scrollTop += target.getBoundingClientRect().top - pad.getBoundingClientRect().top - inset;
    }

    const entry = files.querySelector('[data-source-entry]');
    if (entry) showDefinition(entry);

    files.addEventListener('click', (event) => {
        const button = event.target.closest('button[aria-controls]');
        if (!button) return;
        const target = document.getElementById(button.getAttribute('aria-controls'));
        showDefinition(target);
        target.focus({preventScroll: true});
        const rect = target.getBoundingClientRect();
        if (rect.top < 0 || rect.bottom > innerHeight) target.scrollIntoView({block: 'nearest'});
    });
});

document.querySelectorAll('.project-examples').forEach((examples) => {
    const tabs = [...examples.querySelectorAll('[role="tab"]')];
    const panels = [...examples.querySelectorAll('[role="tabpanel"]')];
    let visible = false;

    function updateReplayImages() {
        for (const panel of panels) {
            const image = panel.querySelector('.example-replay[data-src]');
            if (!image) continue;
            const animate = !panel.hidden && visible && !document.hidden;
            const source = animate ? image.dataset.src : image.dataset.poster;
            if (image.getAttribute('src') !== source) image.src = source;
        }
    }

    function select(tab) {
        for (const candidate of tabs) {
            const selected = candidate === tab;
            candidate.setAttribute('aria-selected', String(selected));
            candidate.tabIndex = selected ? 0 : -1;
        }
        for (const panel of panels) {
            panel.hidden = panel.id !== tab.getAttribute('aria-controls');
            panel.querySelectorAll('.example-code-scroll').forEach((code) => {
                code.scrollTop = 0;
                code.scrollLeft = 0;
            });
        }
        updateReplayImages();
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => select(tab));
        tab.addEventListener('keydown', (event) => {
            let next;
            if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
            if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
            if (event.key === 'Home') next = 0;
            if (event.key === 'End') next = tabs.length - 1;
            if (next === undefined) return;
            event.preventDefault();
            tabs[next].focus();
            select(tabs[next]);
        });
    });

    new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        updateReplayImages();
    }).observe(examples);
    document.addEventListener('visibilitychange', updateReplayImages);
});
