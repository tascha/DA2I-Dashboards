

(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date(); a = s.createElement(o),
        m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

// Don't forget to put your own UA-XXXXXXXX-X code
ga('create', 'UA-163732445-1', 'auto');
ga('set', 'anonymizeIp', true);
ga('send', 'pageview');

function newWidth() {
    return Math.round(document.getElementsByClassName('dashboard-container')[0].offsetWidth - window.innerWidth / 10);
}

var lastWidths = {};
var lastCountry = false;

function handleResize() {
    // $('#country-dropdown input').attr('autocomplete', 'off')
    var graphs = document.getElementsByClassName('js-plotly-plot');
    var i;

    if (document.getElementById('country-icon')) {
        if (lastCountry !== document.getElementById('country-icon').src) {
            lastWidths = {}
        }
        lastCountry = document.getElementById('country-icon').src;
    }

    if (document.getElementById('sidebar')) {
        document.getElementById('sidebar').style.top = document.getElementById('navbar').offsetHeight + 'px';
    }
    for (i = 0; i < graphs.length; i++) {
        if (graphs[i].offsetWidth !== newWidth() && lastWidths[i] !== graphs[i].offsetWidth) {
            lastWidths[i] = graphs[i].offsetWidth;
            Plotly.relayout(graphs[i], { width: newWidth() })
        }
    }
}

function blankLinks() {

}

function updateUrl() {
    if (document.getElementById('countrynameWrap') && document.getElementById('pathnameWrap')) {
        var country = document.getElementById('countrynameWrap').textContent;
        var pathname = document.getElementById('pathnameWrap').textContent;
        if (country.length < 5) { return }
        if (!window.location.pathname.toLowerCase().includes(country.replace('+', ' ').toLowerCase())) {
            console.log("updating url")
            var a = pathname.split("/")
            if (a[1].length < 5) {
                a[1] = 'connectivity'
            }
            a[2] = country.replace(" ", "+")
            var newpath = a.join("/")
            window.history.pushState('newpath', 'Title', newpath);
    
        }
    }
    
}

document.addEventListener("DOMContentLoaded", function () {
    var i = 0;
    handleResize();
    updateUrl();
    setInterval(function () {
        handleResize();
        updateUrl()
    }, 1000)


    console.log("COOKIE BANNER LOADED")


});