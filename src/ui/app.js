const API_URL = 'http://localhost:8000';

const steps = [
  {
    name: 'initial_dependencies',
    title: 'Instalar dependencias',
    description: 'Prepara Scorpio y sus dependencias iniciales.'
  },
  {
    name: 'system_reboot',
    title: 'Reiniciar el sistema',
    description: 'Reinicia la Raspberry Pi para aplicar los cambios.'
  },
  {
    name: 'docker_dependencies',
    title: 'Iniciar infraestructura',
    description: 'Configura Docker y levanta los servicios de Scorpio.'
  }
];

async function refresh() {
  const response = await fetch(`${API_URL}/api/status`);
  if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

  const state = await response.json();
  const currentStep = state.completed ? null : state.current_step;
  const currentIndex = state.completed
    ? steps.length
    : steps.findIndex(step => step.name === currentStep);

  const completedCount = Math.max(0, currentIndex);
  const progress = state.completed ? 100 : (completedCount / steps.length) * 100;

  document.querySelector('#progress-bar').style.width = `${progress}%`;
  document.querySelector('#progress-label').textContent = state.completed
    ? 'Instalación completa'
    : `${completedCount} de ${steps.length} completados`;

  document.querySelector('#steps').innerHTML = steps.map((step, index) => {
    const done = state.completed || index < currentIndex;
    const active = !state.completed && step.name === currentStep;
    const statusClass = done ? 'done' : active ? 'active' : 'pending';

    return `<li class="step ${statusClass}">
      <span class="step-icon">${done ? '✓' : index + 1}</span>
      <div>
        <h3 class="step-title">${step.title}</h3>
        <p class="step-description">${done ? 'Paso completado correctamente.' : step.description}</p>
      </div>
      ${active ? `<button type="button" onclick="runStep('${step.name}')">${step.name === 'system_reboot' ? 'Reiniciar' : 'Iniciar'}</button>` : ''}
    </li>`;
  }).join('');

  if (state.completed) showMessage('Scorpio está configurado y listo para utilizar.', 'success');
}

async function runStep(stepName) {
  const step = steps.find(item => item.name === stepName);
  const confirmation = stepName === 'system_reboot'
    ? 'La Raspberry Pi se reiniciará y perderás la conexión temporalmente. ¿Confirmas que deseas continuar?'
    : `Se ejecutará el paso “${step.title}”. ¿Confirmas que deseas continuar?`;

  if (!confirm(confirmation)) return;

  const button = document.querySelector('.step.active button');
  if (button) {
    button.disabled = true;
    button.textContent = 'Procesando…';
  }

  showMessage('Ejecutando el paso. Esto puede tardar unos minutos…', 'info');

  try {
    const response = await fetch(`${API_URL}/api/confirm_step`, {
      method: 'POST',
      body: JSON.stringify({ step: stepName })
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'No se pudo ejecutar el paso.');

    showMessage(result.message || 'Paso completado correctamente.', 'success');
    await refresh();
  } catch (error) {
    showMessage(error.message || 'No se pudo conectar con el servidor.', 'error');
    if (button) {
      button.disabled = false;
      button.textContent = stepName === 'system_reboot' ? 'Reiniciar' : 'Iniciar';
    }
  }
}

function showMessage(text, type) {
  const message = document.querySelector('#message');
  message.textContent = text;
  message.className = `message ${type}`;
  message.hidden = false;
  sessionStorage.setItem('scorpio-message', JSON.stringify({ text, type }));
}

function restoreMessage() {
  const savedMessage = sessionStorage.getItem('scorpio-message');
  if (!savedMessage) return;

  try {
    const { text, type } = JSON.parse(savedMessage);
    showMessage(text, type);
  } catch {
    sessionStorage.removeItem('scorpio-message');
  }
}

restoreMessage();
refresh().catch(() => showMessage('No se pudo conectar con el servidor de Scorpio.', 'error'));
