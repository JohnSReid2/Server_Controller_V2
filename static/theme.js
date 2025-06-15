function initTheme() {
    let initialTheme = "system"; // Default theme

    if (window.USER_THEME_PREFERENCE && window.USER_THEME_PREFERENCE !== '') {
        initialTheme = window.USER_THEME_PREFERENCE;
        localStorage.setItem("theme", initialTheme);
    } else {
        const localTheme = localStorage.getItem("theme");
        if (localTheme) {
            initialTheme = localTheme;
        }
    }

    applyTheme(initialTheme);
    document.getElementById("theme-select").value = initialTheme;

    const themeSelect = document.getElementById("theme-select");
    if (themeSelect) {
        themeSelect.addEventListener("change", function() {
            handleThemeChange(this);
        });
    }
}

function applyTheme(themeName) {
    let themeToApply = themeName;
    if (themeName === "system") {
        themeToApply = window.matchMedia('(prefers-color-scheme: dark)').matches ? "dark" : "light";
    }

    if (themeToApply === "dark") {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
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
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch("/api/set-theme", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ theme: selected })
    }).catch(err => console.error("Theme save failed:", err));
}