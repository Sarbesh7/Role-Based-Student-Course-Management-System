// Admin utilities - reuse navbar toggle and modals from student.js baseline
(function () {
  const ready = (fn) =>
    document.readyState !== 'loading'
      ? fn()
      : document.addEventListener('DOMContentLoaded', fn);

  ready(() => {
    // Navbar hamburger toggle
    const toggle = document.querySelector('[data-nav-toggle]');
    const container = document.querySelector('.navbar .nav-container');
    if (toggle && container) {
      const setOpen = (open) => {
        container.setAttribute('data-nav-open', open ? 'true' : 'false');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      };
      let isOpen = false;
      toggle.addEventListener('click', () => { isOpen = !isOpen; setOpen(isOpen); });
      container.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => {
        if (isOpen) { isOpen = false; setOpen(false); }
      }));
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && isOpen) { isOpen = false; setOpen(false); } });
    }
  });
})();
