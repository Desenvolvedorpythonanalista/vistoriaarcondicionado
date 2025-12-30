import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import io
from datetime import datetime

# ---------------- CONFIG STREAMLIT ----------------
st.set_page_config(
    page_title="JK Refrigeração – Termo de Visita",
    layout="centered"
)

st.title("*JK REFRIGERAÇÃO*")
st.markdown("📌 **CONFIRMAÇÃO DE VISITA TÉCNICA, ORÇAMENTO E CONTRATAÇÃO DE SERVIÇO**")
st.divider()

# ---------------- CAMPOS DO CLIENTE ----------------
nome = st.text_input("Nome Completo")
telefone = st.text_input("WhatsApp / Telefone")
marca = st.text_input("Marca do Ar Condicionado")
btus = st.text_input("Capacidade de BTUs")
data_visita = st.date_input("Data desejada para a visita")
endereco = st.text_input("Endereço da Visita")  # <<< NOVO CAMPO
aceite = st.checkbox("Li e concordo com todos os termos acima")

# ---------------- FUNÇÃO PDF ----------------
def gerar_pdf():
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # --------- ESTILOS ---------
    estilo_titulo = ParagraphStyle(
        name="Titulo",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=2
    )

    estilo_dados = ParagraphStyle(
        name="DadosCliente",
        parent=styles["Normal"],
        fontSize=11,
        leading=13,
        spaceBefore=1,
        spaceAfter=2
    )

    estilo_termo = ParagraphStyle(
        name="TextoTermo",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        spaceBefore=10,
        spaceAfter=10
    )

    # --------- TÍTULO ---------
    story.append(Paragraph("<b>JK REFRIGERAÇÃO</b>", estilo_titulo))
    story.append(Paragraph(
        "<b>CONFIRMAÇÃO DE VISITA TÉCNICA, ORÇAMENTO E CONTRATAÇÃO DE SERVIÇO</b>",
        estilo_titulo
    ))

    story.append(Spacer(1, 8))

    # --------- DADOS DO CLIENTE ---------
    story.append(Paragraph(f"<b>Nome Completo:</b> {nome}", estilo_dados))
    story.append(Paragraph(f"<b>WhatsApp / Telefone:</b> {telefone}", estilo_dados))
    story.append(Paragraph(f"<b>Marca do Ar Condicionado:</b> {marca}", estilo_dados))
    story.append(Paragraph(f"<b>Capacidade de BTUs:</b> {btus}", estilo_dados))
    story.append(Paragraph(
        f"<b>Data desejada para a visita:</b> {data_visita.strftime('%d/%m/%Y')}",
        estilo_dados
    ))

    story.append(Spacer(1, 14))

    # --------- CLÁUSULAS ---------
    story.append(Paragraph(f"""
Declaro que LI, COMPREENDI E ACEITO as condições abaixo referentes à visita técnica,
avaliação do local e possível contratação do serviço de instalação de ar-condicionado:<br/><br/>

1. Toda instalação depende de visita e avaliação técnica prévia, necessárias para análise
do local, definição do percurso das linhas e levantamento da quantidade de material necessária.<br/><br/>

2. A visita técnica possui o valor de R$ 100,00, referente ao deslocamento e à avaliação
profissional do local, paga antecipadamente.<br/><br/>

3. Após a visita técnica, será apresentada ao cliente a relação de materiais necessários
e as condições do serviço, cabendo ao cliente aceitar ou não o orçamento apresentado.<br/><br/>

4. Caso o orçamento não seja aceito, o valor pago pela visita técnica não é reembolsável,
encerrando-se a prestação sem outras obrigações entre as partes.<br/><br/>

5. Caso o orçamento seja aceito, o valor pago pela visita técnica (R$ 100,00) será descontado
exclusivamente do valor da instalação, não sendo abatido do valor dos materiais.<br/><br/>

6. Os materiais necessários à instalação são de responsabilidade do cliente, podendo variar
de preço conforme fornecedor, marca e disponibilidade, sem alterar o valor do serviço.<br/><br/>

7. O pagamento do serviço de instalação será realizado da seguinte forma:<br/>
– 50% do valor da instalação no início do serviço;<br/>
– 50% restantes na conclusão do serviço.<br/><br/>

8. O início do serviço está condicionado à aquisição prévia dos materiais pelo cliente.<br/><br/>

9. O serviço será executado exclusivamente pelo prestador responsável pela visita técnica
e orçamento, não sendo transferido a terceiros sem novo acordo formal.<br/><br/>

10. As relações entre as partes encerram-se nas seguintes situações:<br/>
a) não aprovação do orçamento apresentado;<br/>
b) opção do cliente por não dar prosseguimento ao serviço;<br/>
c) conclusão do serviço.<br/><br/>

<b>Endereço da Visita:</b> {endereco}<br/>

(A visita será realizada mediante envio do comprovante de pagamento.)<br/><br/>

<b>Responsável:</b> Lucas Barros<br/>
<b>CNPJ:</b> 46.197.212/0001-01<br/>
<b>Aceite eletrônico registrado em:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}
""", estilo_termo))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------- BOTÃO ----------------
if st.button("Gerar PDF"):
    if not (nome and telefone and marca and btus and endereco and aceite):
        st.error("Preencha todos os campos e marque o aceite.")
    else:
        pdf = gerar_pdf()
        st.success("PDF gerado com sucesso.")
        st.download_button(
            label="Baixar PDF",
            data=pdf,
            file_name="JK_Refrigeracao_Termo_Visita_Tecnica.pdf",
            mime="application/pdf"
        )
