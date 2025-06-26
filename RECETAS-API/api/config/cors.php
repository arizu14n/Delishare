<?php
// Archivo simplificado para manejar CORS
function handleCORS() {
    // Headers CORS básicos
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
    header("Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With");
    header("Content-Type: application/json; charset=UTF-8");
    
    // Manejar preflight requests
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit();
    }
}

// Función para respuestas JSON consistentes
function jsonResponse($data, $status_code = 200) {
    http_response_code($status_code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit();
}

// Función para logging de errores (simplificada para Windows)
function logError($message, $context = []) {
    $log_entry = date('Y-m-d H:i:s') . " - " . $message;
    if (!empty($context)) {
        $log_entry .= " - Context: " . json_encode($context);
    }
    
    // Crear archivo de log si no existe
    $log_file = __DIR__ . '/../logs/error.log';
    $log_dir = dirname($log_file);
    
    if (!is_dir($log_dir)) {
        mkdir($log_dir, 0755, true);
    }
    
    error_log($log_entry . PHP_EOL, 3, $log_file);
}
?>
