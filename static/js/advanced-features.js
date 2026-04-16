/**
 * INNOVORA ECOHUB GROUP - Advanced Features Module
 * Analytics, Performance Monitoring, and Web APIs
 */

// ============================================
// ADVANCED ANALYTICS SYSTEM
// ============================================

class AnalyticsEngine {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.events = [];
        this.sessionStart = Date.now();
        this.initialized = false;
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Initialize analytics
     */
    init() {
        this.setupEventTracking();
        this.monitorPerformance();
        this.trackUserBehavior();
        this.initialized = true;
        console.log('✓ Analytics Engine initialized');
    }

    /**
     * Track all user events
     */
    setupEventTracking() {
        // Track button clicks
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
                const button = e.target.tagName === 'BUTTON' ? e.target : e.target.closest('button');
                this.trackEvent('button_click', {
                    buttonText: button.textContent.trim(),
                    buttonClass: button.className
                });
            }
        });

        // Track form submissions
        document.addEventListener('submit', (e) => {
            this.trackEvent('form_submit', {
                formId: e.target.id,
                formName: e.target.name
            });
        });

        // Track link clicks
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'A') {
                this.trackEvent('link_click', {
                    url: e.target.href,
                    text: e.target.textContent.trim()
                });
            }
        });
    }

    /**
     * Monitor page performance metrics
     */
    monitorPerformance() {
        if (window.performance && window.performance.timing) {
            window.addEventListener('load', () => {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                const connectTime = perfData.responseEnd - perfData.requestStart;
                const renderTime = perfData.domComplete - perfData.domLoading;

                this.trackEvent('page_performance', {
                    pageLoadTime: Math.round(pageLoadTime),
                    connectTime: Math.round(connectTime),
                    renderTime: Math.round(renderTime)
                });

                console.log(`⏱️  Performance Metrics:
                    - Page Load: ${Math.round(pageLoadTime)}ms
                    - Connect: ${Math.round(connectTime)}ms
                    - Render: ${Math.round(renderTime)}ms`);
            });
        }
    }

    /**
     * Track user behavior
     */
    trackUserBehavior() {
        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', () => {
            const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            if (scrollPercent > maxScroll) {
                maxScroll = scrollPercent;
                if (maxScroll % 25 === 0) {
                    this.trackEvent('scroll_depth', { percentage: Math.round(maxScroll) });
                }
            }
        });

        // Track time on page
        setInterval(() => {
            const sessionDuration = Math.round((Date.now() - this.sessionStart) / 1000);
            if (sessionDuration % 60 === 0) {
                this.trackEvent('session_time', { seconds: sessionDuration });
            }
        }, 10000);

        // Track visibility changes
        document.addEventListener('visibilitychange', () => {
            this.trackEvent('visibility_change', {
                visible: document.visibilityState === 'visible'
            });
        });
    }

    /**
     * Track custom event
     */
    trackEvent(eventName, data = {}) {
        const event = {
            name: eventName,
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            userAgent: navigator.userAgent,
            language: document.documentElement.lang,
            url: window.location.href,
            data: data
        };

        this.events.push(event);
        
        // Store in localStorage
        const stored = JSON.parse(localStorage.getItem('ecohub-analytics') || '[]');
        stored.push(event);
        localStorage.setItem('ecohub-analytics', JSON.stringify(stored.slice(-100))); // Keep last 100 events
    }

    /**
     * Get analytics summary
     */
    getSummary() {
        return {
            sessionId: this.sessionId,
            eventCount: this.events.length,
            sessionDuration: Math.round((Date.now() - this.sessionStart) / 1000),
            events: this.events
        };
    }

    /**
     * Export analytics data
     */
    exportData() {
        const data = localStorage.getItem('ecohub-analytics') || '[]';
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    }
}

// ============================================
// PERFORMANCE MONITORING
// ============================================

class PerformanceMonitor {
    constructor() {
        this.metrics = {};
    }

    /**
     * Measure function execution time
     */
    measure(functionName, fn) {
        const start = performance.now();
        const result = fn();
        const duration = performance.now() - start;
        
        this.metrics[functionName] = duration;
        
        if (duration > 100) {
            console.warn(`⚠️  Slow function: ${functionName} took ${duration.toFixed(2)}ms`);
        }
        
        return result;
    }

    /**
     * Check Core Web Vitals
     */
    checkWebVitals() {
        if ('web-vital' in window) {
            return window['web-vital'];
        }

        const vitals = {
            LCP: null, // Largest Contentful Paint
            FID: null, // First Input Delay
            CLS: null  // Cumulative Layout Shift
        };

        // Observe Largest Contentful Paint
        if ('PerformanceObserver' in window) {
            try {
                const lcpObserver = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    vitals.LCP = lastEntry.renderTime || lastEntry.loadTime;
                });
                lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            } catch (e) {
                console.log('LCP not supported');
            }
        }

        return vitals;
    }

    /**
     * Get all metrics
     */
    getMetrics() {
        return this.metrics;
    }
}

// ============================================
// GEOLOCATION & OFFLINE DETECTION
// ============================================

class LocationManager {
    constructor() {
        this.location = null;
        this.isOffline = !navigator.onLine;
    }

    /**
     * Get user location (with permission)
     */
    async getLocation() {
        if (!navigator.geolocation) {
            console.warn('Geolocation not supported');
            return null;
        }

        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                position => {
                    this.location = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        timestamp: new Date().toISOString()
                    };
                    console.log('✓ Location obtained:', this.location);
                    resolve(this.location);
                },
                error => {
                    console.warn('Location permission denied:', error);
                    reject(error);
                }
            );
        });
    }

    /**
     * Monitor online/offline status
     */
    monitorConnectivity() {
        window.addEventListener('online', () => {
            this.isOffline = false;
            console.log('✓ Connection restored');
            document.body.classList.remove('offline-mode');
        });

        window.addEventListener('offline', () => {
            this.isOffline = true;
            console.log('⚠️  Connection lost - offline mode');
            document.body.classList.add('offline-mode');
        });

        return !this.isOffline;
    }

    /**
     * Get connection info
     */
    getConnectionInfo() {
        if (navigator.connection) {
            return {
                type: navigator.connection.effectiveType,
                downlink: navigator.connection.downlink,
                rtt: navigator.connection.rtt,
                saveData: navigator.connection.saveData
            };
        }
        return null;
    }
}

// ============================================
// NOTIFICATION SYSTEM
// ============================================

class NotificationManager {
    constructor() {
        this.permission = Notification.permission;
    }

    /**
     * Request notification permission
     */
    async requestPermission() {
        if (!('Notification' in window)) {
            console.warn('Notifications not supported');
            return false;
        }

        if (this.permission === 'denied') {
            console.warn('Notifications denied by user');
            return false;
        }

        if (this.permission === 'granted') {
            return true;
        }

        const result = await Notification.requestPermission();
        this.permission = result;
        return result === 'granted';
    }

    /**
     * Send notification
     */
    async send(title, options = {}) {
        if (this.permission !== 'granted') {
            await this.requestPermission();
        }

        if (this.permission === 'granted') {
            return new Notification(title, {
                icon: '/assets/photo_2026-04-14_11-41-52.jpg',
                badge: '/assets/photo_2026-04-14_11-41-52.jpg',
                ...options
            });
        }
    }
}

// ============================================
// STORAGE MANAGER
// ============================================

class StorageManager {
    constructor() {
        this.quota = 0;
        this.usage = 0;
    }

    /**
     * Get storage quota and usage
     */
    async getStorageInfo() {
        if (navigator.storage && navigator.storage.estimate) {
            const estimate = await navigator.storage.estimate();
            this.quota = estimate.quota;
            this.usage = estimate.usage;
            
            return {
                quota: this.quota,
                usage: this.usage,
                available: this.quota - this.usage,
                percentage: (this.usage / this.quota) * 100
            };
        }
        return null;
    }

    /**
     * Request persistent storage
     */
    async requestPersistent() {
        if (navigator.storage && navigator.storage.persist) {
            const persistent = await navigator.storage.persist();
            console.log(persistent ? '✓ Persistent storage granted' : '⚠️  Persistent storage denied');
            return persistent;
        }
        return false;
    }

    /**
     * Save data to IndexedDB
     */
    async saveToIndexedDB(storeName, data) {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('innovora_db', 1);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                const db = request.result;
                const transaction = db.transaction([storeName], 'readwrite');
                const store = transaction.objectStore(storeName);
                const addRequest = store.add(data);
                addRequest.onsuccess = () => resolve(addRequest.result);
            };

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains(storeName)) {
                    db.createObjectStore(storeName, { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }
}

// ============================================
// GLOBAL INSTANCES
// ============================================

const analytics = new AnalyticsEngine();
const perfMonitor = new PerformanceMonitor();
const locationMgr = new LocationManager();
const notificationMgr = new NotificationManager();
const storageMgr = new StorageManager();

// Initialize when ready
document.addEventListener('DOMContentLoaded', () => {
    analytics.init();
    locationMgr.monitorConnectivity();
    storageMgr.getStorageInfo();
});

// Register service worker
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/service-worker.js')
        .then(reg => console.log('✓ Service Worker registered'))
        .catch(err => console.log('Service Worker registration failed:', err));
}

console.log('✓ Advanced Features Module loaded');
