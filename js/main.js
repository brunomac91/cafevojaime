// ===== Café Vô Jaime — interações =====

// Sombra no header ao rolar
const header = document.querySelector('.header');
window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 10);
}, { passive: true });

// Menu mobile
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
const backdrop = document.querySelector('.nav-backdrop');

function setMenu(open) {
  links.classList.toggle('open', open);
  toggle.classList.toggle('open', open);
  toggle.setAttribute('aria-expanded', open);
  if (open) {
    backdrop.hidden = false;
    requestAnimationFrame(() => backdrop.classList.add('show'));
  } else {
    backdrop.classList.remove('show');
    backdrop.addEventListener('transitionend', () => { backdrop.hidden = true; }, { once: true });
  }
}

toggle.addEventListener('click', () => setMenu(!links.classList.contains('open')));
backdrop.addEventListener('click', () => setMenu(false));
links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && links.classList.contains('open')) setMenu(false);
});

// Animação de entrada
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!reduceMotion) {
  const observer = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    }),
    { threshold: 0.1 }
  );
  document
    .querySelectorAll('.card, .plan, .tier, .public-card, .section-head, .example-box, .duration-strip, .b2b-packs, .story-copy, .seasonal')
    .forEach(el => {
      el.classList.add('reveal');
      observer.observe(el);
    });
}
