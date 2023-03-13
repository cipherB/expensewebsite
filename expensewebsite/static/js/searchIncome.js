const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector(".table-output");
const noResult = document.querySelector(".table-no-result");
const appTable = document.querySelector(".app-table");
const paginationContainer = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
tableOutput.style.display = "none";

searchField.addEventListener('keyup', (e) => {
    const searchValue = e.target.value;

    if(searchValue.trim().length>0) {
        paginationContainer.style.display = "none";
        tbody.innerHTML = "";
        fetch('/income/search-incomes', {
            body: JSON.stringify({searchText: searchValue}),
            method: "POST",
        }).then(res => res.json())
        .then(data => {
            appTable.style.display = "none";
            tableOutput.style.display = "block";
            tbody.innerHTML = "";
            noResult.innerHTML="";
            if(data.length===0){
                tableOutput.style.display = "none";
                noResult.innerHTML = "No results found";
            } else {
                data.forEach((item,id) => {
                    tbody.innerHTML += `
                    <tr key=${id} >
                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                    </tr>
                    `
                });
            }
        })
    } else {
        appTable.style.display = "block";
        paginationContainer.style.display ="block";
        tableOutput.style.display = "none";
    }
})