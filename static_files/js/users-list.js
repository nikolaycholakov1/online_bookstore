document.addEventListener("DOMContentLoaded", function () {
    let table = document.querySelector('.table');

    // Select only th elements with the class 'sortable'
    let thElements = table.querySelectorAll("th.sortable");  // <-- Here's where we select them!

    thElements.forEach((th) => {
        th.style.cursor = 'pointer';  // Set cursor style to pointer
    });


    thElements.forEach((th) => {
        th.addEventListener('click', function () {
            sortTable(getColumnIndex(th));
        });
    });

    function getColumnIndex(thElement) {
        return Array.from(thElement.parentElement.children).indexOf(thElement);
    }

    function sortTable(columnIndex) {
        let rows = table.tBodies[0].rows;
        let sortedRows = Array.from(rows).sort((rowA, rowB) => {
            let cellA = rowA.cells[columnIndex].textContent.trim();
            let cellB = rowB.cells[columnIndex].textContent.trim();

            if (columnIndex === 2 || columnIndex === 3) {
                return parseFloat(cellB) - parseFloat(cellA); // Sort in descending order
            }

            return cellA.localeCompare(cellB);  // Default alphanumeric sort (for future use)
        });

        // Append each row into the table body
        sortedRows.forEach(row => {
            table.tBodies[0].appendChild(row);
        });
    }
});
