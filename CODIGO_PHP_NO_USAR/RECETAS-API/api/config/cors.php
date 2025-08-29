<?php
// Archivo simplificado para manejar CORS
function handleCORS() {
    // Headers CORS básicos
    header("Access-Control-Allow-Origin: *"); // Permitir cualquier origen
    header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS"); // Métodos permitidos, los más comunes en API Rest
    header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With"); // Headers permitidos
    header("Content-Type: application/json; charset=UTF-8"); // Tipo de contenido JSON
    
    // Manejar preflight requests
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { // Si es una solicitud OPTIONS, devuelve un 200 OK para indicar que el servidor está listo para recibir solicitudes
        http_response_code(200);
        exit();
    }
}

// Función para respuestas JSON consistentes
function jsonResponse($data, $status_code = 200) { // Esta función envía una respuesta JSON con el código de estado HTTP especificado. El 200 es el código por defecto para una respuesta exitosa.
    http_response_code($status_code); 
    echo json_encode($data, JSON_UNESCAPED_UNICODE); // JSON_UNESCAPED_UNICODE asegura que los caracteres Unicode se representen correctamente (ñ o acentos)
    exit(); // sale para que se detenga la ejecución del script después de enviar la respuesta
}

// Función para logging de errores (simplificada para Windows)
function logError($message, $context = []) { // Esta función registra errores en un archivo de log. El mensaje es el error y el contexto es un array opcional con información adicional.
    $log_entry = date('Y-m-d H:i:s') . " - " . $message; // Formatea la entrada del log con la fecha y hora actual y el mensaje de error
    if (!empty($context)) {
        $log_entry .= " - Context: " . json_encode($context);
    }
    
    // Crear archivo de log si no existe
    $log_file = __DIR__ . '/../logs/error.log';
    $log_dir = dirname($log_file);
    
    if (!is_dir($log_dir)) {
        mkdir($log_dir, 0755, true);
    }
    
    error_log($log_entry . PHP_EOL, 3, $log_file); // Escribe la entrada del log en el archivo especificado. PHP_EOL asegura que se use el salto de línea correcto para el sistema operativo.
}
?>
