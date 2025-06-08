seld1 = document.getElementById('selD1');
seld1.addEventListener('click', cargarD1)

const formatearFecha = isoString => {
    const fecha = new Date(isoString);
    return new Intl.DateTimeFormat('es-ES', {
        dateStyle: 'long',
        timeStyle: 'short'
    }).format(fecha);
};

function actualizarGraficoVisitas() {
    let requestBody = usuarioSeleccionado === "todos" ? {} : { direccion_mac: usuarioSeleccionado };

    fetch('http://127.0.0.1:5000/estadisticas/visitas/ultimos-30-dias', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(respuesta => {
        const ctx = document.getElementById('grafico_visitas').getContext('2d');

        let todasLasFechas = Object.keys(respuesta);
        let todosLosDatos = Object.values(respuesta);

        // Si ya existe un gráfico, lo destruimos antes de crear uno nuevo
        if (canvas_visitas !== null) {
            canvas_visitas.destroy();
        }

        const data = {
            labels: todasLasFechas,
            datasets: [{
                label: 'Visitas diarias',
                data: todosLosDatos,
                borderColor: 'black',
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: 'red',
                pointBorderColor: 'white',
                tension: 0
            }]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Fecha" }, ticks: { autoSkip: true, maxTicksLimit: 10 } },
                    y: { title: { display: true, text: "Visitas" }, beginAtZero: true }
                },
                plugins: {
                    zoom: {
                        pan: { enabled: true, mode: 'x' },
                        zoom: { 
                            enabled: true, 
                            mode: 'x', 
                            wheel: { enabled: true }, 
                            pinch: { enabled: true },
                            limits: { x: { min: 0, max: 29 } },
                            rangeMin: { x: 23 }
                        }
                    }
                }
            }
        };

        // Crear el nuevo gráfico y almacenarlo en la variable global
        canvas_visitas = new Chart(ctx, config);
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));
}

seld2 = document.getElementById('selD2');
seld2.addEventListener('click', cargarD2)

seld3 = document.getElementById('selD3');
seld3.addEventListener('click', cargarD3)

seld4 = document.getElementById('selD4');
seld4.addEventListener('click', cargarD4)

function actualizarGraficoAcumuladas() {
    let requestBody = usuarioSeleccionado === "todos" ? {} : { direccion_mac: usuarioSeleccionado };

    fetch('http://127.0.0.1:5000/estadisticas/visitas/acumuladas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(respuesta => {
        const ctx2 = document.getElementById('grafico_visitas_acumuladas').getContext('2d');

        const todasLasFechas = Object.keys(respuesta);
        const datosAcumulados = Object.values(respuesta);

        // Si ya existe un gráfico, lo destruimos antes de crear uno nuevo
        if (canvas_visitas_acumuladas !== null) {
            canvas_visitas_acumuladas.destroy();
        }

        // Si no existe, crea el gráfico por primera vez
        const data2 = {
            labels: todasLasFechas,
            datasets: [{
                label: 'Visitas acumuladas',
                data: datosAcumulados,
                borderColor: 'black',
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: 'blue',
                pointBorderColor: 'white',
                tension: 0
            }]
        };

        const config2 = {
            type: 'line',
            data: data2,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { 
                        title: { display: true, text: "Fecha" },
                        ticks: { autoSkip: true, maxTicksLimit: 10 }
                    },
                    y: { title: { display: true, text: "Visitas acumuladas" }, beginAtZero: true }
                },
                plugins: {
                    zoom: {
                        pan: { enabled: true, mode: 'x' },
                        zoom: { 
                            enabled: true, 
                            mode: 'x', 
                            wheel: { enabled: true }, 
                            pinch: { enabled: true },
                            limits: { x: { min: 0, max: 29 } },
                            rangeMin: { x: 23 }
                        }
                    }
                }
            }
        }

            canvas_visitas_acumuladas = new Chart(ctx2, config2);
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));
}

function actualizarGraficoTiempoMedio() {
    let requestBody = usuarioSeleccionado === "todos" ? {} : { direccion_mac: usuarioSeleccionado };

    fetch('http://127.0.0.1:5000/estadisticas/tiempo/promedio-por-dia', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(respuesta => {
        const ctx3 = document.getElementById('grafico_tiempo_medio').getContext('2d');

        const todasLasFechas3 = Object.keys(respuesta);
        const tiempoMedio = Object.values(respuesta);

        if (canvas_tiempo_medio) {
            // Si el gráfico ya existe, lo destruimos antes de crear uno nuevo
            canvas_tiempo_medio.destroy();
        }

        const data3 = {
            labels: todasLasFechas3,
            datasets: [{
                label: 'Tiempo medio en la página (min)',
                data: tiempoMedio,
                borderColor: 'black',
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: 'green',
                pointBorderColor: 'white',
                tension: 0
            }]
        };

        const config3 = {
            type: 'line',
            data: data3,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { 
                        title: { display: true, text: "Fecha" },
                        ticks: { autoSkip: true, maxTicksLimit: 10 }
                    },
                    y: { 
                        title: { display: true, text: "Tiempo medio (min)" },
                        beginAtZero: false
                    }
                },
                plugins: {
                    zoom: {
                        pan: { enabled: true, mode: 'x' },
                        zoom: { 
                            enabled: true, 
                            mode: 'x', 
                            wheel: { enabled: true }, 
                            pinch: { enabled: true },
                            limits: { x: { min: 0, max: 29 } },
                            rangeMin: { x: 23 }
                        }
                    }
                }
            }
        };

        // Crear el gráfico
        canvas_tiempo_medio = new Chart(ctx3, config3);
    })
    .catch(error => console.error('Error al obtener tiempo medio:', error));
}

// Función para generar fechas dinámicamente
const obtenerFechas = (dias) => {
    let fechas = [];
    for (let i = dias - 1; i >= 0; i--) {
        let fecha = new Date();
        fecha.setDate(fecha.getDate() - i);
        fechas.push(fecha.toLocaleDateString());
    }
    return fechas;
};


// Obtener el ícono, la ventana emergente y el botón de cerrar
const abrirPopup = document.getElementById('abrirPopup');
const popup = document.getElementById('popup');
const cerrarPopup = document.getElementById('cerrarPopup');
const usuariosSelect = document.getElementById('usuarios');
const confirmarUsuario = document.getElementById('confirmarUsuario');

// Variable para almacenar el usuario seleccionado
let usuarioSeleccionado = 'todos'; // "todos" por defecto

// Función para llenar el desplegable con los usuarios
function llenarUsuarios() {
    usuariosSelect.innerHTML = ''; // Limpiar opciones previas

    // Agregar la opción "Todos"
    const optionTodos = document.createElement('option');
    optionTodos.value = 'todos';
    optionTodos.textContent = 'Todos';
    usuariosSelect.appendChild(optionTodos);

    fetch('http://127.0.0.1:5000/sesiones/direcciones-mac')
    .then(response => response.json())
    .then(data => {
        usuarios = data;

        usuarios.forEach(usuario => {
            const option = document.createElement('option');
            option.value = usuario;
            option.textContent = usuario;
            usuariosSelect.appendChild(option);
        });

        // Ahora que todas las opciones están agregadas, establecemos la seleccionada
        usuariosSelect.value = usuarioSeleccionado;
    })
    .catch(error => console.error('Error al obtener usuarios:', error));
}

// Mostrar la ventana emergente cuando se hace clic en el ícono
abrirPopup.addEventListener('click', () => {
    popup.style.display = 'block';
    llenarUsuarios(); // Llenamos el desplegable con los usuarios solo cuando se muestra el popup
});

// Cerrar la ventana emergente cuando se hace clic en el botón de cerrar
cerrarPopup.addEventListener('click', () => {
    popup.style.display = 'none';
});

// Cerrar la ventana emergente si se hace clic fuera de la ventana
window.addEventListener('click', (event) => {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
});

// Acción al confirmar la selección del usuario
confirmarUsuario.addEventListener('click', () => {
    // Guardar el valor seleccionado en la variable usuarioSeleccionado
    usuarioSeleccionado = usuariosSelect.value;

    // Aquí puedes realizar la acción que necesites con el usuario seleccionado,
    // como enviar la selección al servidor o realizar otra lógica.

    // Cerrar la ventana emergente
    popup.style.display = 'none';
});

// Variables para almacenar gráficos
let canvas_visitas = null;
var canvas_visitas_acumuladas = null;
var canvas_tiempo_medio = null;
var canvas_navegadores = null;
var canvas_zonas = null;

function cargarD1(){
    document.getElementById("contenedorD1").style.display = "";
    document.getElementById("contenedorD2").style.display = "none";
    document.getElementById("contenedorD3").style.display = "none";
    document.getElementById("contenedorD4").style.display = "none";
    const bloques = document.querySelectorAll('.bloque');
    bloques.forEach(function(elemento) {
    elemento.style.display = 'none';
    });
    const d1 = document.querySelectorAll('.dashboard1');
    d1.forEach(function(div) {
    div.style.display = '';
    });

    total_visitas = document.getElementById('total_visitas');
    total_visitas.innerHTML = "<span class='numero'>-</span><span class='texto'>visitas</span>";

    fetch('http://127.0.0.1:5000/estadisticas/visitas/totales')
    .then(response => response.json())
    .then(data => {
        document.getElementById('total_visitas').innerHTML = `<span class='numero'>${data}</span><span class='texto'>visitas</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

    visitantes_unicos = document.getElementById('visitantes_unicos');
    visitantes_unicos.innerHTML = "<span class='numero'>-</span><span class='texto'>visitantes únicos</span>";

    fetch('http://127.0.0.1:5000/estadisticas/visitantes-unicos')
    .then(response => response.json())
    .then(data => {
        document.getElementById('visitantes_unicos').innerHTML = `<span class='numero'>${data}</span><span class='texto'>visitantes únicos</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

    media_visitas_usuario = document.getElementById('media_visitas_usuario');
    media_visitas_usuario.innerHTML = "<span class='numero'>-</span><span class='texto'>visitas/usuario</span>";

    fetch('http://127.0.0.1:5000/estadisticas/visitas/promedio-por-usuario')
    .then(response => response.json())
    .then(data => {
        document.getElementById('media_visitas_usuario').innerHTML = `<span class='numero'>${data}</span><span class='texto'>visitas/usuario</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));


    duracion_media_visitas = document.getElementById('duracion_media_visitas');
    duracion_media_visitas.innerHTML = "<span class='numero'>-</span><span class='texto'>segundos</span>";

    fetch('http://127.0.0.1:5000/estadisticas/tiempo/promedio-por-usuario')
    .then(response => response.json())
    .then(data => {
        minutos = (data/60).toFixed(2)
        document.getElementById('duracion_media_visitas').innerHTML = `<span class='numero'>${minutos}</span><span class='texto'>minutos</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));


    if (canvas_visitas) {
        canvas_visitas.destroy();  // Elimina el gráfico del canvas
    }

    // Función para generar datos aleatorios
    const obtenerDatos = (cantidad) => {
        return Array.from({ length: cantidad }, () => Math.floor(Math.random() * 100) + 100);
    };

    actualizarGraficoVisitas();

    // Acción al confirmar la selección del usuario
    confirmarUsuario.addEventListener('click', () => {
        usuarioSeleccionado = usuariosSelect.value; // Guardar la selección del usuario
        popup.style.display = 'none'; // Cerrar el popup
        actualizarGraficoVisitas(); // Llamar a la función para actualizar el gráfico aquí
    });

}

function cargarD2(){
    document.getElementById("contenedorD1").style.display = "none";
    document.getElementById("contenedorD2").style.display = "";
    document.getElementById("contenedorD3").style.display = "none";
    document.getElementById("contenedorD4").style.display = "none";
    const bloques = document.querySelectorAll('.bloque');
    bloques.forEach(function(elemento) {
    elemento.style.display = 'none';
    });
    const d2 = document.querySelectorAll('.dashboard2');
    d2.forEach(function(div) {
    div.style.display = '';
    });


    // Cargar Google Charts con el paquete Sankey
    google.charts.load('current', { packages: ['sankey'] });
    google.charts.setOnLoadCallback(cargarGraficoSankey);

    function cargarGraficoSankey() {
    // Asegúrate de que el contenedor esté visible o montado antes de dibujar
    fetch('http://127.0.0.1:5000/estadisticas/datos-flujo')
        .then(res => res.json())
        .then(data => {
        console.log("✅ Datos recibidos del backend:", data);
        dibujarSankey(data);
        })
        .catch(err => {
        console.error("❌ Error al obtener datos del Sankey:", err);
        });
    }

    function dibujarSankey(flujos) {
    const data = new google.visualization.DataTable();
    data.addColumn('string', 'Desde');
    data.addColumn('string', 'Hacia');
    data.addColumn('number', 'Porcentaje');

    flujos.forEach(flujo => {
        console.log(`Agregando fila: ${flujo.origen} → ${flujo.destino} (${flujo.porcentaje}%)`);
        data.addRow([flujo.origen, flujo.destino, flujo.porcentaje]);
    });

    const options = {
        height: 400,
        sankey: {
        node: {
            label: { fontSize: 14, color: '#333' }
        },
        link: {
            colorMode: 'gradient',
            colors: ['#76c7c0']
        }
        }
    };

    const chart = new google.visualization.Sankey(document.getElementById('grafico_flujo'));
    chart.draw(data, options);
    }

    top_elemento = document.getElementById('top_elemento');
    top_elemento.innerHTML = "<span class='numero'>-</span><span class='texto'>es el elemento con más interacciones (-)</span>";

    fetch('http://127.0.0.1:5000/estadisticas/elemento-mas-iteraciones')
    .then(response => response.json())
    .then(data => {
        elemento = data["tag_elemento"]
        interacciones = data["interacciones"]
        document.getElementById('top_elemento').innerHTML = `<span class='numero'>${elemento}</span><span class='texto'>es el elemento con más interacciones (${interacciones})</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));
    
    tasa_rebote = document.getElementById('tasa_rebote');
    tasa_rebote.innerHTML = "<span class='numero'>-%</span>";

    fetch('http://127.0.0.1:5000/estadisticas/tasa-rebote')
    .then(response => response.json())
    .then(data => {
        tr = data.toFixed(2)
        document.getElementById('tasa_rebote').innerHTML = `<span class='numero'>${tr}%</span><span class='texto'>Tasa de rebote</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

    media_paginas = document.getElementById('media_paginas');
    media_paginas.innerHTML = "<span class='numero'>-</span><span class='texto'>páginas/usuario</span>";

    fetch('http://127.0.0.1:5000/estadisticas/paginas/promedio-por-sesion')
    .then(response => response.json())
    .then(data => {
        npu = data.toFixed(2)
        document.getElementById('media_paginas').innerHTML = `<span class='numero'>${npu}</span><span class='texto'>páginas/usuario</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

    media_interacciones = document.getElementById('media_interacciones');
    media_interacciones.innerHTML = "<span class='numero'>-</span><span class='texto'>interacciones/usuario</span>";

    fetch('http://127.0.0.1:5000/estadisticas/iteraciones/promedio-por-usuario')
    .then(response => response.json())
    .then(data => {
        niu = data.toFixed(2)
        document.getElementById('media_interacciones').innerHTML = `<span class='numero'>${niu}</span><span class='texto'>interacciones/usuario</span>`;
    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

}

function cargarD3(){
    document.getElementById("contenedorD1").style.display = "none";
    document.getElementById("contenedorD2").style.display = "none";
    document.getElementById("contenedorD3").style.display = "";
    document.getElementById("contenedorD4").style.display = "none";
    const bloques = document.querySelectorAll('.bloque');
    bloques.forEach(function(elemento) {
    elemento.style.display = 'none';
    });
    const d3 = document.querySelectorAll('.dashboard3');
    d3.forEach(function(div) {
    div.style.display = '';
    });

    if (canvas_visitas_acumuladas) {
        canvas_visitas_acumuladas.destroy();  // Elimina el gráfico del canvas
    }
    if (canvas_tiempo_medio) {
        canvas_tiempo_medio.destroy();  // Elimina el gráfico del canvas
    }
    if (canvas_navegadores) {
        canvas_navegadores.destroy();  // Elimina el gráfico del canvas
    }
    if (canvas_zonas) {
        canvas_zonas.destroy();  // Elimina el gráfico del canvas
    }

    fetch('http://127.0.0.1:5000/estadisticas/navegadores/porcentajes')
    .then(response => response.json())
    .then(respuesta => {
        
        let navs = Object.keys(respuesta);
        let porcentajes = Object.values(respuesta);

        const datosNavegadores = {
        labels: navs,
        datasets: [{
            label: 'Navegadores',
            data: porcentajes,  // Porcentajes de uso de cada navegador
            backgroundColor: [
                '#FF5733',  // Color para Chrome
                '#33FF57',  // Color para Firefox
                '#3357FF',  // Color para Safari
                '#FF33A1',  // Color para Edge
                '#F0E68C'   // Color para "Otros"
            ],
            hoverOffset: 4
        }]
    };

    const config = {
        type: 'pie', // Tipo de gráfico: 'pie' para gráfico de sectores
        data: datosNavegadores,
        options: {
            responsive: true, // Hacer que el gráfico sea responsivo
            maintainAspectRatio: false, // Evitar que mantenga la relación de aspecto predeterminada
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                        }
                    }
                }
            }
        }
    };

    // Obtener el contexto del canvas
    const ctx = document.getElementById('grafico_navegadores').getContext('2d');

    // Crear el gráfico de sectores
    canvas_navegadores = new Chart(ctx, config);

        })
    .catch(error => console.error('Error al obtener total de visitas:', error));



    fetch('http://127.0.0.1:5000/estadisticas/zonas-horarias/porcentajes')
    .then(response => response.json())
    .then(respuesta => {
        
        let zonas = Object.keys(respuesta);
        let porcentajes = Object.values(respuesta);

        // Datos para el gráfico de zonas geográficas
        const datosZonas = {
            labels: zonas,
            datasets: [{
                label: 'Porcentaje de visitas',
                data: porcentajes,
                backgroundColor: [
                    '#FF5733',  // Rojo vibrante para Norteamérica
                    '#33FF57',  // Verde para Europa
                    '#3357FF',  // Azul para Asia
                    '#FF33A1',  // Rosado para América Latina
                    '#F0E68C'   // Amarillo para África
                ],
                borderColor: 'black', // Bordes negros para todos los segmentos
                borderWidth: 2,
                hoverOffset: 4 // Efecto de resaltado al pasar el mouse
            }]
        };
        
        const configZonas = {
            type: 'pie',
            data: datosZonas,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.label + ': ' + tooltipItem.raw + '%';
                            }
                        }
                    }
                }
            }
        };
        
        // Crear el gráfico con las nuevas configuraciones
        canvas_zonas = new Chart(document.getElementById("grafico_zonas"), configZonas);



    })
    .catch(error => console.error('Error al obtener total de visitas:', error));

    actualizarGraficoAcumuladas();

    // Acción al confirmar la selección del usuario
    confirmarUsuario.addEventListener('click', () => {
        usuarioSeleccionado = usuariosSelect.value; // Guardar la selección del usuario
        popup.style.display = 'none'; // Cerrar el popup
        actualizarGraficoAcumuladas(); // Llamar a la función para actualizar el gráfico aquí
    });

    actualizarGraficoTiempoMedio();

    // Acción al confirmar la selección del usuario
    confirmarUsuario.addEventListener('click', () => {
        usuarioSeleccionado = usuariosSelect.value; // Guardar la selección del usuario
        popup.style.display = 'none'; // Cerrar el popup
        actualizarGraficoTiempoMedio(); // Llamar a la función para actualizar el gráfico aquí
    });
    
}

function cargarD4(){
    document.getElementById("contenedorD1").style.display = "none";
    document.getElementById("contenedorD2").style.display = "none";
    document.getElementById("contenedorD3").style.display = "none";
    document.getElementById("contenedorD4").style.display = "";
    const bloques = document.querySelectorAll('.bloque');
    bloques.forEach(function(elemento) {
    elemento.style.display = 'none';
    });
    const d3 = document.querySelectorAll('.dashboard4');
    d3.forEach(function(div) {
    div.style.display = '';
    });

    fetch('http://127.0.0.1:5000/sesiones/direcciones-mac')
    .then(response => response.json())
    .then(data => {

    const listaMacs = document.getElementById('macs');
    // Limpiar cualquier contenido previo
    listaMacs.innerHTML = '';
    
    // Insertar cada dirección MAC en la lista
    data.forEach(mac => {
      const li = document.createElement('li');
      li.className = 'item-mac'; // Añadir la clase de estilo
      li.textContent = mac; // El contenido de la dirección MAC
      li.dataset.mac = mac;
      listaMacs.appendChild(li);
    });

    })
    .catch(error => console.error('Error al obtener usuarios:', error));


    const macList = document.getElementById('macs');
    const sesionesList = document.getElementById('sesiones');
    const infoDiv = document.getElementById('informacion');

    // Delegar eventos en los <li> del ul#macs
    macList.addEventListener('click', (event) => {
        const clickedItem = event.target;

        if (clickedItem.tagName === 'LI') {
        const direccionMac = clickedItem.dataset.mac;

        // Limpiar sesiones existentes
        sesionesList.innerHTML = '';

            fetch('http://127.0.0.1:5000/sesiones/tiempo/direcciones-mac', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ direccion_mac: direccionMac })
            })
            .then(response => response.json())
            .then(data => {
                sesionesList.innerHTML = ''; // Limpiar sesiones previas
            
                // Si hay sesiones disponibles, las mostramos
                if (Array.isArray(data) && data.length > 0) {
                    data.forEach(sesion => {
                        const li = document.createElement('li');
                        li.className = 'item-sesion';
                        li.textContent = `Sesión ${sesion.id}`;
                        li.dataset.sesionId = sesion.id;
                        sesionesList.appendChild(li);
                    });
                } else {
                    sesionesList.innerHTML = '<li>No hay sesiones disponibles</li>';
                }
            
                // Crear y formatear la información para el div#informacion
                const infoDiv = document.getElementById('informacion');
                infoDiv.innerHTML = ''; // Limpiar contenido previo
            
                const ul = document.createElement('ul'); // Crear lista <ul> para las sesiones
            
                data.forEach(sesion => {
                    const li = document.createElement('li'); // Crear elemento <li> para cada sesión
                    const fechaFormateada = formatearFecha(sesion.tiempo_entrada); // Formatear la fecha
                    li.textContent = `${fechaFormateada}: Sesión ${sesion.id}`; // Texto con fecha y sesión
                    ul.appendChild(li); // Añadir el <li> a la lista
                });
            
                infoDiv.appendChild(ul); // Añadir la lista al div#informacion
            })
            .catch(error => {
                console.error('Error al obtener sesiones:', error);
                sesionesList.innerHTML = '<li>Error al cargar sesiones</li>';
            });
        }

    });


    sesionesList.addEventListener('click', (event) => {
        const clickedItem = event.target;

        if (clickedItem.tagName === 'LI') {
            const idSesion = clickedItem.dataset.sesionId;

            fetch('http://127.0.0.1:5000/iteraciones/sesion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id_sesion: idSesion })
            })
            .then(response => response.json())
            .then(data => {
                const infoDiv = document.getElementById('informacion');
                infoDiv.innerHTML = ''; // Limpiar contenido previo

                if (Array.isArray(data) && data.length > 0) {
                    const ul = document.createElement('ul'); // Crear lista <ul>

                    data.forEach(interaccion => {
                        const li = document.createElement('li');
                        const fechaFormateada = formatearFecha(interaccion.tiempo);
                        let texto = `${fechaFormateada}: `;

                        if (interaccion.tipo_evento === 'interaccion') {
                            texto += `Se ha interaccionado con "${interaccion.elemento}".`;
                        } else if (interaccion.tipo_evento === 'cambio_pagina') {
                            texto += `Se ha cambiado de la página "${interaccion.pagina_inicial}" a "${interaccion.pagina_destino}".`;
                        } else if (interaccion.tipo_evento === 'formulario') {
                            texto += `Se ha respondido a la pregunta "${interaccion.pregunta}" con "${interaccion.respuesta}".`;
                        }

                        li.textContent = texto;
                        ul.appendChild(li);
                    });

                    infoDiv.appendChild(ul); // Añadir la lista al div#informacion
                } else {
                    infoDiv.textContent = 'No hay interacciones disponibles para esta sesión.';
                }
            })
            .catch(error => {
                console.error('Error al obtener interacciones:', error);
                infoDiv.textContent = 'Error al cargar las interacciones.';
            });
        }
    });

}

window.onload = cargarD1;

