const searchInput = document.getElementById("stationSearch");
const searchBtn = document.getElementById("searchBtn");
const tableBody = document.getElementById("stationTableBody");
const noResults = document.getElementById("noResults");
const status = document.getElementById("operationStatus");
const showAllBtn = document.getElementById("showAllBtn");
const highestBtn = document.getElementById("highestBtn");
const lowestBtn = document.getElementById("lowestBtn");
if (
    searchInput &&
    searchBtn &&
    tableBody &&
    noResults &&
    status
) {
    function getStationRows() {
        return Array.from(tableBody.querySelectorAll("tr"))
            .filter(row => row.cells.length >= 6);
    }
    function showRows(rowsToShow) {
        const allRows = getStationRows();

        allRows.forEach(row => {
            row.hidden = !rowsToShow.includes(row);
        });
        noResults.hidden = rowsToShow.length !== 0;
    }
    function searchStations() {
        const searchText = searchInput.value
            .toLowerCase()
            .trim();
        const matchingRows = getStationRows().filter(row =>
            row.cells[0].textContent.toLowerCase().includes(searchText) ||
            row.cells[1].textContent.toLowerCase().includes(searchText)
        );
        showRows(matchingRows);
        status.textContent =
            `${matchingRows.length} matching station(s) found.`;
    }
    function showAllStations() {
        searchInput.value = "";
        const rows = getStationRows();
        showRows(rows);
        status.textContent =
            `Showing all ${rows.length} station(s).`;
    }
    function showExtremeAQI(findHighest) {
        const rows = getStationRows();
        if (rows.length === 0) {
            showRows([]);
            status.textContent = "No AQI data available.";
            return;
        }
        const validRows = rows.filter(row =>
            Number.isFinite(Number(row.cells[2].textContent.trim())) &&
            row.cells[2].textContent.trim() !== ""
        );
        if (validRows.length === 0) {
            showRows([]);
            status.textContent = "No valid AQI values available.";
            return;
        }
        const extremeValue = Math[findHighest ? "max" : "min"](
            ...validRows.map(row =>
                Number(row.cells[2].textContent.trim())
            )
        );
        const matchingRows = validRows.filter(row =>
            Number(row.cells[2].textContent.trim()) === extremeValue
        );
        searchInput.value = "";
        showRows(matchingRows);
        const operation = findHighest ? "Highest" : "Lowest";
        status.textContent =
            `${operation} AQI: ${extremeValue}. ` +
            `${matchingRows.length} station(s) with this value.`;
    }
    searchBtn.addEventListener("click", searchStations);
    searchInput.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            searchStations();
        }
    });
    showAllBtn.addEventListener("click", showAllStations);
    highestBtn.addEventListener("click", () => {
        showExtremeAQI(true);
    });
    lowestBtn.addEventListener("click", () => {
        showExtremeAQI(false);
    });
    showAllStations();
}