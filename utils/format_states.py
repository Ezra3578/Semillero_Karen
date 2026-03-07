class FormatStates:

    @staticmethod
    def estado_analisis(muestra):
        estado_fq = muestra.get("Estado_FQ", "pendiente")
        estado_micro = muestra.get("Estado_Micro", "pendiente")

        if estado_fq == "analizado" and estado_micro == "analizado":
            return "Completo"

        if (
            (estado_fq == "analizado" and estado_micro == "pendiente") or
            (estado_micro == "analizado" and estado_fq == "pendiente")
        ):
            return "Parcial"

        if estado_fq == "no_aplica" and estado_micro == "analizado":
            return "Completo (solo microbiológico)"

        if estado_micro == "no_aplica" and estado_fq == "analizado":
            return "Completo (solo físico-químico)"

        if estado_fq == "no_aplica" and estado_micro == "no_aplica":
            return "Sin análisis requerido"

        return "Pendiente"


    @staticmethod
    def format_estado(estado):
        estados = {
            "analizado": "Analizado",
            "pendiente": "Pendiente",
            "no_aplica": "No aplica"
        }
        return estados.get(estado, "N/A")


    @staticmethod
    def resolver_resultado_fq(muestra, parametro):
        parametros_fq = muestra.get("Parámetros a analizar", {}).get("FQ", [])
        resultados_fq = muestra.get("Resultados", {}).get("FQ", {})

        if parametro not in parametros_fq:
            return "N/A"

        if parametro not in resultados_fq:
            return "Pendiente"

        return resultados_fq.get(parametro)


    @staticmethod
    def resolver_resultado_micro(muestra, parametro):
        parametros_micro = muestra.get("Parámetros a analizar", {}).get("Micro", [])
        resultados_micro = muestra.get("Resultados", {}).get("Micro", {})

        if parametro not in parametros_micro:
            return "N/A"

        if parametro not in resultados_micro:
            return "Pendiente"

        datos = resultados_micro.get(parametro, {})

        ensayo_1 = datos.get("ensayo_1")
        ensayo_2 = datos.get("ensayo_2")

        if ensayo_1 is None and ensayo_2 is None:
            return "Pendiente"

        promedio = ((ensayo_1 or 0) + (ensayo_2 or 0)) / 2
        return f"{promedio:.2f}"