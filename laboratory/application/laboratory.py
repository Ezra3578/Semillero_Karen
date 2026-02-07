from laboratory.use_cases.register_sample import register_sample_uc
from laboratory.use_cases.reception import receive_sample_uc
from laboratory.use_cases.update_reception import update_reception_parameters_uc

from laboratory.domain.sample import Sample

from laboratory.repository import load_samples, save_samples


class Laboratory:

    #Hace "públicas" las muestras 
    def get_samples(self):
        return load_samples()

    #Cambia una muestra y guarda la actualizada
    def _replace_and_save(self, samples: list[dict], sample):
        #Reemplaza una muestra del JSON (o la "actualiza" xD)
        for i, s in enumerate(samples):
            if s["Código"] == sample.codigo:
                samples[i] = sample.to_dict()
                break
        else:
            raise ValueError("No se pudo reemplazar la muestra")

        save_samples(samples)



    #REGISTRO
    def register_sample(self, data: dict):
        samples = load_samples()

        existing_codes = [
            s.get("Código") or s.get("codigo")
            for s in samples
            if s.get("Código") or s.get("codigo")
        ]

        sample = register_sample_uc(
            data=data,
            existing_codes=existing_codes,
        )

        samples.append(sample.to_dict())
        save_samples(samples)

        return sample



    #RECEPCION
    def receive_sample(self, *, codigo: str, fecha_recepcion, hora_recepcion,
                       temperatura_recepcion, recepciona,
                       parametros_fq, parametros_micro,) -> Sample:

        #Carga las muestras
        samples = load_samples()

        #Busca por ID
        raw = next((s for s in samples if s["Código"] == codigo), None)
        if not raw:
            raise ValueError("Muestra no encontrada")

        #Construye desde el JSON un Sample
        sample = Sample.from_dict(raw)

        #Aplica la recepcion
        receive_sample_uc(
            sample=sample,
            fecha_recepcion=fecha_recepcion,
            hora_recepcion=hora_recepcion,
            temperatura_recepcion=temperatura_recepcion,
            recepciona=recepciona,
            parametros_fq=parametros_fq,
            parametros_micro=parametros_micro,
        )

        #Reemplaza la existente y la almacena
        self._replace_and_save(samples, sample)
        return sample
    


    #EDITAR UNA RECEPCIONADA
    def update_reception_parameters(self, *, codigo: str,
                                    parametros_fq,
                                    parametros_micro,) -> Sample:

        #Carga las muestras
        samples = load_samples()

        #Busca por codigo
        raw = next((s for s in samples if s["Código"] == codigo), None)
        if not raw:
            raise ValueError("Muestra no encontrada")

        #Construye el Sample del JSON
        sample = Sample.from_dict(raw)

        #Aplica la actualizacion
        update_reception_parameters_uc(
            sample=sample,
            parametros_fq=parametros_fq,
            parametros_micro=parametros_micro,
        )

        #Guarda
        self._replace_and_save(samples, sample)
        return sample