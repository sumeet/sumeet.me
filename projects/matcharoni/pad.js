const prelude = document.getElementById('matcharoni-prelude').content.textContent;
const token = /(?<comment>\/\/[^\n]*)|(?<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')|(?<keyword>\b(?:pat|for|if|else|while)\b)|(?<number>\b\d+\b)|(?<operator><@|=>|<-|<<|@|~|[%#*](?=[a-zA-Z_]))|(?<name>\b[a-zA-Z_]\w*)/g;

function highlight(code, source) {
    const patterns = new Set(Array.from((prelude + '\n' + source).matchAll(/^\s*pat\s+(\w+)/gm), m => m[1]));
    const fragment = document.createDocumentFragment();
    function appendText(text, kind) {
        if (!text) return;
        const span = document.createElement('span');
        // The textarea exposes the source to assistive technology. Only links
        // in the visual copy need to be announced separately.
        span.setAttribute('aria-hidden', 'true');
        if (kind) span.className = 'syntax-' + kind;
        span.textContent = text;
        fragment.append(span);
    }

    let offset = 0;
    for (const match of source.matchAll(token)) {
        appendText(source.slice(offset, match.index));
        const kind = match.groups.name
            ? (patterns.has(match[0]) ? 'pattern' : null)
            : Object.keys(match.groups).find(key => match.groups[key] !== undefined);
        let start = 0;
        if (kind === 'comment') {
            for (const url of match[0].matchAll(/https?:\/\/[^\s<>"']+/g)) {
                appendText(match[0].slice(start, url.index), kind);
                const link = document.createElement('a');
                link.href = url[0];
                link.textContent = url[0];
                link.target = '_blank';
                link.rel = 'noopener';
                fragment.append(link);
                start = url.index + url[0].length;
            }
        }
        appendText(match[0].slice(start), kind);
        offset = match.index + match[0].length;
    }
    appendText(source.slice(offset));
    // A textarea keeps a caret line after a trailing newline. Give its mirror the same height.
    if (!source || source.endsWith('\n')) appendText(' ');
    code.replaceChildren(fragment);
}

function mount(pad) {
    const source = pad.querySelector('.taste-source');
    const code = source.querySelector('code');
    const output = pad.querySelector('.taste-value');
    const result = output.querySelector('samp');
    const editor = document.createElement('textarea');
    editor.value = code.textContent;
    editor.spellcheck = false;
    editor.autocapitalize = 'off';
    editor.setAttribute('autocorrect', 'off');
    editor.setAttribute('aria-label', pad.getAttribute('aria-label') + ' — edit matcharoni code');
    editor.title = 'Edit the code to run it';
    highlight(code, editor.value);
    source.append(editor);

    let worker;
    let timer;
    let running = false;
    function discardWorker() {
        worker?.terminate();
        worker = null;
        running = false;
    }
    function finish(text, failed) {
        clearTimeout(timer);
        running = false;
        if (failed) discardWorker();
        result.textContent = text;
        output.classList.toggle('has-error', failed);
        output.removeAttribute('aria-busy');
        editor.setAttribute('aria-invalid', String(failed));
    }
    function createWorker() {
        const current = new Worker(new URL('./worker.js', import.meta.url), {type: 'module'});
        current.onmessage = ({data}) => {
            if (worker !== current) return;
            if (data.running) {
                // Start the execution clock after the first WASM download has finished.
                clearTimeout(timer);
                timer = setTimeout(() => finish('Evaluation timed out.', true), 2000);
            } else {
                finish(data.text, data.failed);
            }
        };
        current.onerror = () => {
            if (worker === current) finish('Could not start the interpreter. Edit to retry.', true);
        };
        return current;
    }
    function run() {
        try {
            worker ??= createWorker();
            running = true;
            timer = setTimeout(() => finish('Could not load the interpreter. Edit to retry.', true), 30000);
            worker.postMessage({prelude, source: editor.value});
        } catch (error) {
            finish(String(error), true);
        }
    }
    function schedule(delay) {
        clearTimeout(timer);
        if (running) discardWorker();
        output.setAttribute('aria-busy', 'true');
        timer = setTimeout(run, delay);
    }
    editor.addEventListener('input', event => {
        highlight(code, editor.value);
        if (!event.isComposing) schedule(220);
    });
    editor.addEventListener('compositionend', () => schedule(220));
    editor.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey) {
            const link = document.elementsFromPoint(event.clientX, event.clientY)
                .find(el => el.tagName === 'A' && code.contains(el));
            link?.click();
        }
    });
    editor.addEventListener('keydown', event => {
        if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            schedule(0);
        }
    });
}

document.querySelectorAll('#matcharoni .taste-example').forEach(mount);
