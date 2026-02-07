const CACHE_NAME = 'clustersHub-v1';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll([
        '/about',
        '/home',
        '/register',
        '/static/createCluster.css',
        '/static/createCluster.js',
        '/static/banner.jpg',
        '/static/header.js',
        '/static/cluster.jpg',
        '/static/logo.jpg',
        '/user_requests',
        '/clusters',
        '/forgot',
        '/myProfile',
        '/terms',
        '/login',
        '/'
      ]))
      .catch((error) => console.error('Cache error:', error))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});