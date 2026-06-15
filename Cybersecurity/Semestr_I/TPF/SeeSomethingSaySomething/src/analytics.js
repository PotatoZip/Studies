import ReactGA from 'react-ga4';

const MEASUREMENT_ID = import.meta.env.VITE_GA_MEASUREMENT_ID || 'G-HYTP4LMG39';

export const initializeAnalytics = () => {
    ReactGA.initialize(MEASUREMENT_ID);
};

export const trackPageView = (path) => {
    ReactGA.gtag('event', 'page_view', {
        page_path: path,
        page_location: window.location.href,
        page_title: document.title,
        debug_mode: import.meta.env.DEV,
    });
};

export const trackEvent = (category, action, label) => {
    ReactGA.event({
        category: category,
        action: action,
        label: label,
    });
};
