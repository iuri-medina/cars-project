// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
  const menuBtn = document.querySelector('.mobile-menu-btn');
  const userMenu = document.querySelector('.user-menu');

  if (menuBtn && userMenu) {
    menuBtn.addEventListener('click', function () {
      userMenu.classList.toggle('mobile-active');

      // Toggle icon between menu and close
      const icon = this.querySelector('.material-symbols-outlined');
      icon.textContent = userMenu.classList.contains('mobile-active')
        ? 'close'
        : 'menu';
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
      if (!menuBtn.contains(event.target) && !userMenu.contains(event.target)) {
        userMenu.classList.remove('mobile-active');
        const icon = menuBtn.querySelector('.material-symbols-outlined');
        icon.textContent = 'menu';
      }
    });
  }
});
