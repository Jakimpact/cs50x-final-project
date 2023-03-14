// Function for changing color of gain depending on value positive or negative
document.addEventListener('DOMContentLoaded', function() {

    let gains = document.querySelectorAll('.gain');

    for (let i = 0; i < gains.length; i++) {
        if (gains[i].getAttribute('value') < 0) {
            gains[i].style.color = "Red";
        }
        else if (gains[i].getAttribute('value') > 0) {
            gains[i].style.color = "SeaGreen";
        }
    }
})

// Function for sorting column on heading click for table1 (adapted from tutorial found on https://www.w3schools.com/howto/howto_js_sort_table.asp)
function sortTable1(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("table1");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc") {
                // Sort by alphabet
                if (n == 0 || n == 3) {
                    if (x.getAttribute('value').toLowerCase() > y.getAttribute('value').toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // Sort by date
                else if (n == 2) {
                    if (new Date(x.getAttribute('value')) > new Date(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // sort by number
                else if (n == 1 || n == 4 || n == 5 || n == 6) {
                    if (Number(x.getAttribute('value')) > Number(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            else if (dir == "desc") {
                // Sort by alphabet
                if (n == 0 || n == 3) {
                    if (x.getAttribute('value').toLowerCase() < y.getAttribute('value').toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // Sort by date
                else if (n == 2) {
                    if (new Date(x.getAttribute('value')) < new Date(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // sort by number
                else if (n == 1 || n == 4 || n == 5 || n == 6) {
                    if (Number(x.getAttribute('value')) < Number(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }                
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}


// Function for sorting column on heading click for table1 (adapted from tutorial found on https://www.w3schools.com/howto/howto_js_sort_table.asp)
function sortTable2(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("table2");
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc") {
                // Sort by alphabet
                if (n == 0) {
                    if (x.getAttribute('value').toLowerCase() > y.getAttribute('value').toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // sort by number
                else {
                    if (Number(x.getAttribute('value')) > Number(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            else if (dir == "desc") {
                // Sort by alphabet
                if (n == 0) {
                    if (x.getAttribute('value').toLowerCase() < y.getAttribute('value').toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
                // sort by number
                else {
                    if (Number(x.getAttribute('value')) < Number(y.getAttribute('value'))) {
                        shouldSwitch = true;
                        break;
                    }
                }                
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

