import { loadList } from './dataLoader.js';
import { loadSchedule } from './schedule.js';

export const elements = {
    studentsBtn: document.getElementById('studentsBtn'),
    specialistsBtn: document.getElementById('specialistsBtn'),
    scheduleBtn: document.getElementById('scheduleBtn'),
    listContainer: document.getElementById('listContainer'),
    detailContainer: document.getElementById('detailContainer'),
    scheduleContainer: document.getElementById('scheduleContainer')
};

export function setupEventListeners() {
    elements.studentsBtn.addEventListener('click', () => {
        loadList('students');
        hideSchedule();
    });
    elements.specialistsBtn.addEventListener('click', () => {
        loadList('specialists');
        hideSchedule();
    });
    elements.scheduleBtn.addEventListener('click', loadSchedule);
}

function hideSchedule() {
    elements.scheduleContainer.style.display = 'none';
    elements.listContainer.style.display = 'block';
}