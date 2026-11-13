/* SalesTrack — site interactions (no dependencies) */
(function () {
  "use strict";
  var EMAIL = "info@salestrack.co.in";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header shadow + back-to-top */
  var header = $(".site-header");
  var toTop = $(".to-top");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-scrolled", y > 8);
    if (toTop) toTop.classList.toggle("show", y > 700);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" }); });

  /* Mobile menu */
  var toggle = $(".menu-toggle");
  var menu = $("#nav-menu");
  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
  }
  if (toggle) toggle.addEventListener("click", function () { setMenu(toggle.getAttribute("aria-expanded") !== "true"); });
  $$("#nav-menu a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
  window.addEventListener("resize", function () { if (window.innerWidth > 960) setMenu(false); });

  /* Services dropdown (hover on desktop, click everywhere, keyboard friendly) */
  $$(".nav-item.has-dropdown").forEach(function (item) {
    var btn = $(".nav-link", item);
    var hoverable = window.matchMedia("(hover: hover) and (min-width: 961px)");
    function set(open) { item.classList.toggle("open", open); btn.setAttribute("aria-expanded", String(open)); }
    btn.addEventListener("click", function (e) { e.preventDefault(); set(!item.classList.contains("open")); });
    item.addEventListener("mouseenter", function () { if (hoverable.matches) set(true); });
    item.addEventListener("mouseleave", function () { if (hoverable.matches) set(false); });
    item.addEventListener("focusout", function (e) { if (!item.contains(e.relatedTarget)) set(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { set(false); setMenu(false); } });
    document.addEventListener("click", function (e) { if (!item.contains(e.target)) set(false); });
  });

  /* Pipeline: size the travelling signal to the list height */
  var steps = $(".steps");
  function sizeTravel() { if (steps) steps.style.setProperty("--travel", (steps.offsetHeight - 50) + "px"); }
  sizeTravel(); window.addEventListener("resize", sizeTravel);

  /* Scroll reveal — items already on screen stay visible; only lower ones animate in */
  if ("IntersectionObserver" in window && !reduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove("pending"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el, i) {
      if (el.getBoundingClientRect().top > window.innerHeight) {
        el.classList.add("pending");
        el.style.transitionDelay = ((el.dataset.delay || 0) * 80) + "ms";
        io.observe(el);
      }
    });
    setTimeout(function () { $$(".reveal.pending").forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) el.classList.remove("pending"); }); }, 2500);
  }

  /* Services page: tab scroll-spy */
  var tabs = $$(".svc-tabs a");
  if (tabs.length && "IntersectionObserver" in window) {
    var map = {};
    tabs.forEach(function (t) { map[t.getAttribute("href").slice(1)] = t; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tabs.forEach(function (t) { t.classList.remove("active"); t.removeAttribute("aria-current"); });
          var t = map[en.target.id];
          if (t) { t.classList.add("active"); t.setAttribute("aria-current", "true"); t.scrollIntoView({ block: "nearest", inline: "center", behavior: "auto" }); }
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    $$(".svc").forEach(function (s) { spy.observe(s); });
  }

  /* Working hours — Mon–Fri 14:30–23:00 IST (UTC+5:30, no DST) */
  var OPEN_MIN = 14 * 60 + 30, CLOSE_MIN = 23 * 60;
  function istNow() {
    var now = new Date();
    var ist = new Date(now.getTime() + (now.getTimezoneOffset() + 330) * 60000);
    return ist;
  }
  function isOpen(ist) {
    var d = ist.getDay(), m = ist.getHours() * 60 + ist.getMinutes();
    return d >= 1 && d <= 5 && m >= OPEN_MIN && m < CLOSE_MIN;
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function fmt12(h, m) { var ap = h >= 12 ? "PM" : "AM"; var hh = h % 12 || 12; return hh + ":" + pad(m) + " " + ap; }
  function renderHours() {
    var ist = istNow(), open = isOpen(ist);
    $$("[data-status]").forEach(function (el) {
      el.classList.toggle("open", open);
      var t = $("[data-status-text]", el) || el;
      t.textContent = open ? "Our team is available now" : "Currently outside working hours";
    });
    $$("[data-ist-clock]").forEach(function (el) {
      el.innerHTML = fmt12(ist.getHours(), ist.getMinutes()) + "<small>IST</small>";
    });
    var today = ist.getDay();
    $$(".week li").forEach(function (li) { li.classList.toggle("today", Number(li.dataset.day) === today); });
  }
  if ($("[data-status]") || $("[data-ist-clock]")) { renderHours(); setInterval(renderHours, 30000); }

  /* Show the working hours in the visitor's own time zone */
  var local = $("[data-local-hours]");
  if (local) {
    try {
      var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
      if (tz && tz !== "Asia/Calcutta" && tz !== "Asia/Kolkata") {
        var base = new Date(); // next weekday so DST matches the visitor's current offset
        var openUTC = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth(), base.getUTCDate(), 9, 0));
        var closeUTC = new Date(Date.UTC(base.getUTCFullYear(), base.getUTCMonth(), base.getUTCDate(), 17, 30));
        var f = new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" });
        var city = tz.split("/").pop().replace(/_/g, " ");
        local.innerHTML = "That's <b>" + f.format(openUTC) + " – " + f.format(closeUTC) + "</b> your time (" + city + ").";
        local.hidden = false;
      }
    } catch (e) { /* leave hidden */ }
  }

  /* Copy email */
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var label = $("span", btn);
      function done(msg) { if (label) { var old = label.textContent; label.textContent = msg; setTimeout(function () { label.textContent = old; }, 1800); } }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, function () { selectText(btn); done("Select & copy"); });
      } else { selectText(btn); done("Select & copy"); }
    });
  });
  function selectText(btn) {
    var target = btn.parentNode.querySelector("a");
    if (!target || !window.getSelection) return;
    var r = document.createRange(); r.selectNodeContents(target);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  /* Contact form: validation + pre-filled email */
  var form = $("#enquiry-form");
  if (form) {
    var params = new URLSearchParams(window.location.search);
    var pre = params.get("service");
    if (pre && form.service) {
      Array.prototype.forEach.call(form.service.options, function (o) { if (o.value === pre) form.service.value = pre; });
    }
    /* Validation helpers */
    var URL_RE = /(https?:\/\/|ftp:\/\/|www\.|\b[a-z0-9-]+(\.[a-z0-9-]+)*\.(com|net|org|in|co|io|ai|uk|us|info|biz|xyz|online|site|store|shop|app|dev|me|ly|tv|gg|link|click|top|club|live|pro|tech|cloud|digital|agency|blog|website|space|today)\b)/i;
    var hasLink = function (v) { return URL_RE.test(v); };
    var clean = function (v) { return v.replace(/\s+/g, " ").trim(); };
    var NO_LINK = "Please remove website links. They aren't allowed in this form.";
    var rules = {
      name: function (v) {
        v = clean(v);
        if (!v) return "Please enter your full name.";
        if (hasLink(v)) return NO_LINK;
        if (!/^[A-Za-z]+(?: [A-Za-z]+)*$/.test(v)) return "Use English letters (A–Z) and spaces only. No numbers or symbols.";
        if (v.replace(/ /g, "").length < 2) return "Please enter your full name.";
        return true;
      },
      email: function (v) {
        v = v.trim();
        if (!v) return "Please enter your email address.";
        if (/^https?:|^www\./i.test(v)) return NO_LINK;
        if (/^[0-9+\s-]+$/.test(v)) return "That looks like a number. Please enter an email address, like name@company.com.";
        if (v.length > 100 || !/^[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9_%+-])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,24}$/.test(v) || /\.\./.test(v))
          return "Please enter a valid email address, like name@company.com.";
        return true;
      },
      phone: function (v) {
        v = v.trim();
        if (!v) return "Please enter your phone number.";
        if (hasLink(v)) return NO_LINK;
        if (!/^\+?[0-9\s\-()]+$/.test(v) || (v.match(/\+/g) || []).length > 1) return "Use digits only, with an optional + at the start (spaces, - and brackets are fine).";
        var digits = v.replace(/\D/g, "");
        if (digits.length < 10 || digits.length > 15) return "Please enter a valid phone number with 10–15 digits, including the country or area code.";
        if (/^(\d)\1+$/.test(digits)) return "Please enter a real phone number.";
        return true;
      },
      company: function (v) {
        v = clean(v);
        if (!v) return "Please enter your company name.";
        if (hasLink(v)) return NO_LINK;
        if (!/^[A-Za-z0-9][A-Za-z0-9 &.,'()\/-]*$/.test(v) || !/[A-Za-z]/.test(v)) return "Use English letters, numbers, spaces and & . , ' - ( ) / only.";
        if (v.length < 2) return "Please enter your company name.";
        return true;
      },
      service: function (v) { return !!v || "Please choose the service you're interested in."; },
      message: function (v) {
        v = v.trim();
        if (!v) return "Please tell us how we can help.";
        if (hasLink(v)) return NO_LINK;
        if (v.length < 15) return "Tell us a little more (at least 15 characters).";
        if (v.length > 2000) return "Please keep your message under 2,000 characters.";
        return true;
      },
      consent: function (v, el) { return el.checked || "Please tick this box so we can use your details to reply."; }
    };
    function check(name) {
      var el = form.elements[name]; if (!el) return true;
      var res = rules[name](el.value, el);
      var field = el.closest(".field") || el.closest(".consent");
      var err = field && $(".err", field.parentNode.classList.contains("field") ? field.parentNode : field);
      var ok = res === true;
      if (field) field.classList.toggle("invalid", !ok);
      el.setAttribute("aria-invalid", String(!ok));
      var errEl = $("#" + name + "-err");
      if (errEl) errEl.textContent = ok ? "" : res;
      return ok;
    }
    Object.keys(rules).forEach(function (n) {
      var el = form.elements[n]; if (!el) return;
      el.addEventListener("blur", function () { if (el.value || el.type === "checkbox" || el.dataset.touched) check(n); });
      el.addEventListener("input", function () { el.dataset.touched = "1"; });
      el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") check(n); });
      el.addEventListener("change", function () { if (el.getAttribute("aria-invalid") === "true") check(n); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      Object.keys(rules).forEach(function (n) { if (!check(n) && !firstBad) firstBad = form.elements[n]; });
      if (firstBad) { firstBad.focus(); return; }
      var d = function (n) { var v = (form.elements[n] && form.elements[n].value || ""); return n === "message" ? v.trim() : v.replace(/\s+/g, " ").trim(); };
      var subject = "Enquiry: " + d("service") + " — " + d("name") + (d("company") ? " (" + d("company") + ")" : "");
      var body = [
        "Name: " + d("name"),
        "Email: " + d("email"),
        "Phone: " + d("phone"),
        "Company: " + d("company"),
        "Service of interest: " + d("service"),
        "",
        d("message"),
        "",
        "---",
        "Consent: I consent to SalesTrack using my details to respond to this enquiry, as described in the Privacy Notice (version 2, 13 November 2026).",
        "Marketing updates: " + (form.elements.marketing && form.elements.marketing.checked ? "Yes, I opted in" : "No"),
        "Consent given: " + new Date().toISOString()
      ].join("\n");
      var href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      var status = $("#form-status");
      if (status) {
        status.innerHTML = "<p>Your email app should open with your enquiry ready to send.</p><p>If it doesn't, email us directly at <strong>" + EMAIL + "</strong>.</p>";
        status.classList.add("show");
      }
      window.location.href = href;
    });
  }

  /* Footer year */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
