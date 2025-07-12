// Service Worker for Skill Swap Platform
const CACHE_NAME = 'skillswap-v1';
const STATIC_CACHE = 'skillswap-static-v1';
const API_CACHE = 'skillswap-api-v1';

// Static assets to cache
const STATIC_ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/favicon.ico',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// API endpoints to cache
const API_ENDPOINTS = [
    '/api/skills',
    '/api/user_skills/'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - handle requests
self.addEventListener('fetch', event => {
    const request = event.request;
    const url = new URL(request.url);

    // Handle API requests
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(request));
    }
    // Handle static assets
    else if (request.destination === 'style' || 
             request.destination === 'script' || 
             request.destination === 'image' ||
             STATIC_ASSETS.includes(url.pathname)) {
        event.respondWith(handleStaticAsset(request));
    }
    // Handle HTML pages
    else if (request.destination === 'document') {
        event.respondWith(handlePageRequest(request));
    }
});

// Handle API requests with cache-first strategy
async function handleApiRequest(request) {
    const cache = await caches.open(API_CACHE);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
        // Return cached response and update in background
        updateApiCache(request, cache);
        return cachedResponse;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            // Cache successful responses
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.error('API request failed:', error);
        // Return a fallback response if available
        return new Response(JSON.stringify({ error: 'Offline' }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Update API cache in background
async function updateApiCache(request, cache) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
    } catch (error) {
        console.log('Background API update failed:', error);
    }
}

// Handle static assets with cache-first strategy
async function handleStaticAsset(request) {
    const cache = await caches.open(STATIC_CACHE);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.error('Static asset request failed:', error);
        // Return a fallback for critical assets
        if (request.destination === 'style') {
            return new Response('/* Offline fallback */', {
                headers: { 'Content-Type': 'text/css' }
            });
        }
        throw error;
    }
}

// Handle page requests with network-first strategy
async function handlePageRequest(request) {
    try {
        const response = await fetch(request);
        if (response.ok) {
            // Cache successful page responses
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.error('Page request failed:', error);
        
        // Try to return cached version
        const cache = await caches.open(CACHE_NAME);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return offline page if available
        const offlinePage = await cache.match('/offline.html');
        if (offlinePage) {
            return offlinePage;
        }
        
        // Final fallback
        return new Response('You are offline', {
            status: 503,
            headers: { 'Content-Type': 'text/plain' }
        });
    }
}

// Handle background sync for offline actions
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    // Handle any queued offline actions
    console.log('Background sync triggered');
}

// Handle push notifications (if implemented)
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/favicon.ico',
            badge: '/static/favicon.ico',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: data.primaryKey
            }
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    event.waitUntil(
        clients.openWindow('/')
    );
});

// Periodic background sync for cache updates
self.addEventListener('periodicsync', event => {
    if (event.tag === 'cache-update') {
        event.waitUntil(updateCaches());
    }
});

async function updateCaches() {
    console.log('Updating caches...');
    
    // Update API cache
    const apiCache = await caches.open(API_CACHE);
    for (const endpoint of API_ENDPOINTS) {
        try {
            const response = await fetch(endpoint);
            if (response.ok) {
                apiCache.put(endpoint, response.clone());
            }
        } catch (error) {
            console.log(`Failed to update cache for ${endpoint}:`, error);
        }
    }
} 