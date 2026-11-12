/* ORBITRON — the public page, its one script.
 *
 * Four jobs and nothing else:
 *   1. the language switch — English is the page's own text, Bulgarian comes from i18n/bg.json;
 *   2. the numbers — drawn from data/*.json, which the build copies from the repository root;
 *   3. the panels — a tile opens its panel full-screen at its own address (#report, #chain …);
 *   4. the sky — a field of stars, drawn once.
 *
 * No framework, no third-party request, no cookie. A choice of language is remembered in
 * the reader's own browser when the browser allows it, and forgotten when it does not.
 */
(function () {
  "use strict";

  var LANGS = ["en", "bg"];
  var STORE = "orbitron.lang";
  var english = {};          // key -> the page's own English text, read from the DOM once
  var bulgarian = null;      // key -> Bulgarian text, loaded on first need
  var data = null;           // board, chain, patterns, site
  var current = "en";

  // ---------------------------------------------------------------- text

  function remember(el, attr, key) {
    if (english[key] === undefined) {
      english[key] = attr ? el.getAttribute(attr) || "" : el.textContent;
    }
  }

  function collectEnglish() {
    document.querySelectorAll("[data-i18n]").forEach(function (el) { remember(el, null, el.dataset.i18n); });
    document.querySelectorAll("[data-i18n-content]").forEach(function (el) { remember(el, "content", el.dataset.i18nContent); });
    document.querySelectorAll("[data-i18n-alt]").forEach(function (el) { remember(el, "alt", el.dataset.i18nAlt); });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) { remember(el, "aria-label", el.dataset.i18nAria); });
  }

  /** The text of a key in the current language, with {vars} filled in. */
  function t(key, vars) {
    var text = current === "bg" && bulgarian && bulgarian[key] !== undefined ? bulgarian[key] : english[key];
    if (text === undefined) { text = key; }
    if (vars) {
      text = text.replace(/\{(\w+)\}/g, function (all, name) {
        return vars[name] !== undefined ? String(vars[name]) : all;
      });
    }
    return text;
  }

  var vars = {};             // values for elements marked data-vars, keyed by their i18n key

  function applyText() {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(el.dataset.i18n, vars[el.dataset.i18n]);
    });
    document.querySelectorAll("[data-i18n-content]").forEach(function (el) {
      el.setAttribute("content", t(el.dataset.i18nContent));
    });
    document.querySelectorAll("[data-i18n-alt]").forEach(function (el) {
      el.setAttribute("alt", t(el.dataset.i18nAlt));
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      el.setAttribute("aria-label", t(el.dataset.i18nAria, vars[el.dataset.i18nAria]));
    });
    document.documentElement.lang = current;
    document.querySelectorAll(".lang button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.lang === current));
    });
  }

  function loadBulgarian() {
    if (bulgarian) { return Promise.resolve(); }
    return fetch("i18n/bg.json").then(function (r) {
      if (!r.ok) { throw new Error("bg.json " + r.status); }
      return r.json();
    }).then(function (json) { bulgarian = json; });
  }

  function setLang(lang, save) {
    if (LANGS.indexOf(lang) < 0) { lang = "en"; }
    var ready = lang === "bg" ? loadBulgarian() : Promise.resolve();
    return ready.then(function () {
      current = lang;
      applyText();
      render();
      if (save) {
        try { localStorage.setItem(STORE, lang); } catch (e) { /* private window: forget it */ }
      }
    }).catch(function () {
      current = "en";       // a missing translation never leaves the page blank
      applyText();
      render();
    });
  }

  function chosenLang() {
    var asked = new URLSearchParams(location.search).get("lang");
    if (asked && LANGS.indexOf(asked) >= 0) { return asked; }
    try {
      var kept = localStorage.getItem(STORE);
      if (kept && LANGS.indexOf(kept) >= 0) { return kept; }
    } catch (e) { /* no storage — fall through */ }
    var langs = navigator.languages || [navigator.language || "en"];
    return langs.some(function (l) { return /^bg\b/i.test(l); }) ? "bg" : "en";
  }

  // ---------------------------------------------------------------- numbers

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) { node.className = cls; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }

  function renderBoard(board) {
    document.querySelectorAll("[data-board]").forEach(function (node) {
      var value = board[node.dataset.board];
      node.textContent = value === undefined ? "—" : String(value);
    });
    document.querySelectorAll(".rail").forEach(function (rail) {
      rail.textContent = "";
      [["working", "var(--green)"], ["decisions", "var(--decided)"], ["partial", "var(--partial)"], ["not_built", "var(--notbuilt)"]]
        .forEach(function (pair) {
          var share = (board[pair[0]] || 0) / board.total_rows * 100;
          if (share > 0) {
            var bit = el("span");
            bit.style.width = share.toFixed(2) + "%";
            bit.style.background = pair[1];
            rail.appendChild(bit);
          }
        });
    });
    vars["build.note"] = { date: board.generated, total: board.total_rows };
    vars["build.rail"] = { working: board.working, partial: board.partial, not_built: board.not_built, total: board.total_rows };
  }

  function renderChain(chain, lines) {
    var box = document.getElementById("pillars");
    box.textContent = "";
    chain.pillars.forEach(function (pillar) {
      var card = el("article", "pillar");
      card.appendChild(el("span", "pn", pillar.name));
      card.appendChild(el("span", "pe", pillar.epithet));
      var line = current === "bg" && bulgarian ? bulgarian["pillar." + pillar.name] : lines[pillar.name];
      card.appendChild(el("span", "pl", line || ""));
      var list = el("ol");
      pillar.processes.forEach(function (p) {
        var li = el("li");
        li.appendChild(el("b", "", p.name));
        li.appendChild(el("span", "", p.designation));
        list.appendChild(li);
      });
      card.appendChild(list);
      box.appendChild(card);
    });

    var stages = document.getElementById("stages");
    stages.textContent = "";
    chain.stages.forEach(function (name, i) {
      var li = el("li");
      li.style.setProperty("--c", "var(--stage-" + (i + 1) + ")");
      li.appendChild(el("span", "sn", String(i + 1)));
      li.appendChild(el("span", "st", name));
      stages.appendChild(li);
    });
  }

  function renderMini(chain, patterns) {
    var names = document.getElementById("mini-chain");
    names.textContent = "";
    chain.pillars.forEach(function (pillar, i) {
      if (i) { names.appendChild(el("span", "arrow", "▸")); }
      names.appendChild(el("span", "", pillar.name));
    });
    var orbs = document.getElementById("mini-planets");
    orbs.textContent = "";
    patterns.patterns.forEach(function (p) {
      var built = p.version && p.version !== "—";
      var orb = el("span", "orb" + (built ? " live" : ""));
      orb.title = p.name + (built ? " " + p.version : "");
      orbs.appendChild(orb);
    });
  }

  function renderPatterns(patterns) {
    var box = document.getElementById("planets");
    box.textContent = "";
    patterns.patterns.forEach(function (p) {
      var built = p.version && p.version !== "—";
      var li = el("li", built ? "live" : "");
      li.appendChild(el("span", "orb"));
      li.appendChild(el("span", "pname", p.name));
      li.appendChild(el("span", "pver", built ? p.version : t("patterns.none")));
      box.appendChild(li);
    });
  }

  function renderFollow(links) {
    links = links || [];
    document.querySelectorAll(".follow").forEach(function (box) {
      box.querySelectorAll("a").forEach(function (a) { a.remove(); });
      links.forEach(function (link) {
        var a = el("a", "", link.name);
        a.href = link.url;
        a.rel = "me noopener";
        box.appendChild(a);
      });
      box.hidden = !links.length;
    });
    var bar = document.getElementById("follow-bar");
    bar.textContent = "";
    links.forEach(function (link) {
      var a = el("a");
      a.href = link.url;
      a.rel = "me noopener";
      a.appendChild(el("span", "", link.name));
      bar.appendChild(a);
    });
  }

  function render() {
    if (!data) { return; }
    renderBoard(data.board);
    renderChain(data.chain, data.site.pillar_lines);
    renderPatterns(data.patterns);
    renderMini(data.chain, data.patterns);
    renderFollow(data.site.follow);
    // The two elements whose text carries numbers are filled once the numbers are known.
    ["build.note"].forEach(function (key) {
      document.querySelectorAll('[data-i18n="' + key + '"]').forEach(function (n) { n.textContent = t(key, vars[key]); });
    });
    document.querySelectorAll(".rail").forEach(function (rail) {
      rail.setAttribute("aria-label", t("build.rail", vars["build.rail"]));
    });
  }

  function loadData() {
    var names = ["board", "chain", "patterns", "site"];
    return Promise.all(names.map(function (n) {
      return fetch("data/" + n + ".json").then(function (r) {
        if (!r.ok) { throw new Error(n + ".json " + r.status); }
        return r.json();
      });
    })).then(function (all) {
      data = { board: all[0], chain: all[1], patterns: all[2], site: all[3] };
    });
  }

  // ---------------------------------------------------------------- panels

  var PANELS = ["report", "idea", "archive", "build", "chain", "method", "disclaimer"];
  var opener = null;        // the tile that opened the panel, to give focus back to
  var fromHere = false;     // the panel was opened on this page, so "back" closes it

  function setInert(on) {
    ["app"].forEach(function (id) {
      var node = document.getElementById(id);
      if (node) { node.inert = on; }
    });
  }

  function route() {
    var id = location.hash.slice(1);
    var panel = PANELS.indexOf(id) >= 0 ? document.getElementById(id) : null;
    document.querySelectorAll(".panel.open").forEach(function (p) { if (p !== panel) { p.classList.remove("open"); } });
    if (panel) {
      panel.classList.add("open");
      panel.scrollTop = 0;
      document.documentElement.classList.add("locked");
      setInert(true);
      var close = panel.querySelector(".close");
      if (close) { close.focus({ preventScroll: true }); }
    } else {
      document.documentElement.classList.remove("locked");
      setInert(false);
      fromHere = false;
      if (opener) { opener.focus({ preventScroll: true }); opener = null; }
    }
  }

  function openPanel(id, tile) {
    opener = tile || null;
    fromHere = true;
    history.pushState(null, "", "#" + id);
    route();
  }

  function closePanel() {
    if (fromHere) { history.back(); return; }        // popstate routes it
    history.replaceState(null, "", location.pathname + location.search);
    route();
  }

  function wirePanels() {
    document.querySelectorAll("a.report, a.warn, a.item").forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href").slice(1);
        if (PANELS.indexOf(id) < 0 || e.metaKey || e.ctrlKey || e.shiftKey) { return; }
        e.preventDefault();
        openPanel(id, a);
      });
    });
    document.querySelectorAll(".panel .close").forEach(function (a) {
      a.addEventListener("click", function (e) { e.preventDefault(); closePanel(); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.querySelector(".panel.open")) { closePanel(); }
    });
    window.addEventListener("popstate", route);
    window.addEventListener("hashchange", route);
    route();
  }

  // ---------------------------------------------------------------- sky

  function drawSky() {
    var seed = 20260910;                       // the day the public vault was born
    function rand() { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }
    var w = Math.max(window.innerWidth, 1200), h = Math.max(window.innerHeight, 900) * 2;
    var stars = [];
    for (var i = 0; i < 160; i++) {
      var x = Math.round(rand() * w), y = Math.round(rand() * h);
      var a = (0.25 + rand() * 0.6).toFixed(2);
      stars.push(x + "px " + y + "px 0 " + (rand() > 0.92 ? "1px" : "0") + " rgba(255,255,255," + a + ")");
    }
    var sky = document.querySelector(".sky");
    if (sky) { sky.style.setProperty("--stars", stars.join(",")); }
  }

  // ---------------------------------------------------------------- start

  document.addEventListener("DOMContentLoaded", function () {
    collectEnglish();
    if (!window.matchMedia || !window.matchMedia("(prefers-color-scheme: light)").matches) { drawSky(); }
    document.querySelectorAll(".lang button").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.dataset.lang, true); });
    });
    wirePanels();
    loadData().catch(function () { data = null; }).then(function () { return setLang(chosenLang(), false); });
  });
}());
