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
                    const response = await fetch(`js/i18n/${lang}.json`);
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
        let value = this.translations[this.currentLanguage] || {};
        
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

// Initialize immediately with inline translation loading
(async function() {
    try {
        // Load all supported language translations
        for (const lang of i18n.supportedLanguages) {
            try {
                const response = await fetch(`js/i18n/${lang}.json`);
                if (response.ok) {
                    i18n.translations[lang] = await response.json();
                }
            } catch (error) {
                console.warn(`Failed to load language: ${lang}`, error);
            }
        }
        i18n.initialized = true;
        
        // Update page language immediately after translations load
        i18n.updatePageLanguage();
        console.log('✓ I18n initialized successfully with language:', i18n.currentLanguage);
    } catch (error) {
        console.error('Failed to initialize i18n:', error);
    }
})();
