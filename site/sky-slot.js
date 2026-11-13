/* ORBITRON — the sky slot: a small window into the night sky, under the theme
 * and language switches.
 *
 * A pocket edition of the project's live wallpaper, sky only: nebulae and stars,
 * a few that twinkle, shooting stars, and the three comets (blue, yellow, red)
 * taking turns. No labels, no names, no logo — the slot is a picture, not a text.
 *
 * Light by construction:
 *   - two canvases: the still sky is drawn ONCE (and again only when the slot
 *     changes size); the live one carries only what moves;
 *   - glows are small pre-drawn sprites that are only stamped, never blurred;
 *   - at most 30 frames a second, the pixel ratio capped at 2;
 *   - it stands still when nobody can see it: a hidden tab, the slot scrolled
 *     off screen, or a panel open over the page;
 *   - "reduce motion" in the system gets one still picture and no loop at all;
 *   - it starts only after the page has loaded, so it never delays the first paint.
 *
 * Its own file, so app.js keeps its four jobs. Nothing is fetched, nothing is stored.
 * The slot stays dark in both themes on purpose: a window into space, not a background.
 */
(function () {
  "use strict";

  var slot = document.querySelector(".sky-slot");
  var probe = document.createElement("canvas");
  if (!slot || !probe.getContext) { return; }

  var FPS = 30;
  var SHOOTING_EVERY = 7;   // seconds, on average, between two shooting stars
  var COMET_EVERY = 22;     // seconds, on average, between two comets
  var SPACE = "#020103";

  var still = document.createElement("canvas");
  var live = document.createElement("canvas");
  slot.appendChild(still);
  slot.appendChild(live);
  var sctx = still.getContext("2d", { alpha: false });
  var lctx = live.getContext("2d");

  var W = 0, H = 0, DPR = 1, S = 1;   // size in CSS pixels; S scales the wallpaper's measures
  var twinklers = [], shooting = [], comets = [];
  var nextShoot = 0, nextComet = 0, cometIdx = 0;
  var sprites = {};

  // ---------------------------------------------------------------- helpers

  function rng(seed) {                         // mulberry32: the same sky on every visit
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function rgba(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + (n >> 16 & 255) + "," + (n >> 8 & 255) + "," + (n & 255) + "," + a + ")";
  }
  function expo(mean) { return -Math.log(1 - Math.random()) * mean; }   // random gaps around a mean

  function glowSprite(hex, size) {             // a glow drawn once, then only stamped
    var key = hex + size;
    if (sprites[key]) { return sprites[key]; }
    var c = document.createElement("canvas");
    c.width = c.height = size;
    var g = c.getContext("2d"), r = size / 2;
    var grd = g.createRadialGradient(r, r, 0, r, r, r);
    grd.addColorStop(0, rgba(hex, 1)); grd.addColorStop(0.18, rgba(hex, 0.55));
    grd.addColorStop(0.45, rgba(hex, 0.12)); grd.addColorStop(1, rgba(hex, 0));
    g.fillStyle = grd; g.fillRect(0, 0, size, size);
    return (sprites[key] = c);
  }
  function stamp(ctx, sprite, x, y, d, a) {
    ctx.globalAlpha = a; ctx.drawImage(sprite, x - d / 2, y - d / 2, d, d); ctx.globalAlpha = 1;
  }

  // ---------------------------------------------------------------- the still sky

  function drawStill() {
    var ctx = sctx, R = rng(1957), i, x, y;
    twinklers = [];

    ctx.fillStyle = SPACE; ctx.fillRect(0, 0, W, H);
    function nebula(nx, ny, rad, hex, a) {
      var g = ctx.createRadialGradient(nx, ny, 0, nx, ny, rad);
      g.addColorStop(0, rgba(hex, a)); g.addColorStop(1, rgba(hex, 0));
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    nebula(W * 0.10, H * 1.1, W * 0.55, "#5a2d91", 0.22);
    nebula(W * 1.00, H * 0.05, W * 0.50, "#1f6b5a", 0.16);
    nebula(W * 0.92, H * 1.0, W * 0.40, "#7a4a1a", 0.16);
    nebula(W * 0.18, H * 0.35, W * 0.22, "#ff3b2f", 0.08);

    var n = Math.round(W * H / 300);
    for (i = 0; i < n; i++) {
      x = R() * W; y = R() * H;
      var big = R() < 0.07;
      var rad = big ? 0.9 + R() * 0.8 : 0.3 + R() * 0.6;
      var a = big ? 0.75 + R() * 0.25 : 0.25 + R() * 0.55;
      ctx.fillStyle = "rgba(" + (235 + R() * 20 | 0) + "," + (232 + R() * 23 | 0) + ",255," + a + ")";
      ctx.beginPath(); ctx.arc(x, y, rad, 0, 6.2832); ctx.fill();
      if (big && R() < 0.5) { twinklers.push({ x: x, y: y, d: 10, hex: "#ffffff", a: 0.55, w: 0.6 + R() * 1.6, p: R() * 6.28 }); }
    }
    for (i = 0; i < 5; i++) { stamp(ctx, glowSprite("#c9c0e8", 64), R() * W, R() * H, 12 + R() * 16, 0.10); }
    var dwarfs = Math.max(2, Math.round(W * H / 9000));
    for (i = 0; i < dwarfs; i++) {                // red dwarfs, in the colour of the first orbit
      x = R() * W; y = R() * H;
      stamp(ctx, glowSprite("#ff3b2f", 64), x, y, 12, 0.7);
      ctx.fillStyle = "#ffd0c8"; ctx.beginPath(); ctx.arc(x, y, 0.9, 0, 6.2832); ctx.fill();
      twinklers.push({ x: x, y: y, d: 15, hex: "#ff3b2f", a: 0.7, w: 0.5 + R() * 1.4, p: R() * 6.28 });
    }
  }

  // ---------------------------------------------------------------- what moves

  var SHOOT_COLOURS = ["#ffffff", "#cfe3ff", "#ffe2c2", "#d9ccff", "#ff3b2f"];
  var COMET_TYPES = [
    { hex: "#9fe8ff", ion: "#bfe6ff" },        // blue, the first
    { hex: "#ffd84a", ion: "#fff1a8" },        // yellow
    { hex: "#ff3b2f", ion: "#ff6a5c" }         // red
  ];

  function spawnShooting(t) {
    var R = Math.random, goLeft = R() < 0.5;
    var ang = (goLeft ? 200 + R() * 30 : 310 + R() * 30) * Math.PI / 180;
    var speed = (300 + R() * 190) * S;
    shooting.push({
      x: W * (goLeft ? 0.35 + R() * 0.65 : R() * 0.65), y: H * (-0.05 + R() * 0.4),
      vx: Math.cos(ang) * speed, vy: Math.abs(Math.sin(ang)) * speed,
      len: (130 + R() * 110) * S, born: t, life: 1.6 + R() * 0.8,
      hex: SHOOT_COLOURS[R() * SHOOT_COLOURS.length | 0]
    });
  }

  function spawnComet(t) {
    var R = Math.random, fromLeft = R() < 0.5;
    var type = COMET_TYPES[cometIdx++ % COMET_TYPES.length];
    var speed = (55 + R() * 45) * S;
    var ang = (fromLeft ? 8 + R() * 14 : 172 - R() * 14) * Math.PI / 180;
    comets.push({
      x: fromLeft ? -10 : W + 10, y: H * (0.1 + R() * 0.45),
      vx: Math.cos(ang) * speed, vy: Math.sin(ang) * speed,
      len: (320 + R() * 200) * S, born: t, hex: type.hex, ion: type.ion
    });
  }

  function drawShooting(ctx, s, t) {
    var age = t - s.born, k = age / s.life;
    if (k >= 1) { return false; }
    var a = k < 0.12 ? k / 0.12 : 1 - Math.max(0, (k - 0.55) / 0.45);   // fade in, fade out
    var x = s.x + s.vx * age, y = s.y + s.vy * age;
    var sp = Math.hypot(s.vx, s.vy), tx = x - s.vx / sp * s.len, ty = y - s.vy / sp * s.len;
    var g = ctx.createLinearGradient(x, y, tx, ty);
    g.addColorStop(0, rgba(s.hex, 0.22 * a)); g.addColorStop(1, rgba(s.hex, 0));
    ctx.strokeStyle = g; ctx.lineWidth = 3.5; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(tx, ty); ctx.stroke();
    g = ctx.createLinearGradient(x, y, tx, ty);
    g.addColorStop(0, rgba(s.hex, 0.95 * a)); g.addColorStop(1, rgba(s.hex, 0));
    ctx.strokeStyle = g; ctx.lineWidth = 1.1;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(tx, ty); ctx.stroke();
    stamp(ctx, glowSprite(s.hex, 64), x, y, 12, a);
    return true;
  }

  function drawComet(ctx, c, t) {
    var age = t - c.born;
    var x = c.x + c.vx * age, y = c.y + c.vy * age;
    if (x < -c.len * 1.3 || x > W + c.len * 1.3 || y > H + c.len) { return false; }
    var sp = Math.hypot(c.vx, c.vy), ux = c.vx / sp, uy = c.vy / sp, nx = -uy, ny = ux;
    var tx = x - ux * c.len, ty = y - uy * c.len;
    var g = ctx.createLinearGradient(x, y, tx, ty);          // the dust tail: a widening wedge
    g.addColorStop(0, rgba(c.hex, 0.5)); g.addColorStop(0.35, rgba(c.hex, 0.16)); g.addColorStop(1, rgba(c.hex, 0));
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.moveTo(x + nx * 7 * S, y + ny * 7 * S);
    ctx.lineTo(tx + nx * 38 * S, ty + ny * 38 * S);
    ctx.lineTo(tx - nx * 16 * S, ty - ny * 16 * S);
    ctx.lineTo(x - nx * 7 * S, y - ny * 7 * S);
    ctx.closePath(); ctx.fill();
    var ex = x - ux * c.len * 1.3, ey = y - uy * c.len * 1.3;   // the ion tail: one thin straight line
    var g2 = ctx.createLinearGradient(x, y, ex, ey);
    g2.addColorStop(0, rgba(c.ion, 0.45)); g2.addColorStop(1, rgba(c.ion, 0));
    ctx.strokeStyle = g2; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(ex - nx * 6 * S, ey - ny * 6 * S); ctx.stroke();
    stamp(ctx, glowSprite(c.hex, 128), x, y, 78 * S, 0.95);
    ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.arc(x, y, 3.8 * S + 0.6, 0, 6.2832); ctx.fill();
    return true;
  }

  function drawLive(t) {
    var ctx = lctx, i;
    ctx.clearRect(0, 0, W, H);
    for (i = 0; i < twinklers.length; i++) {
      var s = twinklers[i], a = s.a * (0.5 + 0.5 * Math.sin(t * s.w + s.p));
      if (a > 0.03) { stamp(ctx, glowSprite(s.hex, 64), s.x, s.y, s.d, a); }
    }
    if (t >= nextShoot) { spawnShooting(t); nextShoot = t + 2 + expo(SHOOTING_EVERY); }
    shooting = shooting.filter(function (sh) { return drawShooting(ctx, sh, t); });
    if (t >= nextComet && comets.length < 2) { spawnComet(t); nextComet = t + 8 + expo(COMET_EVERY); }
    comets = comets.filter(function (c) { return drawComet(ctx, c, t); });
  }

  // ---------------------------------------------------------------- size

  function resize() {
    var r = slot.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) { return false; }
    W = r.width; H = r.height;
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    S = H / 360;                                // the wallpaper's measures, fitted to a slot
    [still, live].forEach(function (c) { c.width = Math.round(W * DPR); c.height = Math.round(H * DPR); });
    sctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    lctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    drawStill();
    return true;
  }

  // ---------------------------------------------------------------- when it runs

  var calm = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;
  var inView = true, running = false, last = 0;

  function shouldRun() {
    return inView && !document.hidden && !(calm && calm.matches) &&
      !document.documentElement.classList.contains("locked");
  }
  function loop(now) {
    if (!running) { return; }
    requestAnimationFrame(loop);
    if (now - last < 1000 / FPS - 1) { return; }
    last = now;
    drawLive(now / 1000);
  }
  function wake() {
    var should = shouldRun();
    if (should && !running) { running = true; requestAnimationFrame(loop); }
    else if (!should && running) { running = false; }
    if (!should && calm && calm.matches) { drawLive(0); }   // one still picture, twinkles frozen
  }

  function start() {
    if (!resize()) { return; }
    var t = performance.now() / 1000;
    nextShoot = t + 1.5;                        // a visitor sees something move early
    nextComet = t + 4;
    drawLive(t);

    document.addEventListener("visibilitychange", wake);
    new MutationObserver(wake).observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });
    if (calm) {
      if (calm.addEventListener) { calm.addEventListener("change", wake); }
      else if (calm.addListener) { calm.addListener(wake); }
    }
    if (window.IntersectionObserver) {
      new IntersectionObserver(function (entries) {
        inView = entries[entries.length - 1].isIntersecting;
        wake();
      }).observe(slot);
    }
    var pending = null;
    function later() { clearTimeout(pending); pending = setTimeout(function () { resize(); wake(); }, 200); }
    if (window.ResizeObserver) { new ResizeObserver(later).observe(slot); }
    else { window.addEventListener("resize", later); }
    wake();
  }

  if (document.readyState === "complete") { start(); }
  else { window.addEventListener("load", start); }
}());
