/* lexa-article.js
   Rend dynamiquement le bloc "Derniers articles" en fin de page article.
   Source de donnees : window.LEXA_ARTICLES (defini dans /assets/lexa-articles.js),
   liste ordonnee du plus recent au plus ancien : { url, title, cat, excerpt }.
   Le bloc s'auto-masque s'il n'y a pas de registre ou aucun autre article. */
(function () {
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  function currentPaths() {
    var p = location.pathname;
    var noIndex = p.replace(/index\.html$/, '');
    var withSlash = noIndex.charAt(noIndex.length - 1) === '/' ? noIndex : noIndex + '/';
    return [p, noIndex, withSlash];
  }

  function render() {
    var sec = document.getElementById('latest-articles');
    var host = document.getElementById('latest-articles-grid');
    if (!sec || !host) return;

    var list = Array.isArray(window.LEXA_ARTICLES) ? window.LEXA_ARTICLES : [];
    var here = currentPaths();
    var current = list.filter(function (a) { return a && a.url && here.indexOf(a.url) !== -1; })[0];
    var curCat = current && current.cat;
    var pool = list.filter(function (a) {
      return a && a.url && here.indexOf(a.url) === -1;
    });

    // Priorite aux articles de la meme rubrique (tri stable : l'ordre de recence est conserve dans chaque groupe)
    if (curCat) {
      pool.sort(function (a, b) {
        return (a.cat === curCat ? 0 : 1) - (b.cat === curCat ? 0 : 1);
      });
    }

    var howMany = parseInt(host.getAttribute('data-count'), 10);
    if (!howMany || howMany < 1) howMany = 3;
    var pick = pool.slice(0, howMany);

    if (!pick.length) { sec.style.display = 'none'; return; }

    var arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 5l7 7-7 7"/></svg>';

    host.innerHTML = pick.map(function (a) {
      return '<a class="la-card" href="' + esc(a.url) + '">' +
        '<span class="la-cat">' + esc(a.cat || 'Article') + '</span>' +
        '<h3>' + esc(a.title) + '</h3>' +
        '<p>' + esc(a.excerpt || '') + '</p>' +
        '<span class="la-more">' + "Lire l'article " + arrow + '</span>' +
        '</a>';
    }).join('');
  }

  if (document.readyState !== 'loading') render();
  else document.addEventListener('DOMContentLoaded', render);
})();
