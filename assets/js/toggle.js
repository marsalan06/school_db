function toggleMenu() {
    var menu = document.getElementById('mobileMenu');
    menu.classList.toggle('menu-open');

    var menuBar = document.querySelector('.menu-bar');
    menuBar.classList.toggle('active');
}