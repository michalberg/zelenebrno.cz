// Generic horizontal slider driven by data-attributes
function initSlider(root) {
  const track = root.querySelector('[data-slider-track]');
  if (!track) return;

  const prev = root.querySelector('[data-slider-prev]');
  const next = root.querySelector('[data-slider-next]');
  const originals = Array.from(track.children);
  const N = originals.length;
  let idx = 0;
  let loopMode = false;

  // Always loop (infinite scroll)
  const mql = window.matchMedia('(max-width: 1100px)');

  // Autoplay
  const AUTOPLAY_DELAY = 4000;
  let autoTimer = null;
  let userPaused = false;

  function startAutoplay() {
    if (userPaused) return;
    clearInterval(autoTimer);
    autoTimer = setInterval(() => {
      if (document.hidden) return;
      idx++;
      update();
    }, AUTOPLAY_DELAY);
  }

  function pauseAutoplay() {
    userPaused = true;
    clearInterval(autoTimer);
    autoTimer = null;
  }

  // Clone a slide for the infinite-loop buffer, but strip data-fancybox from
  // the clone so the lightbox gallery only ever contains the originals (clones
  // were causing each photo to appear 3× in the Fancybox filmstrip). A click on
  // a clone is forwarded to the matching original so the lightbox still opens.
  function prepClone(node, originalIndex) {
    const clone = node.cloneNode(true);
    clone.querySelectorAll('[data-fancybox]').forEach((el) => {
      el.removeAttribute('data-fancybox');
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const orig = originals[originalIndex]?.querySelector('[data-fancybox]');
        if (orig) orig.click();
      });
    });
    return clone;
  }

  function rebuild() {
    const shouldLoop = N > 1;
    if (shouldLoop === loopMode && track.children.length > 0) return;

    track.style.transition = 'none';
    track.replaceChildren();
    if (shouldLoop) {
      const before = originals.map((c, i) => prepClone(c, i));
      const after = originals.map((c, i) => prepClone(c, i));
      [...before, ...originals, ...after].forEach((c) => track.appendChild(c));
      idx = 0;
    } else {
      originals.forEach((c) => track.appendChild(c));
      idx = 0;
    }
    loopMode = shouldLoop;
    void track.offsetWidth;
    track.style.transition = '';
  }

  function metrics() {
    const card = track.children[0];
    const cardWidth = card ? card.getBoundingClientRect().width : 0;
    const gap = parseFloat(getComputedStyle(track).gap) || 0;
    const viewportWidth = track.parentElement.getBoundingClientRect().width;
    return { cardWidth, gap, viewportWidth, step: cardWidth + gap };
  }

  function trackIndex() {
    return loopMode ? N + idx : idx;
  }

  function offsetFor(i) {
    const { step } = metrics();
    return i * step;
  }

  function desktopMaxIdx() {
    const { cardWidth, viewportWidth, step } = metrics();
    const total = N * cardWidth + (N - 1) * (step - cardWidth);
    const maxOffset = Math.max(0, total - viewportWidth);
    if (step <= 0) return 0;
    const fullSteps = Math.floor(maxOffset / step);
    const remainder = maxOffset - fullSteps * step;
    return remainder > step / 2 ? fullSteps + 1 : Math.max(0, fullSteps);
  }

  function update(animate = true) {
    if (!track.children.length) return;
    if (!animate) track.style.transition = 'none';
    if (!loopMode) {
      idx = Math.max(0, Math.min(idx, desktopMaxIdx()));
    }
    const offset = offsetFor(trackIndex());
    track.style.transform = `translateX(${-offset}px)`;
    if (!animate) {
      void track.offsetWidth;
      track.style.transition = '';
    }
    if (prev) prev.disabled = !loopMode && idx === 0;
    if (next) next.disabled = !loopMode && idx >= desktopMaxIdx();
  }

  track.addEventListener('transitionend', (e) => {
    if (e.propertyName !== 'transform' || !loopMode) return;
    if (idx < 0) { idx += N; update(false); }
    else if (idx >= N) { idx -= N; update(false); }
  });

  function normalizeNow() {
    if (!loopMode) return;
    if (idx < 0) { idx += N; update(false); }
    else if (idx >= N) { idx -= N; update(false); }
  }

  if (prev) prev.addEventListener('click', () => { pauseAutoplay(); normalizeNow(); idx--; update(); });
  if (next) next.addEventListener('click', () => { pauseAutoplay(); normalizeNow(); idx++; update(); });

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { rebuild(); update(false); }, 100);
  });

  rebuild();
  update(false);
  startAutoplay();

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) { normalizeNow(); update(false); }
  });

  // Swipe / drag support
  let startX = 0;
  let startY = 0;
  let dragging = false;
  let baseOffset = 0;
  let locked = null;

  function currentOffset() {
    const m = /translateX\((-?[\d.]+)px\)/.exec(track.style.transform);
    return m ? parseFloat(m[1]) : 0;
  }

  track.style.touchAction = 'pan-y';
  track.style.cursor = 'grab';

  track.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    dragging = true;
    locked = null;
    startX = e.clientX;
    startY = e.clientY;
    baseOffset = currentOffset();
    track.style.transition = 'none';
    track.style.cursor = 'grabbing';
  });

  track.addEventListener('pointermove', (e) => {
    if (!dragging) return;
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    if (locked === null) {
      if (Math.abs(dx) < 6 && Math.abs(dy) < 6) return;
      locked = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
      if (locked === 'x') { try { track.setPointerCapture(e.pointerId); } catch {} }
    }
    if (locked !== 'x') return;
    e.preventDefault();
    track.style.transform = `translateX(${baseOffset + dx}px)`;
  });

  let suppressClick = false;
  function endDrag(e) {
    if (!dragging) return;
    dragging = false;
    track.style.transition = '';
    track.style.cursor = 'grab';
    if (locked === 'x') {
      const dx = e.clientX - startX;
      if (Math.abs(dx) > 6) suppressClick = true;
      const { cardWidth } = metrics();
      const threshold = Math.max(40, cardWidth * 0.18);
      if (dx <= -threshold) { pauseAutoplay(); idx++; }
      else if (dx >= threshold) { pauseAutoplay(); idx--; }
    }
    update();
  }

  track.addEventListener('pointerup', endDrag);
  track.addEventListener('pointercancel', endDrag);
  track.addEventListener('dragstart', (e) => e.preventDefault());
  track.addEventListener('click', (e) => {
    if (suppressClick) {
      e.preventDefault();
      e.stopPropagation();
      suppressClick = false;
    }
  }, true);
}

document.querySelectorAll('[data-slider]').forEach(initSlider);

// Hero heading: snap-typing loop. Cycles through phrases — types prefix +
// accent word (green box grows with the accent letters), pauses, erases
// everything, then types the next phrase. The trailing dot stays visible
// and rides along at the end of the typed text.
function initHeroTyping(root) {
  const typeDelay = 140;
  const eraseDelay = 70;
  const holdAfterType = 1800;
  const holdAfterErase = 250;

  const container = root.querySelector('[data-hero-content]');
  if (!container) return;

  let phrases;
  try { phrases = JSON.parse(root.dataset.heroPhrases || '[]'); }
  catch (e) { return; }
  if (!phrases.length) return;

  const sleep = (ms) => new Promise(r => setTimeout(r, ms));

  function makeChar(ch) {
    // Use real text nodes (so word-spacing and wrapping behave normally)
    return document.createTextNode(ch === ' ' ? ' ' : ch);
  }

  function reset(phrase) {
    container.innerHTML = '';
    const prefixHolder = document.createElement('span');
    prefixHolder.className = 'accent-prefix';
    container.appendChild(prefixHolder);

    const accent = document.createElement('span');
    accent.className = 'accent-mark';
    accent.style.setProperty('--accent-progress', '0');
    container.appendChild(accent);

    // Visible part of the accent word — letters appear here one by one.
    const visible = document.createElement('span');
    accent.appendChild(visible);

    // Dot rides along after the visible letters (inside accent so it
    // stays glued to the typed text, no extra padding gap).
    const dot = document.createElement('span');
    dot.className = 'accent-dot';
    dot.textContent = '.';
    accent.appendChild(dot);

    // Ghost holds the remaining letters at full width so the green bar
    // (which scales relative to .accent-mark's box) is always sized to
    // the FINAL word width — that way scaleX(revealed/total) covers
    // exactly the revealed letters.
    const ghost = document.createElement('span');
    ghost.className = 'accent-mark__ghost';
    ghost.textContent = phrase.accent || '';
    accent.appendChild(ghost);

    return { prefixHolder, accent, visible, ghost };
  }

  async function typeIn(phrase, { prefixHolder, accent, visible, ghost }) {
    // Build the prefix as a single growing text node (not one node per char) so
    // the browser wraps it normally by words; per-node chars never broke lines.
    for (let i = 0; i < phrase.prefix.length; i++) {
      prefixHolder.textContent = phrase.prefix.slice(0, i + 1);
      await sleep(typeDelay);
    }
    const word = phrase.accent || '';
    const total = word.length || 1;
    for (let i = 0; i < word.length; i++) {
      visible.appendChild(makeChar(word[i]));
      ghost.textContent = word.slice(i + 1);
      accent.style.setProperty('--accent-progress', ((i + 1) / total).toFixed(3));
      await sleep(typeDelay);
    }
  }

  async function eraseOut(phrase, { prefixHolder, accent, visible, ghost }) {
    const word = phrase.accent || '';
    const total = word.length || 1;
    while (visible.lastChild) {
      visible.removeChild(visible.lastChild);
      const remaining = visible.childNodes.length;
      ghost.textContent = word.slice(remaining);
      accent.style.setProperty('--accent-progress', (remaining / total).toFixed(3));
      await sleep(eraseDelay);
    }
    accent.style.setProperty('--accent-progress', '0');
    let plen = prefixHolder.textContent.length;
    while (plen > 0) {
      plen--;
      prefixHolder.textContent = prefixHolder.textContent.slice(0, plen);
      await sleep(eraseDelay);
    }
  }

  async function loop() {
    let idx = 0;
    while (true) {
      const parts = reset(phrases[idx]);
      await typeIn(phrases[idx], parts);
      await sleep(holdAfterType);
      await eraseOut(phrases[idx], parts);
      await sleep(holdAfterErase);
      idx = (idx + 1) % phrases.length;
    }
  }

  loop();
}

document.querySelectorAll('[data-hero-typing]').forEach(initHeroTyping);

// Mobile nav: toggle hamburger / overlay
(function initNav() {
  const toggle = document.querySelector('[data-nav-toggle]');
  const overlay = document.querySelector('[data-nav-overlay]');
  if (!toggle || !overlay) return;

  function setOpen(open) {
    toggle.classList.toggle('is-open', open);
    overlay.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    overlay.setAttribute('aria-hidden', String(!open));
    document.body.classList.toggle('nav-open', open);
  }

  toggle.addEventListener('click', () => setOpen(!toggle.classList.contains('is-open')));
  const closeBtn = overlay.querySelector('[data-nav-close]');
  if (closeBtn) closeBtn.addEventListener('click', () => setOpen(false));
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) setOpen(false);
  });
  overlay.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false);
  });
})();

// Section scroll fade-in
(function () {
  if (!window.IntersectionObserver) return;

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    },
    // threshold 0 so tall elements (e.g. a long WYSIWYG block whose 8% height
    // exceeds the viewport) still reveal as soon as any part enters view.
    { threshold: 0, rootMargin: '0px 0px -8% 0px' }
  );

  document.querySelectorAll('section').forEach((section) => {
    if (section.classList.contains('hero-full')) return;
    section.querySelectorAll(':scope > *').forEach((el) => {
      el.classList.add('fade-in');
      io.observe(el);
    });
  });
})();

// Person modal
(function () {
  const modal = document.getElementById('personModal');
  if (!modal) return;

  const backdrop = modal.querySelector('.person-modal__backdrop');
  const img = modal.querySelector('.person-modal__img');
  const role = modal.querySelector('.person-modal__role');
  const name = modal.querySelector('.person-modal__name');
  const bio = modal.querySelector('.person-modal__bio');
  const socials = modal.querySelector('.person-modal__socials');

  const assetsBase = modal.dataset.assets || 'assets/img';
  const SOCIAL_NETWORKS = [
    { key: 'linkedin',  label: 'LinkedIn',  icon: assetsBase + '/linkedin.svg' },
    { key: 'facebook',  label: 'Facebook',  icon: assetsBase + '/facebook.svg' },
    { key: 'instagram', label: 'Instagram', icon: assetsBase + '/instagram.svg' },
    { key: 'bluesky',   label: 'Bluesky',   icon: assetsBase + '/bluesky.svg' },
  ];

  function open(card) {
    img.src = card.dataset.img || '';
    img.alt = card.dataset.name || '';
    role.textContent = card.dataset.role || '';
    name.textContent = card.dataset.name || '';
    bio.innerHTML = card.dataset.bio || '';

    if (socials) {
      socials.innerHTML = SOCIAL_NETWORKS
        .filter(net => card.dataset[net.key])
        .map(net => `
          <li>
            <a href="${card.dataset[net.key]}" target="_blank" rel="noopener noreferrer" aria-label="${net.label}">
              <img src="${net.icon}" alt="" />
            </a>
          </li>
        `).join('');
    }

    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  document.addEventListener('click', (e) => {
    const card = e.target.closest('[data-person]');
    if (card) { open(card); return; }
    if (e.target === backdrop || e.target.closest('.person-modal__close')) close();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });
})();

// Hero slider (fade autoplay)
(function () {
  document.querySelectorAll('[data-hero-slider]').forEach((slider) => {
    const slides = slider.querySelectorAll('.hero-slider__img');
    if (slides.length < 2) return;

    const interval = parseInt(slider.dataset.interval, 10) || 5000;
    let active = Array.from(slides).findIndex((s) => s.classList.contains('is-active'));
    if (active < 0) {
      active = 0;
      slides[0].classList.add('is-active');
    }

    setInterval(() => {
      slides[active].classList.remove('is-active');
      active = (active + 1) % slides.length;
      slides[active].classList.add('is-active');
    }, interval);
  });
})();

// Fancybox lightbox
if (typeof Fancybox !== 'undefined') {
  Fancybox.bind('[data-fancybox]', {});
}

// Smooth scroll for in-page anchor links (e.g. program/menu links to #section)
(function () {
  const nav = document.querySelector('.site-nav');

  // The nav is in normal flow on desktop and position:fixed on mobile.
  // Only offset by its height while it actually overlaps the content.
  function navOffset() {
    if (!nav) return 0;
    return getComputedStyle(nav).position === 'fixed' ? nav.offsetHeight : 0;
  }

  function scrollToTarget(target) {
    const top = target.getBoundingClientRect().top + window.pageYOffset - navOffset();
    window.scrollTo({ top, behavior: 'smooth' });
  }

  document.addEventListener('click', (e) => {
    const link = e.target.closest('a[href*="#"]');
    if (!link) return;

    // Same-page only: ignore links pointing to another path.
    const url = new URL(link.href, window.location.href);
    if (url.pathname !== window.location.pathname || url.search !== window.location.search) return;

    const id = decodeURIComponent(url.hash.slice(1));
    if (!id) return;

    const target = document.getElementById(id);
    if (!target) return;

    e.preventDefault();
    scrollToTarget(target);
    history.pushState(null, '', url.hash);
  });

  // Honour an offset when landing on the page with a hash already in the URL.
  if (window.location.hash.length > 1) {
    const target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    if (target) {
      window.addEventListener('load', () => {
        window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - navOffset() });
      });
    }
  }
})();

