// Profile Toggle
function toggleProfileMenu() {
    const menu = document.getElementById('profile-dropdown');
    menu.classList.toggle('hidden');
}

// Mobile Menu
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    const openIcon = document.getElementById('mobile-icon-open');
    const closeIcon = document.getElementById('mobile-icon-close');

    menu.classList.toggle('hidden');
    menu.classList.toggle('flex');

    if (menu.classList.contains('hidden')) {
        // Menu is CLOSED -> Show Hamburger, Hide Cross
        openIcon.classList.remove('hidden');
        openIcon.classList.add('block');
        closeIcon.classList.remove('block');
        closeIcon.classList.add('hidden');
    } else {
        // Menu is OPEN -> Hide Hamburger, Show Cross
        openIcon.classList.remove('block');
        openIcon.classList.add('hidden');
        closeIcon.classList.remove('hidden');
        closeIcon.classList.add('block');
    }
}

// MOBILE MENU
document.addEventListener('click', function (event) {
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileButton = event.target.closest('button');

    if (!mobileMenu.classList.contains('hidden') && !mobileMenu.contains(event.target) && !mobileButton) {
        toggleMobileMenu();
    }
});

// Close menu when clicking outside
document.addEventListener('click', function (event) {
    const menu = document.getElementById('profile-dropdown');
    const button = event.target.closest('button');
    const dropdown = event.target.closest('#profile-dropdown');

    if (!button && !dropdown && !menu.classList.contains('hidden')) {
        menu.classList.add('hidden');
    }
});