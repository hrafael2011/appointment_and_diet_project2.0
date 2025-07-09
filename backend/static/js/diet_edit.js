document.addEventListener('DOMContentLoaded', function () {
    const editableCells = document.querySelectorAll('.editable-cell');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    editableCells.forEach(cell => {
        cell.addEventListener('dblclick', function () {
            const currentValue = cell.textContent.trim();
            const dietaId = cell.closest('.dieta-container').dataset.dietaId;
            const dia = cell.closest('tr').dataset.dia;
            const campo = cell.dataset.campo;

            if (cell.querySelector('textarea')) return;

            const textarea = document.createElement('textarea');
            textarea.className = 'w-full h-full border-none bg-[#f9f5ff] rounded p-1 focus:outline-none focus:ring-2 focus:ring-purple-300 resize-none';
            textarea.value = currentValue;
            textarea.rows = 3;

            textarea.addEventListener('blur', function () {
                const newValue = textarea.value.trim();

                if (newValue === currentValue) {
                    cell.textContent = currentValue;
                    return;
                }

                cell.textContent = newValue;
                cell.classList.add('modified-cell');
                cell.closest('.dieta-container').classList.add('has-changes');
            });

            textarea.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    textarea.blur();
                } else if (e.key === 'Escape') {
                    cell.textContent = currentValue;
                }
            });

            cell.textContent = '';
            cell.appendChild(textarea);
            textarea.focus();
            textarea.select();
        });
    });

    document.querySelectorAll('[id^="guardar-dieta-"]').forEach(button => {
        const dietaId = button.id.replace('guardar-dieta-', '');

        button.addEventListener('click', function () {
            guardarDieta(dietaId);
        });
    });
});

function guardarDieta(dietaId) {
    const dietaContainer = document.querySelector(`[data-dieta-id="${dietaId}"]`);

    if (!dietaContainer) {
        console.error(`No se encontró el contenedor de dieta con ID: ${dietaId}`);
        return;
    }

    const filas = dietaContainer.querySelectorAll("tr[data-dia]");
    const dietaData = { dias: [] };

    filas.forEach(fila => {
        const dia = parseInt(fila.dataset.dia);
        const desayuno = fila.querySelector('[data-campo="desayuno"]').textContent.trim();
        const almuerzo = fila.querySelector('[data-campo="almuerzo"]').textContent.trim();
        const merienda = fila.querySelector('[data-campo="merienda"]').textContent.trim();
        const cena = fila.querySelector('[data-campo="cena"]').textContent.trim();

        dietaData.dias.push({
            "dia": dia,
            "desayuno": desayuno,
            "almuerzo": almuerzo,
            "merienda": merienda,
            "cena": cena
        });

        const formData = new FormData();
        formData.append('dieta_id', dietaId);
        formData.append('dia', dia);
        formData.append('desayuno', desayuno);
        formData.append('almuerzo', almuerzo);
        formData.append('merienda', merienda);
        formData.append('cena', cena);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch("/actualizar-dieta/", {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fila.querySelectorAll('.modified-cell').forEach(cell => {
                        cell.classList.remove('modified-cell');
                    });

                    if (parseInt(fila.dataset.dia) === filas.length) {
                        const notification = document.createElement('div');
                        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg transition-opacity duration-500';
                        notification.textContent = 'Dieta actualizada correctamente';
                        document.body.appendChild(notification);

                        setTimeout(() => {
                            notification.style.opacity = '0';
                            setTimeout(() => notification.remove(), 500);
                        }, 3000);
                    }
                } else {
                    alert("Error al actualizar: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error en la solicitud:", error);
                alert("Error de conexión");
            });
    });
}
