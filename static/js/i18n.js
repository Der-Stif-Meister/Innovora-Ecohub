/**
 * INNOVORA ECOHUB GROUP - Advanced Internationalization Module
 * Handles multilingual support with localStorage persistence
 */

class I18nManager {
    constructor() {
        this.currentLanguage = localStorage.getItem('ecohub-language') || 'en';
        this.translations = {};
        this.supportedLanguages = ['en', 'es', 'fr', 'de', 'zh', 'pt', 'ar', 'ja'];
        this.initialized = false;
    }

    /**
     * Initialize i18n system by loading language files
     */
    async init() {
        try {
            // Load all supported language translations
            for (const lang of this.supportedLanguages) {
                try {
                    const response = await fetch(`/static/js/i18n/${lang}.json`);
                    if (response.ok) {
                        this.translations[lang] = await response.json();
                    }
                } catch (error) {
                    console.warn(`Failed to load language: ${lang}`, error);
                }
            }
            this.initialized = true;
            this.updatePageLanguage();
            console.log('✓ I18n initialized successfully');
        } catch (error) {
            console.error('Failed to initialize i18n:', error);
        }
    }

    /**
     * Set the active language and update the page
     */
    setLanguage(lang) {
        if (this.supportedLanguages.includes(lang)) {
            this.currentLanguage = lang;
            localStorage.setItem('ecohub-language', lang);
            this.updatePageLanguage();
            this.onLanguageChanged();
        }
    }

    /**
     * Get current language
     */
    getLanguage() {
        return this.currentLanguage;
    }

    /**
     * Get translation for a key
     */
    t(key, defaultValue = key) {
        const keys = key.split('.');
        let value = this.translations[this.currentLanguage];
        
        // Fallback to English if current language not loaded
        if (!value) {
            console.warn(`Translations for ${this.currentLanguage} not loaded yet, trying English`);
            value = this.translations['en'] || {};
        }
        
        for (const k of keys) {
            value = value[k];
            if (value === undefined) {
                return defaultValue;
            }
        }
        
        return value;
    }

    /**
     * Translate all elements with data-i18n attribute
     */
    updatePageLanguage() {
        // Only update if translations are loaded
        if (!this.translations[this.currentLanguage]) {
            console.warn(`Translations for ${this.currentLanguage} not loaded, skipping page update`);
            return;
        }
        
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'BUTTON') {
                if (element.hasAttribute('placeholder')) {
                    element.setAttribute('placeholder', this.t(`${key}.placeholder`));
                } else {
                    element.textContent = translation;
                }
            } else if (element.hasAttribute('data-i18n-html')) {
                element.innerHTML = translation;
            } else {
                element.textContent = translation;
            }
        });

        // Update page language attribute for CSS
        document.documentElement.lang = this.currentLanguage;
        
        // Store preference
        localStorage.setItem('ecohub-language', this.currentLanguage);
    }

    /**
     * Callback when language changes
     */
    onLanguageChanged() {
        const event = new CustomEvent('languageChanged', {
            detail: { language: this.currentLanguage }
        });
        document.dispatchEvent(event);
    }

    /**
     * Get all supported languages
     */
    getSupportedLanguages() {
        return this.supportedLanguages;
    }

    /**
     * Get language name in English
     */
    getLanguageName(lang) {
        const names = {
            'en': 'English',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'zh': '中文',
            'pt': 'Português',
            'ar': 'العربية',
            'ja': '日本語'
        };
        return names[lang] || lang;
    }
}

// Create global instance
const i18n = new I18nManager();

// Initialize with DOM ready check
function initializeI18n() {
    (async function() {
        try {
            console.log('Starting i18n initialization...');
            // Load all supported language translations
            const loadPromises = i18n.supportedLanguages.map(async (lang) => {
                try {
                    const response = await fetch(`/static/js/i18n/${lang}.json`);
                    if (response.ok) {
                        i18n.translations[lang] = await response.json();
                        console.log(`✓ Loaded ${lang} translations`);
                        return true;
                    } else {
                        console.error(`Failed to load ${lang}: ${response.status}`);
                        return false;
                    }
                } catch (error) {
                    console.error(`Failed to load language: ${lang}`, error);
                    return false;
                }
            });
            
            // Wait for all languages to load
            await Promise.all(loadPromises);
            
            i18n.initialized = true;
            console.log('All translations loaded, current language:', i18n.currentLanguage);
            console.log('Translations object keys:', Object.keys(i18n.translations));
            
            // Update page language ONLY after all translations are loaded
            i18n.updatePageLanguage();
            console.log('✓ I18n initialized successfully and page updated');
        } catch (error) {
            console.error('Failed to initialize i18n:', error);
        }
    })();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeI18n);
} else {
    initializeI18n();
}
