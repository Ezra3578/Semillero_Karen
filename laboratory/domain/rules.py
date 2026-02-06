class ValidationError(ValueError):
    """Error de validación de dominio"""
    pass

# --REGISTRO--
#Campos básicos
def validate_required_fields(data: dict):
    required = [
        "tipo_muestra",
        "fecha",
        "hora",
        "fuente",
        "quien_muestra",
        "dispositivo",
        "tipo_agua",
    ]

    missing = [f for f in required if not data.get(f)]
    if missing:
        raise ValidationError(
            f"Campos obligatorios faltantes: {', '.join(missing)}"
        )

#Campo "Codigo_Red" de Red
def validate_red_sample(data: dict):
    if data.get("tipo_muestra") != "Red":
        return

    if not data.get("codigo_red"):
        raise ValidationError(
            "El código del punto de red es obligatorio para muestras tipo Red"
        )

#Campo "Otro" de Dispositivo
def validate_dispositivo(data: dict):
    if data.get("dispositivo") == "Otro":
        raise ValidationError(
            "Debe especificar el dispositivo cuando selecciona 'Otro'"
        )

#Campo "Otro" de Agua
def validate_tipo_agua(data: dict):
    if data.get("tipo_agua") == "Otra (O)":
        raise ValidationError(
            "Debe especificar el tipo de agua cuando selecciona 'Otra'"
        )

def validate_sample_input(data: dict):
    validate_required_fields(data)
    validate_red_sample(data)
    validate_dispositivo(data)
    validate_tipo_agua(data)
