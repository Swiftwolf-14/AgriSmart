const menuButton = document.getElementById("menuButton");
const sidebar = document.getElementById("sidebar");

if (menuButton && sidebar) {
    menuButton.addEventListener("click", () => {
        sidebar.classList.toggle("open");
    });
}

// Close the mobile sidebar after selecting a navigation link.
document.querySelectorAll(".sidebar-nav .nav-link").forEach(link => {
    link.addEventListener("click", () => {
        if (window.innerWidth <= 760) {
            sidebar?.classList.remove("open");
        }
    });
});