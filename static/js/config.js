// Функция для получения базового URL
const getBaseUrl = () => {
    // Сразу возвращаем localhost без проверки IP
    //return 'http://localhost:8000';
    return 'http://192.168.19.103:8000';

};

// Определяем базовый URL API
const API_BASE_URL = getBaseUrl();

export const API_URLS = {
    SPECIALISTS: `${API_BASE_URL}/specialists/`,
    POSITIONS: `${API_BASE_URL}/specialists/positions/`,
    SCHEDULE: `${API_BASE_URL}/schedule/`,
    ATTENDANCE: `${API_BASE_URL}/schedule/attendance/`,
    DUPLICATE_SCHEDULE: `${API_BASE_URL}/schedule/duplicate/`,
};