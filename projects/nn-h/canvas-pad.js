// A DOM/Canvas2D view for browsers where egui's WebGL renderer cannot start.
// The Rust CpuDrawingPad owns the same strokes -> MNIST -> network pipeline.
export function startCanvasPad(CpuDrawingPad, weights) {
  const model = new CpuDrawingPad(weights);
  const root = document.createElement('div');
  root.className = 'canvas-pad';
  root.innerHTML = `<div class="drawing">
    <label for="drawing">Draw a digit</label>
    <canvas id="drawing" aria-label="Draw a handwritten digit" width="400" height="400"></canvas>
    <div class="actions"><button id="recognize" disabled>Feed forward</button><button id="clear">Clear</button></div>
  </div><div class="prediction"><span>Prediction</span><output aria-live="polite">—</output></div>`;
  document.querySelector('#canvas').replaceWith(root);
  const canvas = root.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Canvas2D unavailable');
  const recognize = root.querySelector('#recognize');
  const output = root.querySelector('output');
  const announcement = document.querySelector('#result');
  let pointer = null;
  let last = null;
  let hasInk = false;
  const position = event => {
    const rect = canvas.getBoundingClientRect();
    return [Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width)),
      Math.max(0, Math.min(1, (event.clientY - rect.top) / rect.height))];
  };
  ctx.strokeStyle = '#2a2e33';
  ctx.lineWidth = 10;
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';
  canvas.addEventListener('pointerdown', event => {
    if (pointer !== null || event.button !== 0) return;
    event.preventDefault();
    pointer = event.pointerId;
    canvas.setPointerCapture(pointer);
    last = position(event);
    model.begin_stroke();
    model.point(...last);
  });
  function move(event) {
    if (event.pointerId !== pointer) return;
    const next = position(event);
    if (next[0] === last[0] && next[1] === last[1]) return;
    model.point(...next);
    ctx.beginPath();
    ctx.moveTo(last[0] * canvas.width, last[1] * canvas.height);
    ctx.lineTo(next[0] * canvas.width, next[1] * canvas.height);
    ctx.stroke();
    last = next;
    hasInk = true;
    recognize.disabled = false;
  }
  canvas.addEventListener('pointermove', move);
  canvas.addEventListener('pointerup', event => {
    if (event.pointerId !== pointer) return;
    move(event);
    pointer = null;
  });
  for (const type of ['pointercancel', 'lostpointercapture']) {
    canvas.addEventListener(type, event => {
      if (event.pointerId === pointer) pointer = null;
    });
  }
  recognize.addEventListener('click', () => {
    if (!hasInk) return;
    const digit = model.predict();
    output.textContent = String(digit);
    announcement.textContent = `Prediction: ${digit}`;
  });
  root.querySelector('#clear').addEventListener('click', () => {
    model.clear();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pointer = null;
    hasInk = false;
    recognize.disabled = true;
    output.textContent = '—';
    announcement.textContent = 'Draw a digit, then press Feed forward.';
  });
  return model;
}
