-- Base de datos actualizada con mejoras de seguridad y rendimiento
CREATE DATABASE IF NOT EXISTS recetas_cocina_prueba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE recetas_cocina_prueba;

-- Tabla de usuarios con mejoras
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    tipo_suscripcion ENUM('gratuito', 'premium') DEFAULT 'gratuito',
    fecha_suscripcion DATE NULL,
    fecha_vencimiento DATE NULL,
    activo BOOLEAN DEFAULT TRUE,
    intentos_login INT DEFAULT 0,
    bloqueado_hasta TIMESTAMP NULL,
    ultimo_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_email (email),
    INDEX idx_tipo_suscripcion (tipo_suscripcion),
    INDEX idx_activo (activo)
);

-- Tabla de categorías
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    icono VARCHAR(50) DEFAULT 'fas fa-utensils',
    activo BOOLEAN DEFAULT TRUE,
    orden INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_activo (activo),
    INDEX idx_orden (orden)
);

-- Tabla de recetas mejorada
CREATE TABLE recetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    ingredientes TEXT NOT NULL,
    instrucciones TEXT NOT NULL,
    tiempo_preparacion INT DEFAULT 0, -- en minutos
    porciones INT DEFAULT 1,
    dificultad ENUM('Fácil', 'Intermedio', 'Difícil') DEFAULT 'Fácil',
    categoria_id INT,
    imagen_url VARCHAR(500),
    autor VARCHAR(100) DEFAULT 'Anónimo',
    es_premium BOOLEAN DEFAULT FALSE,
    vistas INT DEFAULT 0,
    likes INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
    
    INDEX idx_categoria (categoria_id),
    INDEX idx_es_premium (es_premium),
    INDEX idx_dificultad (dificultad),
    INDEX idx_activo (activo),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_busqueda (titulo, descripcion, ingredientes)
);

-- Tabla de valoraciones
CREATE TABLE valoraciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receta_id INT NOT NULL,
    usuario_id INT NULL,
    puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    nombre_usuario VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    
    INDEX idx_receta (receta_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_puntuacion (puntuacion)
);

-- Tabla de favoritos
CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    receta_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_favorito (usuario_id, receta_id),
    INDEX idx_usuario (usuario_id),
    INDEX idx_receta (receta_id)
);

-- Tabla de planes de suscripción
CREATE TABLE planes_suscripcion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion_dias INT NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_activo (activo)
);

-- Tabla de logs de actividad
CREATE TABLE logs_actividad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    
    INDEX idx_usuario (usuario_id),
    INDEX idx_accion (accion),
    INDEX idx_created_at (created_at)
);

-- Insertar categorías con iconos
INSERT INTO categorias (nombre, descripcion, icono, orden) VALUES
('Desayunos', 'Recetas para comenzar el día', 'fas fa-coffee', 1),
('Almuerzos', 'Comidas principales del mediodía', 'fas fa-hamburger', 2),
('Cenas', 'Recetas para la noche', 'fas fa-moon', 3),
('Postres', 'Dulces y postres deliciosos', 'fas fa-ice-cream', 4),
('Bebidas', 'Jugos, batidos y bebidas', 'fas fa-glass-cheers', 5),
('Aperitivos', 'Entradas y bocadillos', 'fas fa-cheese', 6),
('Vegetarianas', 'Recetas sin carne', 'fas fa-leaf', 7),
('Veganas', 'Recetas completamente vegetales', 'fas fa-seedling', 8);

-- Insertar planes de suscripción
INSERT INTO planes_suscripcion (nombre, precio, duracion_dias, descripcion) VALUES
('Mensual', 9.99, 30, 'Acceso completo por 1 mes'),
('Trimestral', 24.99, 90, 'Acceso completo por 3 meses (17% descuento)'),
('Anual', 79.99, 365, 'Acceso completo por 1 año (33% descuento)');

-- Insertar usuario administrador (contraseña: admin123)
INSERT INTO usuarios (nombre, email, password, tipo_suscripcion) VALUES
('Administrador', 'admin@recetas.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'premium');

-- Insertar recetas de ejemplo mejoradas
INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, porciones, dificultad, categoria_id, autor, es_premium) VALUES
('Pancakes Esponjosos', 'Deliciosos pancakes perfectos para el desayuno familiar', 
'2 tazas de harina todo uso\n1 taza de leche entera\n2 huevos grandes\n2 cucharadas de azúcar\n1 cucharadita de polvo de hornear\nPizca de sal\nMantequilla para cocinar\nMiel o jarabe de maple para servir', 
'1. En un bowl grande, mezclar todos los ingredientes secos: harina, azúcar, polvo de hornear y sal\n2. En otro bowl, batir los huevos con la leche hasta integrar completamente\n3. Verter la mezcla líquida sobre los ingredientes secos y mezclar hasta obtener una masa homogénea (no sobre mezclar)\n4. Calentar una sartén antiadherente a fuego medio y agregar un poco de mantequilla\n5. Verter 1/4 taza de masa por cada pancake\n6. Cocinar 2-3 minutos hasta que aparezcan burbujas en la superficie\n7. Voltear cuidadosamente y cocinar 1-2 minutos más hasta dorar\n8. Servir inmediatamente con miel o jarabe de maple caliente', 
20, 4, 'Fácil', 1, 'Chef María González', FALSE),

('Ensalada César Gourmet', 'La clásica ensalada César con un toque gourmet y aderezo casero', 
'2 lechugas romanas grandes\n4 rebanadas de pan integral\n100g de queso parmesano\n2 pechugas de pollo\n1/2 taza de aceite de oliva extra virgen\n2 limones\n3 dientes de ajo\n1 cucharada de mostaza Dijon\n4 filetes de anchoas\n1 huevo\nSal y pimienta negra recién molida', 
'1. Lavar y secar completamente las lechugas, cortar en trozos medianos\n2. Para el aderezo: en un bowl pequeño, machacar el ajo con sal hasta formar una pasta\n3. Agregar mostaza Dijon, anchoas picadas y mezclar bien\n4. Incorporar el jugo de limón y batir mientras se agrega el aceite de oliva lentamente\n5. Agregar el huevo y batir hasta obtener una consistencia cremosa\n6. Sazonar con pimienta negra recién molida\n7. Cortar el pan en cubos y tostar en el horno hasta dorar\n8. Cocinar las pechugas de pollo con sal, pimienta y hierbas hasta dorar completamente\n9. Dejar reposar el pollo 5 minutos y cortar en tiras\n10. En un bowl grande, mezclar la lechuga con el aderezo\n11. Agregar el pollo en tiras y los crutones\n12. Espolvorear generosamente con queso parmesano rallado\n13. Servir inmediatamente acompañado de pan tostado', 
35, 2, 'Intermedio', 2, 'Chef Carlos Mendoza', TRUE);

-- Crear vistas para consultas frecuentes
CREATE VIEW vista_recetas_populares AS
SELECT r.*, c.nombre as categoria_nombre, 
       (SELECT AVG(puntuacion) FROM valoraciones v WHERE v.receta_id = r.id) as rating_promedio,
       (SELECT COUNT(*) FROM valoraciones v WHERE v.receta_id = r.id) as total_valoraciones
FROM recetas r
LEFT JOIN categorias c ON r.categoria_id = c.id
WHERE r.activo = TRUE
ORDER BY r.vistas DESC, r.likes DESC;

-- Procedimiento almacenado para actualizar estadísticas
DELIMITER //
CREATE PROCEDURE ActualizarEstadisticasReceta(IN receta_id INT)
BEGIN
    UPDATE recetas 
    SET vistas = vistas + 1 
    WHERE id = receta_id;
END //
DELIMITER ;
