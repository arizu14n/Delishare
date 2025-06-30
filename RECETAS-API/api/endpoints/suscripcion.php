<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");

include_once '../config/database.php';
include_once '../models/Usuario.php';

$database = new Database();
$db = $database->getConnection();
$usuario = new Usuario($db);

$method = $_SERVER['REQUEST_METHOD'];

switch($method) {
    case 'POST':
        $data = json_decode(file_get_contents("php://input"));
        
        if(isset($data->action) && $data->action === 'subscribe') {
            if(!empty($data->usuario_id) && !empty($data->plan)) {
                
                // Simular procesamiento de pago exitoso
                // En producción aquí iría la integración con Stripe/PayPal
                
                $query = "UPDATE usuarios SET 
                         tipo_suscripcion = 'premium',
                         fecha_suscripcion = CURDATE(),
                         fecha_vencimiento = DATE_ADD(CURDATE(), INTERVAL " . 
                         ($data->plan === 'anual' ? '365' : '30') . " DAY)
                         WHERE id = ?";
                
                $stmt = $db->prepare($query);
                $stmt->bindParam(1, $data->usuario_id);
                
                if($stmt->execute()) {
                    echo json_encode(array(
                        "success" => true,
                        "message" => "Suscripción activada exitosamente",
                        "plan" => $data->plan,
                        "fecha_vencimiento" => date('Y-m-d', strtotime('+' . ($data->plan === 'anual' ? '365' : '30') . ' days'))
                    ));
                } else {
                    echo json_encode(array("success" => false, "message" => "Error al activar la suscripción"));
                }
            } else {
                echo json_encode(array("success" => false, "message" => "Datos incompletos"));
            }
        } else {
            echo json_encode(array("success" => false, "message" => "Acción no válida"));
        }
        break;
        
    default:
        echo json_encode(array("success" => false, "message" => "Método no permitido"));
        break;
}
?>
