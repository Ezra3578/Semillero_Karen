from datetime import date, time
from typing import List

from laboratory.domain.sample import Sample

#Recepción a una muestra
def receive_sample_uc( *, sample: Sample, fecha_recepcion: date, hora_recepcion: time,
                    temperatura_recepcion: float, recepciona: str,
                    parametros_fq: List[str], parametros_micro: List[str],) -> Sample:
    

    sample.receive(
        fecha=fecha_recepcion,
        hora=hora_recepcion,
        temperatura=temperatura_recepcion,
        recepciona=recepciona,
        parametros_fq=parametros_fq,
        parametros_micro=parametros_micro,
    )

    return sample
