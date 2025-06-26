<?php
class Categoria {
    private $conn;
    private $table_name = "categorias";

    public $id;
    public $nombre;
    public $descripcion;

    public function __construct($db) {
        $this->conn = $db;
    }

    public function obtenerTodas() {
        $query = "SELECT * FROM " . $this->table_name . " ORDER BY descripcion";
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }
}
?>
