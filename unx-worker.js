self.addEventListener("install", event => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", event => {
  event.waitUntil(self.clients.claim());
});

const gameURL = new URL("game.unx", self.registration.scope);

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" ||
      url.origin !== gameURL.origin ||
      url.pathname !== gameURL.pathname) return;

  event.respondWith((async () => {
    const chunks = await Promise.all([1, 2].map(async number => {
      const response = await fetch(new URL(`game.unx.part${number}`, gameURL));
      if (!response.ok) throw new Error(`Missing game.unx.part${number}`);
      return response.arrayBuffer();
    }));

    return new Response(new Blob(chunks), {
      headers: { "Content-Type": "application/octet-stream" }
    });
  })());
});