// 것모닝 시상 룰렛 서비스 워커: 행사장 인터넷이 끊겨도 열리도록 앱 파일과 글꼴을 저장해 둔다
const VERSION = "gm-award-v1";
const CORE = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/apple-touch-icon.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE.map(u => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  const same = url.origin === location.origin;
  if (!same && !url.host.endsWith("fonts.googleapis.com") && !url.host.endsWith("fonts.gstatic.com")) return;
  const key = e.request.mode === "navigate" ? "index.html" : e.request;
  e.respondWith(caches.open(VERSION).then(async c => {
    const hit = await c.match(key);
    const net = fetch(e.request).then(r => { if (r.ok || r.type === "opaque") c.put(key, r.clone()); return r; });
    if (hit) { e.waitUntil(net.catch(() => {})); return hit; }
    return net;
  }));
});
