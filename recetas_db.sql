-- Tabla de usuarios con mejoras
CREATE TABLE Usuario (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
     tipo_suscripcion NVARCHAR(20) NOT NULL DEFAULT 'gratuito'
        CHECK (tipo_suscripcion IN ('gratuito','premium')),
    fecha_suscripcion DATE NULL,
    fecha_vencimiento DATE NULL,
    activo bit DEFAULT 1,
    intentos_login INT DEFAULT 0,
    bloqueado_hasta DATETIME NULL,
    ultimo_login DATETIME NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
);

CREATE INDEX idx_email ON Usuario(email);
CREATE INDEX idx_tipo_suscripcion ON Usuario(tipo_suscripcion);
CREATE INDEX idx_activo_users ON Usuario(activo);

-- Tabla de categorías
CREATE TABLE categorias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    icono VARCHAR(50) DEFAULT 'fas fa-utensils',
    activo bit DEFAULT 1,
    orden INT DEFAULT 0,
    created_at DATETIME DEFAULT GetDate(),
);

CREATE INDEX idx_activo_categorias ON categorias(activo);
CREATE INDEX idx_orden_categorias ON categorias(orden);

-- Tabla de recetas mejorada
CREATE TABLE recetas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    ingredientes TEXT NOT NULL,
    instrucciones TEXT NOT NULL,
    tiempo_preparacion INT DEFAULT 0, -- en minutos
    porciones INT DEFAULT 1,
    dificultad NVARCHAR(20) NOT NULL DEFAULT 'Fácil'
        CHECK (dificultad IN ('Fácil','Intermedio','Difícil')),
    categoria_id INT,
    imagen_url VARCHAR(500),
    autor VARCHAR(100) DEFAULT 'Anónimo',
    es_premium bit DEFAULT 0,
    vistas INT DEFAULT 0,
    likes INT DEFAULT 0,
    activo bit DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
);

CREATE INDEX idx_categoria_recetas ON recetas(categoria_id);
CREATE INDEX idx_es_premium_recetas ON recetas(es_premium);
CREATE INDEX idx_dificultad_recetas ON recetas(dificultad);
CREATE INDEX idx_activo_recetas ON recetas(activo);
CREATE INDEX idx_created_recetas ON recetas(created_at);

-- Tabla de valoraciones
CREATE TABLE valoraciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    receta_id INT NOT NULL,
    usuario_id INT NULL,
    puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
    comentario TEXT,
    nombre_usuario VARCHAR(100),
    activo bit DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL,
);

CREATE INDEX idx_receta_val ON valoraciones(receta_id);
CREATE INDEX idx_usuario_val ON valoraciones(usuario_id);
CREATE INDEX idx_puntuacion_val ON valoraciones(puntuacion);

-- Tabla de favoritos
CREATE TABLE favoritos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NOT NULL,
    receta_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
	CONSTRAINT unique_favorito UNIQUE (usuario_id, receta_id)
);

CREATE INDEX idx_usuario_fav ON favoritos(usuario_id);
CREATE INDEX idx_receta_fav ON favoritos(receta_id);

-- Tabla de planes de suscripción
CREATE TABLE planes_suscripcion (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion_dias INT NOT NULL,
    descripcion TEXT,
    activo bit DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
);

CREATE INDEX idx_activo_planes ON planes_suscripcion(activo);

-- Tabla de logs de actividad
CREATE TABLE logs_actividad (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NULL,
    accion VARCHAR(100) NOT NULL,
    tabla_afectada VARCHAR(50),
    registro_id INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL,    
);

CREATE INDEX idx_usuario_logs ON logs_actividad(usuario_id);
CREATE INDEX idx_accion_logs ON logs_actividad(accion);
CREATE INDEX idx_created_logs ON logs_actividad(created_at);

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

-- Insertar users administrador (contraseña: admin123)
INSERT INTO Usuario (nombre, email, password_hash, tipo_suscripcion) VALUES
('Administrador', 'admin@recetas.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'premium');

-- Insertar recetas de ejemplo mejoradas
INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, porciones, dificultad, categoria_id, autor, es_premium) VALUES
('Pancakes Esponjosos', 'Deliciosos pancakes perfectos para el desayuno familiar', 
'2 tazas de harina todo uso\n1 taza de leche entera\n2 huevos grandes\n2 cucharadas de azúcar\n1 cucharadita de polvo de hornear\nPizca de sal\nMantequilla para cocinar\nMiel o jarabe de maple para servir', 
'1. En un bowl grande, mezclar todos los ingredientes secos: harina, azúcar, polvo de hornear y sal\n2. En otro bowl, batir los huevos con la leche hasta integrar completamente\n3. Verter la mezcla líquida sobre los ingredientes secos y mezclar hasta obtener una masa homogénea (no sobre mezclar)\n4. Calentar una sartén antiadherente a fuego medio y agregar un poco de mantequilla\n5. Verter 1/4 taza de masa por cada pancake\n6. Cocinar 2-3 minutos hasta que aparezcan burbujas en la superficie\n7. Voltear cuidadosamente y cocinar 1-2 minutos más hasta dorar\n8. Servir inmediatamente con miel o jarabe de maple caliente', 
20, 4, 'Fácil', 1, 'Chef María González', 0),

('Ensalada César Gourmet', 'La clásica ensalada César con un toque gourmet y aderezo casero', 
'2 lechugas romanas grandes\n4 rebanadas de pan integral\n100g de queso parmesano\n2 pechugas de pollo\n1/2 taza de aceite de oliva extra virgen\n2 limones\n3 dientes de ajo\n1 cucharada de mostaza Dijon\n4 filetes de anchoas\n1 huevo\nSal y pimienta negra recién molida', 
'1. Lavar y secar completamente las lechugas, cortar en trozos medianos\n2. Para el aderezo: en un bowl pequeño, machacar el ajo con sal hasta formar una pasta\n3. Agregar mostaza Dijon, anchoas picadas y mezclar bien\n4. Incorporar el jugo de limón y batir mientras se agrega el aceite de oliva lentamente\n5. Agregar el huevo y batir hasta obtener una consistencia cremosa\n6. Sazonar con pimienta negra recién molida\n7. Cortar el pan en cubos y tostar en el horno hasta dorar\n8. Cocinar las pechugas de pollo con sal, pimienta y hierbas hasta dorar completamente\n9. Dejar reposar el pollo 5 minutos y cortar en tiras\n10. En un bowl grande, mezclar la lechuga con el aderezo\n11. Agregar el pollo en tiras y los crutones\n12. Espolvorear generosamente con queso parmesano rallado\n13. Servir inmediatamente acompañado de pan tostado', 
35, 2, 'Intermedio', 2, 'Chef Carlos Mendoza', 1);

GO
-- Vista de recetas populares
CREATE VIEW vista_recetas_populares AS
SELECT r.*, c.nombre as categoria_nombre,
       (SELECT AVG(puntuacion) FROM valoraciones v WHERE v.receta_id = r.id) as rating_promedio,
       (SELECT COUNT(*) FROM valoraciones v WHERE v.receta_id = r.id) as total_valoraciones
FROM recetas r
LEFT JOIN categorias c ON r.categoria_id = c.id
WHERE r.activo = 1;
GO

-- Procedimiento almacenado para actualizar estadísticas
CREATE PROCEDURE ActualizarEstadisticasReceta @receta_id INT
AS
BEGIN
    UPDATE recetas
    SET vistas = vistas + 1,
        updated_at = GETDATE()
    WHERE id = @receta_id;
END;
GO
