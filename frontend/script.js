const API_URL = "http://127.0.0.1:8000";

const resultado = document.getElementById("resultado");

const rotulosCampos = {
    id: "ID",
    numero: "Linha",
    area: "Area",
    terminal_inicial: "Terminal inicial",
    terminal_final: "Terminal final",
    empresa: "Empresa",
    codigo: "Codigo",
    nome: "Nome",
    endereco: "Endereco",
    latitude: "Latitude",
    longitude: "Longitude",
    horario: "Horario",
    destino: "Destino",
    previsao: "Previsao"
};

function formatarRotulo(campo) {
    return rotulosCampos[campo] || campo
        .replaceAll("_", " ")
        .replace(/\b\w/g, letra => letra.toUpperCase());
}

function escaparHtml(valor) {
    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function formatarValor(valor) {
    if (valor === null || valor === undefined || valor === "") {
        return "-";
    }

    if (typeof valor === "object") {
        return JSON.stringify(valor);
    }

    return String(valor);
}

function obterLinhas(dados) {
    if (Array.isArray(dados)) {
        return dados;
    }

    if (dados && typeof dados === "object") {
        const lista = Object.values(dados).find(Array.isArray);
        return lista || [dados];
    }

    return [];
}

function mostrarResultado(dados) {
    //Garante que os dados sejam tratados como uma lsta
    //se a API retornar apenas um objeto. ele vira uma lista
  const lista = obterLinhas(dados);

  //Se a lista estiver vazia, mostra uma mensagem
  if (!lista.length){
    mostrarMensagem("Nenhum resultado encontrado!")
    return;
  }

  //pega os nomes dos campos do primeiro item
  const campos=Object.keys(lista[0])
  //troca a lasse do resultado e aplica o estilo da tabela
  resultado.className="result-content";
  //monta o html ue sera exibido
  resultado.innerHTML = `
  <div class="result-summary">
    <strong>${lista.length}</strong>
    <span>${lista.length === 1 ? "registro encontrado" : "Registros encontrados"}</span>
  </div>
  <!-- Cria uma área com rolagem caso a tabela fique grande -->
  <div class="table-wrap">
    <table>
        <thead>
            <tr>
                ${campos.map(campo => `<th>${escaparHtml(formatarRotulo(campo))}</th>`).join("")}
            </tr>
        </thead>
        <tbody>
        <!-- Cria uma linha da tabela para cada item retornado pela API -->
        ${lista.map(item => `
            <tr>
            ${campos.map(campo=> `<td>${escaparHtml(formatarValor(item[campo]))}</td>`).join("")}
            </tr>`).join("")}
        </tbody>
    </table>
  </div>
  `;
}

function mostrarMensagem(mensagem) {
    //Aplica o estilo de mensagem simple, sem tabela
    resultado.className = "result-state";
    //exibe o texto da mensagem na tela
    resultado.textContent = mensagem;
}

async function chamarApi(url) {
    const resposta = await fetch(url);
    const dados = await resposta.json();

    if (!resposta.ok) {
        throw new Error(dados.detail || "Erro ao chamar a API");
    }

    return dados;
}

async function listarLinhas() {
    try {
        const dados = await chamarApi(`${API_URL}/linhas/`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function buscarLinhaPorNumero() {
    const numero = document.getElementById("inputNumeroLinha").value;

    if (!numero) {
        mostrarMensagem("Digite o número da linha.");
        return;
    }

    try {
        const dados = await chamarApi(`${API_URL}/linhas/buscar/${numero}`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function listarParadas() {
    try {
        const dados = await chamarApi(`${API_URL}/paradas/`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function buscarParadaPorNome() {
    const nome = document.getElementById("inputNomeParada").value;

    if (!nome) {
        mostrarMensagem("Digite o nome da parada.");
        return;
    }

    try {
        const dados = await chamarApi(`${API_URL}/paradas/buscar/${nome}`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function buscarParadaPorId() {
    const id = document.getElementById("inputIdParada").value;

    if (!id) {
        mostrarMensagem("Digite o ID da parada.");
        return;
    }

    try {
        const dados = await chamarApi(`${API_URL}/paradas/${id}`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function buscarPrevisaoPorParada() {
    const codigoParada = document.getElementById("inputCodigoParada").value;

    if (!codigoParada) {
        mostrarMensagem("Digite o código da parada.");
        return;
    }

    try {
        const dados = await chamarApi(`${API_URL}/previsoes/parada/${codigoParada}`);        
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

async function listarEmpresas() {
    try {
        const dados = await chamarApi(`${API_URL}/empresas/`);
        mostrarResultado(dados);
    } catch (erro) {
        mostrarMensagem(erro.message);
    }
}

document.getElementById("btnListarLinhas").addEventListener("click", listarLinhas);
document.getElementById("btnBuscarLinha").addEventListener("click", buscarLinhaPorNumero);

document.getElementById("btnListarParadas").addEventListener("click", listarParadas);
document.getElementById("btnBuscarParadaNome").addEventListener("click", buscarParadaPorNome);
document.getElementById("btnBuscarParadaId").addEventListener("click", buscarParadaPorId);

document.getElementById("btnPrevisaoParada").addEventListener("click", buscarPrevisaoPorParada);
document.getElementById("btnEmpresas").addEventListener("click", listarEmpresas);
