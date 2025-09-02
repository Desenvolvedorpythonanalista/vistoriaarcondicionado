import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

# ===== Dados iniciais =====
patrimonios = [
    ("AC-01", "Comeco"), ("AC-02", "Etrolux"), ("AC-03", "Etrolux"), ("AC-04", "Comeco"),
    ("AC-05", "Comeco"), ("AC-06", "Etrolux"), ("AC-07", "Etrolux"), ("AC-08", "Comeco"),
    ("AC-09", "Comeco"), ("AC-10", "Etrolux"), ("AC-11", "Etrolux"), ("AC-12", "Comeco"),
    ("AC-13", "Comeco"), ("AC-14", "Etrolux"), ("AC-15", "Etrolux"), ("AC-16", "Comeco"),
    ("AC-17", "Comeco"), ("AC-18", "Etrolux"), ("AC-19", "Etrolux"), ("AC-20", "Comeco")
]

salas = ["Sala 1", "Sala 2", "Sala 3", "Sala 4", "Sala 5"]
periodos = ["Manhã"] * 10 + ["Tarde"] * 10

# ===== Criar DataFrames =====
df_id = pd.DataFrame(columns=["Período", "Sala", "Patrimônio", "Modelo", "Horário da Vistoria"])
for i, (patrimonio, modelo) in enumerate(patrimonios):
    sala_index = i // 4
    df_id = pd.concat([df_id, pd.DataFrame([{
        "Período": periodos[i],
        "Sala": salas[sala_index],
        "Patrimônio": patrimonio,
        "Modelo": modelo,
        "Horário da Vistoria": ""
    }])], ignore_index=True)

# Tabela de vistoria com colunas renomeadas
df_vistoria = pd.DataFrame(columns=[
    "Patrimônio", "Estado de Limpeza", "Sistema de Compressão", "Vazando/Goteira/Ruído",
    "(A) Padrão", "(A) Aferida"
])
for patrimonio, _ in patrimonios:
    df_vistoria = pd.concat([df_vistoria, pd.DataFrame([{
        "Patrimônio": patrimonio,
        "Estado de Limpeza": False,
        "Sistema de Compressão": False,
        "Vazando/Goteira/Ruído": False,
        "(A) Padrão": "",
        "(A) Aferida": ""
    }])], ignore_index=True)

# ===== Streamlit =====
st.title("Checklist de Vistoria Diária de Ar-Condicionado")
st.markdown("Preencha os campos e clique em gerar PDF.")

st.subheader("Identificação do Patrimônio")
df_id_edit = st.data_editor(df_id, num_rows="dynamic")

st.subheader("Vistoria e Medições")
df_vistoria_edit = st.data_editor(df_vistoria, num_rows="dynamic")

# ===== Função para gerar PDF =====
def gerar_pdf(df_id, df_vistoria):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 20
    row_height = 25

    # Cabeçalho fixo
    def cabecalho(c, title):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, height - 50, title)
        c.setFont("Helvetica", 10)
        c.drawRightString(width - margin, height - 50, f"Data: {datetime.now().strftime('%d/%m/%Y')}")
        c.line(margin, height - 55, width - margin, height - 55)

    # Função para desenhar tabela com grid
    def desenhar_tabela(c, df, y_start, col_widths=None):
        if not col_widths:
            col_widths = [ (width - 2*margin)/len(df.columns) ]*len(df.columns)

        y = y_start
        # Cabeçalho
        c.setFont("Helvetica-Bold", 10)
        for i, col in enumerate(df.columns):
            c.rect(margin + sum(col_widths[:i]), y - row_height, col_widths[i], row_height, stroke=1, fill=0)
            c.drawString(margin + sum(col_widths[:i]) + 2, y - row_height + 7, str(col))
        y -= row_height

        # Linhas
        c.setFont("Helvetica", 9)
        for _, row in df.iterrows():
            for i, col in enumerate(df.columns):
                c.rect(margin + sum(col_widths[:i]), y - row_height, col_widths[i], row_height, stroke=1, fill=0)
                value = "[X]" if row[col] is True else "[ ]" if row[col] is False else str(row[col])
                max_text_width = col_widths[i] - 4
                text = value
                if c.stringWidth(value, "Helvetica", 9) > max_text_width:
                    text = value[:int(max_text_width/5)] + "..."
                c.drawString(margin + sum(col_widths[:i]) + 2, y - row_height + 7, text)
            y -= row_height
        return

    # ===== Página 1 – Identificação =====
    cabecalho(c, "Vistoria do Técnico - Identificação")
    desenhar_tabela(c, df_id, height - 80)
    c.showPage()

    # ===== Página 2 – Vistoria =====
    cabecalho(c, "Vistoria do Técnico - Medições e Estado")
    col_widths_vistoria = [60, 100, 120, 120, 80, 80]
    desenhar_tabela(c, df_vistoria, height - 80, col_widths=col_widths_vistoria)
    c.showPage()

    c.save()
    buffer.seek(0)
    return buffer

# ===== Botão para gerar PDF =====
if st.button("Gerar PDF"):
    pdf_file = gerar_pdf(df_id_edit, df_vistoria_edit)
    st.download_button(
        label="Download do PDF",
        data=pdf_file,
        file_name=f"Checklist_ArCondicionado_{datetime.now().strftime('%d%m%Y')}.pdf",
        mime="application/pdf"
    )
