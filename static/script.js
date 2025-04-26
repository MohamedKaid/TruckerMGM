document.querySelector('.mobile-nav-toggle').addEventListener('click', function () {
    const navLinks = document.querySelector('.mobile-nav-links');
    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    this.setAttribute('aria-expanded', !isExpanded);
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
});
