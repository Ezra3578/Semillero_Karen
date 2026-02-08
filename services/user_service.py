import json
import bcrypt

USUARIOS_FILE = "data/usuarios.json"

def cargar_usuarios() -> list[dict]:
    """Cargar usuarios desde JSON"""
    try:
        with open(USUARIOS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_usuarios(usuarios: list[dict]):
    """Guardar usuarios en JSON"""
    with open(USUARIOS_FILE, "w") as f:
        json.dump(usuarios, f, indent=4)

def crear_usuario(nombre: str, correo: str, usuario: str, contrasena: str, rol: str) -> dict:
    """Crear un usuario con contraseña hasheada"""
    hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()
    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "usuario": usuario,
        "contrasena": hashed,
        "rol": rol
    }
    return nuevo_usuario

def actualizar_usuario(usuario_obj: dict, nombre: str, correo: str, rol: str, nueva_contrasena: str | None = None):
    """Actualizar campos de un usuario existente"""
    usuario_obj["nombre"] = nombre
    usuario_obj["correo"] = correo
    usuario_obj["rol"] = rol
    if nueva_contrasena:
        hashed = bcrypt.hashpw(nueva_contrasena.encode(), bcrypt.gensalt()).decode()
        usuario_obj["contrasena"] = hashed

def eliminar_usuario(usuarios: list[dict], usuario_nombre: str) -> list[dict]:
    """Eliminar usuario por su nombre de usuario"""
    return [u for u in usuarios if u["usuario"] != usuario_nombre]
