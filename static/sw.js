const CACHE_NAME = 'clustersHub-v21';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll([
        '/',
        '/about',
        '/home',
        '/register',
        '/login',
        '/static/createCluster.css',
        '/static/createCluster.js',
        '/static/banner.jpg',
        '/static/header.js',
        '/static/cluster.jpg',
        '/static/logo.jpg'
      ]))
      .catch((error) => console.error('Cache error:', error))
  );
});

self.addEventListener('fetch', (event) => {
  console.log('Fetching:', event.request.url);
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});