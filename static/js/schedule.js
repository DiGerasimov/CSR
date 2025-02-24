import { elements } from './uiElements.js';
import { loadList } from './dataLoader.js';
import { API_URLS } from './config.js';

let currentDate = new Date();
let currentView = 'month';
let currentSpecialist = '';
let currentPosition = '';
let specialists = [];
let positions = [];
let scheduleData = []; 

export function loadSchedule() {
    elements.scheduleContainer.innerHTML = generateScheduleHTML();
    elements.scheduleContainer.style.display = 'block';
    elements.listContainer.style.display = 'none';
    elements.detailContainer.style.display = 'none';
    
    setupScheduleEventListeners();
    loadSpecialistsAndPositions();
}

function generateScheduleHTML() {
    return `
        <div class="schedule-wrapper">
            <div class="schedule-header">
                <div class="schedule-nav">
                    <button id="prevBtn">&lt;</button>
                    <h2 id="currentPeriod"></h2>
                    <button id="nextBtn">&gt;</button>
                </div>
                <div class="schedule-controls">
                    <div class="schedule-view-toggle">
                        <button id="weekViewBtn">Неделя</button>
                        <button id="monthViewBtn" class="active">Месяц</button>
                    </div>
                    <div class="schedule-filters">
                        <input type="date" id="datePicker" required>
                        <select id="positionFilter">
                            <option value="">Все должности</option>
                        </select>
                        <select id="specialistFilter">
                            <option value="">Все специалисты</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="schedule-info">
                <span id="eventCount" class="event-count"></span>
                <div class="schedule-legend">
                    <div class="legend-item"><span class="color-box event-current"></span> Текущее</div>
                    <div class="legend-item"><span class="color-box event-past"></span> Прошедшее</div>
                    <div class="legend-item"><span class="color-box"></span> Предстоящее</div>
                </div>
            </div>
            <div class="schedule-grid-container">
                <div id="scheduleGrid" class="schedule-grid"></div>
            </div>
        </div>
        <div id="eventDetails" class="event-details"></div>
    `;
}

function setupScheduleEventListeners() {
    document.getElementById('prevBtn').addEventListener('click', () => navigateSchedule('prev'));
    document.getElementById('nextBtn').addEventListener('click', () => navigateSchedule('next'));
    document.getElementById('weekViewBtn').addEventListener('click', () => changeView('week'));
    document.getElementById('monthViewBtn').addEventListener('click', () => changeView('month'));
    document.getElementById('datePicker').addEventListener('change', (e) => {
        currentDate = new Date(e.target.value);
        updateSchedule();
    });
    document.getElementById('positionFilter').addEventListener('change', (e) => {
        currentPosition = e.target.value;
        updateSchedule();
    });
    document.getElementById('specialistFilter').addEventListener('change', (e) => {
        currentSpecialist = e.target.value;
        updateSchedule();
    });

    document.getElementById('positionFilter').addEventListener('change', (e) => {
        currentPosition = e.target.value;
        updateSpecialistFilter();
        updateSchedule();
    });
    document.getElementById('specialistFilter').addEventListener('change', (e) => {
        currentSpecialist = e.target.value;
        if (currentSpecialist) {
            currentPosition = '';
            document.getElementById('positionFilter').value = '';
            document.getElementById('positionFilter').disabled = true;
        } else {
            document.getElementById('positionFilter').disabled = false;
        }
        updateSchedule();
    });
}

// ... существующий код ...

async function loadSpecialistsAndPositions() {
    try {
        const specialistsResponse = await fetch(API_URLS.SPECIALISTS);
        specialists = await specialistsResponse.json();

        const positionsResponse = await fetch(API_URLS.POSITIONS);
        positions = await positionsResponse.json();

        updatePositionFilter();
        updateSpecialistFilter();
        updateSchedule();
    } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
    }
}

async function updateSchedule() {
    const scheduleGrid = document.getElementById('scheduleGrid');
    const currentPeriod = document.getElementById('currentPeriod');
    const datePicker = document.getElementById('datePicker');
    const eventCount = document.getElementById('eventCount');

    let startDate, endDate;

    if (currentView === 'week') {
        startDate = getWeekStart(currentDate);
        endDate = new Date(startDate);
        endDate.setDate(endDate.getDate() + 6);
    } else {
        startDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
        endDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    }

    const url = new URL(API_URLS.SCHEDULE);
    url.searchParams.append('start_date', startDate.toISOString().split('T')[0]);
    url.searchParams.append('end_date', endDate.toISOString().split('T')[0]);
    url.searchParams.append('view', currentView);

    if (currentSpecialist) {
        url.searchParams.append('specialist_id', currentSpecialist);
    }

    if (currentPosition) {
        url.searchParams.append('position', currentPosition);
    }

    try {
        const response = await fetch(url);
        scheduleData = await response.json();

        if (currentView === 'week') {
            scheduleGrid.innerHTML = generateWeekSchedule(scheduleData);
            currentPeriod.textContent = getWeekRangeText(currentDate);
        } else {
            scheduleGrid.innerHTML = generateMonthSchedule(scheduleData);
            currentPeriod.textContent = getMonthYearText(currentDate);
        }

        // Обновляем счетчик занятий
        const eventCount = document.getElementById('eventCount');
        eventCount.textContent = `Занятий: ${scheduleData.length}`;

        datePicker.value = currentDate.toISOString().split('T')[0];
    } catch (error) {
        console.error('Ошибка при загрузке расписания:', error);
    }
}

function updatePositionFilter() {
    const positionFilter = document.getElementById('positionFilter');
    positionFilter.innerHTML = '<option value="">Все должности</option>';
    positions.forEach(position => {
        positionFilter.innerHTML += `<option value="${position.name}">${position.name}</option>`;
    });
}

function updateSpecialistFilter() {
    const specialistFilter = document.getElementById('specialistFilter');
    specialistFilter.innerHTML = '<option value="">Все специалисты</option>';
    specialists.filter(specialist => !currentPosition || specialist.position.name === currentPosition)
               .forEach(specialist => {
                   specialistFilter.innerHTML += `<option value="${specialist.id}">${specialist.full_name}</option>`;
               });
}

function navigateSchedule(direction) {
    if (currentView === 'week') {
        currentDate.setDate(currentDate.getDate() + (direction === 'prev' ? -7 : 7));
    } else {
        currentDate.setMonth(currentDate.getMonth() + (direction === 'prev' ? -1 : 1));
    }
    updateSchedule();
}

function changeView(view) {
    currentView = view;
    document.getElementById('weekViewBtn').classList.toggle('active', view === 'week');
    document.getElementById('monthViewBtn').classList.toggle('active', view === 'month');
    updateSchedule();
}


function generateMonthSchedule(scheduleData) {
    const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    const lastDay = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - startDate.getDay() + 1);

    let html = '<div class="schedule-grid schedule-grid-month">';
    html += '<div class="schedule-cell header">Пн</div><div class="schedule-cell header">Вт</div><div class="schedule-cell header">Ср</div><div class="schedule-cell header">Чт</div><div class="schedule-cell header">Пт</div><div class="schedule-cell header">Сб</div><div class="schedule-cell header">Вс</div>';

    while (startDate <= lastDay) {
        for (let i = 0; i < 7; i++) {
            const cellDate = new Date(startDate);
            if (cellDate.getMonth() === currentDate.getMonth()) {
                const dateString = cellDate.toISOString().split('T')[0];
                const dayEvents = scheduleData.filter(event => 
                    new Date(event.time_start).toISOString().split('T')[0] === dateString
                );
                html += `<div class="schedule-cell">
                    <div class="date">${cellDate.getDate()}</div>
                    ${dayEvents.map(event => generateEventHTML(event)).join('')}
                </div>`;
            } else {
                html += '<div class="schedule-cell other-month"></div>';
            }
            startDate.setDate(startDate.getDate() + 1);
        }
    }

    html += '</div>';
    return html;
}


// ... существующий код ...

function generateWeekSchedule(scheduleData) {
    const weekStart = getWeekStart(currentDate);
    let html = '<div class="schedule-grid schedule-grid-week">';
    html += '<div class="schedule-cell header"></div>';
    
    for (let i = 0; i < 7; i++) {
        const day = new Date(weekStart);
        day.setDate(weekStart.getDate() + i);
        html += `<div class="schedule-cell header">${getDayName(day)}<br>${day.getDate()}</div>`;
    }

    // Получаем уникальные времена начала событий
    const uniqueStartTimes = [...new Set(scheduleData.map(event => {
        const startTime = new Date(event.time_start);
        return `${startTime.getHours()}:${startTime.getMinutes().toString().padStart(2, '0')}`;
    }))].sort();

    // Генерируем ячейки для каждого уникального времени
    uniqueStartTimes.forEach(time => {
        html += `<div class="schedule-cell time">${time}</div>`;
        for (let i = 0; i < 7; i++) {
            const cellDate = new Date(weekStart);
            cellDate.setDate(weekStart.getDate() + i);
            const [hours, minutes] = time.split(':').map(Number);
            cellDate.setHours(hours, minutes, 0, 0);
            const cellEvents = scheduleData.filter(event => {
                const eventStart = new Date(event.time_start);
                return eventStart.getDate() === cellDate.getDate() && 
                       eventStart.getHours() === hours &&
                       eventStart.getMinutes() === minutes;
            });
            html += `<div class="schedule-cell">${cellEvents.map(event => generateEventHTML(event)).join('')}</div>`;
        }
    });

    html += '</div>';
    return html;
}



function formatTime(date) {
    const adjustedDate = new Date(date.getTime() + 3 * 60 * 60 * 1000); // Добавляем 3 часа
    return adjustedDate.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' });
}

function formatDateTime(date) {
    const adjustedDate = new Date(date.getTime() + 3 * 60 * 60 * 1000); // Добавляем 3 часа
    return adjustedDate.toLocaleString('ru-RU', { timeZone: 'UTC' });
}

function getWeekStart(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

function getDayName(date) {
    return date.toLocaleDateString('ru-RU', { weekday: 'short' });
}

function getWeekRangeText(date) {
    const weekStart = getWeekStart(date);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 6);
    return `${weekStart.toLocaleDateString('ru-RU')} - ${weekEnd.toLocaleDateString('ru-RU')}`;
}

function getMonthYearText(date) {
    return date.toLocaleDateString('ru-RU', { month: 'long', year: 'numeric' });
}



function getEventColor(startDate, endDate) {
    const now = new Date();
    if (startDate <= now && now < endDate) {
        return 'event-current';
    } else if (endDate <= now) {
        return 'event-past';
    }
    return '';
}

function generateEventHTML(event) {
    const startTime = new Date(event.time_start);
    const endTime = new Date(event.time_end);
    
    let eventText = `<strong>${formatTime(startTime)}-${formatTime(endTime)}</strong><br>`;
    
    // Улучшаем отображение специалистов с должностями
    const specialistsShort = event.specialists.map(specialist => {
        // Проверяем, содержит ли строка с именем специалиста информацию о должности в скобках
        const roleMatch = specialist.match(/\((.*?)\)$/);
        let displayName = specialist;
        
        if (!roleMatch) {
            // Если должности нет в строке специалиста, проверяем название события
            const eventRoleMatch = event.name ? event.name.match(/\((.*?)\)/) : null;
            const role = eventRoleMatch ? eventRoleMatch[1] : '';
            
            // Получаем только имя специалиста (без должности)
            const nameParts = specialist.split(' ');
            if (nameParts.length >= 2) {
                // Берем фамилию полностью и первую букву имени
                displayName = `${nameParts[0]} ${nameParts.length > 1 ? nameParts[1][0] + '.' : ''}`;
                // Добавляем должность, если она есть
                if (role) {
                    displayName += ` (${role})`;
                }
            }
        } else {
            // Если должность уже есть в строке специалиста, форматируем отображение
            const name = specialist.replace(/\s*\(.*?\)$/, ''); // Удаляем должность из имени
            const nameParts = name.split(' ');
            if (nameParts.length >= 2) {
                // Берем фамилию полностью и первую букву имени
                displayName = `${nameParts[0]} ${nameParts.length > 1 ? nameParts[1][0] + '.'  : ''} ${roleMatch[0]}`;
            }
        }
        
        return displayName;
    }).join('<br>');
    
    eventText += specialistsShort;
    
    // Добавляем информацию о кабинете
    if (event.room) {
        eventText += `<br>Каб. ${event.room}`;
    }
    
    // Добавляем список детей более компактно
    if (event.students && event.students.length > 0) {
        eventText += `<br><small>Дети (${event.students.length}): `;
        // Берем только первые 3 имени, чтобы не перегружать карточку
        const studentNames = event.students.slice(0, 3).map(student => {
            const name = student.full_name.split(' ')[0];
            return name;
        });
        
        if (event.students.length > 3) {
            eventText += studentNames.join(', ') + '...';
        } else {
            eventText += studentNames.join(', ');
        }
        eventText += '</small>';
    }
    
    const eventColor = getEventColor(startTime, endTime);
    
    // Добавляем title с полной информацией для отображения при наведении
    const fullTitle = `${event.name}
${event.specialists.join('\n')}
Кабинет: ${event.room || 'Не указан'}
Дети: ${event.students.map(s => s.full_name).join(', ')}
Дополнительная информация: ${event.additional_info || ''}`;
    
    return `<div class="schedule-event ${eventColor}" onclick="showEventDetails('${event.id}')" title="${fullTitle}">${eventText}</div>`;
}

window.showEventDetails = function(eventId) {
    const event = scheduleData.find(e => e.id === eventId);
    if (!event) {
        console.error('Событие не найдено:', eventId);
        return;
    }

    // Отладочная информация для проверки структуры данных
    console.log('Event data:', event);

    const eventDetails = document.getElementById('eventDetails');
    const modalOverlay = document.getElementById('modalOverlay');
    
    // Улучшенная логика для отображения специалистов с должностями
    let specialistsHtml = '';
    
    // Проверяем, есть ли в данных специалиста информация о должности
    specialistsHtml = event.specialists.map(specialist => {
        // Проверяем, содержит ли строка с именем специалиста информацию о должности в скобках
        const roleMatch = specialist.match(/\((.*?)\)$/);
        
        if (roleMatch) {
            // Если должность уже есть в строке специалиста, просто возвращаем как есть
            return `
                <tr>
                    <th>ФИО специалиста</th>
                    <td>${specialist}</td>
                </tr>
            `;
        } else {
            // Если должности нет в строке специалиста, проверяем название события
            const eventRoleMatch = event.name ? event.name.match(/\((.*?)\)/) : null;
            const role = eventRoleMatch ? eventRoleMatch[1] : '';
            
            return `
                <tr>
                    <th>ФИО специалиста</th>
                    <td>${specialist}${role ? ` (${role})` : ''}</td>
                </tr>
            `;
        }
    }).join('');

    // Всегда добавляем строку с дополнительной информацией
    const additionalInfoHtml = `
        <tr>
            <th>Дополнительная информация</th>
            <td>${event.additional_info || ''}</td>
        </tr>
    `;

    eventDetails.innerHTML = `
        <h3>Подробная информация</h3>
        <button onclick="closeEventDetails()" class="close-btn">✖️</button>
        <table>
            <tr><th>Название</th><td>${event.name}</td></tr>
            ${specialistsHtml}
            <tr><th>Кабинет</th><td>${event.room}</td></tr>
            <tr><th>Время начала</th><td>${formatDateTime(new Date(event.time_start))}</td></tr>
            <tr><th>Время окончания</th><td>${formatDateTime(new Date(event.time_end))}</td></tr>
            ${additionalInfoHtml}
        </table>
        <div class="action-buttons">
            <button onclick="duplicateSchedule('${event.id}')" class="duplicate-btn">Дублировать на следующие недели</button>
        </div>
        <h4>Посещаемость обучающихся:</h4>
        <form id="attendanceForm">
            <table class="attendance-table">
                <thead>
                    <tr>
                        <th>Обучающийся</th>
                        <th>Присутствие</th>
                    </tr>
                </thead>
                <tbody>
                    ${event.students.map(student => `
                        <tr>
                            <td>${student.full_name}</td>
                            <td>
                                <input type="checkbox" name="student_${student.id}" value="${student.id}" ${event.attendances.find(a => a.student_id === student.id)?.is_present ? 'checked' : ''}>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <div style="margin-top: 20px;"></div>
            <button type="submit" class="save-attendance-btn">Сохранить посещаемость</button>
        </form>
    `;
    eventDetails.style.display = 'block';
    modalOverlay.style.display = 'block';

    document.getElementById('attendanceForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const attendances = [];
        event.students.forEach(student => {
            attendances.push({
                student_id: student.id,
                is_present: formData.has(`student_${student.id}`)
            });
        });
        
        try {
            const csrftoken = getCookie('csrftoken');
            const response = await fetch(API_URLS.ATTENDANCE, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    schedule_id: eventId,
                    attendances: attendances
                }),
            });
    

            if (response.ok) {
                closeEventDetails();
                await updateSchedule(); // Обновляем расписание после сохранения посещаемости
            } else {
                throw new Error('Ошибка при сохранении посещаемости');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при сохранении посещаемости');
        }
    });
};

// Функция для дублирования карточки расписания
window.duplicateSchedule = async function(scheduleId) {
    // Запрашиваем у пользователя количество недель для дублирования
    const weeksCount = prompt('Введите количество недель для дублирования (от 1 до 52):', '1');
    
    // Проверяем введенное значение
    if (weeksCount === null) {
        return; // Пользователь отменил операцию
    }
    
    const weeks = parseInt(weeksCount);
    if (isNaN(weeks) || weeks < 1 || weeks > 52) {
        alert('Пожалуйста, введите корректное число от 1 до 52');
        return;
    }
    
    try {
        const csrftoken = getCookie('csrftoken');
        const response = await fetch(API_URLS.DUPLICATE_SCHEDULE, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                schedule_id: scheduleId,
                weeks_count: weeks
            }),
        });

        const result = await response.json();
        
        if (response.ok) {
            alert(result.message);
            closeEventDetails();
            await updateSchedule(); // Обновляем расписание после дублирования
        } else {
            throw new Error(result.error || 'Ошибка при дублировании расписания');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при дублировании расписания: ' + error.message);
    }
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.closeEventDetails = function() {
    document.getElementById('eventDetails').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
}

// Добавьте этот код в конец файла
document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.createElement('div');
    modalOverlay.id = 'modalOverlay';
    modalOverlay.className = 'modal-overlay';
    document.body.appendChild(modalOverlay);

    modalOverlay.addEventListener('click', function(event) {
        if (event.target === modalOverlay) {
            closeEventDetails();
        }
    });
});

