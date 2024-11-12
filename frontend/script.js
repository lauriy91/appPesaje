async function obtenerPeso() {
    const res = await fetch("http://localhost:5000/peso");
    const data = await res.json();
    document.getElementById("peso").innerText = `Peso: ${data.peso} kg`;
}

async function obtenerPesoPorFecha() {
    const res = await fetch("http://localhost:5000/pesoPorFecha");
    const data = await res.json();
    document.getElementById("peso").innerText = `Peso: ${data.peso_total} kg`;
}

setInterval(() => {
    obtenerPeso();
    obtenerPesoPorFecha();
}, 5000);
