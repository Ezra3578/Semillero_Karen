from typing import List
from laboratory.domain.sample import Sample


def update_reception_parameters_uc(*, sample: Sample,
                                parametros_fq: List[str],
                                parametros_micro: List[str],) -> Sample:

    #Solo muestra ya recepcionada
    if sample.estado_recepcion != "recibida":
        raise ValueError("Solo se pueden modificar muestras ya recepcionadas")

    #Actualizacion xD
    sample.parametros_a_analizar = {
        "FQ": parametros_fq,
        "Micro": parametros_micro,
    }

    #Reajuste de estados
    sample.estado_fq = "pendiente" if parametros_fq else "no_aplica"
    sample.estado_micro = "pendiente" if parametros_micro else "no_aplica"

    return sample
