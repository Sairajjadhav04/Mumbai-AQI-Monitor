const searchInput = document.getElementById("stationSearch");
const tableBody = document.getElementById("stationTableBody");
const noResults = document.getElementById("noResults");
if (searchInput && tableBody && noResults) {
    searchInput.addEventListener("input", function () {
        const searchText = searchInput.value.toLowerCase().trim();
        const rows = tableBody.querySelectorAll("tr");
        let visibleRows = 0;
        rows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();
            const matches = rowText.includes(searchText);
            row.hidden = !matches;
            if (matches) {
                visibleRows++;
            }
        });
        noResults.hidden = visibleRows !== 0;
    });
}
