<?php
// Configuración general de la aplicación
define('APP_NAME', 'Recetas Premium API');
define('APP_VERSION', '1.0.0');
define('APP_DEBUG', false); // Cambiar a false en producción

// Configuración de timezone
date_default_timezone_set('America/Mexico_City');

// Configuración de errores
if (APP_DEBUG) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
    ini_set('log_errors', 1);
    ini_set('error_log', __DIR__ . '/../logs/php_errors.log');
}

// Configuración de sesión
ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 1);
ini_set('session.use_strict_mode', 1);

// Límites de memoria y tiempo
ini_set('memory_limit', '128M');
ini_set('max_execution_time', 30);

// Configuración de subida de archivos
ini_set('upload_max_filesize', '10M');
ini_set('post_max_size', '10M');
ini_set('max_file_uploads', 5);

// Configuraciones de la aplicación
define('JWT_SECRET', 'tu_clave_secreta_muy_segura_aqui'); // Cambiar en producción
define('PASSWORD_MIN_LENGTH', 6);
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOGIN_LOCKOUT_TIME', 900); // 15 minutos

// Configuración de paginación
define('DEFAULT_PAGE_SIZE', 20);
define('MAX_PAGE_SIZE', 100);

// Configuración de cache
define('CACHE_ENABLED', true);
define('CACHE_TTL', 3600); // 1 hora
?>
