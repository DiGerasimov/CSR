import { elements } from './uiElements.js';
import { generateListHTML, generateDetailsHTML } from './htmlGenerators.js';
import { handleError, resetLayout } from './uiHelpers.js';

export async function loadList(type, filter = '') {
    try {
        const [items, filterOptions] = await Promise.all([
            fetchData(`/${type}/?${getFilterParam(type)}=${filter}`),
            fetchData(`/${type}/${getFilterOptionsEndpoint(type)}/`)
        ]);

        const html = generateListHTML(type, items, filterOptions, filter);
        elements.listContainer.innerHTML = html;

        document.getElementById(`${type}Filter`).addEventListener('change', (e) => {
            loadList(type, e.target.value);
        });

        elements.detailContainer.innerHTML = '';
        resetLayout();
    } catch (error) {
        handleError(error, elements.listContainer);
    }
}

export async function loadDetails(type, id) {
    try {
        const item = await fetchData(`/${type}/${id}/`);
        const html = generateDetailsHTML(type, item);
        elements.detailContainer.innerHTML = html;
        showDetails();
    } catch (error) {
        handleError(error, elements.detailContainer);
    }
}

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Ошибка при загрузке данных: ${response.statusText}`);
    return await response.json();
}

function getFilterParam(type) {
    return type === 'students' ? 'age_group' : 'position';
}

function getFilterOptionsEndpoint(type) {
    return type === 'students' ? 'age-groups' : 'positions';
}

function showDetails() {
    elements.listContainer.style.width = '70%';
    elements.detailContainer.style.display = 'block';
    document.body.classList.add('details-open');
}