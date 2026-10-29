//TOAST NOTIFICATION
const toast = document.getElementById("toast");
let timer;

function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");

    clearTimeout(timer);

    timer = setTimeout(() => {
        toast.classList.remove("show");
    }, 2800);
}

   //NAVIGATION LINKS
document.querySelectorAll("nav a").forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();

        // Remove active class from all navigation links
        document.querySelectorAll("nav a").forEach(a => {
            a.classList.remove("active");
        });

        // Activate the clicked navigation link
        link.classList.add("active");

        // Display a message for pages other than Home
        if (link.dataset.page !== "Home") {
            showToast(
                `${link.dataset.page} selected. Connect this item to its page when ready.`
            );
        }
    });
});

   // BUTTONS WITH DATA-MSG
document.querySelectorAll("[data-msg]").forEach(button => {
    button.addEventListener("click", () => {
        showToast(button.dataset.msg);
    });
});

   //FEATURE LINKS
document.querySelectorAll("[data-feature]").forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();

        showToast(`${link.dataset.feature} details selected.`);
    });
});

   // PROFILE MENU
// Toggle the profile dropdown menu
document.getElementById("profile").addEventListener("click", () => {
    document.getElementById("profileMenu").classList.toggle("open");
});

// Close the profile menu when clicking outside it
document.addEventListener("click", event => {
    if (
        !event.target.closest("#profile") &&
        !event.target.closest("#profileMenu")
    ) {
        document.getElementById("profileMenu").classList.remove("open");
    }
});

//NOTIFICATIONS
document.getElementById("notify").addEventListener("click", () => {
    showToast("You have 3 recent farm alerts.");
});

   //ALL FARMS LINK
document.getElementById("allFarms").addEventListener("click", event => {
    event.preventDefault();

    showToast("Showing the farms registered in this dashboard.");
});

// ALL ALERTS LINK
document.getElementById("allAlerts").addEventListener("click", event => {
    event.preventDefault();

    showToast("Showing recent soil, water, and crop alerts.");
});
