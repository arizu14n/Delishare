<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");


include_once '../config/database.php';
include_once '../models/Categoria.php';


$database = new Database();
$db = $database->getConnection();
$categoria = new Categoria($db);


$stmt = $categoria->obtenerTodas();
$num = $stmt->rowCount();


if($num > 0) {
    $categorias_arr = array();
    while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
        extract($row);
        $categoria_item = array(
            "id" => $id,
            "nombre" => $nombre,
            "descripcion" => $descripcion
        );
        array_push($categorias_arr, $categoria_item);
    }
    echo json_encode($categorias_arr);
} else {
    echo json_encode(array("message" => "No se encontraron categorías."));
}
?>