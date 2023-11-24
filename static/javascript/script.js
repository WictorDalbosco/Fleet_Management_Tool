// Definindo a URL da API
const API_URL = 'http://localhost:5000';

// Função para carregar a tabela de veículos
function loadTable() {
    
    // Criando uma requisição XMLHttpRequest
    const xhttp = new XMLHttpRequest();
    
    // Configurando a requisição GET para obter todos os veículos
    xhttp.open("GET", `${API_URL}/request_all`);
    xhttp.send();
    
    // Definindo a função a ser chamada quando o estado da requisição muda
    xhttp.onreadystatechange = function () {
        // Verificando se a requisição foi concluída com sucesso (estado 4) e o status HTTP é 200
        if (this.readyState == 4 && this.status == 200) {
            // Exibindo a resposta no console (pode ser removido em produção)
            console.log(this.responseText);
            
            // Criando o HTML para a tabela de veículos
            var trHTML = "";
            const vehicles = JSON.parse(this.responseText);
            
            // Iterando sobre os veículos e construindo as linhas da tabela
            for (let vehicle of vehicles.res) {
                trHTML += "<tr>";
                trHTML += `<td>${vehicle.id}</td>`;
                trHTML += `<td>${vehicle.model}</td>`;
                trHTML += `<td>${vehicle.plate}</td>`;
                trHTML += `<td>${vehicle.year}</td>`;
                trHTML += '<td>' +
                    `<button type="button" class="btn btn-outline-secondary" onclick="showVehicleEditBox(${vehicle.id})">Edit</button>` +
                    `<button type="button" class="btn btn-outline-danger" style="margin-left: 5px; "onclick="deleteVehicle(${vehicle.id})">Del</button>` +
                    '</td>';
                trHTML += "</tr>";
            }
            
            // Atualizando o conteúdo da tabela no HTML
            document.getElementById("vehicle-list").innerHTML = trHTML;
        }
    };
}

// Função para exibir a caixa de criação de veículo
function showVehicleCreateBox() {
    
    // Utilizando a biblioteca SweetAlert para exibir um modal de criação de veículo
    Swal.fire({
        title: "Create Vehicle",
        html:
            '<input id="id" type="hidden">' +
            '<input id="model" class="swal2-input" placeholder="Model">' +
            '<input id="plate" class="swal2-input" placeholder="Plate (e.g., ABC1D23)">' +
            '<input id="year" class="swal2-input" placeholder="Year">',
        focusConfirm: false,
        preConfirm: () => {
            // Chamando a função de criação de veículo quando o modal é confirmado
            vehicleCreate();
        },
    });
}

// Função para criar um novo veículo
function vehicleCreate() {
    // Obtendo os valores dos campos do modal
    const model = document.getElementById("model").value;
    const plate = document.getElementById("plate").value;
    const year = document.getElementById("year").value;

    // Adicionando validação de campos vazios
     if (!model || !plate || !year) {
        Swal.fire("Error", "Please fill in all fields.", "error");
        return;
    }

    // Adicionando validação do ano
    const currentYear = new Date().getFullYear();
    if (parseInt(year) > currentYear + 1 || parseInt(year) < 1900) {
        Swal.fire("Error", "Invalid year. The year cannot be greater than the current year + 1 or less than 1900", "error");
        return;
    }

    // Adicionando validação da placa
    const plateRegex = /^[A-Z]{3}\d[A-Z]\d{2}$/;
    if (!plateRegex.test(plate)) {
        Swal.fire("Error", "Invalid plate. Please enter a valid Mercosul plate. (e.g., ABC1D23)", "error");
        return;
    }

    // Criando uma requisição XMLHttpRequest para enviar os dados de criação do veículo
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", `${API_URL}/request`);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    
    // Enviando os dados em formato JSON
    xhttp.send(
        JSON.stringify({
            model: model,
            plate: plate,
            year: year,
        })
    );
    
    // Definindo a função a ser chamada quando o estado da requisição muda
    xhttp.onreadystatechange = function () {
        // Verificando se a requisição foi concluída com sucesso (estado 4) e o status HTTP é 200
        if (this.readyState == 4 && this.status == 200) {
            // Parseando a resposta JSON
            const response = JSON.parse(this.responseText);
            // Exibindo a mensagem da resposta usando o SweetAlert
            Swal.fire(response.msg);
            // Recarregando a tabela após a criação do veículo
            loadTable();
        }
    };
}

// Função para exibir a caixa de edição de veículo
function showVehicleEditBox(id) {
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", `${API_URL}/request/${id}`);
    xhttp.send();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            const vehicle = JSON.parse(this.responseText).res;
            Swal.fire({
                title: "Edit Vehicle",
                html:
                    `<input id="id" type="hidden" value=${vehicle.id}>` +
                    `<input id="model" class="swal2-input" placeholder="Model" value="${vehicle.model}">` +
                    `<input id="plate" class="swal2-input" placeholder="Plate (e.g., ABC1D23)" value="${vehicle.plate}">` +
                    `<input id="year" class="swal2-input" placeholder="Year" value="${vehicle.year}">`,
                focusConfirm: false,
                preConfirm: () => {
                    vehicleEdit();
                },
            });
        }
    };
}

// Função para editar um veículo existente
function vehicleEdit() {
    const id = document.getElementById("id").value;
    const model = document.getElementById("model").value;
    const plate = document.getElementById("plate").value;
    const year = document.getElementById("year").value;

     // Adicionando validação do ano
     const currentYear = new Date().getFullYear();
    if (parseInt(year) > currentYear + 1 || parseInt(year) < 1900) {
        Swal.fire("Error", "The year cannot be greater than the current year + 1 or less than 1900", "error");
        return;
    }

    // Adicionando validação da placa
    const plateRegex = /^[A-Z]{3}\d[A-Z]\d{2}$/;
    if (!plateRegex.test(plate)) {
        Swal.fire("Error", "Invalid plate. Please enter a valid Mercosul plate. (e.g., ABC1D23)", "error");
        return;
    }

    // Criando uma requisição XMLHttpRequest para enviar os dados de edição do veículo
    const xhttp = new XMLHttpRequest();
    xhttp.open("PUT", `${API_URL}/request/${id}`);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    
    // Enviando os dados em formato JSON
    xhttp.send(
        JSON.stringify({
            id: id,
            model: model,
            plate: plate,
            year: year,
        })
    );
    // Definindo a função a ser chamada quando o estado da requisição muda
    xhttp.onreadystatechange = function () {
        // Verificando se a requisição foi concluída com sucesso (estado 4) e o status HTTP é 200
        if (this.readyState == 4 && this.status == 200) {
            // Parseando a resposta JSON
            const response = JSON.parse(this.responseText);

            // Exibindo a mensagem da resposta usando o SweetAlert
            Swal.fire(response.msg);

            // Recarregando a tabela após a edição do veículo
            loadTable();
        }
    };

}

// Função para deletar um veículo pelo ID
function deleteVehicle(id) {
    // Criando uma requisição XMLHttpRequest para deletar o veículo pelo ID
    const xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", `${API_URL}/request/${id}`);
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send();
    
    // Definindo a função a ser chamada quando o estado da requisição muda
    xhttp.onreadystatechange = function () {
        // Verificando se a requisição foi concluída com sucesso (estado 4)
        if (this.readyState == 4) {
            // Parseando a resposta JSON
            const response = JSON.parse(this.responseText);
            // Exibindo a mensagem da resposta usando o SweetAlert
            Swal.fire(response.msg);
            // Recarregando a tabela após a exclusão do veículo
            loadTable();
        }
    };
}

// Evento que é acionado quando o conteúdo DOM é totalmente carregado
document.addEventListener("DOMContentLoaded", function () {
    loadTable();
});