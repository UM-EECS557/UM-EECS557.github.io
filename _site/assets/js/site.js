document.addEventListener('DOMContentLoaded', () => {
  const toc = document.getElementById('toc');
  const sections = Array.from(document.querySelectorAll('.toc-section'));

  sections.forEach(section => {
    const id = section.id;
    const title = section.querySelector('h2')?.textContent || id;
    const link = document.createElement('a');
    link.href = `#${id}`;
    link.textContent = title;
    toc.appendChild(link);
  });

  const links = Array.from(toc.querySelectorAll('a'));
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      links.forEach(a => a.classList.remove('active'));
      const link = toc.querySelector(`a[href="#${entry.target.id}"]`);
      if (link) link.classList.add('active');
    });
  }, { rootMargin: '-20% 0px -65% 0px', threshold: 0.01 });

  sections.forEach(section => observer.observe(section));
});
