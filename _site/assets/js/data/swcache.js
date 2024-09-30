const resource = [
    /* --- CSS --- */
    '/gunnargriese.github.io/assets/css/style.css',

    /* --- PWA --- */
    '/gunnargriese.github.io/app.js',
    '/gunnargriese.github.io/sw.js',

    /* --- HTML --- */
    '/gunnargriese.github.io/index.html',
    '/gunnargriese.github.io/404.html',

    
        '/gunnargriese.github.io/services/',
    
        '/gunnargriese.github.io/about/',
    
        '/gunnargriese.github.io/tools/',
    
        '/gunnargriese.github.io/categories/',
    
        '/gunnargriese.github.io/tags/',
    
        '/gunnargriese.github.io/archives/',
    

    /* --- Favicons & compressed JS --- */
    
    
        '/gunnargriese.github.io/assets/img/favicons/android-chrome-192x192.png',
        '/gunnargriese.github.io/assets/img/favicons/android-chrome-512x512.png',
        '/gunnargriese.github.io/assets/img/favicons/apple-touch-icon.png',
        '/gunnargriese.github.io/assets/img/favicons/favicon-16x16.png',
        '/gunnargriese.github.io/assets/img/favicons/favicon-32x32.png',
        '/gunnargriese.github.io/assets/img/favicons/favicon.ico',
        '/gunnargriese.github.io/assets/img/favicons/mstile-150x150.png',
        '/gunnargriese.github.io/assets/js/dist/categories.min.js',
        '/gunnargriese.github.io/assets/js/dist/commons.min.js',
        '/gunnargriese.github.io/assets/js/dist/misc.min.js',
        '/gunnargriese.github.io/assets/js/dist/page.min.js',
        '/gunnargriese.github.io/assets/js/dist/post.min.js'
];

/* The request url with below domain will be cached */
const allowedDomains = [
    

    'localhost:4000',

    

    'fonts.gstatic.com',
    'fonts.googleapis.com',
    'cdn.jsdelivr.net',
    'polyfill.io'
];

/* Requests that include the following path will be banned */
const denyUrls = [
    
];

