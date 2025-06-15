function applyTheme(theme) {
    if (theme === "system") {
        const systemTheme = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        document.documentElement.setAttribute("data-theme", systemTheme);
    } else {
        document.documentElement.setAttribute("data-theme", theme);
    }
}

function initTheme() {
    let initialTheme = "system"; // Default theme

    // Check for server-provided theme if user is authenticated
    if (current_user.is_authenticated && current_user.theme_preference) {
        initialTheme = "{{ current_user.theme_preference }}";
        localStorage.setItem("theme", initialTheme); // Update localStorage to match server preference
    }    
    else {
         // If no server theme, try localStorage
        const localTheme = localStorage.getItem("theme");
        if (localTheme) {
            initialTheme = localTheme;
    }
    
    applyTheme(initialTheme);
    document.getElementById("theme-select").value = initialTheme;
}

window.addEventListener("DOMContentLoaded", initTheme);
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (localStorage.getItem("theme") === "system") {
        applyTheme("system");
    }
});

function handleThemeChange(select) {
    const selected = select.value;
    localStorage.setItem("theme", selected);
    applyTheme(selected);

    // If logged in, update user preference on server
    fetch("/api/set-theme", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ theme: selected })
    }).catch(err => console.error("Theme save failed:", err))}};
