<?php
// Archivo de prueba para verificar que todo funciona
echo "Probando configuración...<br>";

// Probar conexión a base de datos
try {
    include_once 'config/database.php';
    $database = new Database();
    $db = $database->getConnection();
    echo "✅ Conexión a base de datos: OK<br>";
} catch (Exception $e) {
    echo "❌ Error de base de datos: " . $e->getMessage() . "<br>";
}

// Probar CORS
try {
    include_once 'config/cors.php';
    echo "✅ Configuración CORS: OK<br>";
} catch (Exception $e) {
    echo "❌ Error CORS: " . $e->getMessage() . "<br>";
}

// Probar modelo de recetas
try {
    include_once 'models/Receta.php';
    $receta = new Receta($db);
    echo "✅ Modelo Receta: OK<br>";
} catch (Exception $e) {
    echo "❌ Error modelo Receta: " . $e->getMessage() . "<br>";
}

// Información del sistema
echo "<br><strong>Información del sistema:</strong><br>";
echo "PHP Version: " . phpversion() . "<br>";
echo "Directorio actual: " . __DIR__ . "<br>";
echo "Carpeta logs existe: " . (is_dir(__DIR__ . '/logs') ? 'Sí' : 'No') . "<br>";

phpinfo();
?>
