<?php
class Usuario {
    private $conn;
    private $table_name = "usuarios";

    public $id;
    public $nombre;
    public $email;
    public $password;
    public $tipo_suscripcion;
    public $fecha_suscripcion;
    public $fecha_vencimiento;
    public $activo;

    public function __construct($db) {
        $this->conn = $db;
    }

    // Registrar nuevo usuario
    public function registrar() {
        $query = "INSERT INTO " . $this->table_name . " 
                  SET nombre=:nombre, email=:email, password=:password";
        
        $stmt = $this->conn->prepare($query);
        
        // Hash de la contraseña
        $password_hash = password_hash($this->password, PASSWORD_DEFAULT);
        
        $stmt->bindParam(":nombre", $this->nombre);
        $stmt->bindParam(":email", $this->email);
        $stmt->bindParam(":password", $password_hash);
        
        if($stmt->execute()) {
            $this->id = $this->conn->lastInsertId();
            return true;
        }
        return false;
    }

    // Login de usuario
    public function login() {
        $query = "SELECT id, nombre, email, password, tipo_suscripcion, fecha_vencimiento 
                  FROM " . $this->table_name . " 
                  WHERE email = ? AND activo = 1 LIMIT 0,1";
        
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->email);
        $stmt->execute();
        
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if($row && password_verify($this->password, $row['password'])) {
            $this->id = $row['id'];
            $this->nombre = $row['nombre'];
            $this->tipo_suscripcion = $row['tipo_suscripcion'];
            $this->fecha_vencimiento = $row['fecha_vencimiento'];
            return true;
        }
        return false;
    }

    // Verificar si el usuario tiene suscripción activa
    public function tieneSuscripcionActiva() {
        if($this->tipo_suscripcion === 'premium') {
            if($this->fecha_vencimiento === null || $this->fecha_vencimiento > date('Y-m-d')) {
                return true;
            }
        }
        return false;
    }

    // Verificar si email ya existe
    public function emailExiste() {
        $query = "SELECT id FROM " . $this->table_name . " WHERE email = ? LIMIT 0,1";
        $stmt = $this->conn->prepare($query);
        $stmt->bindParam(1, $this->email);
        $stmt->execute();
        
        if($stmt->rowCount() > 0) {
            return true;
        }
        return false;
    }
}
?>
