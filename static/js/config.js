// Функция для получения базового URL
const getBaseUrl = () => {
    const ipUrl = 'http://192.168.19.103:8000';
    const localhostUrl = 'http://localhost:8000';
    
    // Проверяем доступность IP-адреса
    try {
        // Создаем тестовый запрос для проверки доступности сервера
        const xhr = new XMLHttpRequest();
        xhr.open('HEAD', ipUrl, false); // Синхронный запрос для простоты
        xhr.timeout = 2000; // Таймаут 2 секунды
        xhr.send();
        
        // Если статус успешный (2xx), возвращаем IP URL
        if (xhr.status >= 200 && xhr.status < 300) {
            return ipUrl;
        } else {
            console.log('Сервер вернул ошибку, переключаемся на localhost');
            return localhostUrl;
        }
    } catch (error) {
        console.log('Ошибка при подключении к серверу:', error);
        return localhostUrl;
    }
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