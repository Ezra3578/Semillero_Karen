from datetime import date
from typing import Iterable


def generate_sample_code(*, fecha: date, tipo_muestra: str, existing_codes: Iterable[str],) -> str:
    
    # Genera un código único de muestra con el formato:
    # <Letra><YYMMDD><NNN>

    # Ejemplo:
    # R250205003
    

    # Fecha en formato YYMMDD
    fecha_codigo = fecha.strftime("%y%m%d")

    # Prefijo según tipo de muestra
    letra = {
        "Interna": "I",
        "Red": "R",
        "Externa": "E",
    }.get(tipo_muestra)

    if not letra:
        raise ValueError(f"Tipo de muestra inválido: {tipo_muestra}")

    # Extraer consecutivos del mismo día
    consecutivos = []
    for codigo in existing_codes:
        if not codigo or len(codigo) < 8:
            continue

        if codigo[1:7] == fecha_codigo:
            try:
                consecutivos.append(int(codigo[7:]))
            except ValueError:
                continue

    # Calcular siguiente consecutivo
    siguiente = max(consecutivos, default=0) + 1

    return f"{letra}{fecha_codigo}{siguiente:03d}"
