document.addEventListener("DOMContentLoaded", function () {
    const ordersTable = document.getElementById("orders-table");

    if (ordersTable) {
        // Get the headers that are sortable
        const headers = ordersTable.querySelectorAll("thead th.sortable");

        // Add pointer cursor and sorting functionality to each sortable header
        headers.forEach(function (header) {
            header.style.cursor = "pointer";
            header.addEventListener("click", function () {
                // Identify the column index that was clicked
                const columnIndex = Array.from(header.parentElement.children).indexOf(header);

                const rows = Array.from(ordersTable.querySelectorAll("tbody tr"));

                if (columnIndex === 0) {
                    const statusPriority = {
                        "Shipped": 0,
                        "Processing": 1,
                        "Pending": 2,
                        "Delivered": 3,
                        "Cancelled": 4,
                    };
                    // Sort based on status priority
                    rows.sort(function (rowA, rowB) {
                        const cellA = rowA.querySelectorAll("td")[columnIndex].textContent.trim();
                        const cellB = rowB.querySelectorAll("td")[columnIndex].textContent.trim();
                        return statusPriority[cellA] - statusPriority[cellB];
                    });
                } else if (columnIndex === 1) {
                    // Sort based on Date Order (latest to oldest)
                    rows.sort(function (rowA, rowB) {
                        const cellA = new Date(rowA.querySelectorAll("td")[columnIndex].textContent.trim());
                        const cellB = new Date(rowB.querySelectorAll("td")[columnIndex].textContent.trim());
                        return cellB - cellA;
                    });
                } else if (columnIndex === 2) {
                    // Sort based on Total Price (highest to lowest)
                    rows.sort(function (rowA, rowB) {
                        const cellA = parseFloat(rowA.querySelectorAll("td")[columnIndex].textContent.replace("$", ""));
                        const cellB = parseFloat(rowB.querySelectorAll("td")[columnIndex].textContent.replace("$", ""));
                        return cellB - cellA;
                    });
                } else {
                    // Sort based on other columns (lexicographic order)
                    rows.sort(function (rowA, rowB) {
                        const cellA = rowA.querySelectorAll("td")[columnIndex].textContent.trim();
                        const cellB = rowB.querySelectorAll("td")[columnIndex].textContent.trim();
                        return cellA.localeCompare(cellB);
                    });
                }

                // Clear existing rows
                ordersTable.querySelector("tbody").innerHTML = "";

                // Append sorted rows
                rows.forEach(function (row) {
                    ordersTable.querySelector("tbody").appendChild(row);
                });
            });
        });

        // Add background colors based on status
        const statusCells = ordersTable.querySelectorAll("td[data-status]");
        statusCells.forEach(function (cell) {
            const status = cell.getAttribute("data-status");
            // Apply background color based on status
            switch (status) {
                case "Delivered":
                    cell.style.backgroundColor = "#0275d8";
                    break;
                case "Shipped":
                    cell.style.backgroundColor = "#5cb85c";
                    break;
                case "Processing":
                    cell.style.backgroundColor = "#5bc0de";
                    break;
                case "Pending":
                    cell.style.backgroundColor = "#f0ad4e";
                    break;
                case "Cancelled":
                    cell.style.backgroundColor = "#d9534f";
                    break;
            }
        });
    }
});


