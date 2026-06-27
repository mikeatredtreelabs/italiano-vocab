/* ═══════════════════════════════════════════════════════════════════
   Sengeri — Service Worker v2.0.2
   Network-first for shell, cache-first for pack files
   ═══════════════════════════════════════════════════════════════════ */

const CACHE_NAME = 'sengeri-v3';

// Shell files: always try network first so updates come through
const SHELL_FILES = [
  './app.html',
  './app.js',
  './manifest.json',
  './whats-new.html',
];

// Pack files: cache-first (they never change once deployed)
const PACK_FILES = [
  './pack-greet.js',
  './pack-food.js',
  './pack-travel.js',
  './pack-verbs.js',
  './pack-adjectives.js',
  './pack-numbers.js',
  './pack-family.js',
  './pack-body.js',
  './pack-health.js',
  './pack-shopping.js',
  './pack-clothing.js',
  './pack-home.js',
  './pack-nature.js',
  './pack-animals.js',
  './pack-work.js',
  './pack-tech.js',
  './pack-sports.js',
  './pack-arts.js',
  './pack-emotions.js',
  './pack-advverbs.js',
];

/* ── Install: cache everything upfront ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll([...SHELL_FILES, ...PACK_FILES]))
      .then(() => self.skipWaiting())
  );
});

/* ── Activate: delete ALL old caches ── */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* ── Fetch strategy ── */
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isShell = SHELL_FILES.some(f => url.pathname.endsWith(f.replace('./', '/')));
  const isPack  = PACK_FILES.some(f => url.pathname.endsWith(f.replace('./', '/')));

  if (isShell) {
    // Network-first: try fresh copy, fall back to cache if offline
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  } else if (isPack) {
    // Cache-first: packs don't change
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
  }
  // Everything else: just fetch normally
});
