from datetime import date, time
from typing import Optional, Dict, List


class Sample:
    """
    Entidad de dominio que representa una muestra de laboratorio
    durante todo su ciclo de vida:
    registro → recepción → análisis
    """

    def __init__(
        self,
        *,
        codigo: str,

        # Registro
        fecha: date,
        hora: time,
        quien_muestra: str,
        dispositivo: str,
        fuente: str,
        tipo_agua: str,
        codigo_red: Optional[str] = None,   #Opcional pues depende de Red
        observaciones: Optional[str] = None,#Pueden no haber observaciones

        # Datos in situ - Pueden no agregarse valores
        ph: Optional[float] = None,
        cloro: Optional[float] = None,
        temperatura: Optional[float] = None,

        # Recepción (inicialmente vacíos)
        fecha_recepcion: Optional[date] = None,
        hora_recepcion: Optional[time] = None,
        temperatura_recepcion: Optional[float] = None,
        recepciona: Optional[str] = None,
        parametros_a_analizar: Optional[Dict[str, List[str]]] = None,

        # Estados
        estado_recepcion: str = "sin_recibir",  #Estados: sin_recibir, recibida
        estado_fq: str = "sin_definir",         #Estados: "sin_definir", "no_aplica", "pendiente", "analizado"
        estado_micro: str = "sin_definir",      #Estados: "sin_definir", "no_aplica", "pendiente", "analizado"

        # Resultados
        resultados: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        #ID
        self.codigo = codigo

        #Datos de Registro
        self.fecha = fecha
        self.hora = hora
        self.quien_muestra = quien_muestra
        self.dispositivo = dispositivo
        self.fuente = fuente
        self.tipo_agua = tipo_agua
        self.codigo_red = codigo_red
        self.observaciones = observaciones

        #Datos in Situ
        self.ph = ph
        self.cloro = cloro
        self.temperatura = temperatura

        #Datos de Recepcion
        self.fecha_recepcion = fecha_recepcion
        self.hora_recepcion = hora_recepcion
        self.temperatura_recepcion = temperatura_recepcion
        self.recepciona = recepciona
        self.parametros_a_analizar = parametros_a_analizar or {
            "FQ": [],
            "Micro": []
        }

        #Estado de recepcion y analisis
        self.estado_recepcion = estado_recepcion
        self.estado_fq = estado_fq
        self.estado_micro = estado_micro

        #Resultados de la muestra (vacíos o los que posea)
        self.resultados = resultados or {
            "FQ": {},
            "Micro": {}
        }

    #Recepcion de la muestra
    def receive(self, *, fecha: date, hora: time,
                temperatura: float, recepciona: str,
                parametros_fq: List[str], parametros_micro: List[str],):
        
        if self.estado_recepcion != "sin_recibir":  #Si ya fue recibida marca error
            raise ValueError("La muestra ya fue recepcionada")

        self.estado_recepcion = "recibida"
        self.fecha_recepcion = fecha
        self.hora_recepcion = hora
        self.temperatura_recepcion = temperatura
        self.recepciona = recepciona

        self.parametros_a_analizar = {
            "FQ": parametros_fq,
            "Micro": parametros_micro,
        }

        self.estado_fq = "pendiente" if parametros_fq else "no_aplica"
        self.estado_micro = "pendiente" if parametros_micro else "no_aplica"


    #Resultados de Análisis
    def add_results(self, *,
                    fq: Optional[Dict[str, float]] = None,
                    micro: Optional[Dict[str, float]] = None,):
        
        if self.estado_recepcion != "recibida": #Si la muestra sigue "sin_recibir", marca error
            raise ValueError("No se puede analizar una muestra no recibida")

        if fq:
            self.resultados["FQ"].update(fq)
            self.estado_fq = "analizado"

        if micro:
            self.resultados["Micro"].update(micro)
            self.estado_micro = "analizado"

    
    #Convierte el objeto al formato JSON
    def to_dict(self) -> dict:
        
        return {
            "Código": self.codigo,
            "Fecha": self.fecha.isoformat(),
            "Hora": self.hora.strftime("%H:%M"),
            "Quién Muestra": self.quien_muestra,
            "Dispositivo": self.dispositivo,
            "Fuente": self.fuente,
            "Código Red": self.codigo_red,
            "Tipo Agua": self.tipo_agua,
            "pH": self.ph,
            "Cloro": self.cloro,
            "Temperatura": self.temperatura,
            "Observaciones": self.observaciones,

            "Estado Recepción": self.estado_recepcion,
            "Fecha Recepción": self.fecha_recepcion.isoformat() if self.fecha_recepcion else None,
            "Hora Recepción": self.hora_recepcion.strftime("%H:%M") if self.hora_recepcion else None,
            "Temperatura Recepción": self.temperatura_recepcion,
            "Recepcionó": self.recepciona,

            "Parámetros a analizar": self.parametros_a_analizar,
            "Estado_FQ": self.estado_fq,
            "Estado_Micro": self.estado_micro,
            "Resultados": self.resultados,
        }
    
    #Convierte de JSON a Sample
    @classmethod
    def from_dict(cls, data: dict) -> "Sample":
        from datetime import date, time

        return cls(
            codigo=data["Código"],
            fecha=date.fromisoformat(data["Fecha"]),
            hora=time.fromisoformat(data["Hora"]),
            quien_muestra=data["Quién Muestra"],
            dispositivo=data["Dispositivo"],
            fuente=data["Fuente"],
            tipo_agua=data["Tipo Agua"],
            codigo_red=data.get("Código Red"),
            observaciones=data.get("Observaciones"),

            ph=data.get("pH"),
            cloro=data.get("Cloro"),
            temperatura=data.get("Temperatura"),

            fecha_recepcion=date.fromisoformat(data["Fecha Recepción"])
            if data.get("Fecha Recepción") else None,

            hora_recepcion=time.fromisoformat(data["Hora Recepción"])
            if data.get("Hora Recepción") else None,

            temperatura_recepcion=data.get("Temperatura Recepción"),
            recepciona=data.get("Recepcionó"),

            parametros_a_analizar=data.get("Parámetros a analizar"),

            estado_recepcion=data.get("Estado Recepción", "sin_recibir"),
            estado_fq=data.get("Estado_FQ", "sin_definir"),
            estado_micro=data.get("Estado_Micro", "sin_definir"),

            resultados=data.get("Resultados"),
        )

