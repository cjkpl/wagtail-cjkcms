// Adapted from Sebastvin/wagtail-character-counter (MIT), by Sebastvin.
// https://github.com/Sebastvin/wagtail-character-counter/tree/000f1ae62ca0b90cd052942b2ef38afbea052089
(() => {
  const EDITOR_SELECTOR = '.w-field--draftail_rich_text_area';
  const EDITABLE_SELECTOR = '.DraftEditor-editorContainer [contenteditable="true"]';
  const BLOCK_SELECTOR = '[data-block="true"]';
  const WORD_SEPARATOR = /\s+/;

  const counters = new WeakMap();
  const observers = new WeakMap();

  const getOrInsertComputed = (map, key, compute) => {
    if (typeof map.getOrInsertComputed === 'function') {
      return map.getOrInsertComputed(key, compute);
    }
    if (!map.has(key)) {
      map.set(key, compute(key));
    }
    return /** @type {V} */ (map.get(key));
  };

  const isError = (value) =>
    typeof Error.isError === 'function' ? Error.isError(value) : value instanceof Error;

  const reportError = (error) => {
    console.error('cjkcms character counter:', isError(error) ? error.message : error);
  };

  const guard =
    (callback) =>
    (...args) => {
      try {
        callback(...args);
      } catch (error) {
        reportError(error);
      }
    };

  const countWords = (text) => text.split(WORD_SEPARATOR).filter(Boolean).length;

  const measure = (editable) => {
    const blocks = [...editable.querySelectorAll(BLOCK_SELECTOR)];
    const texts =
      blocks.length > 0
        ? blocks.map((block) => block.textContent ?? '')
        : [editable.textContent ?? ''];

    return texts.reduce(
      (counts, text) => ({
        characters: counts.characters + text.length,
        words: counts.words + countWords(text),
      }),
      { characters: 0, words: 0 },
    );
  };

  const createCounter = (editor) => {
    const characters = document.createElement('div');
    const words = document.createElement('div');

    characters.className = 'character-counter character-counter--characters';
    words.className = 'character-counter character-counter--words';
    editor.after(characters, words);

    return { characters, words };
  };

  const render = (counter, counts) => {
    counter.characters.replaceChildren(`Characters: ${counts.characters}`);
    counter.words.replaceChildren(`Words: ${counts.words}`);
  };

  const updateCounter = guard((/** @type {Element} */ editor) => {
    const editable = editor.querySelector(EDITABLE_SELECTOR);

    if (editable) {
      render(getOrInsertComputed(counters, editor, createCounter), measure(editable));
    }
  });

  const createObserver = (editor) => {
    const observer = new MutationObserver(() => updateCounter(editor));

    observer.observe(editor, { characterData: true, childList: true, subtree: true });
    updateCounter(editor);

    return observer;
  };

  const watchEditor = (editor) => {
    getOrInsertComputed(observers, editor, createObserver);
  };

  const findEditors = (node) => {
    if (!(node instanceof Element)) {
      return [];
    }
    return [
      ...(node.matches(EDITOR_SELECTOR) ? [node] : []),
      ...node.querySelectorAll(EDITOR_SELECTOR),
    ];
  };

  const watchAddedEditors = guard((/** @type {MutationRecord[]} */ mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => findEditors(node).forEach(watchEditor));
    });
  });

  const start = guard(() => {
    document.querySelectorAll(EDITOR_SELECTOR).forEach(watchEditor);
    new MutationObserver(watchAddedEditors).observe(document.body, {
      childList: true,
      subtree: true,
    });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
