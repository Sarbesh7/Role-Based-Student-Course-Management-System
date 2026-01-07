// Lightweight UI utilities for student pages
// - Ripple on buttons
// - Focus styling for form fields
// - Modal confirm helper
// - Toast notifications

(function () {
  const ready = (fn) =>
    document.readyState !== 'loading'
      ? fn()
      : document.addEventListener('DOMContentLoaded', fn);

  function addRipple(el) {
    el.classList.add('ripple-container');
    el.addEventListener('click', function (e) {
      const rect = el.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      ripple.className = 'ripple';
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = e.clientX - rect.left - size / 2 + 'px';
      ripple.style.top = e.clientY - rect.top - size / 2 + 'px';
      el.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  }

  function wireRipples() {
    document.querySelectorAll('.btn, [data-ripple="true"]').forEach(addRipple);
  }

  function wireFormFocus() {
    const selector = '.form-field input, .form-field select, .form-field textarea';
    document.addEventListener('focusin', (e) => {
      if (e.target.matches(selector)) {
        e.target.closest('.form-field')?.classList.add('is-focused');
      }
    });
    document.addEventListener('focusout', (e) => {
      if (e.target.matches(selector)) {
        e.target.closest('.form-field')?.classList.remove('is-focused');
      }
    });
  }

  function createModal({ title = 'Confirm', message = '', confirmText = 'Confirm', cancelText = 'Cancel', onConfirm }) {
    const backdrop = document.createElement('div');
    backdrop.className = 'modal-backdrop';
    backdrop.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true">
        <h3>${title}</h3>
        <p>${message}</p>
        <div class="actions">
          <button class="btn btn-outline" data-modal-cancel>${cancelText}</button>
          <button class="btn btn-danger" data-modal-confirm>${confirmText}</button>
        </div>
      </div>
    `;
    function close() { backdrop.remove(); document.removeEventListener('keydown', onKey); }
    function onKey(e) { if (e.key === 'Escape') close(); }
    backdrop.addEventListener('click', (e) => { if (e.target === backdrop) close(); });
    backdrop.querySelector('[data-modal-cancel]')?.addEventListener('click', close);
    backdrop.querySelector('[data-modal-confirm]')?.addEventListener('click', () => { onConfirm?.(); close(); });
    document.addEventListener('keydown', onKey);
    document.body.appendChild(backdrop);
    return close;
  }

  function wireConfirmLinks() {
    // Use: <a href="..." data-confirm="Message here">Delete</a>
    document.addEventListener('click', (e) => {
      const t = e.target.closest('[data-confirm]');
      if (!t) return;
      const href = t.getAttribute('href');
      const form = t.closest('form');
      e.preventDefault();
      createModal({
        title: 'Please Confirm',
        message: t.getAttribute('data-confirm') || 'Are you sure?',
        confirmText: 'Yes',
        cancelText: 'No',
        onConfirm: () => {
          if (href) window.location.href = href;
          else if (form) form.submit();
        }
      });
    });
  }

  function ensureToastContainer() {
    let c = document.querySelector('.toast-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'toast-container';
      document.body.appendChild(c);
    }
    return c;
  }

  window.StudentUI = {
    toast(message, timeout = 2500) {
      const c = ensureToastContainer();
      const t = document.createElement('div');
      t.className = 'toast';
      t.textContent = message;
      c.appendChild(t);
      setTimeout(() => t.remove(), timeout);
    },
    confirm(opts) { return createModal(opts); }
  };

  ready(() => {
    wireRipples();
    wireFormFocus();
    wireConfirmLinks();

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
      // Close on route click (mobile)
      container.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => {
        if (isOpen) { isOpen = false; setOpen(false); }
      }));
      // Close on escape
      document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && isOpen) { isOpen = false; setOpen(false); } });
    }
  });
})();
