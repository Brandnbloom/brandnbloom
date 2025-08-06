self.addEventListener("install", e => {
  console.log("✅ Service Worker Installed");
  e.waitUntil(
    caches.open("brand-n-bloom").then(cache =>
      cache.addAll([
        "/",
        "/index.html",
        "/manifest.json",
        "/favicon.ico",
        "/icons/icon-192.png",
        "/icons/icon-512.png"
      ])
    )
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(response => response || fetch(e.request))
  );
});