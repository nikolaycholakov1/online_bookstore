document.addEventListener('DOMContentLoaded', function () {
    let table = document.querySelector('.table');
    let tbody = table.querySelector('tbody');

    // Apply the color coding for status
    const statusCells = tbody.querySelectorAll("td[data-status]");
    statusCells.forEach(function (cell) {
        const status = cell.getAttribute("data-status");
        // Applying background color based on status
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

    // Handle the sorting
    table.querySelectorAll('th').forEach((header, idx) => {
        // Check if it's a sortable header
        if (["Date", "Current Status", "Total Items", "Total Price"].includes(header.innerText)) {
            header.style.cursor = 'pointer';  // Add the pointer cursor style to sortable headers

            header.addEventListener('click', function () {
                let sortedRows = Array.from(tbody.rows)
                    .sort((rowA, rowB) => {
                        let cellA = rowA.cells[idx].innerText;
                        let cellB = rowB.cells[idx].innerText;

                        switch (header.innerText) {
                            case 'Date':
                                return new Date(cellA) - new Date(cellB);
                            case 'Current Status':
                                let statusPriority = {
                                    "Shipped": 0,
                                    "Processing": 1,
                                    "Pending": 2,
                                    "Delivered": 3,
                                    "Cancelled": 4,
                                };
                                return statusPriority[cellA] - statusPriority[cellB];
                            case 'Total Items':
                                return cellB - cellA; // Reverse order for descending
                            case 'Total Price':
                                return parseFloat(cellB.slice(1)) - parseFloat(cellA.slice(1)); // Remove $ sign and compare
                            default:
                                return 0;
                        }
                    });

                tbody.append(...sortedRows);
            });
        }
    });
});
