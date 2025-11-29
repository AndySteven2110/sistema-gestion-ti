-- ============================================================
--  SCHEMA COMPLETO DEL SISTEMA DE GESTIÓN DE TI
--  Basado fielmente en el diagrama ER proporcionado
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

CREATE TABLE categorias_equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    vida_util_anos INT,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE movimientos_equipos (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT NOW(),
    ubicacion_origen_id INT REFERENCES ubicaciones(id),
    ubicacion_destino_id INT REFERENCES ubicaciones(id),
    motivo TEXT,
    observaciones TEXT,
    usuario_responsable_id INT REFERENCES usuarios(id),
    equipo_id INT REFERENCES equipos(id)
);

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

CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedores(id),
    numero_contrato VARCHAR(100),
    tipo VARCHAR(100),
    fecha_inicio DATE,
    fecha_fin DATE,
    monto_total DECIMAL(12,2),
    archivo_url TEXT,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT NOW()
);

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

