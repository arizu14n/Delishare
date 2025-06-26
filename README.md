Delishare: Tu Cocina, Nuestros Secretos 👨‍🍳👩‍🍳
Descripción del Proyecto
Delishare es una aplicación web de recetas que permite a los usuarios explorar, buscar y compartir una vasta colección de recetas. Ofrece funcionalidades de autenticación de usuarios (registro e inicio de sesión), gestión de recetas, visualización de categorías, y un sistema de suscripción premium para acceder a contenido exclusivo.
El proyecto está dividido en dos componentes principales: un backend API RESTful desarrollado en PHP y un frontend interactivo construido con HTML, CSS y JavaScript puro.
Características Principales
Para Usuarios No Registrados:
Explorar todas las recetas gratuitas.
Buscar recetas por título, descripción e ingredientes.
Filtrar recetas por categoría y dificultad.
Ver listados de categorías.
Acceder a las páginas de inicio de sesión y registro.
Conocer los planes de suscripción.
Para Usuarios Registrados (Gratuitos):
Todas las características de usuarios no registrados.
Añadir nuevas recetas (que por defecto no son premium).
Para Usuarios Premium (Suscritos):
Acceso a todas las recetas, incluyendo las marcadas como premium.
Todas las características de los usuarios registrados gratuitos.
Posibilidad de marcar sus propias recetas como premium al crearlas.
Funcionalidades Técnicas:
API RESTful para la gestión de datos.
Autenticación de usuarios segura (hashing de contraseñas).
Manejo de CORS para comunicación entre frontend y backend.
Simulación de activación de suscripciones.
Interfaz de usuario interactiva y responsiva.
Tecnologías Utilizadas
Backend (API RESTful)
PHP: Lenguaje de programación principal.
PDO: Para una interacción segura y orientada a objetos con la base de datos.
MySQL: Sistema de gestión de bases de datos relacionales.
Frontend
HTML5: Estructura de las páginas web.
CSS3: Estilos y diseño 
JavaScript (Vanilla JS): Lógica interactiva del lado del cliente, manejo de la API y manipulación del DOM.
Font Awesome: Biblioteca de iconos para elementos visuales.
Requisitos
Backend
Servidor Web: Apache, Nginx o similar con soporte para PHP.
PHP: Versión 7.4+ (se recomienda PHP 8.x para mejor rendimiento y seguridad).
Extensión PDO_MySQL: Habilitada en PHP.
MySQL: Base de datos relacional.
Frontend
 	Un navegador web moderno (Chrome, Firefox, Edge, Safari, etc.).
Instalación y Configuración
Sigue estos pasos para poner el proyecto en funcionamiento en tu máquina local.
1.	Clonar el Repositorio
Bash
git clone https://github.com/arizu14n/Delishare.git
cd Delishare
2.	Configuración del Backend
1. Configurar Base de Datos MySQL:
Crea una base de datos MySQL (ej: recetas_db ).
Esquema de la Base de Datos: Deberás crear las tablas usuarios , categorias y recetas con las estructuras que se desprenden de los modelos PHP (consulta los 
archivos models/usuario.php , models/categoria.php , models/receta.php para los campos requeridos). Aquí un esquema simplificado a modo de guía:
SQL
2.	-- Base de datos actualizada con mejoras de seguridad y rendimiento
3.	CREATE DATABASE IF NOT EXISTS recetas_cocina_prueba CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
4.	USE recetas_cocina_prueba;
5.	
6.	-- Tabla de usuarios con mejoras
7.	CREATE TABLE usuarios (
8.	    id INT AUTO_INCREMENT PRIMARY KEY,
9.	    nombre VARCHAR(100) NOT NULL,
10.	    email VARCHAR(150) NOT NULL UNIQUE,
11.	    password VARCHAR(255) NOT NULL,
12.	    tipo_suscripcion ENUM('gratuito', 'premium') DEFAULT 'gratuito',
13.	    fecha_suscripcion DATE NULL,
14.	    fecha_vencimiento DATE NULL,
15.	    activo BOOLEAN DEFAULT TRUE,
16.	    intentos_login INT DEFAULT 0,
17.	    bloqueado_hasta TIMESTAMP NULL,
18.	    ultimo_login TIMESTAMP NULL,
19.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
20.	    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
21.	    
22.	    INDEX idx_email (email),
23.	    INDEX idx_tipo_suscripcion (tipo_suscripcion),
24.	    INDEX idx_activo (activo)
25.	);
26.	
27.	-- Tabla de categorías
28.	CREATE TABLE categorias (
29.	    id INT AUTO_INCREMENT PRIMARY KEY,
30.	    nombre VARCHAR(100) NOT NULL UNIQUE,
31.	    descripcion TEXT,
32.	    icono VARCHAR(50) DEFAULT 'fas fa-utensils',
33.	    activo BOOLEAN DEFAULT TRUE,
34.	    orden INT DEFAULT 0,
35.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
36.	    
37.	    INDEX idx_activo (activo),
38.	    INDEX idx_orden (orden)
39.	);
40.	
41.	-- Tabla de recetas mejorada
42.	CREATE TABLE recetas (
43.	    id INT AUTO_INCREMENT PRIMARY KEY,
44.	    titulo VARCHAR(200) NOT NULL,
45.	    descripcion TEXT,
46.	    ingredientes TEXT NOT NULL,
47.	    instrucciones TEXT NOT NULL,
48.	    tiempo_preparacion INT DEFAULT 0, -- en minutos
49.	    porciones INT DEFAULT 1,
50.	    dificultad ENUM('Fácil', 'Intermedio', 'Difícil') DEFAULT 'Fácil',
51.	    categoria_id INT,
52.	    imagen_url VARCHAR(500),
53.	    autor VARCHAR(100) DEFAULT 'Anónimo',
54.	    es_premium BOOLEAN DEFAULT FALSE,
55.	    vistas INT DEFAULT 0,
56.	    likes INT DEFAULT 0,
57.	    activo BOOLEAN DEFAULT TRUE,
58.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
59.	    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
60.	    
61.	    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
62.	    
63.	    INDEX idx_categoria (categoria_id),
64.	    INDEX idx_es_premium (es_premium),
65.	    INDEX idx_dificultad (dificultad),
66.	    INDEX idx_activo (activo),
67.	    INDEX idx_created_at (created_at),
68.	    FULLTEXT idx_busqueda (titulo, descripcion, ingredientes)
69.	);
70.	
71.	-- Tabla de valoraciones
72.	CREATE TABLE valoraciones (
73.	    id INT AUTO_INCREMENT PRIMARY KEY,
74.	    receta_id INT NOT NULL,
75.	    usuario_id INT NULL,
76.	    puntuacion INT CHECK (puntuacion >= 1 AND puntuacion <= 5),
77.	    comentario TEXT,
78.	    nombre_usuario VARCHAR(100),
79.	    activo BOOLEAN DEFAULT TRUE,
80.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
81.	    
82.	    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
83.	    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
84.	    
85.	    INDEX idx_receta (receta_id),
86.	    INDEX idx_usuario (usuario_id),
87.	    INDEX idx_puntuacion (puntuacion)
88.	);
89.	
90.	-- Tabla de favoritos
91.	CREATE TABLE favoritos (
92.	    id INT AUTO_INCREMENT PRIMARY KEY,
93.	    usuario_id INT NOT NULL,
94.	    receta_id INT NOT NULL,
95.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
96.	    
97.	    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
98.	    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
99.	    
100.	    UNIQUE KEY unique_favorito (usuario_id, receta_id),
101.	    INDEX idx_usuario (usuario_id),
102.	    INDEX idx_receta (receta_id)
103.	);
104.	
105.	-- Tabla de planes de suscripción
106.	CREATE TABLE planes_suscripcion (
107.	    id INT AUTO_INCREMENT PRIMARY KEY,
108.	    nombre VARCHAR(50) NOT NULL,
109.	    precio DECIMAL(10,2) NOT NULL,
110.	    duracion_dias INT NOT NULL,
111.	    descripcion TEXT,
112.	    activo BOOLEAN DEFAULT TRUE,
113.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
114.	    
115.	    INDEX idx_activo (activo)
116.	);
117.	
118.	-- Tabla de logs de actividad
119.	CREATE TABLE logs_actividad (
120.	    id INT AUTO_INCREMENT PRIMARY KEY,
121.	    usuario_id INT NULL,
122.	    accion VARCHAR(100) NOT NULL,
123.	    tabla_afectada VARCHAR(50),
124.	    registro_id INT,
125.	    ip_address VARCHAR(45),
126.	    user_agent TEXT,
127.	    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
128.	    
129.	    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
130.	    
131.	    INDEX idx_usuario (usuario_id),
132.	    INDEX idx_accion (accion),
133.	    INDEX idx_created_at (created_at)
134.	);
135.	
136.	-- Insertar categorías con iconos
137.	INSERT INTO categorias (nombre, descripcion, icono, orden) VALUES
138.	('Desayunos', 'Recetas para comenzar el día', 'fas fa-coffee', 1),
139.	('Almuerzos', 'Comidas principales del mediodía', 'fas fa-hamburger', 2),
140.	('Cenas', 'Recetas para la noche', 'fas fa-moon', 3),
141.	('Postres', 'Dulces y postres deliciosos', 'fas fa-ice-cream', 4),
142.	('Bebidas', 'Jugos, batidos y bebidas', 'fas fa-glass-cheers', 5),
143.	('Aperitivos', 'Entradas y bocadillos', 'fas fa-cheese', 6),
144.	('Vegetarianas', 'Recetas sin carne', 'fas fa-leaf', 7),
145.	('Veganas', 'Recetas completamente vegetales', 'fas fa-seedling', 8);
146.	
147.	-- Insertar planes de suscripción
148.	INSERT INTO planes_suscripcion (nombre, precio, duracion_dias, descripcion) VALUES
149.	('Mensual', 9.99, 30, 'Acceso completo por 1 mes'),
150.	('Trimestral', 24.99, 90, 'Acceso completo por 3 meses (17% descuento)'),
151.	('Anual', 79.99, 365, 'Acceso completo por 1 año (33% descuento)');
152.	
153.	-- Insertar usuario administrador (contraseña: admin123)
154.	INSERT INTO usuarios (nombre, email, password, tipo_suscripcion) VALUES
155.	('Administrador', 'admin@recetas.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'premium');
156.	
157.	-- Insertar recetas de ejemplo mejoradas
158.	INSERT INTO recetas (titulo, descripcion, ingredientes, instrucciones, tiempo_preparacion, porciones, dificultad, categoria_id, autor, es_premium) VALUES
159.	('Pancakes Esponjosos', 'Deliciosos pancakes perfectos para el desayuno familiar', 
160.	'2 tazas de harina todo uso\n1 taza de leche entera\n2 huevos grandes\n2 cucharadas de azúcar\n1 cucharadita de polvo de hornear\nPizca de sal\nMantequilla para cocinar\nMiel o jarabe de maple para servir', 
161.	'1. En un bowl grande, mezclar todos los ingredientes secos: harina, azúcar, polvo de hornear y sal\n2. En otro bowl, batir los huevos con la leche hasta integrar completamente\n3. Verter la mezcla líquida sobre los ingredientes secos y mezclar hasta obtener una masa homogénea (no sobre mezclar)\n4. Calentar una sartén antiadherente a fuego medio y agregar un poco de mantequilla\n5. Verter 1/4 taza de masa por cada pancake\n6. Cocinar 2-3 minutos hasta que aparezcan burbujas en la superficie\n7. Voltear cuidadosamente y cocinar 1-2 minutos más hasta dorar\n8. Servir inmediatamente con miel o jarabe de maple caliente', 
162.	20, 4, 'Fácil', 1, 'Chef María González', FALSE),
163.	
164.	('Ensalada César Gourmet', 'La clásica ensalada César con un toque gourmet y aderezo casero', 
165.	'2 lechugas romanas grandes\n4 rebanadas de pan integral\n100g de queso parmesano\n2 pechugas de pollo\n1/2 taza de aceite de oliva extra virgen\n2 limones\n3 dientes de ajo\n1 cucharada de mostaza Dijon\n4 filetes de anchoas\n1 huevo\nSal y pimienta negra recién molida', 
166.	'1. Lavar y secar completamente las lechugas, cortar en trozos medianos\n2. Para el aderezo: en un bowl pequeño, machacar el ajo con sal hasta formar una pasta\n3. Agregar mostaza Dijon, anchoas picadas y mezclar bien\n4. Incorporar el jugo de limón y batir mientras se agrega el aceite de oliva lentamente\n5. Agregar el huevo y batir hasta obtener una consistencia cremosa\n6. Sazonar con pimienta negra recién molida\n7. Cortar el pan en cubos y tostar en el horno hasta dorar\n8. Cocinar las pechugas de pollo con sal, pimienta y hierbas hasta dorar completamente\n9. Dejar reposar el pollo 5 minutos y cortar en tiras\n10. En un bowl grande, mezclar la lechuga con el aderezo\n11. Agregar el pollo en tiras y los crutones\n12. Espolvorear generosamente con queso parmesano rallado\n13. Servir inmediatamente acompañado de pan tostado', 
167.	35, 2, 'Intermedio', 2, 'Chef Carlos Mendoza', TRUE);
168.	
169.	-- Crear vistas para consultas frecuentes
170.	CREATE VIEW vista_recetas_populares AS
171.	SELECT r.*, c.nombre as categoria_nombre, 
172.	       (SELECT AVG(puntuacion) FROM valoraciones v WHERE v.receta_id = r.id) as rating_promedio,
173.	       (SELECT COUNT(*) FROM valoraciones v WHERE v.receta_id = r.id) as total_valoraciones
174.	FROM recetas r
175.	LEFT JOIN categorias c ON r.categoria_id = c.id
176.	WHERE r.activo = TRUE
177.	ORDER BY r.vistas DESC, r.likes DESC;
178.	
179.	-- Procedimiento almacenado para actualizar estadísticas
180.	DELIMITER //
181.	CREATE PROCEDURE ActualizarEstadisticasReceta(IN receta_id INT)
182.	BEGIN
183.	    UPDATE recetas 
184.	    SET vistas = vistas + 1 
185.	    WHERE id = receta_id;
186.	END //
187.	DELIMITER ;


Actualizar Configuración de la Base de Datos:
Abre recetas-api/config/config.php .
Edita las constantes DB_HOST , DB_NAME , DB_USER , DB_PASS con tus credenciales de MySQL.
Servir el Backend:
 	Coloca el contenido de la carpeta recetas-api/ en tu servidor web (por ejemplo, en htdocs de Apache o un directorio configurado para Nginx).
	 	Asegúrate de que la URL base de tu API apunte correctamente a recetas-api/endpoints/ . 
Por ejemplo, si lo colocas en la raíz de tu localhost , sería http://localhost/endpoints .
  Importante: Asegúrate de que la constante API_BASE_URL en recetas-frontend/js/shared.js coincida con la URL de tu API backend (ej: const API_BASE_URL = "http://localhost/recetas-api/api/endpoints"; ).
3. Configuración del Frontend
1. Servir el Frontend:
 	Coloca el contenido de la carpeta recetas-frontend/ en tu servidor web o simplemente abre recetas-frontend/inicio.html directamente en tu navegador. Dado que es JavaScript puro, no 
requiere un servidor de desarrollo complejo.
Uso de la Aplicación
1.	Abre inicio.html en tu navegador.
2.	Explora Recetas: Navega por las categorías destacadas, utiliza la barra de búsqueda o visita la página de Recetas para ver todas las opciones.
3.	Registro: Si eres un nuevo usuario, haz clic en Registrarse y completa el formulario.
4.	Inicio de Sesión: Si ya tienes una cuenta, haz clic en Iniciar Sesión para acceder a tu perfil.
5.	Añadir Recetas: Una vez iniciada la sesión, en la página de Recetas , podrás ver el botón "Añadir Receta". Completa el formulario para compartir tus propias creaciones.
6.	Suscripción Premium: En la página de Suscripción , podrás ver los beneficios del plan premium. Los usuarios autenticados pueden simular la actualización a premium.
Endpoints de la API (Resumen)
El backend expone los siguientes endpoints principales:
  POST /auth.php : Gestiona el registro ( action=register ) y el inicio de sesión ( action=login ) de usuarios.
 	GET /recetas.php : Obtiene una lista de recetas (todas, filtradas por búsqueda/categoría/dificultad) o los detalles de una receta específica por ID.
POST /recetas.php : Permite crear una nueva receta.
GET /categorias.php : Devuelve una lista de todas las categorías de recetas.
POST /suscripcion.php : Simula la activación o actualización de la suscripción de un usuario a un plan premium.
Posibles Mejoras Futuras
Autenticación JWT: Implementar tokens JWT para una gestión de sesiones más segura y escalable.
Funcionalidades CRUD Completas: Añadir la capacidad de actualizar y eliminar recetas/categorías desde el frontend.
Integración Real de Pagos: Conectar el endpoint de suscripción con pasarelas de pago reales (ej. Stripe, PayPal).
Perfiles de Usuario: Permitir a los usuarios editar su perfil, cambiar contraseña, etc.
Favoritos/Colecciones: Implementar funcionalidad para que los usuarios guarden sus recetas favoritas.
Sistema de Valoraciones: Permitir a los usuarios calificar y dejar comentarios en las recetas.
Dashboard de Administrador: Interfaz para gestionar usuarios, recetas y categorías por parte de un administrador.
Manejo de Imágenes: Implementar carga de imágenes directamente al servidor en lugar de solo URLs.
Manejo de Errores Consistente: Asegurar que todos los endpoints utilicen jsonResponse() y bloques try-catch para un manejo de errores estandarizado.
