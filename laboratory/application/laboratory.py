from typing import Literal

from laboratory.use_cases.register_sample import register_sample_uc
from laboratory.use_cases.reception import receive_sample_uc
from laboratory.use_cases.update_reception import update_reception_parameters_uc
from laboratory.use_cases.analysis import analyze_sample_uc

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

    def get_samples(self) -> list[dict]:
        return load_samples()
    
    def search_sample_by_code(self, codigo: str, samples: list[dict]) -> dict:
        sample = next((s for s in samples if s.get("Código") == codigo), None)
        if not sample:
            raise ValueError("Muestra no encontrada")
        return sample

    def get_analysis_view(self,*,
                          tipe: Literal["FQ", "Micro"],
                          state: Literal["pendiente", "analizado"],) -> dict[str, dict]:

        samples = load_samples()
        state_key = "Estado_FQ" if tipe == "FQ" else "Estado_Micro"

        result = {}
        for s in samples:
            if s.get(state_key) == state:
                result[s["Código"]] = {
                    "analizar": s.get("Parámetros a analizar", {}).get(tipe, []),
                    "resultados": s.get("Resultados", {}).get(tipe, {}),
                }

        return result

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
