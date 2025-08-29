<?php
// Configuración general de la aplicación
define('APP_NAME', 'DeliShare'); // Nombre de la aplicación
define('APP_VERSION', '1.0.0'); // Versión de la aplicación
define('APP_DEBUG', false); // Cambiar a false en producción

// Configuración de timezone
date_default_timezone_set('America/Argentina'); // Configuracion de la zona horaria

// Configuración de errores
if (APP_DEBUG) {
    error_reporting(E_ALL); //reportar todos los errores si está en modo desarrollo
    ini_set('display_errors', 1); // Mostrar errores en pantalla
} else {
    error_reporting(0); // No reportar errores en producción
    ini_set('display_errors', 0); // No mostrar errores en pantalla
    ini_set('log_errors', 1); // Registrar errores en el log
    ini_set('error_log', __DIR__ . '/../logs/php_errors.log'); // Ruta del archivo de log de errores
}

// Configuración de sesión
ini_set('session.cookie_httponly', 1); // Evitar acceso a cookies de sesión desde JavaScript
ini_set('session.cookie_secure', 1); // Usar cookies seguras (HTTPS)
ini_set('session.use_strict_mode', 1); // Usar modo estricto para sesiones

// Límites de memoria y tiempo
ini_set('memory_limit', '128M'); // Límite de memoria para el script para evitar ataques de denegación de servicio
ini_set('max_execution_time', 30); // Tiempo máximo de ejecución del script en segundos para evitar ataques de denegación de servicio

// Configuración de subida de archivos
ini_set('upload_max_filesize', '10M'); // Tamaño máximo de archivo para subir
ini_set('post_max_size', '10M'); // Tamaño máximo de datos POST
ini_set('max_file_uploads', 5); // Número máximo de archivos que se pueden subir en una sola solicitud

// Configuraciones de la aplicación
define('JWT_SECRET', 'tu_clave_secreta_muy_segura_aqui'); // Cambiar en producción 
define('PASSWORD_MIN_LENGTH', 6); // Longitud mínima de la contraseña
define('MAX_LOGIN_ATTEMPTS', 5); // Número máximo de intentos de inicio de sesión antes de bloquear la cuenta
define('LOGIN_LOCKOUT_TIME', 900); // Tiempo de bloqueo de cuenta en segundos (15 minutos)

// Configuración de paginación
define('DEFAULT_PAGE_SIZE', 20); // Tamaño de página por defecto
define('MAX_PAGE_SIZE', 100); // Tamaño máximo de página permitido

// Configuración de cache
define('CACHE_ENABLED', true); // Habilitar cache
define('CACHE_TTL', 3600); // Tiempo de vida del cache en segundos (1 hora)
?>
