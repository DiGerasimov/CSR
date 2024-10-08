export function generateListHTML(type, items, filterOptions, currentFilter) {
    const capitalized = type === 'students' ? 'Обучающиеся' : 'Специалисты';
    let html = `<h2>${capitalized} (${items.length})</h2>`;
    html += generateFilterHTML(type, filterOptions, currentFilter);
    html += '<table><tr><th>Имя</th><th>Категория</th><th>Действия</th></tr>';
    items.forEach(item => {
        let additionalInfo = type === 'students' ? item.age_group : item.position.name;
        html += `<tr>
            <td>${item.full_name}</td>
            <td>${additionalInfo}</td>
            <td><button onclick="loadDetails('${type}', '${item.id}')">Подробнее</button></td>
        </tr>`;
    });
    html += '</table>';
    return html;
}

export function generateDetailsHTML(type, item) {
    let html = `<h2>Информация о ${type === 'students' ? 'обучающемся' : 'специалисте'} <button onclick="closeDetails()" class="close-btn">✖</button></h2>`;
    
    if (type === 'students') {
        html += generateStudentDetailsHTML(item);
    } else {
        html += generateSpecialistDetailsHTML(item);
    }

    return html;
}

function generateSpecialistDetailsHTML(specialist) {
    let html = '<div class="button-group">';
    html += `<button onclick="exportSpecialistSchedule('${specialist.id}', 'all')">Выгрузить все расписание</button>`;
    html += `<button onclick="exportSpecialistSchedule('${specialist.id}', 'month')">Выгрузить за месяц</button>`;
    html += `<button onclick="exportSpecialistSchedule('${specialist.id}', 'week')">Выгрузить за неделю</button>`;
    html += '</div>';
    html += generateTableFromObject(specialist);
    return html;
}
function generateFilterHTML(type, options, currentFilter) {
    const filterName = type === 'students' ? 'возрастной группе' : 'должности';
    let html = `<div class="filter"><label for="${type}Filter">Фильтр по ${filterName}: </label>`;
    html += `<select id="${type}Filter"><option value="">Все ${type === 'students' ? 'группы' : 'должности'}</option>`;
    options.forEach(option => {
        const value = type === 'students' ? option.value : option.name;
        const display = type === 'students' ? option.display : option.name;
        html += `<option value="${value}" ${currentFilter === value ? 'selected' : ''}>${display}</option>`;
    });
    html += '</select></div>';
    return html;
}

function generateStudentDetailsHTML(student) {
    let html = '<div class="button-group">';
    html += `<button onclick="exportStudentSchedule('${student.ID}')">Выгрузить расписание</button>`;
    html += `<button id="toggleRelativesBtn" onclick="toggleRelatives('${student.ID}')">Родственники</button>`;
    html += '</div><div id="studentInfo">';
    html += generateTableFromObject(student, ['ID', 'Родственники']);
    html += '</div>';

    html += generateRelativesHTML(student.Родственники);

    return html;
}

function generateRelativesHTML(relatives) {
    let html = '<div id="relativesInfo" style="display: none;">';
    if (relatives && Array.isArray(relatives) && relatives.length > 0) {
        html += '<h3>Родственники</h3>';
        html += '<table><tr><th>Имя</th><th>Пол</th><th>Отношение</th></tr>';
        relatives.forEach(relative => {
            html += `<tr>
                <td>${relative.full_name || 'Нет данных'}</td>
                <td>${relative.gender_display || 'Нет данных'}</td>
                <td>${relative.relation_display || 'Нет данных'}</td>
            </tr>`;
        });
        html += '</table>';
    } else {
        html += '<p>У этого обучающегося нет родственников в базе данных.</p>';
    }
    html += '</div>';
    return html;
}

function generateTableFromObject(obj, excludeKeys = []) {
    let html = '<table>';
    for (const [key, value] of Object.entries(obj)) {
        if (!excludeKeys.includes(key)) {
            html += `<tr><th>${key}</th><td>${value}</td></tr>`;
        }
    }
    html += '</table>';
    return html;
}