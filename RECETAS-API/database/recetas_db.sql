-- Base de datos para el sistema de recetas
CREATE DATABASE recetas_cocina;
USE recetas_cocina;


-- Tabla de categorías
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabla de recetas
CREATE TABLE recetas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    ingredientes TEXT NOT NULL,
    instrucciones TEXT NOT NULL,
    tiempo_preparacion INT, -- en minutos
    porciones INT,
    dificultad ENUM('Fácil', 'Intermedio', 'Difícil') DEFAULT 'Fácil',
    categoria_id INT,
    imagen_url VARCHAR(500),
    autor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);


-- Tabla de valoraciones
CREATE TABLE valoraciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    receta_id INT,
    puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    autor VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE
);


-- Insertar categorías iniciales
INSERT INTO categorias (nombre, descripcion) VALUES
('Desayunos', 'Recetas para comenzar el día'),
('Almuerzos', 'Comidas principales del mediodía'),
('Cenas', 'Recetas para la noche'),
('Postres', 'Dulces y postres deliciosos'),
('Bebidas', 'Bebidas refrescantes y calientes'),
('Aperitivos', 'Bocadillos y entradas'),
('Vegetarianas', 'Recetas sin carne'),
('Veganas', 'Recetas completamente vegetales');


-- Insertar recetas de ejemplo
INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, porciones, dificultad, categoria_id, autor) VALUES
('Pancakes Esponjosos', 'Deliciosos pancakes perfectos para el desayuno',
'2 tazas de harina\n1 taza de leche\n2 huevos\n2 cucharadas de azúcar\n1 cucharadita de polvo de hornear\nPizca de sal\nMantequilla para cocinar',
'1. Mezclar ingredientes secos\n2. Batir huevos con leche\n3. Combinar todo hasta obtener masa homogénea\n4. Cocinar en sartén caliente\n5. Servir calientes',
20, 4, 'Fácil', 1, 'Chef María'),


('Ensalada César', 'Clásica ensalada con aderezo casero',
'Lechuga romana\nPan tostado\nQueso parmesano\nPollo a la plancha\nAceite de oliva\nLimón\nAjo\nMostaza\nSal y pimienta',
'1. Lavar y cortar la lechuga\n2. Preparar aderezo con aceite, limón, ajo y mostaza\n3. Tostar el pan\n4. Cocinar el pollo\n5. Mezclar todo y servir',
25, 2, 'Fácil', 2, 'Chef Carlos');
