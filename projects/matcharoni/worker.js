import init, {evaluate} from './pkg/matcharoni.js';

self.onmessage = async ({data: {prelude, source}}) => {
    try {
        await init();
        self.postMessage({running: true});
        self.postMessage({text: evaluate(prelude, source), failed: false});
    } catch (error) {
        self.postMessage({text: String(error), failed: true});
    }
};
