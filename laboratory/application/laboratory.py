from typing import Literal

from laboratory.use_cases.register_sample import register_sample_uc
from laboratory.use_cases.reception import receive_sample_uc
from laboratory.use_cases.update_reception import update_reception_parameters_uc
from laboratory.use_cases.analysis import analyze_sample_uc
from laboratory.use_cases import consult

from laboratory.domain.sample import Sample
from laboratory.repository import load_samples, save_samples


class Laboratory:

    # ---------- HELPERS ----------

    #Reemplazar y guardar la mues
    def _replace_and_save(self, samples: list[dict], sample: Sample):
        for i, s in enumerate(samples):
            if s.get("Código") == sample.codigo:
                samples[i] = sample.to_dict()
                break
        else:
            raise ValueError("No se pudo reemplazar la muestra")
        
        save_samples(samples)


    # ---------- QUERIES ----------

    #Obtener todas las muestras
    def get_samples(self) -> list[dict]:
        return load_samples()

    # Filtrar muestras según criterios
    def filter_samples(self, *, fuente=None, mes=None, dia=None) -> list[dict]:
        samples = load_samples()
        filtradas = consult.filter_samples_by_fuente_uc(samples, fuente)
        filtradas = consult.filter_samples_by_mes_uc(filtradas, mes)
        filtradas = consult.filter_samples_by_dia_uc(filtradas, dia)
        return filtradas

    #Buscar una muestra por su código    
    def search_sample_by_code(self, codigo: str, samples) -> dict:
        return consult.search_sample_by_code_uc(samples, codigo)

    #Busqueda de las muestras para el analisis. Según el tipo (FQ o Micro) y su estado (pendiente o analizado)
    def get_analysis_view(self, *, tipe: Literal["FQ", "Micro"], state: Literal["pendiente", "analizado"]) -> dict[str, dict]:
        samples = load_samples()
        return consult.get_analysis_view_uc(samples, tipe=tipe, state=state)
    
    #Obtiene las muestras que estén pendientes por ser recibidas
    def get_pending_samples(self) -> list[dict]:
        samples = load_samples()
        return consult.filter_samples_by_reception_state_uc(samples, estados=[None, "sin_recibir"])
    
    #Obtiene las muestras que fueron recibidas
    def get_received_samples(self) -> list[dict]:
        samples = load_samples()
        return consult.filter_samples_by_reception_state_uc(samples, estados=["recibida"])
    
    # Eliminar muestra
    def delete_sample(self, codigo: str) -> bool:
        samples = load_samples()
        samples = consult.delete_sample_from_list_uc(samples, codigo)
        save_samples(samples)
        return True

    # ---------- COMMANDS ----------
    #Registrar una muestra
    def register_sample(self, data: dict) -> Sample:
        samples = load_samples()
        existing_codes = [s["Código"] for s in samples if "Código" in s]

        sample = register_sample_uc(
            data=data,
            existing_codes=existing_codes,
        )

        samples.append(sample.to_dict())
        save_samples(samples)
        return sample

    #Recibir una muestra
    def receive_sample(self,*,codigo: str, fecha_recepcion,hora_recepcion, 
                       temperatura_recepcion, recepciona,
                       parametros_fq, parametros_micro,):

        #Cargar muestras
        samples = load_samples()
        
        #Buscar por codigo
        raw = self.search_sample_by_code(codigo, samples)

        #Construir objeto de Sample
        sample = Sample.from_dict(raw)

        #Aplicar recepcion
        receive_sample_uc(
            sample=sample,
            fecha_recepcion=fecha_recepcion,
            hora_recepcion=hora_recepcion,
            temperatura_recepcion=temperatura_recepcion,
            recepciona=recepciona,
            parametros_fq=parametros_fq,
            parametros_micro=parametros_micro,
        )

        #Persistencia
        self._replace_and_save(samples, sample)
        return sample

    def update_reception_parameters(self, *, codigo: str,
                                    parametros_fq, parametros_micro,):

        # Cargar muestras
        samples = load_samples()

        #Buscar por código
        raw = self.search_sample_by_code(codigo, samples)
        
        #Construir la Sample
        sample = Sample.from_dict(raw)

        #Aplicar actualizacion
        update_reception_parameters_uc(
            sample=sample,
            parametros_fq=parametros_fq,
            parametros_micro=parametros_micro,
        )

        #Persistencia
        self._replace_and_save(samples, sample)
        return sample

    #Analizar la muestra
    def analyze_sample(self, *, codigo: str,
                       fq: dict | None = None,
                       micro: dict | None = None,):

        #Cargar muestra
        samples = load_samples()
        
        #Buscar por código
        raw = self.search_sample_by_code(codigo, samples)
        
        #Crear Sample
        sample = Sample.from_dict(raw)

        #Aplicar Análisis
        analyze_sample_uc(
            sample=sample,
            fq=fq,
            micro=micro
        )

        self._replace_and_save(samples, sample)
        return sample
