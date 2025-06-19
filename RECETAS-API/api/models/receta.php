<?php
class Receta {
    private $conn;
    private $table_name = "recetas";


    public $id;
    public $titulo;
    public $descripcion;
    public $ingredientes;
    public $instrucciones;
    public $tiempo_preparacion;
    public $porciones;
    public $dificultad;
    public $categoria_id;
    public $imagen_url;
    public $autor;
    public $created_at;


    public function __construct($db) {
        $this->conn = $db;
    }


    // Obtener todas las recetas
    public function obtenerTodas() {
        $query = "SELECT r.*, c.nombre as categoria_nombre
                  FROM " . $this->table_name . " r
                  LEFT JOIN categorias c ON r.categoria_id = c.id
                  ORDER BY r.created_at DESC";
       
        $stmt = $this->conn->prepare($query);
        $stmt->execute();
        return $stmt;
    }


    // Obtener receta por ID
    public function obtenerPorId() {
        $query = "SELECT r.*, c.nombre as categoria_nombre
                  FROM " . $this->table_name . " r
                  LEFT JOIN categorias c ON r.categoria_id = c.id
                  WHERE r.id = ? LIMIT 0,1";
       
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->id);
        $stmt->execute();
       
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
       
        if($row) {
            $this->titulo = $row['titulo'];
            $this->descripcion = $row['descripcion'];
            $this->ingredientes = $row['ingredientes'];
            $this->instrucciones = $row['instrucciones'];
            $this->tiempo_preparacion = $row['tiempo_preparacion'];
            $this->porciones = $row['porciones'];
            $this->dificultad = $row['dificultad'];
            $this->categoria_id = $row['categoria_id'];
            $this->imagen_url = $row['imagen_url'];
            $this->autor = $row['autor'];
            $this->created_at = $row['created_at'];
            return true;
        }
        return false;
    }


    // Crear nueva receta
    public function crear() {
        $query = "INSERT INTO " . $this->table_name . "
                  SET titulo=:titulo, descripcion=:descripcion, ingredientes=:ingredientes,
                      instrucciones=:instrucciones, tiempo_preparacion=:tiempo_preparacion,
                      porciones=:porciones, dificultad=:dificultad, categoria_id=:categoria_id,
                      imagen_url=:imagen_url, autor=:autor";


        $stmt = $this->conn->prepare($query);


        // Limpiar datos
        $this->titulo = htmlspecialchars(strip_tags($this->titulo));
        $this->descripcion = htmlspecialchars(strip_tags($this->descripcion));
        $this->ingredientes = htmlspecialchars(strip_tags($this->ingredientes));
        $this->instrucciones = htmlspecialchars(strip_tags($this->instrucciones));
        $this->autor = htmlspecialchars(strip_tags($this->autor));


        // Bind valores
        $stmt->bindParam(":titulo", $this->titulo);
        $stmt->bindParam(":descripcion", $this->descripcion);
        $stmt->bindParam(":ingredientes", $this->ingredientes);
        $stmt->bindParam(":instrucciones", $this->instrucciones);
        $stmt->bindParam(":tiempo_preparacion", $this->tiempo_preparacion);
        $stmt->bindParam(":porciones", $this->porciones);
        $stmt->bindParam(":dificultad", $this->dificultad);
        $stmt->bindParam(":categoria_id", $this->categoria_id);
        $stmt->bindParam(":imagen_url", $this->imagen_url);
        $stmt->bindParam(":autor", $this->autor);


        if($stmt->execute()) {
            return true;
        }
        return false;
    }


    // Buscar recetas
    public function buscar($keywords) {
        $query = "SELECT r.*, c.nombre as categoria_nombre
                  FROM " . $this->table_name . " r
                  LEFT JOIN categorias c ON r.categoria_id = c.id
                  WHERE r.titulo LIKE ? OR r.descripcion LIKE ? OR r.ingredientes LIKE ?
                  ORDER BY r.created_at DESC";
       
        $stmt = $this->conn->prepare($query);
        $keywords = "%{$keywords}%";
        $stmt->bindParam(1, $keywords);
        $stmt->bindParam(2, $keywords);
        $stmt->bindParam(3, $keywords);
        $stmt->execute();
       
        return $stmt;
    }
}
?>


