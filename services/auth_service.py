import json
import os
import bcrypt

from utils.validator import validar_contrasena, validar_email

RUTA_USUARIOS = "data/usuarios.json"


# PERSISTENCIA (Más adelante usando DB, actual JSON)
def _cargar_usuarios() -> list:
    if not os.path.exists(RUTA_USUARIOS):
        return []

    try:
        with open(RUTA_USUARIOS, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _guardar_usuarios(usuarios: list) -> None:
    with open(RUTA_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)



# REGISTRO
def registrar_usuario(nombre, correo, usuario, contrasena, rol="usuario"):
    if not all([nombre, correo, usuario, contrasena]):
        return False, "Todos los campos son obligatorios."

    if not validar_email(correo):
        return False, "Correo electrónico inválido."

    if not validar_contrasena(contrasena):
        return False, "La contraseña no cumple los requisitos de seguridad.Debe contener al menos 8 carácteres, una mayúscula, una minúscula, un número y un carácter especial."

    usuarios = _cargar_usuarios()

    if any(u["usuario"] == usuario for u in usuarios):
        return False, "El nombre de usuario ya existe."

    hashed = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

    usuarios.append({
        "nombre": nombre,
        "correo": correo,
        "usuario": usuario,
        "contrasena": hashed,
        "rol": rol
    })

    _guardar_usuarios(usuarios)
    return True, "Usuario registrado exitosamente."


# LOGIN
def login(usuario, contrasena):
    usuarios = _cargar_usuarios()

    user = next((u for u in usuarios if u["usuario"] == usuario), None)
    if not user:
        return False, "Usuario no encontrado.", None

    if not bcrypt.checkpw(contrasena.encode(), user["contrasena"].encode()):
        return False, "Contraseña incorrecta.", None

    return True, "Login exitoso.", {
        "usuario": user["usuario"],
        "nombre": user["nombre"],
        "rol": user.get("rol", "usuario")
    }
