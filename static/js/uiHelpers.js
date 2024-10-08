import { elements } from './uiElements.js';

export function handleError(error, container) {
    console.error('Ошибка:', error);
    container.innerHTML = `<p>Произошла ошибка при загрузке данных: ${error.message}</p>`;
}

export function closeDetails() {
    resetLayout();
}

export function resetLayout() {
    elements.listContainer.style.width = '100%';
    elements.detailContainer.style.display = 'none';
    document.body.classList.remove('details-open');
}