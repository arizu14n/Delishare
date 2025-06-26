<?php
require_once '../config/cors.php';
handleCORS();

include_once '../config/database.php';
include_once '../models/Usuario.php';

try {
    $database = new Database();
    $db = $database->getConnection();
    $usuario = new Usuario($db);

    $method = $_SERVER['REQUEST_METHOD'];

    switch($method) {
        case 'POST':
            $input = file_get_contents("php://input");
            $data = json_decode($input, true);
            
            if (json_last_error() !== JSON_ERROR_NONE) {
                jsonResponse([
                    "success" => false, 
                    "message" => "Datos JSON inválidos"
                ], 400);
            }
            
            if(!isset($data['action'])) {
                jsonResponse([
                    "success" => false, 
                    "message" => "Acción requerida"
                ], 400);
            }
            
            switch($data['action']) {
                case 'register':
                    handleRegister($usuario, $data);
                    break;
                    
                case 'login':
                    handleLogin($usuario, $data);
                    break;
                    
                default:
                    jsonResponse([
                        "success" => false, 
                        "message" => "Acción no válida"
                    ], 400);
                    break;
            }
            break;
            
        default:
            jsonResponse([
                "success" => false, 
                "message" => "Método no permitido"
            ], 405);
            break;
    }

} catch (Exception $e) {
    logError("Error en auth.php: " . $e->getMessage());
    jsonResponse([
        "success" => false, 
        "message" => "Error interno del servidor"
    ], 500);
}

function handleRegister($usuario, $data) {
    // Validación más robusta
    $required_fields = ['nombre', 'email', 'password'];
    foreach ($required_fields as $field) {
        if (empty($data[$field])) {
            jsonResponse([
                "success" => false, 
                "message" => "El campo {$field} es requerido"
            ], 400);
        }
    }
    
    // Validar email
    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        jsonResponse([
            "success" => false, 
            "message" => "Email inválido"
        ], 400);
    }
    
    // Validar contraseña
    if (strlen($data['password']) < 6) {
        jsonResponse([
            "success" => false, 
            "message" => "La contraseña debe tener al menos 6 caracteres"
        ], 400);
    }
    
    // Sanitizar datos
    $usuario->nombre = htmlspecialchars(strip_tags($data['nombre']));
    $usuario->email = filter_var($data['email'], FILTER_SANITIZE_EMAIL);
    $usuario->password = $data['password'];
    
    if($usuario->emailExiste()) {
        jsonResponse([
            "success" => false, 
            "message" => "El email ya está registrado"
        ], 409);
    }
    
    if($usuario->registrar()) {
        jsonResponse([
            "success" => true, 
            "message" => "Usuario registrado exitosamente",
            "user" => [
                "id" => $usuario->id,
                "nombre" => $usuario->nombre,
                "email" => $usuario->email,
                "tipo_suscripcion" => "gratuito",
                "suscripcion_activa" => false
            ]
        ], 201);
    } else {
        jsonResponse([
            "success" => false, 
            "message" => "No se pudo registrar el usuario"
        ], 500);
    }
}

function handleLogin($usuario, $data) {
    // Validación
    if (empty($data['email']) || empty($data['password'])) {
        jsonResponse([
            "success" => false, 
            "message" => "Email y contraseña requeridos"
        ], 400);
    }
    
    // Sanitizar email
    $usuario->email = filter_var($data['email'], FILTER_SANITIZE_EMAIL);
    $usuario->password = $data['password'];
    
    if($usuario->login()) {
        jsonResponse([
            "success" => true,
            "message" => "Login exitoso",
            "user" => [
                "id" => $usuario->id,
                "nombre" => $usuario->nombre,
                "email" => $usuario->email,
                "tipo_suscripcion" => $usuario->tipo_suscripcion,
                "suscripcion_activa" => $usuario->tieneSuscripcionActiva()
            ]
        ]);
    } else {
        // Log intento de login fallido
        logError("Intento de login fallido", ["email" => $usuario->email]);
        
        jsonResponse([
            "success" => false, 
            "message" => "Credenciales incorrectas"
        ], 401);
    }
}
?>
