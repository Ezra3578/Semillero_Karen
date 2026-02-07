from typing import Iterable

from laboratory.domain.sample import Sample
from laboratory.domain.rules import validate_sample_input
from laboratory.domain.sample_code_generator import generate_sample_code


def register_sample_uc(data: dict, *, existing_codes: Iterable[str],) -> Sample:
    
    # Validar reglas de negocio
    validate_sample_input(data)

    # Generar el ID
    codigo = generate_sample_code(
        fecha=data["fecha"],
        tipo_muestra=data["tipo_muestra"],
        existing_codes=existing_codes,
    )

    # Crea la muestra
    sample = Sample(
        codigo=codigo,
        fecha=data["fecha"],
        hora=data["hora"],
        fuente=data["fuente"],
        quien_muestra=data["quien_muestra"],
        dispositivo=data["dispositivo"],
        tipo_agua=data["tipo_agua"],
        codigo_red=data.get("codigo_red"),
        observaciones=data.get("observaciones"),
        ph=data.get("ph"),
        cloro=data.get("cloro"),
        temperatura=data.get("temperatura"),
    )

    return sample
