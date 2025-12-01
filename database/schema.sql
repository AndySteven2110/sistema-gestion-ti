-- ============================================================
--  SCHEMA COMPLETO DEL SISTEMA DE GESTIÓN DE TI + DATOS DE PRUEBA
-- ============================================================

DROP TABLE IF EXISTS notificaciones CASCADE;
DROP TABLE IF EXISTS mantenimientos CASCADE;
DROP TABLE IF EXISTS movimientos_equipos CASCADE;
DROP TABLE IF EXISTS equipos CASCADE;
DROP TABLE IF EXISTS contratos CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;
DROP TABLE IF EXISTS categorias_equipos CASCADE;
DROP TABLE IF EXISTS ubicaciones CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- ============================================================
-- TABLA USUARIOS
-- ============================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol VARCHAR(50) NOT NULL,
    nombre_completo VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    ultima_conexion TIMESTAMP
);

INSERT INTO usuarios (username, email, password_hash, rol, nombre_completo)
VALUES
('admin', 'admin@universidad.edu', 'hash123', 'admin', 'Administrador TI'),
('tecnico1', 'tecnico1@universidad.edu', 'hash123', 'tecnico', 'Juan Pérez'),
('tecnico2', 'tecnico2@universidad.edu', 'hash123', 'tecnico', 'Ana Torres');

-- ============================================================
-- TABLA UBICACIONES
-- ============================================================
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    edificio VARCHAR(150),
    piso VARCHAR(50),
    aula_oficina VARCHAR(100),
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    responsable_id INT REFERENCES usuarios(id)
);

INSERT INTO ubicaciones (edificio, piso, aula_oficina, descripcion, responsable_id)
VALUES
('Edificio A', '1', 'Aula 101', 'Laboratorio de Informática', 1),
('Edificio B', '2', 'Oficina 205', 'Área Administrativa TI', 1),
('Edificio C', '3', 'Aula 302', 'Laboratorio Redes', 2);

-- ============================================================
-- TABLA CATEGORÍAS
-- ============================================================
CREATE TABLE categorias_equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    vida_util_anos INT,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

INSERT INTO categorias_equipos (nombre, descripcion, vida_util_anos)
VALUES
('Laptop', 'Equipos portátiles', 4),
('PC Escritorio', 'Equipos de oficina', 5),
('Proyector', 'Equipos multimedia', 6),
('Impresora', 'Equipos de impresión', 5);

-- ============================================================
-- TABLA PROVEEDORES
-- ============================================================
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    razon_social VARCHAR(200) NOT NULL,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    direccion TEXT,
    telefono VARCHAR(30),
    email VARCHAR(200),
    contacto_nombre VARCHAR(200),
    contacto_telefono VARCHAR(50),
    sitio_web VARCHAR(200),
    calificacion DECIMAL(3,2),
    fecha_registro TIMESTAMP DEFAULT NOW(),
    notas TEXT
);

INSERT INTO proveedores (razon_social, ruc, telefono, email, contacto_nombre, contacto_telefono, calificacion)
VALUES
('TechSupply SAC', '20123456789', '987654321', 'ventas@techsupply.com', 'Carlos Ruiz', '955123456', 4.5),
('Proveedores UNI SRL', '20654321987', '912345678', 'contacto@uni-proveedores.com', 'María Lopez', '944998877', 4.0);

-- ============================================================
-- TABLA EQUIPOS
-- ============================================================
CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    ubicacion_actual_id INT REFERENCES ubicaciones(id),
    codigo_inventario VARCHAR(100) UNIQUE NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(150),
    numero_serie VARCHAR(150),
    especificaciones TEXT,
    fecha_compra DATE,
    costo_compra DECIMAL(12,2),
    categoria_id INT REFERENCES categorias_equipos(id),
    fecha_garantia_fin DATE,
    estado_operativo VARCHAR(50),
    estado_fisico VARCHAR(50),
    imagen_url TEXT,
    notas TEXT,
    fecha_registro TIMESTAMP DEFAULT NOW(),
    asignado_a_id INT REFERENCES usuarios(id),
    fecha_ultima_actualizacion TIMESTAMP DEFAULT NOW(),
    proveedor_id INT REFERENCES proveedores(id)
);

INSERT INTO equipos (
    ubicacion_actual_id, codigo_inventario, marca, modelo, numero_serie, 
    especificaciones, fecha_compra, costo_compra, categoria_id,
    fecha_garantia_fin, estado_operativo, estado_fisico, proveedor_id
) VALUES
(1, 'EQ-2024-001', 'Dell', 'Inspiron 15', 'SN123', 'i5, 8GB RAM, 256GB SSD', '2023-01-10', 2500.00, 1, '2025-01-10', 'operativo', 'bueno', 1),
(1, 'EQ-2024-002', 'HP', 'ProDesk 400', 'SN456', 'i7, 16GB RAM, 512GB SSD', '2022-05-18', 3200.00, 2, '2024-05-18', 'en_reparacion', 'regular', 2),
(2, 'EQ-2024-003', 'Epson', 'X450', 'SN789', 'Proyector HD', '2021-03-08', 1800.00, 3, '2023-03-08', 'operativo', 'bueno', 1),
(3, 'EQ-2024-004', 'Canon', 'LBP6030', 'SN159', 'Impresora Láser', '2020-10-21', 900.00, 4, '2022-10-21', 'obsoleto', 'regular', 2);

-- ============================================================
-- TABLA MANTENIMIENTOS
-- ============================================================
CREATE TABLE mantenimientos (
    id SERIAL PRIMARY KEY,
    equipo_id INT REFERENCES equipos(id),
    fecha_programada DATE,
    fecha_realizada DATE,
    descripcion TEXT,
    problema_reportado TEXT,
    solucion_aplicada TEXT,
    costo DECIMAL(12,2),
    tecnico_id INT REFERENCES usuarios(id),
    tiempo_fuera_servicio_horas INT,
    estado VARCHAR(50),
    prioridad VARCHAR(50),
    partes_reemplazadas JSON,
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    proveedor_id INT REFERENCES proveedores(id)
);

INSERT INTO mantenimientos (
    equipo_id, fecha_programada, fecha_realizada, descripcion,
    problema_reportado, solucion_aplicada, costo, tecnico_id,
    tiempo_fuera_servicio_horas, estado, prioridad, partes_reemplazadas
) VALUES
(1, '2024-01-10', '2024-01-12', 'Mantenimiento preventivo',
 'Ruido en ventilador', 'Limpieza interna', 120.00, 2, 4, 'completado', 'media', '["ventilador"]'),
(2, '2024-02-05', NULL, 'Revisión general',
 'No enciende', NULL, 0, 2, 0, 'pendiente', 'alta', '[]');

-- ============================================================
-- TABLA NOTIFICACIONES
-- ============================================================
CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    equipo_id INT REFERENCES equipos(id),
    tipo VARCHAR(100),
    mensaje TEXT NOT NULL,
    leido BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_lectura TIMESTAMP,
    mantenimiento_id INT REFERENCES mantenimientos(id),
    usuario_id INT REFERENCES usuarios(id)
);

INSERT INTO notificaciones (equipo_id, tipo, mensaje, usuario_id)
VALUES
(2, 'alerta', 'El equipo EQ-2024-002 requiere atención inmediata.', 1),
(1, 'recordatorio', 'Mantenimiento programado en 2 días.', 1);
