/* ============================================================
   Phuket Interactive Textbook — vocab click-to-define
   ------------------------------------------------------------
   Wrap any word with: <span class="vocab" data-def="...">word</span>
   Optionally add data-pron="pronunciation hint".
   Tap or click the word to see a definition popover.
   Tap outside, press Esc, or scroll to dismiss.
   ============================================================ */

(function () {
  let activePop = null;
  let activeSpan = null;

  function closePop() {
    if (activePop) {
      activePop.remove();
      activePop = null;
    }
    if (activeSpan) {
      activeSpan.classList.remove('is-open');
      activeSpan.setAttribute('aria-expanded', 'false');
      activeSpan = null;
    }
  }

  function positionPop(span, pop) {
    const r = span.getBoundingClientRect();
    const popRect = pop.getBoundingClientRect();
    const margin = 8;

    // Horizontal: center on the word, but clamp inside viewport
    let left = r.left + window.scrollX + r.width / 2 - popRect.width / 2;
    const minLeft = window.scrollX + margin;
    const maxLeft = window.scrollX + document.documentElement.clientWidth - popRect.width - margin;
    left = Math.max(minLeft, Math.min(left, maxLeft));

    // Vertical: below by default; flip above if no room
    let top = r.bottom + window.scrollY + 8;
    const viewportBottom = window.scrollY + window.innerHeight - margin;
    if (top + popRect.height > viewportBottom && r.top - popRect.height - 8 > window.scrollY) {
      top = r.top + window.scrollY - popRect.height - 8;
    }

    pop.style.left = left + 'px';
    pop.style.top = top + 'px';
  }

  function openPop(span) {
    closePop();
    const def = span.dataset.def;
    if (!def) return;

    const term = (span.dataset.term || span.textContent || '').trim();
    const pron = span.dataset.pron;

    const pop = document.createElement('div');
    pop.className = 'vocab-pop';
    pop.setAttribute('role', 'tooltip');

    const termEl = document.createElement('div');
    termEl.className = 'vocab-pop-term';
    termEl.textContent = term;
    pop.appendChild(termEl);

    const defEl = document.createElement('div');
    defEl.className = 'vocab-pop-def';
    defEl.textContent = def;
    pop.appendChild(defEl);

    if (pron) {
      const pronEl = document.createElement('div');
      pronEl.className = 'vocab-pop-pron';
      pronEl.textContent = '/ ' + pron + ' /';
      pop.appendChild(pronEl);
    }

    document.body.appendChild(pop);
    positionPop(span, pop);

    span.classList.add('is-open');
    span.setAttribute('aria-expanded', 'true');
    activePop = pop;
    activeSpan = span;
  }

  function onClick(e) {
    const v = e.target.closest('.vocab');
    if (v) {
      e.stopPropagation();
      if (activeSpan === v) {
        closePop();
      } else {
        openPop(v);
      }
      return;
    }
    if (!e.target.closest('.vocab-pop')) {
      closePop();
    }
  }

  function onKey(e) {
    if (e.key === 'Escape') closePop();
    if ((e.key === 'Enter' || e.key === ' ') && document.activeElement && document.activeElement.classList.contains('vocab')) {
      e.preventDefault();
      const v = document.activeElement;
      if (activeSpan === v) closePop();
      else openPop(v);
    }
  }

  // Add accessibility attributes to vocab spans inside `root` (defaults to document).
  // Safe to call repeatedly — used after dynamic content is inserted into a chapter.
  function attach(root) {
    (root || document).querySelectorAll('.vocab').forEach(el => {
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
      el.setAttribute('role', 'button');
      el.setAttribute('aria-expanded', 'false');
      const def = el.dataset.def;
      if (def) el.setAttribute('aria-label', el.textContent + ': click to define');
    });
  }

  function init() {
    attach(document);
    document.addEventListener('click', onClick);
    document.addEventListener('keydown', onKey);
    window.addEventListener('scroll', closePop, true);
    window.addEventListener('resize', closePop);
  }

  // Public API for chapters that inject vocab spans dynamically.
  window.Vocab = { attach: attach, close: closePop };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
