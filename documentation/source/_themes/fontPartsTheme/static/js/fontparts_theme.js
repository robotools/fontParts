function collapseSidebar() {
    var sidebar = document.querySelector('#sidebar');

    if (sidebar != null) {
        sidebar.classList.add('mobile-slideout')
    }
};

window.addEventListener('DOMContentLoaded', function () {
    collapseSidebar()

    var navButton = document.querySelector('#nav-button');
    navButton.addEventListener('click', toggleNav)
}, true);

function toggleNav() {
    var fpNavSidebar = document.querySelector('#sidebar');
    fpNavSidebar.classList.toggle('expanded')

    var fpNavOverlay = document.querySelector('#mobile-nav-overlay');
    fpNavOverlay.classList.toggle('hidden')
    fpNavOverlay.addEventListener('click', toggleNav)

    var fpNavIcon = document.querySelector('#nav-icon');
    fpNavIcon.classList.toggle('open')

}