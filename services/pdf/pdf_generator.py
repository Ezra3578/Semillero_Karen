from io import BytesIO

from laboratory.domain.parameters import FQ_PARAMETERS, MICRO_PARAMETERS, UNIDADES, NORMA_CUMPLIMIENTO

from images import routes

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4

from utils.format_states import FormatStates

class PDF:

    def aplica_norma(self, muestra):
        return muestra.get("Tipo Agua") == "Agua potable (AP)" or muestra.get("Tipo Agua") == "Agua superficial (ASP)"

    #Establecer tamaños de columnas
    def get_column_config(self, muestra, width):
        left_margin = 45
        right_margin = 45
        usable_width = width - left_margin - right_margin

        if self.aplica_norma(muestra):
            headers = ["Parámetro", "Unidad", "Resultado", "Resolución 2115/2007", "Cumplimiento"]
            ratios  = [1.5, 0.8, 0.8, 1, 1]
        else:
            headers = ["Parámetro", "Unidad", "Resultado"]
            ratios  = [3, 1.2, 0.8]

        total = sum(ratios)
        x = left_margin
        cols = []

        for r in ratios:
            cols.append(x)
            x += usable_width * (r / total)

        return headers, cols
    
    def cumple_limite(self, parametro: str, valor):
        regla = NORMA_CUMPLIMIENTO.get(parametro)

        #Si no hay regla
        if not regla:
            return None, "N/A"

        tipo = regla.get("type")

        #Valor vacío o no numérico
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            return None, "N/A"

        #Regla por rango
        if tipo == "range":
            minimo = regla.get("min")
            maximo = regla.get("max")

            if minimo is None or maximo is None:
                return None, "N/A"

            return minimo <= valor <= maximo, f"{minimo} - {maximo}"

        #Regla por valor exacto
        if tipo == "exact":
            esperado = regla.get("value")

            if esperado is None:
                return None, "N/A"

            return valor == esperado, str(esperado)

        #Tipo desconocido
        return None, "N/A"


    
    def evaluar_parametro(self, parametro, valor):
        cumple, val_norma = self.cumple_limite(parametro, valor)

        if cumple is None:
            return {
                "estado": "N/A",
                "val_norma": val_norma
            }

        return {
            "estado": "Cumple" if cumple else "No cumple",
            "val_norma": val_norma
        }


    #Creación del PDF
    def generar_pdf_masivo(self, data):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        for i, muestra in enumerate(data):
            if i > 0:
                p.showPage()

            y = self.draw_header_pdf(p, width, height)
            self.draw_footer_pdf(p, width)

            # 1. INFORMACIÓN DE RECEPCIÓN
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "1. INFORMACIÓN DE RECEPCIÓN Y MUESTREO")
            y -= 20

            p.setFont("Helvetica", 9)
            p.setFillColor(Color(0, 0, 0))

            col1, col2 = 60, 320

            datos = [
                (f"Código: {muestra.get('Código', 'N/A')}", f"Fuente: {muestra.get('Fuente', 'N/A')}"),
                (f"Fecha Muestra: {muestra.get('Fecha', 'N/A')}", f"Hora Muestra: {muestra.get('Hora', 'N/A')}"),
                (f"Fecha Recepción: {muestra.get('Fecha Recepción', 'N/A')}", f"Recepcionista: {muestra.get('Recepcionó', 'N/A')}"),
                (f"Temp. Recepción: {muestra.get('Temperatura Recepción', '0')} °C", f"Tipo de Agua: {muestra.get('Tipo Agua', 'N/A')}"),
                (f"Estado FQ: {FormatStates.format_estado(muestra.get('Estado_FQ'))}", f"Estado Micro: {FormatStates.format_estado(muestra.get('Estado_Micro'))}"),
                (f"Estado del análisis: {FormatStates.estado_analisis(muestra)}", "")
            ]

            for d1, d2 in datos:
                p.drawString(col1, y, d1)
                p.drawString(col2, y, d2)
                y -= 14

            # 2. ANÁLISIS FÍSICO-QUÍMICO
            y -= 10
            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "2. ANÁLISIS FÍSICO-QUÍMICO")
            y -= 18

            headers, x_cols = self.get_column_config(muestra, width)

            p.setFont("Helvetica-Bold", 9)
            p.setFillColor(Color(0, 0, 0))

            for header, x in zip(headers, x_cols):
                p.drawString(x, y, header)

            p.line(45, y - 2, width - 45, y - 2)
            y -= 15

            for param in FQ_PARAMETERS:
                y = self.check_y(width, height, y, p)

                p.setFont("Helvetica", 9)

                p.drawString(x_cols[0], y, param)
                self.draw_unit_safely(p, x_cols[1], y, UNIDADES.get(param, ""))

                resultado = FormatStates.resolver_resultado_fq(muestra, param)
                p.drawString(x_cols[2], y, str(resultado))

                if self.aplica_norma(muestra):

                    if isinstance(resultado, (int, float)):
                        valores = self.evaluar_parametro(param, resultado)
                    else:
                        valores = {"val_norma": "N/A", "estado": "N/A"}

                    p.drawString(x_cols[3], y, str(valores["val_norma"]))
                    p.drawString(x_cols[4], y, str(valores["estado"]))

                y -= 13

            # 3. ANÁLISIS MICROBIOLÓGICO
            y -= 15
            y = self.check_y(width, height, y, p)

            p.setFont("Helvetica-Bold", 12)
            p.setFillColor(Color(0, 0.2, 0.4))
            p.drawString(45, y, "3. ANÁLISIS MICROBIOLÓGICO")
            y -= 18

            p.line(45, y + 10, width - 45, y + 10)

            for param in MICRO_PARAMETERS:
                y = self.check_y(width, height, y, p)

                p.setFont("Helvetica", 9)

                p.drawString(x_cols[0], y, param)
                self.draw_unit_safely(p, x_cols[1], y, UNIDADES.get(param, ""))

                resultado = FormatStates.resolver_resultado_micro(muestra, param)
                p.drawString(x_cols[2], y, str(resultado))

                if self.aplica_norma(muestra):

                    try:
                        valor_num = float(resultado)
                        valores = self.evaluar_parametro(param, valor_num)
                    except:
                        valores = {"val_norma": "N/A", "estado": "N/A"}

                    p.drawString(x_cols[3], y, str(valores["val_norma"]))
                    p.drawString(x_cols[4], y, str(valores["estado"]))

                y -= 13

        p.save()
        buffer.seek(0)

        return buffer.getvalue()
    
    def check_y(self, width, height, current_y, p_obj):
            if current_y < 80:
                p_obj.showPage()
                self.draw_footer_pdf(p_obj, width)
                return self.draw_header_pdf(p_obj, width, height)
            return current_y
    
    def draw_header_pdf(self, p, width, height):
        #Dibuja el encabezado. Ajustado para que el logo USTA no se vea corrido.
        y_start = height - 40 
        # Logo Empresa (Izquierda)
        try:
            logo_empresa = ImageReader(routes.logo_empresa_route)
            p.drawImage(logo_empresa, 50, y_start - 45, width=65, height=65, preserveAspectRatio=True, mask='auto')
        except: pass
        
        # Logo USTA (Derecha) - Coordenadas corregidas
        try:
            logo_usta = ImageReader(routes.logo_usta_route)
            p.drawImage(logo_usta, width - 125, y_start - 45, width=80, height=80, preserveAspectRatio=True, mask='auto')
        except: pass
        
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(Color(0, 0.34, 0.63))
        p.drawCentredString(width / 2, y_start - 25, "UNIVERSIDAD SANTO TOMÁS")
        p.setFont("Helvetica-Bold", 11)
        p.drawCentredString(width / 2, y_start - 45, "SISTEMA DE GESTIÓN DE LABORATORIO")
        p.setStrokeColor(Color(0, 0.34, 0.63))
        p.line(40, height - 100, width - 40, height - 100)
        return height - 125 

    def draw_footer_pdf(self, p, width):
        footer_y = 45 
        p.setFillColor(Color(0.95, 0.95, 0.95)) 
        p.rect(0, 0, width, footer_y + 10, fill=1, stroke=0)
        p.setFillColor(Color(0, 0, 0))
        p.setFont("Helvetica-Bold", 8)
        p.drawString(45, footer_y, "Laboratorio de Calidad del Agua")
        p.setFont("Helvetica", 7)
        p.drawString(45, footer_y - 10, "Universidad Santo Tomás – Facultad de Ingeniería Ambiental")
        p.drawString(45, footer_y - 20, "📍 Bogotá D.C. | ☎️ +57 314 367 9332 | ✉️ km@usantotomas.edu.co")

    def draw_unit_safely(self, p, x, y, unit_text):
        """Dibuja unidades como Cl2 o CaCO3 sin usar caracteres unicode problemáticos."""
        p.setFont("Helvetica", 9)
        # Diccionario de reemplazos manuales para subíndices
        if "Cl2" in unit_text:
            p.drawString(x, y, "mg Cl")
            p.setFont("Helvetica", 6); p.drawString(x + 25, y - 2, "2"); p.setFont("Helvetica", 9)
            p.drawString(x + 30, y, "/L")
        elif "CaCO3" in unit_text:
            p.drawString(x, y, "mg CaCO")
            p.setFont("Helvetica", 6); p.drawString(x + 38, y - 2, "3"); p.setFont("Helvetica", 9)
            p.drawString(x + 43, y, "/L")
        elif "PO4" in unit_text:
            p.drawString(x, y, "mg PO")
            p.setFont("Helvetica", 6); p.drawString(x + 28, y - 2, "4"); p.setFont("Helvetica", 9)
            p.drawString(x + 33, y, "/L")
        else:
            p.drawString(x, y, unit_text)