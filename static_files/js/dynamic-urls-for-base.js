document.addEventListener("DOMContentLoaded", function () {
        // Get the <a> element with the 'url' ID
        const urlLink = document.getElementById("url");

        if (urlLink) {
            // Get the current URL path
            const currentPath = window.location.pathname;

            // Remove the leading slash from the current URL path
            const trimmedPath = currentPath.substring(1);

            // Set the text content of the <a> element with the trimmed URL path
            urlLink.textContent = trimmedPath;
            // Set the href attribute of the <a> element to the current URL path
            urlLink.href = currentPath;
        }
    });

