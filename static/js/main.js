import { loadList, loadDetails } from './dataLoader.js';
import { elements, setupEventListeners } from './uiElements.js';
import { closeDetails, resetLayout } from './uiHelpers.js';
import { loadSchedule } from './schedule.js';

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    
    window.loadDetails = loadDetails;
    window.exportStudentSchedule = (studentId) => {
        window.location.href = `students/${studentId}/export-schedule/`;
    };
    window.exportSpecialistSchedule = (specialistId, period) => {
        window.location.href = `specialists/${specialistId}/export-schedule/?period=${period}`;
    };
    window.toggleRelatives = toggleRelatives;
    window.closeDetails = closeDetails;

    loadList('students');
});


function toggleRelatives(studentId) {
    const studentInfo = document.getElementById('studentInfo');
    const relativesInfo = document.getElementById('relativesInfo');
    const toggleBtn = document.getElementById('toggleRelativesBtn');

    if (studentInfo.style.display !== 'none') {
        studentInfo.style.display = 'none';
        relativesInfo.style.display = 'block';
        toggleBtn.textContent = 'Данные пользователя';
    } else {
        studentInfo.style.display = 'block';
        relativesInfo.style.display = 'none';
        toggleBtn.textContent = 'Родственники';
    }
}

// Экспортируем функцию loadSchedule для использования в других модулях
export { loadSchedule };