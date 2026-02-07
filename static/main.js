if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register("/static/sw.js")
    .then((registration) => console.log('SW registered: ' + registration.scope))
    .catch((error) => console.log('SW registration failed: ' + error));
}