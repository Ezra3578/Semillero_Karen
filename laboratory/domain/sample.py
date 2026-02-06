from datetime import date, time
from typing import Optional, Dict


class Sample:
    def __init__(
        self,
        *,
        codigo: str,
        fecha: date,
        hora: time,
        fuente: str,
        quien_muestra: str,
        dispositivo: str,
        tipo_agua: str,
        codigo_red: Optional[str] = None,
        observaciones: Optional[str] = None,
        ph: Optional[float] = None,
        cloro: Optional[float] = None,
        temperatura: Optional[float] = None,
    ):
        # Identidad
        self.codigo = codigo

        # Registro
        self.fecha = fecha
        self.hora = hora
        self.fuente = fuente
        self.quien_muestra = quien_muestra
        self.dispositivo = dispositivo
        self.tipo_agua = tipo_agua
        self.codigo_red = codigo_red
        self.observaciones = observaciones

        # Datos in situ
        self.ph = ph
        self.cloro = cloro
        self.temperatura = temperatura

        # Estados (Por defecto)
        self.estado_fq = "no_aplica"
        self.estado_micro = "no_aplica"

        # Resultados (inicialmente vacíos)
        self.resultados_fq: Dict[str, float] = {}
        self.resultados_micro: Dict[str, float] = {}


    def to_dict(self) -> dict:
        return {
            "Código": self.codigo,
            "Fecha": self.fecha.strftime("%Y-%m-%d"),
            "Hora": self.hora.strftime("%H:%M"),
            "Fuente": self.fuente,
            "Quién Muestra": self.quien_muestra,
            "Dispositivo": self.dispositivo,
            "Tipo Agua": self.tipo_agua,
            "Código Red": self.codigo_red,
            "pH": self.ph,
            "Cloro": self.cloro,
            "Temperatura": self.temperatura,
            "Observaciones": self.observaciones,
            "Estado_FQ": self.estado_fq,
            "Estado_Micro": self.estado_micro,
            "Resultados_FQ": self.resultados_fq,
            "Resultados_Micro": self.resultados_micro,
        }

    
    def add_resultado_fq(self, parametro: str, valor: float):
        self.resultados_fq[parametro] = valor
        self.estado_fq = "completado"


    def add_resultado_micro(self, parametro: str, valor: float):
        self.resultados_micro[parametro] = valor
        self.estado_micro = "completado"
