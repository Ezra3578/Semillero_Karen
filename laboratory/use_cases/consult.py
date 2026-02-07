from typing import Literal

#Filtrar las muestras segun la fuente
def filter_samples_by_fuente_uc(samples: list[dict], fuente: str | None = None) -> list[dict]:
    if fuente:
        return [s for s in samples if s["Fuente"] == fuente]
    return samples


#Filtrar las muestras según el mes
def filter_samples_by_mes_uc(samples: list[dict], mes: str | None = None) -> list[dict]:
    if mes:
        return [s for s in samples if s["Código"][3:5] == mes]
    return samples


#Filtrar las muestra por el día
def filter_samples_by_dia_uc(samples: list[dict], dia: str | None = None) -> list[dict]:
    if dia:
        return [s for s in samples if s["Código"][5:7] == dia]
    return samples

#Buscar una muestra por su código
def search_sample_by_code_uc(samples: list[dict], codigo: str) -> dict:
    sample = next((s for s in samples if s.get("Código") == codigo), None)
    if not sample:
        raise ValueError("Muestra no encontrada")
    return sample

#Método para las muestras en análisis según el Tipo y el Estado
def get_analysis_view_uc(samples: list[dict], *, tipe: Literal["FQ", "Micro"], state: Literal["pendiente", "analizado"]) -> dict[str, dict]:
    state_key = "Estado_FQ" if tipe == "FQ" else "Estado_Micro"
    result = {}
    for s in samples:
        if s.get(state_key) == state:
            result[s["Código"]] = {
                "analizar": s.get("Parámetros a analizar", {}).get(tipe, []),
                "resultados": s.get("Resultados", {}).get(tipe, {}),
            }
    return result

#Filtra muest
def filter_samples_by_reception_state_uc(samples: list[dict], *, estados: list[dict])->list[dict]:
    return [s for s in samples if s.get("Estado Recepción") in estados]


#Eliminar una muestra de la lista
def delete_sample_from_list_uc(samples: list[dict], codigo: str) -> list[dict]:
    return [m for m in samples if m["Código"] != codigo]
