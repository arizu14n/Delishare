<?php
class Database {
    private $host = "localhost";
    private $db_name = "recetas_cocina_prueba";
    private $username = "root";
    private $password = "";
    public $conn;

    public function getConnection() {
        $this->conn = null;
        try {
            $dsn = "mysql:host=" . $this->host . ";dbname=" . $this->db_name . ";charset=utf8mb4";
            $this->conn = new PDO($dsn, $this->username, $this->password);
            
            // Configuraciones de PDO
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->conn->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
            
        } catch(PDOException $exception) {
            error_log("Error de conexión a la base de datos: " . $exception->getMessage());
            http_response_code(500);
            echo json_encode([
                "success" => false, 
                "message" => "Error de conexión a la base de datos"
            ]);
            exit();
        }
        return $this->conn;
    }
}
?>
