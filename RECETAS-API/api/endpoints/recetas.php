<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");


include_once '../config/database.php';
include_once '../models/Receta.php';


$database = new Database();
$db = $database->getConnection();
$receta = new Receta($db);


$method = $_SERVER['REQUEST_METHOD'];


switch($method) {
    case 'GET':
        if(isset($_GET['id'])) {
            // Obtener receta específica
            $receta->id = $_GET['id'];
            if($receta->obtenerPorId()) {
                $receta_arr = array(
                    "id" => $receta->id,
                    "titulo" => $receta->titulo,
                    "descripcion" => $receta->descripcion,
                    "ingredientes" => $receta->ingredientes,
                    "instrucciones" => $receta->instrucciones,
                    "tiempo_preparacion" => $receta->tiempo_preparacion,
                    "porciones" => $receta->porciones,
                    "dificultad" => $receta->dificultad,
                    "categoria_id" => $receta->categoria_id,
                    "imagen_url" => $receta->imagen_url,
                    "autor" => $receta->autor,
                    "created_at" => $receta->created_at
                );
                echo json_encode($receta_arr);
            } else {
                echo json_encode(array("message" => "Receta no encontrada."));
            }
        } elseif(isset($_GET['buscar'])) {
            // Buscar recetas
            $stmt = $receta->buscar($_GET['buscar']);
            $num = $stmt->rowCount();
           
            if($num > 0) {
                $recetas_arr = array();
                while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                    extract($row);
                    $receta_item = array(
                        "id" => $id,
                        "titulo" => $titulo,
                        "descripcion" => $descripcion,
                        "tiempo_preparacion" => $tiempo_preparacion,
                        "porciones" => $porciones,
                        "dificultad" => $dificultad,
                        "categoria_nombre" => $categoria_nombre,
                        "imagen_url" => $imagen_url,
                        "autor" => $autor,
                        "created_at" => $created_at
                    );
                    array_push($recetas_arr, $receta_item);
                }
                echo json_encode($recetas_arr);
            } else {
                echo json_encode(array("message" => "No se encontraron recetas."));
            }
        } else {
            // Obtener todas las recetas
            $stmt = $receta->obtenerTodas();
            $num = $stmt->rowCount();
           
            if($num > 0) {
                $recetas_arr = array();
                while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                    extract($row);
                    $receta_item = array(
                        "id" => $id,
                        "titulo" => $titulo,
                        "descripcion" => $descripcion,
                        "ingredientes" => $ingredientes,
                        "instrucciones" => $instrucciones, 
                        "tiempo_preparacion" => $tiempo_preparacion,
                        "porciones" => $porciones,
                        "dificultad" => $dificultad,
                        "categoria_nombre" => $categoria_nombre,
                        "imagen_url" => $imagen_url,
                        "autor" => $autor,
                        "created_at" => $created_at
                    );
                    array_push($recetas_arr, $receta_item);
                }
                echo json_encode($recetas_arr);
            } else {
                echo json_encode(array("message" => "No se encontraron recetas."));
            }
        }
        break;
       
    case 'POST':
        // Crear nueva receta
        $data = json_decode(file_get_contents("php://input"));
       
        if(!empty($data->titulo) && !empty($data->ingredientes) && !empty($data->instrucciones)) {
            $receta->titulo = $data->titulo;
            $receta->descripcion = $data->descripcion;
            $receta->ingredientes = $data->ingredientes;
            $receta->instrucciones = $data->instrucciones;
            $receta->tiempo_preparacion = $data->tiempo_preparacion;
            $receta->porciones = $data->porciones;
            $receta->dificultad = $data->dificultad;
            $receta->categoria_id = $data->categoria_id;
            $receta->imagen_url = $data->imagen_url;
            $receta->autor = $data->autor;
           
            if($receta->crear()) {
                echo json_encode(array("message" => "Receta creada exitosamente."));
            } else {
                echo json_encode(array("message" => "No se pudo crear la receta."));
            }
        } else {
            echo json_encode(array("message" => "Datos incompletos."));
        }
        break;
}
?>


