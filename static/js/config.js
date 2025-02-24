// Функция для проверки доступности сервера и выбора подходящего URL
const getBaseUrl = () => {
    const primaryUrl = 'http://192.168.19.103:8000';
    const backupUrl = 'http://localhost:8000';
    
    // Создаем переменную для хранения выбранного URL
    let baseUrl = primaryUrl;
    
    // Проверяем доступность основного URL и переключаемся на резервный при необходимости
    try {
        const xhr = new XMLHttpRequest();
        xhr.open('HEAD', primaryUrl, false); // Синхронный запрос для простоты
        xhr.timeout = 2000; // Таймаут 2 секунды
        try {
            xhr.send();
            if (xhr.status >= 200 && xhr.status < 300) {
                baseUrl = primaryUrl;
            } else {
                baseUrl = backupUrl;
            }
        } catch (e) {
            baseUrl = backupUrl;
        }
    } catch (e) {
        baseUrl = backupUrl;
    }
    
    return baseUrl;
};

// Определяем базовый URL API с учетом доступности серверов
const API_BASE_URL = getBaseUrl();

export const API_URLS = {
    SPECIALISTS: `${API_BASE_URL}/specialists/`,
    POSITIONS: `${API_BASE_URL}/specialists/positions/`,
    SCHEDULE: `${API_BASE_URL}/schedule/`,
    ATTENDANCE: `${API_BASE_URL}/schedule/attendance/`,
    DUPLICATE_SCHEDULE: `${API_BASE_URL}/schedule/duplicate/`,
};