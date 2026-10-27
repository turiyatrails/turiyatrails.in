/* Turiya Trails — small, dependency-free behaviour for every page. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove('no-js');

  var header = document.querySelector('.site-header');
  var floatBtn = document.querySelector('.wa-float');

  // Header turns solid once the page has scrolled.
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('is-solid', y > 40);
    if (floatBtn) floatBtn.classList.toggle('is-visible', y > window.innerHeight * 0.7);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu.
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('mobile-menu');
  function setMenu(open) {
    document.body.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.label').textContent = open ? 'Close' : 'Menu';
    menu.setAttribute('aria-hidden', String(!open));
    if (open) {
      menu.removeAttribute('inert');
      var first = menu.querySelector('a');
      if (first) first.focus();
    } else {
      menu.setAttribute('inert', '');
    }
  }
  if (toggle && menu) {
    menu.setAttribute('inert', '');
    toggle.addEventListener('click', function () {
      setMenu(!document.body.classList.contains('menu-open'));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) {
        setMenu(false);
        toggle.focus();
      }
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
  }

  // Gentle reveal on scroll.
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && items.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px 10% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Enquiry form: builds a WhatsApp message. Nothing is stored or sent anywhere else.
  var form = document.getElementById('enquiry-form');
  if (form) {
    var params = new URLSearchParams(window.location.search);
    var preset = params.get('journey');
    if (preset && form.interest) {
      Array.prototype.forEach.call(form.interest.options, function (o) {
        if (o.value === preset || o.dataset.slug === preset) o.selected = true;
      });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var lines = ['Namaste Turiya Trails,'];
      var name = f.name.value.trim();
      if (name) lines.push('I am ' + name + '.');
      if (f.interest.value) lines.push('I am interested in: ' + f.interest.value + '.');
      if (f.dates.value.trim()) lines.push('Approximate dates: ' + f.dates.value.trim() + '.');
      if (f.people.value) lines.push('Number of people: ' + f.people.value + '.');
      if (f.message.value.trim()) lines.push('', f.message.value.trim());
      var text = lines.join('\n');
      var url = 'https://wa.me/' + form.dataset.phone + '?text=' + encodeURIComponent(text);
      window.open(url, '_blank', 'noopener');
    });
  }
})();
