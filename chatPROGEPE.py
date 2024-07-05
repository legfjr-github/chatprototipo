import os
from datetime import datetime
import pygsheets
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import json
import base64

load_dotenv(find_dotenv())
# encoded_key = os.getenv("TESTE")
# service_key= json.loads(base64.b64decode(encoded_key).decode('ASCII'))

# with open('temp.json', 'w') as file:
#     json.dump(service_key, file)

st.set_page_config(page_title="Assistente PROGEPE")

st.markdown("""
<style>
header{visibility: hidden;}
.viewerBadge_link__qRIco{visibility: hidden; width: 0px; height: 0px;}
#MainMenu {visibility: hidden;} 
footer {visibility: hidden;}
.viewerBadge_link__qRIco{visibility: hidden}
.st-emotion-cache-ztfqz8 ef3psqc5{visibility: hidden;}
.st-emotion-cache-ztfqz8 ef3psqc5{visibility: hidden;}
.st-emotion-cache-15ecox0 ezrtsby0{visibility: hidden;}
.st-emotion-cache-q16mip e3g6aar1{visibility: hidden;}
.viewerBadge_container__r5tak styles_viewerBadge__CvC9N{visibility: hidden;}
.st-emotion-cache-h4xjwg ezrtsby2{visibility: hidden;}
.st-emotion-cache-ch5dnh ef3psqc5{visibility: hidden;}
span{visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown('<img style="float: left;" width=150px src="https://www.ufpe.br/documents/20181/60718/Progepe-100px-margem.png/cb408fe1-7c38-4cef-9619-cb861e8f5310?t=1471545541049" /><h1>Assistente PROGEPE</h1>', unsafe_allow_html=True)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

credential_file = "temp.json"
sheet_title = "1.ProgepeChat"
worksheet_title = "Log"
gc = pygsheets.authorize(service_account_file=credential_file)
temp = gc.open(sheet_title)
sheet = temp.worksheet_by_title(worksheet_title)
if "diff" not in st.session_state:
    cont = int(sheet.cell("E1").value) + 1
    st.session_state.diff = f"Chat nº {cont} iniciado as {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}" 
    sheet.update_value(f'E1', cont)


def save_message(sheet, speaker, message):
    all_records = sheet.get_all_records()
    last_row = len(all_records) + 2  # Próxima linha vazia
    sheet.update_value(f'A{last_row}', speaker)
    sheet.update_value(f'B{last_row}', message)
    sheet.update_value(f'C{last_row}', st.session_state.diff)

inicio = 0
if inicio == 0:
    inicio = 1

# st.image('PGDLOGO.png')
# st.title("Chat-PGD")
if "diff" not in st.session_state:
    st.session_state.diff = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
if "messages" not in st.session_state:
    st.session_state.messages = []
    save_message(sheet, "NovoChat", "NovoChat")

pergunta = """Você é um assistente virtual para orientar o servidor sobre os assuntos da PROGEPE e ajuda dando um passo a passo do que o servidor precisar. Você dá todo o suporte possível para que o servidor possa abrir o processo ou fazer a solicitação desejada, baseado nas informações a seguir, evite inventar informações. Se pedir informações sobre um assunto e ajuda dê todas as informações sobre o assunto que tiver, o que é, todo o procedimento para abertura do processo quando estiver junto a informação do assunto(tipo do processo, classificação, assunto detalhado, natureza, etc), para que setor enviar, documentação necessária, base legal, procedimentos, informações gerais, contatos do setor, etc. Sempre dê as respostas mais completas possíveis para que o servidor tire o máximo de dúvidas.\nVocê não dá respostas sobre nenhum outro assunto além disso, independente do que seja solicitado. A única exceção é se for perguntado qual foi a última pergunta, nesse caso pode responder normalmente.
Você não deve responder sobre assuntos históricos, nem geografia, ciências nem nada que não tenha a ver com a PROGEPE e os assuntos que ela trata, devendo informar que não pode responder sobre o assunto. Você deve tratar as pessoas bem e responder da forma mais humanizada possível.
Você deve ajudar o servidor fornecendo informações sobre os assuntos que ele perguntar, como proceder, contatos importantes para a resolução do assunto e informações que tiver.
Sempre dê o máximo de informações possíveis, como proceder, que setor contactar e um passo a passo sempre que tiver informações. Quando não tiver informações suficientes sobre o assunto para poder explicar apenas encaminhe para o setor responsável.
Sempre que possível dê o passo a passo de como fazer, apenas direcione para o setor quando não tiver como dar as informações sobre o assunto que o servidor perguntou.
Se o servidor pedir mais informações pode toda informação relacionada ao assunto que estiver entre "---Início das informações---" e "---Fim das informações---"
---Início das informações---
---Abono Permanência---

**ABONO PERMANÊNCIA**
Incentivo pago ao servidor que preenche todos os requisitos para se aposentar, mas
opta por permanecer na ativa. Depois de deferido, o abono de permanência passa a
ser pago em valor idêntico ao da contribuição previdenciária, que continua sendo
recolhida pelo servidor, na mesma folha de pagamento.

**Público Alvo**
Servidores que têm condições para a aposentadoria voluntária e optam por permanecer em atividade.

**Requisitos Básicos**
1. Obtenção das condições para a aposentadoria voluntária e opção por permanecer
em atividade.

**Documentação necessária**
1 - Requerimento de Abono de Permanência;

**Base legal**
1. Constituição Federal de 1988, art. 40, § 7º e 8°;
2. Lei n° 7.713/1988, art. 6°, XV e XXI;
3. Lei nº 8.112/1990, arts.185 II, “a”; 215 a 225 e 248;
4. Lei n° 9.527/1997, art. 7°;
5. Lei n° 10.887/2004;
6. Instrução Normativa SRF n° 15, de 06/02/2001, art. 5°, XII, §§ 1°, 2°, 3°, 4° e 5° e art. 52;
7. Orientação Normativa nº 9, de 5 de novembro de 2010;
8. Nota Informativa nº 314/2010/COGES/DENOP/SRH/MP;
9. Emenda Constitucional 103/2019.

**Setor responsável**:
CAPE - Coordenação de Aposentadoria e Pensão
Contatos: Fone: 2126-8675
E-mail: cape.progepe@ufpe.br

**Link do requerimento de Abono Permanência.**
https://www.ufpe.br/documents/3803744/4421502/REQUERIMENTO+ABONO+PERMAN%C3%8ANCIA.pdf/f30e1902-f892-49a1-91aa-07ac4a5ebb23

---Fim das informações sobre Abono Permanência---

---Acumulação de Cargos---

**ACUMULAÇÃO DE CARGO** 

Como regra geral, não é permitida a acumulação de cargos ou empregos públicos, exceto nas seguintes situações: 

**Constituição Federal**

“Art. 37. A administração pública direta e indireta de qualquer dos Poderes da União, dos Estados, do Distrito Federal e dos Municípios obedecerá aos princípios de legalidade, impessoalidade, moralidade, publicidade e eficiência e, também, ao seguinte: . (...)

XVI - é vedada a acumulação remunerada de cargos públicos, exceto, quando houver compatibilidade de horários, observado em qualquer caso o disposto no inciso XI:

a) a de dois cargos de professor;         

b) a de um cargo de professor com outro técnico ou científico,

c) a de dois cargos ou empregos privativos de profissionais de saúde, com profissões regulamentadas; . (...)


Art. 40. (...)

§11 - Aplica-se o limite fixado no art. 37, XI, à soma total dos proventos de inatividade, inclusive quando decorrentes da acumulação de cargos ou empregos públicos, bem como de outras atividades sujeitas a contribuição para o regime geral de previdência social, e ao montante resultante da adição de proventos de inatividade com remuneração de cargo acumulável na forma desta Constituição, cargo em comissão declarado em lei de livre nomeação e exoneração, e de cargo eletivo.” 


A unidade da PROGEPE responsável pela análise de eventual acumulação de cargos, empregos e funções do servidor é a Coordenação de Acumulação de Cargos e Empregos – CACE.

**Setor responsável:**
 

CACE - Coordenação de Acumulação de Cargos e Empregos 

Contatos:    Fone: 2126-8172    E-mail: cace@ufpe.br

Link da Página: https://www.ufpe.br/manual-do-servidor/acumulacao-de-cargos

---Fim das informações sobre Acumulação de Cargos---

---Adicionais Ocupacionais---

**ADICIONAIS OCUPACIONAIS**

Percentual adicionado à remuneração do servidor que trabalha em ambiente ou
executando atividade com exposição a risco previsto na legislação, podendo ser
adicional de insalubridade, de periculosidade, de irradiação ionizante ou gratificação
por trabalhos com raio-x ou substância radioativa.
A concessão dos adicionais ocupacionais, estabelecida na legislação vigente, refere-se a
formas de indenização do risco à saúde e integridade física do servidor, e possui
caráter transitório, uma vez que estará vigente enquanto durar a exposição ao risco
que ensejou a concessão.
- Adicional de Insalubridade corresponde a compensação pecuniária concedida ao
servidor que trabalhe, de forma permanente ou com habitualidade, em operações ou
locais insalubres.
- Adicional de Periculosidade é uma vantagem pecuniária concedida ao servidor
que trabalhe, de forma permanente ou com habitualidade, em atividades ou operações
perigosas, com risco de vida ou de violência física.
- Adicional de Radiação Ionizante é uma vantagem pecuniária, concedida aos
servidores que desempenhem efetivamente suas atividades em áreas que possam estar
sujeitas a irradiações ionizantes.
- Gratificação de Raios X ou Substâncias Radioativas é um benefício, devido ao
servidor que opere, obrigatória e habitualmente, por período mínimo de 12 (doze)
horas semanais, com raios X ou substâncias radioativas, próximo às fontes de
irradiação.

**Público Alvo**
Servidores ativos ocupantes de cargo efetivo ou em comissão.

**Base legal**
- Decreto nº 93.412, de 14 de outubro de 1986;
- Decreto nº 97.458, de 15 de janeiro de 1989;
- Lei no 8.112, de 11 de dezembro de 1990;
- Lei no 8.270, de 17 de dezembro de 1991;
- Decreto nº 877, de 20 de julho de 1993;
- Norma Regulamentadora nº 15 da Portaria 3.214/78 do MTE;
- Norma Regulamentadora nº 16 da Portaria 3.214/78 do MTE;
- Orientação Normativa Segep/MP n.º 4, de 14 de fevereiro de 2017; e
- Portaria Inmetro n° 48, de 27 de janeiro de 2016.

**Setores responsáveis:**
COSAIP - Comissão Interna de Supervisão de Atividades Insalubres e Perigosas
Contatos: E-mail: secretaria.cosaip@ufpe.br
CORAX - Comissão de Raio-X e Substâncias Radioativas
Contatos: E-mail: corax.ufpe@gmail.br


---Adicional de Insalubridade---

**ADICIONAL DE INSALUBRIDADE**

É uma vantagem pecuniária concedida ao servidor, de caráter transitório, que trabalha
com habitualidade ou em contato em operações e/ou atividades insalubres.

**Público Alvo** 
Servidores da Administração Pública Federal direta, autárquica e fundacional ativos,
anistiados, servidores com contratação temporária e servidores cedidos à UFPE.

**Requisitos Básicos**
1 – Ser servidor(a) civil da União, das autarquias e das fundações públicas federais que
esteja exposto(a) a agentes de riscos físicos, químicos e/ou biológicos ensejadores do
adicional nos termos da legislação vigente;
2 – Estar desempenhando as atribuições de seu cargo, em atividade presencial;
3 – Abertura de processo administrativo no sistema informatizado de protocolo SIPAC;
4– Emissão de Laudo Técnico de Insalubridade no sistema informatizado para
concessão de adicionais ocupacionais emitido pela COSAIP – Comissão de Supervisão
de Atividades Insalubres, em conformidade com a legislação vigente
5 – Emissão de Portaria de concessão do adicional de insalubridade.

**Documentação necessária**
Técnicos Administrativos em Educação (TAE):
1- Formulário de Solicitação de Adicional de Insalubridade/Periculosidade devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar/Superintendente
Professor de Magistério Superior (efetivos ou substitutos):
1- Formulário de Solicitação de Adicional de Insalubridade/Periculosidade devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar;
2- Plano Anual Atividades Docente (PAAD) atualizado;
3- Declaração atualizada da Chefia do Departamento discriminando para as disciplinas
ministradas, a carga horária semanal teórica e prática, separadamente

**Base legal**
- Lei nº 8112 de 11/12/1990 (Seção II - das Gratificações e Adicionais, Subseção IV).
- Decreto-Lei nº 1873 de 27/05/1981
- Decreto nº 97458 de 11/01/1989 (Regulamenta a concessão dos Adicionais de
Periculosidade e de Insalubridade)
- Instrução Normativa N° 15 de 16/03/2022 (Estabelece orientações sobre a concessão
dos adicionais de insalubridade, periculosidade, irradiação ionizante e gratificação por
trabalhos com raios-x ou substâncias radioativas)
- Norma Regulamentadora N° 15 de 1978 - Atividades e Operações Insalubres

**Orientações Gerais**
- No âmbito da UFPE, a competência técnica para a avaliação da concessão do adicional
de insalubridade pertence à Comissão de Supervisão das Atividades Insalubres e
Perigosas – COSAIP.

**Solicitação do Adicional de Insalubridade**
- O adicional de insalubridade deverá ser requerido pelo servidor, cabendo à sua chefia
atestar a veracidade das informações apresentadas, quanto às atividades
desempenhadas, à natureza, duração e local (is) de trabalho onde atua o interessado.
- A solicitação deverá ser encaminhada à COSAIP por meio da abertura de um processo
administrativo no sistema de protocolo SIPAC instruído com a documentação requerida
pelo Formulário de Solicitação de Adicional de Insalubridade/Periculosidade.

**Avaliação, Laudos e Pareceres Técnicos**
- Para a avaliação da concessão do adicional de insalubridade, a COSAIP realizará uma
avaliação no(s) local(is) de trabalho junto ao servidor.
- Com base na entrevista no local de trabalho e na análise da documentação
apresentada, a COSAIP irá avaliar a concessão do adicional observando a previsão legal
para enquadramento da exposição ao agente de risco e, caso haja concessão, verificar o
grau de insalubridade estabelecido por legislação vigente.
- A COSAIP deverá inserir o Laudo Técnico para concessão de adicionais ocupacionais
no sistema informatizado Siapenet – módulo: Saúde e Segurança do Trabalho com um
parecer conclusivo, e em seguida, anexá-los ao processo administrativo
SIPAC para assinaturas pelos membros da Comissão e posterior envio à Diretoria de
Administração de Pessoal - DAP.

**Competências da DAP**
- A DAP analisará o processo administrativo SIPAC para a emissão de ato
administrativo pela Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida – PROGEPE
que determinará a efetiva autorização para pagamento.
- A DAP deverá garantir os preceitos administrativos para a
implantação/revisão/suspensão do adicional e decidir sobre as situações nas quais se
caracterizam afastamentos não considerados de efetivo exercício e/ou a concessão de
valores retroativos à emissão do laudo técnico.
- A DAP procederá, de ofício, o cancelamento do adicional, sempre que ocorrer remoção
do servidor, ou cessão a órgão externo à Universidade, cabendo ao interessado, se for o
caso, requerer nova concessão, em razão nas atividades que realize.

**Manutenção do Adicional de Insalubridade**
- A concessão dos adicionais de insalubridade fica condicionada à permanência da
atividade nas condições que, conforme verificadas, a justificaram, tornando-se
insubsistente no momento em que a atividade ou condições originárias não mais
existirem.
- Cabe à chefia imediata do servidor informar à COSAIP sobre quaisquer alterações nos
riscos que ensejam a percepção do adicional.

**Procedimentos em caso de não concessão**
- Em caso de não concessão, o processo administrativo SIPAC deverá ser enviado à
unidade de lotação do servidor para ciência e posterior arquivamento na Seção de
Arquivo de Pessoal – SAP.

**Pedidos de Reconsideração**
- Os pedidos de reconsideração deverão ser apresentados à COSAIP dentro do prazo
determinado pela Lei do Processo Administrativo (Lei n° 9.784/99).

**Revisão do Adicional de Insalubridade**
- A COSAIP poderá proceder com a revisão das concessões dos adicionais por iniciativa
da Comissão ou por solicitação dos órgãos de controle, da área de recursos humanos,
dos servidores, e/ou de gestores, verificando se houve alteração dos riscos e/ou da
exposição do servidor que deu origem à concessão ou em razão de atualização de
aspectos normativos, emitindo novo Laudo técnico com fins de revalidar a concessão do
adicional.
- Sempre que solicitado, os servidores deverão disponibilizar informações atualizadas
para a revisão das situações dos adicionais de insalubridade.
- O não fornecimento de informações por parte do servidor para o processo de revisão
compromete a análise da manutenção do adicional, retirando a validade do laudo
anteriormente produzido, o que implicará na suspensão do adicional de insalubridade.

**Servidores Cedidos**
- Para servidores cedidos a outros órgãos e/ou que atuem externamente à UFPE, a
COSAIP deverá:
I - requerer informações sobre a cessão formal e/ou termo de convênio
firmado, conforme o caso;
II - solicitar Laudo técnico de insalubridade do órgão externo para as
atividades de servidores da UFPE nos ambientes, sendo estes laudos
elaborados por servidor público da esfera federal, estadual, distrital ou
municipal, ou militar, ocupante de cargo público ou posto militar de médico
com especialização em medicina do trabalho, ou de engenheiro ou de
arquiteto com especialização em segurança do trabalho;
III - validar o Laudo Técnico emitido observando se os critérios legais foram
cumpridos na íntegra e o enquadramento do adicional, emitindo parecer
sobre a conclusão; e
IV - caso o órgão declare a inexistência de profissional com esta
responsabilidade técnica, a COSAIP poderá solicitar autorização para
realizá-la nas instalações do órgão.

**Procedimentos**
- Abertura do Processo no sistema de protocolo informatizado SIPAC.
Origem: Processo Interno
Tipo do processo: ADICIONAL DE INSALUBRIDADE E PERICULOSIDADE
Classificação: 023.164 - ADICIONAL DE INSALUBRIDADE
Eletrônico: Sim
Assunto detalhado: PROCESSO PARA AVALIAÇÃO DA SOLICITAÇÃO DO
ADICIONAL DE INSALUBRIDADE DO SERVIDOR <nome servidor> - SIAPE
<número>
Tipo do documento: Formulário/Declaração/PAAD/RAAD etc.
Natureza do documento: Ostensivo
Forma do documento: Anexar documento digital
Natureza do processo: Ostensivo
Data do Documento: Data de emissão/assinaturas
Data do Recebimento: Data da Abertura
Tipo de Conferência: Documento Original (se gerado eletronicamente)/Cópia
Simples (se escaneado)
Arquivo Digital: Formulário/Declarações/Plano Anual de Atividades Docentes etc
Assinantes: O formulário deve ser assinado eletronicamente ou escaneado e,
conter as assinaturas do servidor interessado, chefia imediata e diretor de
centro/superintendente. Ainda que as assinaturas constem no documento
escaneado, o SIPAC requererá ao menos um assinante responsável pela inserção
do documento
Servidor: Incluir nome do servidor interessado/solicitante
E-mail: Incluir e-mail, caso não esteja cadastrado no SIPAC
Destino: Outra Unidade
Unidade de Destino: 11.07.11 (COSAIP)
Setor Responsável:
COSAIP - Comissão Interna de Supervisão de Atividades Insalubres e Perigosas
Contatos: Fone: 2126 - 8003
E-mail: secretaria.cosaip@ufpe.br


---Fim das Informações sobre Adicional de Insalubridade---

---Adicional por Irradiação Ionizante---

**ADICIONAL POR IRRADIAÇÃO IONIZANTE**

É uma compensação pecuniária, concedida aos servidores que desempenham
efetivamente suas atividades em áreas que possam estar sujeitas à exposição habitual ou
permanente à irradiação ionizante.

**Público-alvo**
Servidores da Administração Pública Federal direta, autárquica e fundacional ativos,
anistiados, servidores com contratação temporária e servidores cedidos à UFPE.

**Requisitos Básicos**
1 – Ser servidor(a) civil da União, das autarquias e das fundações públicas federais que
desempenhe efetivamente suas atividades em áreas que possam estar sujeitas à exposição
habitual ou permanente à irradiação ionizante, nos termos da legislação vigente;
2 – Estar desempenhando as atribuições de seu cargo, em atividade presencial;
3 - Ter formação em curso reconhecido por Órgão Oficial de Ensino que, em sua grade
curricular, apresente disciplinas que contemplem conceitos básicos em Proteção
Radiológica em uma ou mais das seguintes áreas: pesquisa e desenvolvimento, aplicações
médicas.
3.1 - Excepcionalmente, uma vez justificada sua designação, o servidor cuja
formação não atenda ao referido requisito poderá ser autorizado a exercer sua
atividade após comprovação de treinamento em Radioproteção com carga horária
de, no mínimo, 40 horas, por instrutor devidamente habilitado.
4 – Realizar a abertura de processo administrativo no sistema informatizado de protocolo
SIPAC;
5– Emissão de Relatório de Inspeção e Laudo Técnico no sistema informatizado para
concessão de adicionais ocupacionais, emitido pela CORAX – Comissão de Raios-X e
Substâncias Radioativas, em conformidade com a legislação vigente;
6 – Emissão de Portaria de concessão do adicional de irradiação ionizante.

**Documentação necessária**
1 - Formulário de Solicitação de Adicional de Raios- X/Radiação Ionizante devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar/Superintendente.
2 – Atestado de Saúde Ocupacional (ASO), obtido no Núcleo de Atenção à Saúde do
Servidor – NASS/UFPE.

**Base legal**
• Lei nº 8112 de 11/12/1990 (Seção II - das Gratificações e Adicionais, Subseção IV
e Art. 72).
• Orientação Normativa DRH/SAF/MARE nº 62, de 17/01/91 (DOU 18/01/91).
• Lei nº 8.270, de 17/12/91 – Artigo 12, parágrafos 1º, 3º e 5º e artigos 25 e 26.
• Decreto nº 877, de 20/07/1993 (DOU 21/07/1993);
• Posição Regulatória 3.01/001 – CNEN – Energia Nuclear.
• Instrução Normativa SGP/SEGGG/ME N° 15 de 16/03/2022 (Estabelece
orientações sobre a concessão dos adicionais de insalubridade, periculosidade,
irradiação ionizante e gratificação por trabalhos com raios-x ou substâncias
radioativas).

**Orientações Gerais**
- No âmbito da UFPE, a competência técnica para a avaliação da concessão do adicional
por irradiação ionizante pertence à Comissão de Raios X e Substâncias Radioativas –
CORAX.
- O adicional de irradiação ionizante de que trata o art. 12, § 1° da Lei n° 8.270, de 17 de
dezembro de 1991, será devido aos servidores civis da União, das autarquias e das
fundações públicas federais, que estejam desempenhando efetivamente suas atividades
em áreas que possam resultar na exposição a essas irradiações. (Artigo 1º do Decreto no
877, de 20 de julho de 1993)
- Em relação ao adicional de irradiação ionizante, considerar-se-á
Indivíduos Ocupacionalmente Expostos (IOE) aqueles que exerçam atividades
envolvendo fontes de radiação ionizante desde a produção, manipulação, utilização,
operação, controle, fiscalização, armazenamento, processamento, transporte até a
respectiva deposição, bem como aqueles que atuam em situações de emergência
radiológica. (Artigo 1º, § 1º do Decreto no 877, de 20 de julho de 1993; Art. 6º, Inc. I da
ON SEGEP/MPOG n° 6/2013)
- Em relação ao adicional de irradiação ionizante, considerar-se-á área controlada aquela
sujeita a regras especiais de proteção e segurança com a finalidade de controlar as
exposições normais, de prevenir a disseminação de contaminação radioativa ou de
prevenir ou limitar a amplitude das exposições potenciais e área supervisionada qualquer
área sob vigilância não classificada como controlada, mas onde as medidas gerais de
proteção e segurança necessitam ser mantidas sob supervisão. (Art. 6º, Inc. II e III da ON
SEGEP/MPOG n° 6/2013)
- O adicional de irradiação ionizante somente poderá ser concedido aos Indivíduos
Ocupacionalmente Expostos – IOE, que exerçam atividades em área controlada ou em
área supervisionada. (Art. 7º da ON SEGEP/MPOG n° 6/2013)
- Os adicionais de insalubridade, de periculosidade e de irradiação ionizante, bem como
a gratificação por trabalhos com Raios X ou Substâncias Radioativas, estabelecidos na
legislação vigente, não se acumulam e são formas de compensação por risco à saúde dos
trabalhadores, tendo caráter transitório, enquanto durar a exposição. (Art. 4º, da IN
SGP/SEGGG/ME nº 15/2022)
- O adicional será calculado sobre o vencimento do cargo efetivo do servidor, com base
nos seguintes percentuais: de 5% (cinco por cento), 10% (dez por cento) ou 20% (vinte
por cento). (Art. 12, § 1º e 3º da Lei nº 8.270/91 e art. 5º da IN SGP/SEGGG/ME nº
15/2022; anexo único do Decreto nº 877/1993)
- Os servidores que operam com raios-x serão submetidos a exames
médicos a cada 6 (seis) meses. (Art. 72, § único da Lei nº 8.112/90);
- O servidor que opera direta e permanentemente com Raios X ou substâncias radioativas
gozará 20 (vinte) dias consecutivos de férias, por semestre de atividade profissional,
proibida em qualquer hipótese a acumulação. (Art. 79 da Lei nº 8.112/90).
- Sempre que houver alteração nas condições técnicas que justificaram a concessão,
haverá revisão do percentual do adicional. (Art. 4º do Decreto nº 877/93).
- Se descaracterizadas as condições de que resultaram na concessão do adicional de que
trata esta norma, cessará o direito a sua percepção. (Art. 4º, parágrafo único do Decreto
nº 877/93)

**Solicitação do Adicional por Irradiação Ionizante**
- O adicional deverá ser requerido pelo servidor, cabendo à sua chefia atestar a
veracidade das informações apresentadas, quanto às atividades desempenhadas, à
natureza, duração e local(is) de trabalho onde atua o interessado.
- A solicitação deverá ser encaminhada à CORAX por meio da abertura de um
processo administrativo no sistema de protocolo SIPAC instruído com a
documentação requerida pelo Formulário de Solicitação de Adicional de Raios
X/Radiação Ionizante.

**Avaliação, Laudos e Pareceres Técnicos**
- Para a avaliação da concessão do adicional por irradiação ionizante, a CORAX
realizará uma avaliação no(s) local(is) de trabalho junto ao servidor.
- Com base na entrevista no local de trabalho e na análise da documentação
apresentada, a CORAX irá avaliar a concessão do adicional, observando a previsão
legal para enquadramento da exposição ao agente de risco.
- A CORAX elaborará um Relatório de Inspeção e deverá inserir o Laudo Técnico
para concessão de adicionais ocupacionais no sistema informatizado Siapenet –
módulo: Saúde e Segurança do Trabalho com um parecer conclusivo, e em seguida,
anexá-los ao processo administrativo SIPAC para assinaturas pelos membros da
Comissão e posterior envio à Diretoria de Administração de Pessoal - DAP.

**Competências da DAP**
- A DAP analisará o processo administrativo SIPAC para a emissão de ato
administrativo pela Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida –
PROGEPE que determinará a efetiva autorização para pagamento.
- A DAP deverá garantir os preceitos administrativos para a
implantação/revisão/suspensão do adicional e decidir sobre as situações nas quais
se caracterizam afastamentos não considerados de efetivo exercício e/ou a
concessão de valores retroativos à emissão do laudo técnico.
- A DAP procederá, de ofício, o cancelamento do adicional, sempre que ocorrer
remoção do servidor ou cessão a órgão externo à Universidade, cabendo ao
interessado, se for o caso, requerer nova concessão, em razão das atividades que
realize.

**Manutenção da Gratificação por Trabalhos Com Raios X ou Substâncias Radioativas**
- A concessão do adicional fica condicionada à permanência da atividade nas
condições que, conforme verificadas, a justificaram, tornando-se insubsistente no
momento em que a atividade ou condições originárias não mais existirem.
- A concessão do adicional fica condicionada ainda a realização de exames médicos
a cada 6 (seis) meses. (Art. 72, § único da Lei nº 8.112/90) e entrega do Atestado
de Saúde Ocupacional Periódico (ASO), obtido no Núcleo de Atenção à Saúde do
Servidor – NASS, à CORAX.
- Caso o servidor não realize seu Exame Médico ou seja considerado inapto para a
função específica (através do ASO), deverá ser imediatamente afastado das
atividades que envolvam exposição obrigatória às radiações ionizantes e terá
cessada a concessão do adicional. (Instrução Normativa SGP/SEGGG/ME Nº15,
de 16 de março de 2022).
- Cabe à chefia imediata do servidor informar à CORAX sobre quaisquer alterações
nos riscos que ensejam a percepção do adicional.

**Procedimentos em caso de não concessão**
- Em caso de não concessão, o processo administrativo SIPAC deverá ser enviado
à unidade de lotação do servidor para ciência e posterior arquivamento na Seção
de Arquivo de Pessoal – SAP.

**Pedidos de Reconsideração**
- Os pedidos de reconsideração deverão ser apresentados à CORAX dentro do
prazo determinado pela Lei do Processo Administrativo (Lei n° 9.784/99).

**Revisão do Adicional por Irradiação Ionizante**
- A CORAX poderá proceder com a revisão das concessões do adicional por
iniciativa da Comissão ou por solicitação dos órgãos de controle, da área de
recursos humanos, dos servidores, e/ou de gestores, verificando se houve alteração
dos riscos e/ou da exposição do servidor que deu origem à concessão ou em razão
de atualização de aspectos normativos, emitindo novo Laudo técnico com
fins de revalidar a concessão do adicional.
- Sempre que solicitado, os servidores deverão disponibilizar informações
atualizadas para a revisão das situações do adicional por irradiação Ionizante.
- O não fornecimento de informações por parte do servidor para o processo de
revisão compromete a análise da manutenção do adicional, retirando a validade do
laudo anteriormente produzido, o que implicará na suspensão do adicional por
irradiação Ionizante.

**Procedimentos**
- Abertura do Processo no sistema de protocolo informatizado SIPAC.
Origem: Processo Interno
Tipo do processo: GRATIFICAÇÃO DE IRRADIAÇÃO IONIZANTE: SOLICITAÇÃO
Classificação: 023.164 - INSALUBRIDADE
Eletrônico: Sim
Assunto detalhado: PROCESSO PARA AVALIAÇÃO DA SOLICITAÇÃO DO
ADICIONAL POR IRRADIAÇÃO IONIZANTE <nome servidor> - SIAPE <número>
Tipo do documento: Formulário/Declaração etc.
Natureza do documento: Ostensivo
Forma do documento: Anexar documento digital
Natureza do processo: Ostensivo
Data do Documento: Data de emissão/assinaturas
Data do Recebimento: Data da Abertura
Tipo de Conferência: Documento Original (se gerado eletronicamente) / Cópia
Simples (se escaneado)
Arquivo Digital: Formulário/Declarações etc
Assinantes: O formulário deve ser assinado eletronicamente ou escaneado e, conter as
assinaturas do servidor interessado, chefia imediata e diretor de centro/superintendente.
Ainda que as assinaturas constem no documento escaneado, o SIPAC
requererá ao menos um assinante responsável pela inserção do documento
Servidor: Incluir nome do servidor interessado/solicitante
E-mail: Incluir e-mail, caso não esteja cadastrado no SIPAC
Destino: Outra Unidade
Unidade de Destino: 11.07.47 (CORAX)
Setor responsável:
CORAX - Comissão de Raios X e Substâncias Radioativas
Contatos: Fone: 2126-8003
 E-mail: corax.ufpe@gmail.br

---Fim das Informações sobre Adicional por Irradiação Ionizante---

---Adicional de Periculosidade---


**ADICIONAL DE PERICULOSIDADE**

É uma vantagem pecuniária concedida ao servidor, de caráter transitório, que trabalha
com habitualidade ou em contato em operações e/ou atividades perigosas.

**Público Alvo**
Servidores da Administração Pública Federal direta, autárquica e fundacional ativos,
anistiados, servidores com contratação temporária e servidores cedidos à UFPE.

**Requisitos Básicos**
1 – Ser servidor(a) civil da União, das autarquias e das fundações públicas federais que
esteja exposto(a) a agentes de riscos físicos, químicos e/ou biológicos ensejadores do
adicional nos termos da legislação vigente;
2 – Estar desempenhando as atribuições de seu cargo, em atividade presencial;
3 – Abertura de processo administrativo no sistema informatizado de protocolo SIPAC;
4– Emissão de Laudo Técnico de Periculosidade no sistema informatizado para
concessão de adicionais ocupacionais emitido pela COSAIP – Comissão de Supervisão
de Atividades Insalubres, em conformidade com a legislação vigente
5 – Emissão de Portaria de concessão do adicional de periculosidade.

**Documentação necessária**
Técnicos Administrativos em Educação (TAE):
1- Formulário de Solicitação de Adicional de Insalubridade/Periculosidade devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar/Superintendente
Professor de Magistério Superior (efetivos ou substitutos):
1- Formulário de Solicitação de Adicional de Insalubridade/Periculosidade devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar;
2- Plano Anual Atividades Docente (PAAD) atualizado;
3- Declaração atualizada da Chefia do Departamento discriminando para as disciplinas
ministradas, a carga horária semanal teórica e prática, separadamente
Link de onde encontrar o formulário: https://www.ufpe.br/proplan/planejamento-institucional?p_p_id=101&p_p_lifecycle=0&p_p_state=maximized&p_p_mode=view&_101_struts_action=%2Fasset_publisher%2Fview_content&_101_assetEntryId=4271645&_101_type=content&_101_urlTitle=corax&inheritRedirect=false
**Base legal**
- Lei nº 8112 de 11/12/1990 (Seção II - das Gratificações e Adicionais, Subseção IV).
- Decreto-Lei nº 1873 de 27/05/1981
- Decreto nº 97458 de 11/01/1989 (Regulamenta a concessão dos Adicionais de
Periculosidade e de Insalubridade)
- Norma Regulamentadora N° 16 de 1978 - Atividades e Operações Perigosas

**Orientações Gerais**
- No âmbito da UFPE, a competência técnica para a avaliação da concessão do adicional
de periculosidade pertence à Comissão de Supervisão das Atividades Insalubres e
Perigosas – COSAIP.

**Solicitação do Adicional de Insalubridade**
- O adicional de periculosidade deverá ser requerido pelo servidor, cabendo à sua chefia
atestar a veracidade das informações apresentadas, quanto às atividades
desempenhadas, à natureza, duração e local (is) de trabalho onde atua o interessado.
- A solicitação deverá ser encaminhada à COSAIP por meio da abertura de um processo
administrativo no sistema de protocolo SIPAC instruído com a documentação requerida
pelo Formulário de Solicitação de Adicional de Insalubridade/Periculosidade.

**Avaliação, Laudos e Pareceres Técnicos**
- Para a avaliação da concessão do adicional de periculosidade, a COSAIP realizará uma
avaliação no(s) local(is) de trabalho junto ao servidor.
- Com base na entrevista no local de trabalho e na análise da documentação
apresentada, a COSAIP irá avaliar a concessão do adicional observando a previsão legal
para enquadramento da exposição ao agente de risco, estabelecido por legislação
vigente.
- A COSAIP deverá inserir o Laudo Técnico para concessão de adicionais ocupacionais
no sistema informatizado Siapenet – módulo: Saúde e Segurança do Trabalho com um
parecer conclusivo, e em seguida, anexá-los ao processo administrativo SIPAC para
assinaturas pelos membros da Comissão e posterior envio à Diretoria de Administração
de Pessoal - DAP.

**Competências da DAP**
- A DAP analisará o processo administrativo SIPAC para a emissão de ato
administrativo pela Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida – PROGEPE
que determinará a efetiva autorização para pagamento.
- A DAP deverá garantir os preceitos administrativos para a
implantação/revisão/suspensão do adicional e decidir sobre as situações nas quais se
caracterizam afastamentos não considerados de efetivo exercício e/ou a concessão de
valores retroativos à emissão do laudo técnico.
- A DAP procederá, de ofício, o cancelamento do adicional, sempre que ocorrer remoção
do servidor, ou cessão a órgão externo à Universidade, cabendo ao interessado, se for o
caso, requerer nova concessão, em razão nas atividades que realize.

**Manutenção do Adicional de Periculosidade**
- A concessão dos adicionais de periculosidade fica condicionada à permanência da
atividade nas condições que, conforme verificadas, a justificaram, tornando-se
insubsistente no momento em que a atividade ou condições originárias não mais
existirem.
- Cabe à chefia imediata do servidor informar à COSAIP sobre quaisquer alterações nos
riscos que ensejam a percepção do adicional.

**Procedimentos em caso de não concessão**
- Em caso de não concessão, o processo administrativo SIPAC deverá ser enviado à unidade de lotação do servidor para ciência e posterior arquivamento na Seção deArquivo de Pessoal – SAP.

**Pedidos de Reconsideração**
- Os pedidos de reconsideração deverão ser apresentados à COSAIP dentro do prazo
determinado pela Lei do Processo Administrativo (Lei n° 9.784/99).

**Revisão do Adicional de Periculosidade**
- A COSAIP poderá proceder com a revisão das concessões dos adicionais por iniciativa
da Comissão ou por solicitação dos órgãos de controle, da área de recursos humanos,
dos servidores, e/ou de gestores, verificando se houve alteração dos riscos e/ou da
exposição do servidor que deu origem à concessão ou em razão de atualização de
aspectos normativos, emitindo novo Laudo técnico com fins de revalidar a concessão do
adicional.
- Sempre que solicitado, os servidores deverão disponibilizar informações atualizadas
para a revisão das situações dos adicionais de periculosidade.
- O não fornecimento de informações por parte do servidor para o processo de revisão
compromete a análise da manutenção do adicional, retirando a validade do laudo
anteriormente produzido, o que implicará na suspensão do adicional de periculosidade.

**Servidores Cedidos**
- Para servidores cedidos a outros órgãos e/ou que atuem externamente à UFPE, a
COSAIP deverá:
I - requerer informações sobre a cessão formal e/ou termo de convênio
firmado, conforme o caso;
II - solicitar Laudo técnico de periculosidade do órgão externo para as
atividades de servidores da UFPE nos ambientes, sendo estes laudos
elaborados por servidor público da esfera federal, estadual, distrital ou
municipal, ou militar, ocupante de cargo público ou posto militar de médico
com especialização em medicina do trabalho, ou de engenheiro ou de
arquiteto com especialização em segurança do trabalho;
III - validar o Laudo Técnico emitido observando se os critérios legais foram
cumpridos na íntegra e o enquadramento do adicional, emitindo parecer
sobre a conclusão; e
IV - caso o órgão declare a inexistência de profissional com esta
responsabilidade técnica, a COSAIP poderá solicitar autorização para
realizá-la nas instalações do órgão.

**Procedimentos**
- Abertura do Processo no sistema de protocolo informatizado SIPAC.
Origem: Processo Interno
Tipo do processo: ADICIONAL DE INSALUBRIDADE E PERICULOSIDADE
Classificação: 023.163 - ADICIONAL DE PERICULOSIDADE
Eletrônico: Sim
Assunto detalhado: PROCESSO PARA AVALIAÇÃO DA SOLICITAÇÃO DO
ADICIONAL DE PERICULOSIDADE DO SERVIDOR <nome servidor> - SIAPE
<número>
Tipo do documento: Formulário/Declaração/PAAD/RAAD etc.
Natureza do documento: Ostensivo
Forma do documento: Anexar documento digital
Natureza do processo: Ostensivo
Data do Documento: Data de emissão/assinaturas
Data do Recebimento: Data da Abertura
Tipo de Conferência: Documento Original (se gerado eletronicamente)/Cópia
Simples (se escaneado)
Arquivo Digital: Formulário/Declarações/Plano Anual de Atividades Docentes etc
Assinantes: O formulário deve ser assinado eletronicamente ou escaneado e,
conter as assinaturas do servidor interessado, chefia imediata e diretor de
centro/superintendente. Ainda que as assinaturas constem no documento
escaneado, o SIPAC requererá ao menos um assinante responsável pela inserção
do documento
Servidor: Incluir nome do servidor interessado/solicitante
E-mail: Incluir e-mail, caso não esteja cadastrado no SIPAC
Destino: Outra Unidade
Unidade de Destino: 11.07.11 (COSAIP)
Setor Responsável:
COSAIP - Comissão Interna de Supervisão de Atividades Insalubres e Perigosas
Contatos: Fone: 2126-8003
E-mail: secretaria.cosaip@ufpe.br

---Fim das Informações sobre Adicional de Periculosidade---

---Gratificação por Trabalhos com Raios X ou Substâncias Radioativas---

**GRATIFICAÇÃO POR TRABALHOS COM RAIOS X OU SUBSTÂNCIAS RADIOATIVAS**

Gratificação devida ao servidor que opere direta, obrigatória e habitualmente com Raios
X ou Substâncias Radioativas, junto às fontes de irradiação por um período mínimo de
12 (doze) horas semanais, como parte integrante das atribuições do cargo ou função
exercida; tenham sido designados por portaria do dirigente do órgão onde tenham
exercício para operar direta e habitualmente com Raios X ou Substâncias Radioativas; e
que exerçam suas atividades em área controlada.

**Público-alvo**
Servidores da Administração Pública Federal direta, autárquica e fundacional ativos,
anistiados, servidores com contratação temporária e servidores cedidos à UFPE.

**Requisitos Básicos**
1 – Ser servidor(a) civil da União, das autarquias e das fundações públicas federais que
opere direta, obrigatória e habitualmente no exercício de suas atribuições com Raios X ou
Substâncias Radioativas, junto às fontes de irradiação por um período mínimo de 12
(doze) horas semanais, como parte integrante das atribuições do cargo ou função
exercida, nos termos da legislação vigente;
2 – Ter formação em curso reconhecido por Órgão Oficial de Ensino que, em sua grade
curricular, apresente disciplinas que contemplem conceitos básicos em Proteção
Radiológica em uma ou mais das seguintes áreas: pesquisa e desenvolvimento, Radiologia
diagnóstica ou terapêutica .
2.1 - Excepcionalmente, uma vez justificada sua designação, o servidor cuja
formação não atenda ao referido requisito poderá ser autorizado a exercer sua
atividade após comprovação de treinamento em Radioproteção com carga horária
de, no mínimo, 40 horas, por instrutor devidamente habilitado.
3 – Estar desempenhando as atribuições de seu cargo, em atividade presencial;
4 – Realizar abertura de processo administrativo, no sistema informatizado de protocolo SIPAC
4.1 – É imprescindível a informação, no processo, da escala (dias e horários) de trabalho;
4.2 – O servidor deverá estar disponível, de acordo com a escala de trabalho
informada, onde serão avaliadas as condições de trabalho. OBS: A Inspeção não será
agendada, podendo ocorrer em qualquer um dos dias e horários informados na escala de
trabalho.
5 – Emissão de Relatório de Inspeção e Laudo Técnico no sistema informatizado para
concessão de adicionais ocupacionais, emitido pela CORAX – Comissão de Raios-X e
Substâncias Radioativas, em conformidade com a legislação vigente.
6 – Emissão de Portaria de concessão da gratificação por Raios X ou Substâncias
Radioativas.

**Documentação necessária**
1 - Formulário de Solicitação de Adicional de Raios X/Radiação Ionizante devidamente
preenchido e assinado (física ou eletronicamente) pelo servidor, chefia imediata e
diretoria do Centro/Órgão Suplementar/Superintendente.
2 – Atestado de Saúde Ocupacional (ASO), obtido no Núcleo de Atenção à Saúde do
Servidor – NASS/UFPE

**Base legal**
• Lei nº 8112 de 11/12/1990 (Seção II - das Gratificações e Adicionais, Subseção IV
e Art. 72).
• Orientação Normativa DRH/SAF/MARE nº 62, de 17/01/91 (DOU 18/01/91).
• Lei nº 8.270, de 17/12/91 – Artigo 12, parágrafos 1º, 3º e 5º e artigos 25 e 26.
• Instrução Normativa SGP/SEGGG/ME N° 15 de 16/03/2022 (Estabelece
orientações sobre a concessão dos adicionais de insalubridade, periculosidade, irradiação ionizante e gratificação por trabalhos com Raios-x ou Substâncias Radioativas).

**Orientações Gerais**
- No âmbito da UFPE, a competência técnica para a avaliação da concessão da gratificação
por trabalhos com Raios X ou Substâncias Radioativas pertence à Comissão de Raios X e
Substâncias Radioativas – CORAX.
- Os locais de trabalho e os servidores que operam com Raios X ou Substâncias
Radioativas serão mantidos sob controle permanente, de modo que as doses de radiação
ionizante não ultrapassem o nível máximo previsto na legislação própria. (Art. 72 da Lei
nº 8.112/90);
- A gratificação por trabalhos com Raios X ou Substâncias Radioativas será calculada
sobre o vencimento básico do cargo efetivo dos servidores civis da União, das autarquias
e das fundações públicas federais, com base no percentual de 10% (dez por cento). (Art.
12, § 2º da lei nº 8.270/91);
- Os servidores que operam com Raios X ou Substâncias Radioativas serão submetidos a
exames médicos a cada 6 (seis) meses. (Art. 72, § único da Lei nº 8.112/90);
- O servidor que opera direta e permanentemente com Raios X ou Substâncias
Radioativas gozará 20 (vinte) dias consecutivos de férias, por semestre de atividade
profissional, proibida em qualquer hipótese a acumulação. (Art. 79 da Lei nº 8.112/90);
- No caso específico do servidor docente, as férias deverão ser gozadas em 20
(vinte) ou 25 (vinte cinco) dias consecutivos em cada semestre, não ultrapassando 45
(quarenta e cinco) dias de férias no ano de atividade profissional.
- O afastamento para o desempenho de tarefas sem riscos de irradiação será, sempre, por
prazo determinado, findo o qual será o servidor submetido a novo exame de saúde. (Art.
6º, § 1º do Dec. nº 81.384/78);
- Os adicionais de insalubridade, de periculosidade e de irradiação ionizante, bem como
a gratificação por trabalhos com Raios X ou Substâncias Radioativas, estabelecidos na
legislação vigente, não se acumulam e são formas de compensação por risco à saúde dos
trabalhadores, tendo caráter transitório, enquanto durar a exposição. (Art. 4º, da IN
SGP/SEGGG/ME nº 15/2022);

**Solicitação da Gratificação por Trabalhos com Raios X ou Substâncias Radioativas**
- A Gratificação deverá ser requerida pelo servidor, cabendo à sua chefia atestar a
veracidade das informações apresentadas, quanto às atividades desempenhadas, à
natureza, duração e local(is) de trabalho onde atua o interessado.
- A solicitação deverá ser encaminhada à CORAX por meio da abertura de um
processo administrativo no sistema de protocolo SIPAC instruído com a
documentação requerida pelo Formulário de Solicitação de Adicional de Raios
X/Radiação Ionizante.

**Avaliação, Laudos e Pareceres Técnicos**
- Para a avaliação da concessão da gratificação por trabalhos com Raios X ou
Substâncias Radioativas, a CORAX realizará uma avaliação no(s) local(is) de
trabalho junto ao servidor.
- Com base na entrevista no local de trabalho e na análise da documentação
apresentada, a CORAX irá avaliar a concessão da gratificação, observando a
previsão legal para enquadramento da exposição ao agente de risco.
- A CORAX elaborará um Relatório de Inspeção e deverá inserir o Laudo Técnico
para concessão de adicionais ocupacionais no sistema informatizado Siapenet –
módulo: Saúde e Segurança do Trabalho com um parecer conclusivo, e em seguida,
anexá-los ao processo administrativo SIPAC para assinaturas pelos membros da
Comissão e posterior envio à Diretoria de Administração de Pessoal - DAP.

**Competências da DAP**
- A DAP analisará o processo administrativo SIPAC para a emissão de ato
administrativo pela Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida –
PROGEPE que determinará a efetiva autorização para pagamento.
- A DAP deverá garantir os preceitos administrativos para a
implantação/revisão/suspensão da gratificação e decidir sobre as situações nas
quais se caracterizam afastamentos não considerados de efetivo exercício e/ou a
concessão de valores retroativos à emissão do laudo técnico.
- A DAP procederá, de ofício, o cancelamento do adicional, sempre que ocorrer
remoção do servidor ou cessão a órgão externo à Universidade, cabendo ao
interessado, se for o caso, requerer nova concessão, em razão das atividades que
realize.

**Manutenção da Gratificação por Trabalhos Com Raios X ou Substâncias Radioativas**
- A concessão das gratificações fica condicionada à permanência da atividade nas
condições que, conforme verificadas, a justificaram, tornando-se insubsistente no
momento em que a atividade ou condições originárias não mais existirem.
- A concessão das gratificações fica condicionada ainda a realização de exames
médicos a cada 6 (seis) meses. (Art. 72, § único da Lei nº 8.112/90) e entrega do
Atestado de Saúde Ocupacional Periódico (ASO), obtido no Núcleo de Atenção a
Saúde do Servidor – NASS, à CORAX.
- Caso o servidor não realize seu Exame Médico, ou seja considerado inapto para a
função específica (através do ASO), deverá ser imediatamente afastado das
atividades que envolvam exposição obrigatória às radiações ionizantes e terá
cessada a concessão da gratificação. (Instrução Normativa SGP/SEGGG/ME Nº15,
de 16 de março de 2022).
- Cabe à chefia imediata do servidor informar à CORAX sobre quaisquer alterações
nos riscos que ensejam a percepção da gratificação.

**Procedimentos em caso de não concessão**
- Em caso de não concessão, o processo administrativo SIPAC deverá ser enviado
à unidade de lotação do servidor para ciência e posterior arquivamento na Seção
de Arquivo de Pessoal – SAP.

**Pedidos de Reconsideração**
- Os pedidos de reconsideração deverão ser apresentados à CORAX dentro do
prazo determinado pela Lei do Processo Administrativo (Lei n° 9.784/99).

**Revisão da Gratificação por Trabalhos Com Raios X ou Substâncias Radioativas**
- A CORAX poderá proceder com a revisão das concessões das gratificações por
iniciativa da Comissão ou por solicitação dos órgãos de controle, da área de
recursos humanos, dos servidores, e/ou de gestores, verificando se houve alteração
dos riscos e/ou da exposição do servidor que deu origem à concessão ou em razão
de atualização de aspectos normativos, emitindo novo Laudo técnico com fins de
revalidar a concessão da gratificação.
- Sempre que solicitado, os servidores deverão disponibilizar informações
atualizadas para a revisão das situações da gratificação por trabalhos com Raios X
ou Substâncias Radioativas.
- O não fornecimento de informações por parte do servidor para o processo de
revisão compromete a análise da manutenção da gratificação, retirando a validade
do laudo anteriormente produzido, o que implicará na suspensão da gratificação
por trabalhos com Raios X ou Substâncias Radioativas.

**Procedimentos**
- Abertura do Processo no sistema de protocolo informatizado SIPAC.
Origem: Processo Interno
Tipo do processo: GRATIFICAÇÃO DE RAIO X: SOLICITAÇÃO
Classificação: 023.164 - INSALUBRIDADE
Eletrônico: Sim
Assunto detalhado: PROCESSO PARA AVALIAÇÃO DA SOLICITAÇÃO DA
GRATIFICAÇÃO POR TRABALHOS COM RAIOS X OU SUBSTÂNCIAS RADIOATIVAS
<nome servidor> - SIAPE <número>
Tipo do documento: Formulário/Declaração etc.
Natureza do documento: Ostensivo
Forma do documento: Anexar documento digital
Natureza do processo: Ostensivo
Data do Documento: Data de emissão/assinaturas
Data do Recebimento: Data da Abertura
Tipo de Conferência: Documento Original (se gerado eletronicamente) / Cópia Simples (se escaneado)
Arquivo Digital: Formulário/Declarações etc
Assinantes: O formulário deve ser assinado eletronicamente ou escaneado e, conter as
assinaturas do servidor interessado, chefia imediata e diretor de centro/superintendente.
Ainda que as assinaturas constem no documento escaneado, o SIPAC requererá ao menos
um assinante responsável pela inserção do documento
Servidor: Incluir nome do servidor interessado/solicitante
E-mail: Incluir e-mail, caso não esteja cadastrado no SIPAC
Destino: Outra Unidade
Unidade de Destino: 11.07.47 (CORAX)
Setor responsável:
CORAX - Comissão de Raios X e Substâncias Radioativas
Contatos: Fone: 2126-8003
 E-mail: corax.ufpe@gmail.br

---Fim das Informações sobre Gratificação por Trabalhos com Raios X ou Substâncias Radioativas---


---Fim das Informações sobre Adicionais Ocupacionais---

---Provimento por Nomeação em Cargo Efetivo---

**PROVIMENTO POR NOMEAÇÃO EM CARGO EFETIVO**

PROVIMENTO POR NOMEAÇÃO EM CARGO EFETIVO

Sequência de atos admissionais previstos na Lei 8.112/1990 e que garantem o início da
vida funcional de servidores aprovados em concurso público. Composto por nomeação,
posse e efetivo exercício.

**Público Alvo**
Técnico-administrativo e docente.

**Requisitos Básicos**
- Ter a nacionalidade brasileira ou portuguesa e, no caso de nacionalidade
portuguesa, estar amparado pelo estatuto de igualdade entre brasileiros e
portugueses, com reconhecimento do gozo dos direitos políticos, nos termos do §
1º do artigo 12 da Constituição Federal;
- Prévia habilitação em concurso público de provas ou de provas e títulos,
obedecidos o prazo de sua validade e a ordem de classificação.
- Estar em gozo dos direitos políticos;
- Estar quite com as obrigações militares, em caso de candidato do sexo masculino;
- Estar quite com as obrigações eleitorais;
- Possuir nível de escolaridade exigido para o exercício do cargo;
- Ter a idade mínima de dezoito anos completos na data da posse;
- Ter aptidão física e mental para o exercício das atribuições do cargo;
- Declaração de bens e valores que constituem seu patrimônio e
- Declaração quanto ao exercício ou não de outro cargo, emprego ou função
pública;
- As atribuições do cargo podem justificar a exigência de outros requisitos
estabelecidos em lei.

**Documentação necessária**
As orientações, formulários e documentação necessária serão encaminhados aos
candidatos após a publicação da nomeação no Diário Oficial da União, através do
e-mail cadastrado no momento do curso.

**Base legal**
● Constituição Federal de 1988;
● Lei n° 8.112, de 11 de dezembro de 1990;
● Lei 12.990, de 9 de junho de 2014;
● Lei 11.091, de 12 de janeiro de 2005;
● Decreto nº 9.739, de 28 de março de 2019.

**Informações Gerais**
1 - A nomeação para cargo de carreira ou cargo isolado de provimento efetivo depende
de prévia habilitação em concurso público de provas ou de provas e títulos, obedecidos a
ordem de classificação e o prazo de sua validade;
2 - O provimento dos cargos públicos far-se-á mediante ato da autoridade competente
do órgão ou entidade responsável pela realização do concurso público, que homologará
e publicará no Diário Oficial da União a relação dos candidatos aprovados no certame,
por ordem de classificação;
3 - A investidura em cargo público ocorrerá com a posse. A posse dar-se-á pela
assinatura do respectivo termo;
4 - A posse ocorrerá no prazo de trinta dias contados da publicação do ato de
provimento.
5 - Em se tratando de servidor, que esteja na data de publicação do ato de provimento,
em licença prevista nos incisos I, III e V do art. 81, ou afastado nas hipóteses dos incisos
I, IV, VI, VIII, alíneas "a", "b", "d", "e" e "f", IX e X do art. 102 da Lei 8112/1990, o prazo
será contado do término do impedimento.
6 - Será tornado sem efeito o ato de nomeação se a posse não ocorrer no prazo previsto
de 30 (trinta) dias após a sua publicação.
7 - A posse poderá dar-se mediante procuração específica para aquele fim;
8 - A posse em cargo público dependerá de prévia inspeção médica oficial, que será
agendada após a nomeação, seguindo-se as orientações enviadas aos candidatos quando
da publicação do ato de nomeação em Diário Oficial da União (DOU).

**Procedimentos:**
Os procedimentos admissionais são realizados seguindo as orientações encaminhadas
aos candidatos nomeados, após publicação do ato de nomeação no DOU. Consiste
basicamente em avaliação física e psicológica pela Junta Médica, apresentação da
documentação exigida, avaliação de acumulação de cargos e empregos, posse, e
apresentação à unidade de lotação para efetivo exercício do cargo.

**Setor responsável:**
Coordenação de Provimentos e Concursos
Contatos: Fone: 2126-8672
E-mail: provimentos.progepe@ufpe.br

---Fim das informações de Provimento por Nomeação em Cargo Efetivo---

---Informações sobre Afastamentos---

## Tipos de Afastamento para Servidores da UFPE 

Este documento consolida as informações sobre os diferentes tipos de afastamento para servidores (docentes e técnico-administrativos) da UFPE, com base nos documentos fornecidos. 

**1. Afastamento para Participar de Curso de Formação (Art. 20, § 4º da Lei 8.112/90)**

* **O que é?** Afastamento para participação em curso de formação decorrente de aprovação em concurso para outro cargo na Administração Pública Federal.
* **Público Alvo:** Servidor ativo permanente da UFPE.
* **Requisitos:**
    * Ser servidor ativo permanente.
* **Documentação Necessária:**
    * Edital de aprovação no concurso.
    * Edital de convocação para participação do curso de formação com marcações no nome do servidor.
    * Requerimento próprio com datas de início e fim do curso.
    * Informativo sobre a remuneração que o servidor irá optar (ver Informações Gerais).
* **Base Legal:**
    * Lei nº 8.112, de 11/12/1990 (Art. 20, § 4º e § 5º).
    * Lei nº 9.624/98 (Art. 14).
* **Informações Gerais:**
    * Durante o curso, o servidor pode optar por receber 50% da remuneração da classe inicial do cargo almejado OU o vencimento e vantagens do cargo efetivo atual.
    * O estágio probatório fica suspenso e retorna após o término do curso.
    * O tempo no curso conta como efetivo exercício para o novo cargo (exceto para estágio probatório, estabilidade, férias e promoção).
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: 
        * CURSOS PROMOVIDOS POR OUTRAS INSTITUCOES NO BRASIL - TECNICO (PESSOAL). 
        * CURSOS PROMOVIDOS POR OUTRAS INSTITUCOES NO BRASIL - DOCENTE (PESSOAL).
    * Classificação (CONARQ): 023.4 - AFASTAMENTOS.
    * Código do Setor Responsável: 11.07.30.
* **Setor Responsável:** SMP - Seção de Movimentação de Pessoal.
    * Telefone: (81) 2126-8165
    * E-mail: smp.progepe@ufpe.br


**2. Afastamento para Ações de Desenvolvimento (Curta e Longa Duração)**

**2.1 Afastamento de Curta Duração (até 30 dias)**

* **O que é?**  Afastamento para participar de ações formativas (ouvinte) no Brasil ou no exterior, com duração máxima de 30 dias. Inclui cursos, eventos (congressos, seminários, etc.) e aprendizagem experiencial (estágios, visitas técnicas, intercâmbios).
* **Público Alvo:** Servidores técnico-administrativos e docentes da UFPE.
* **Requisitos:**
    * Ser servidor efetivo (docente ou técnico-administrativo).
    * A ação deve ser relacionada ao cargo/função/ambiente organizacional.
    * Autorização da chefia imediata.
    * Autorização da direção do centro acadêmico (e da superintendência, órgão suplementar ou unidade da administração central, no caso de técnico-administrativos).
    * Incompatibilidade de horário da ação com a jornada de trabalho.
    * Não coincidir com férias programadas ou outros afastamentos.
* **Documentação Necessária:**
    * Requerimento.
    * Autorização da chefia imediata.
    * Autorização da direção de centro acadêmico (e da superintendência, órgão suplementar ou unidade da administração central, no caso de técnico-administrativos).
    * Comprovante de solicitação ou de concessão de bolsa/auxílio (se houver).
    * Documento informando o período de férias do servidor.
    * Documento relativo ao evento/curso/ação.
* **Base Legal:**
    * Decreto nº 91.800 de 18/10/1985.
    * Decreto nº 9.991 de 28/08/2019.
    * Portaria MEC nº 404 de 23/04/2009.
    * Portaria MEC nº 204 de 06/02/2020.
    * Portaria Normativa UFPE nº 03 de 10/02/2020.
    * Resolução n.º 11/2022 - CEPE/UFPE.
    * Portaria Normativa nº 9 de 23 de maio de 2006(específico para afastamento no Brasil)
* **Informações Gerais:**
    * O processo deve ser aberto com pelo menos 30 dias de antecedência da data de início.
    * O comprovante de concessão de bolsa/auxílio (se houver) deve ser apresentado assim que disponível.
    * Tipos de ônus: 
        * **Com Ônus:** Remuneração + bolsa/auxílio (se houver). Direito a passagens e diárias.
        * **Com Ônus Limitado:** Remuneração OU bolsa/auxílio. Sem direito a passagens e diárias.
        * **Sem Ônus:** Perda total da remuneração. Sem direito a passagens e diárias.
    * Após o afastamento, anexar documentação comprobatória ao processo e enviar para a Seção de Arquivo de Pessoal (código SIPAC 11.07.22).
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo:
        * Afastamento para estudo de curta duração no Brasil (CONARQ: 023.4 – AFASTAMENTOS).
        * Afastamento para estudo de curta duração no Exterior (CONARQ: 023.4 – AFASTAMENTOS).
    * Classificação (CONARQ): 023.4 - AFASTAMENTOS
    * Código do Setor Responsável: 11.07.47.
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Telefone: (81) 2126-8671 / 2126-8669
    * E-mail: saapq.cfc@ufpe.br

**2.2 Afastamento de Longa Duração (mais de 30 dias)**

* **O que é?** Afastamento para participar de programa de Pós-Graduação Stricto Sensu (mestrado e doutorado) e pós-doutorado no Brasil ou no exterior, com duração superior a 30 dias. 
* **Público Alvo:** Servidores técnico-administrativos e docentes da UFPE.
* **Requisitos:**
    * **Requisitos Comuns (Docentes e Técnicos):**
        * Ser servidor efetivo.
        * A ação deve ser relacionada ao cargo/função/ambiente organizacional.
        * Autorização da chefia imediata.
        * Incompatibilidade de horário da ação com a jornada de trabalho.
        * Não coincidir com férias programadas ou outros afastamentos.
        * Não ter se afastado nos últimos 2 anos por licença para tratar de assuntos particulares ou licença capacitação (para mestrado e doutorado).
        * Não ocupar cargo em comissão, função de confiança ou cargo de direção (se ocupar, anexar comprovante de solicitação de exoneração/dispensa).
    * **Requisitos Específicos para Técnicos-Administrativos:**
        * Tempo mínimo no cargo efetivo:
            * Mestrado: 3 anos (incluindo estágio probatório).
            * Doutorado e Pós-doutorado: 4 anos (incluindo estágio probatório).
    * **Requisitos Específicos para Docentes (Pós-Doutorado):**
        * Apresentar PAAD e RAAD devidamente homologados.
        * Indicar o professor substituto durante o afastamento.
* **Documentação Necessária:**
    * **Documentação Comum (Docentes e Técnicos):**
        * Requerimento.
        * Termo de compromisso.
        * Plano de estudo/trabalho.
        * Comprovante de vínculo com a instituição de destino.
        * Comprovante de solicitação ou de concessão de bolsa/auxílio (se houver).
        * Documento informando o período de férias do servidor (para afastamentos menores que 365 dias).
        * Comprovante de abertura de processo solicitando exoneração/dispensa do cargo em comissão, função de confiança ou cargo de direção (se aplicável), ou declaração de que não exerce nenhuma dessas funções.
    * **Documentação Específica para Docentes:**
        * Extrato/cópia da ata da reunião do departamento aprovando o afastamento.
        * Extrato/cópia da ata da reunião do conselho do centro aprovando o afastamento.
        * PAAD e RAAD homologados (apenas para pós-doutorado).
        * Documento indicando o professor substituto (apenas para pós-doutorado).
* **Base Legal:**
    * Lei nº 8.112 de 11/12/1990.
    * Decreto nº 91.800 de 18/10/1985.
    * Decreto nº 1.387 de 07/02/1995.
    * Decreto nº 9.991 de 28/08/2019.
    * Instrução Normativa SGP-ENAP/SEDGG/ME nº 21/2021.
    * Resolução nº 06/2018 - CEPE/UFPE (para pós-doutorado).
    * Ofício Circular nº 14/2021 - DGBS PROGEST – UFPE.
* **Informações Gerais:**
    * O processo deve ser aberto com pelo menos 90 dias de antecedência da data de início.
    * Prorrogações:
        * Devem ser solicitadas no mesmo processo, com antecedência mínima de 45 dias da data de término.
        * Anexar documentação atualizada (exceto comprovante de exoneração/dispensa).
        * Incluir relatório de atividades e avaliação do orientador (se aplicável).
    * Processos físicos de prorrogação devem ser digitalizados (ver Ofício Circular nº 14/2021).
    * O comprovante de concessão de bolsa/auxílio (se houver) deve ser apresentado assim que disponível.
    * A remuneração do cargo efetivo é mantida (exceto em afastamentos sem ônus), mas adicionais/gratificações por insalubridade, periculosidade etc. são suspensos.
    * Tipos de ônus:
        * **Com Ônus:** Remuneração + bolsa/auxílio (se houver). Direito a passagens e diárias.
        * **Com Ônus Limitado:** Remuneração OU bolsa/auxílio. Sem direito a passagens e diárias.
        * **Sem Ônus:** Perda total da remuneração. Sem direito a passagens e diárias.
    * Tempo de afastamento:
        * Mestrado: até 1 ano, prorrogável até 24 meses.
        * Doutorado: até 1 ano, prorrogável até 48 meses.
        * Pós-doutorado: até 12 meses (sem prorrogação).
    * Após o término, é necessário um período igual ao do afastamento para novo afastamento.
    * **Permanência Obrigatória (após o retorno):**
        * Afastamento no Brasil: período igual ao do afastamento. Se houver exoneração/aposentadoria antes do prazo, o servidor deve ressarcir a UFPE pelos gastos com o aperfeiçoamento (Lei 8.112/1990, Art. 96-A).
        * Afastamento no Exterior: período igual ao do afastamento (máximo de 4 anos). Não é permitida exoneração ou licença para tratar de interesse particular antes disso, exceto com ressarcimento dos gastos (Lei 8.112/1990, Art. 95).
    * No prazo de 90 dias (pós-doutorado) ou 30 dias (demais), após o término, anexar relatório circunstanciado e documentação comprobatória ao processo.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: 
        * Afastamento para estudos de longa duração no Brasil (CONARQ: 023.3).
        * Afastamento para estudos de longa duração no Exterior (CONARQ: 023.3).
    * Classificação (CONARQ): 023.3.
    * Código do Setor Responsável: 11.07.47.
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Telefone: (81) 2126-8671 / 2126-8669
    * E-mail: saapq.cfc@ufpe.br 

---Fim de informações sobre Afastamentos---

---Informações sobre Aposentadorias e Desligamentos---

## Desligamento e Aposentadoria de Servidores da UFPE: Guia Completo

Este guia apresenta, de forma consolidada, os procedimentos para os diferentes tipos de desligamento e aposentadoria de servidores da UFPE, com base nos documentos fornecidos. 

**1. Exoneração de Cargo Efetivo**

* **O que é?** Desligamento definitivo e sem caráter punitivo do cargo público efetivo, rompendo o vínculo jurídico entre o servidor e a UFPE.
* **Público Alvo:** Servidores técnico-administrativos e docentes efetivos.
* **Requisitos:**
    * Ocupar cargo efetivo.
    * Não responder a processo disciplinar (ver Lei 8.112/90, Art. 172).
* **Documentação Necessária:**
    * Requerimento de Exoneração.
    * Cópia do documento oficial com foto (RG, CNH, Passaporte) e CPF.
    * Declaração de bens OU cópia da Declaração de Imposto de Renda completa com recibo de entrega.
    * Se aplicável: cópias da procuração e documento oficial com foto do procurador.
* **Base Legal:**
    * Lei 8.112/90 (Art. 34, 47 e 172).
    * Nota Informativa nº 305/2010/COGES/DENOP/SRH/MP.
    * Nota Técnica nº 236/2009/COGES/DENOP/SRH/MP.
    * Nota Técnica nº 385/2009/COGES/DENOP/SRH/MP.
    * Nota Técnica nº 313/2013/CGNOR/DENOP/SEGEP/MP.
    * Nota Informativa nº 365/2010/COGES/DENOP/SRH/MP.
    * Parecer AGU/WM –1/2000 (Anexo ao Parecer AGU nº GM- 13/2000).
    * Parecer AGU nº 13/GM de 11/12/2000.
    * Parecer nº AGU/LS-04/97.
    * Ofício COGLE/DENOR/SRH/SEAP nº 117/99.
* **Informações Gerais:**
    * A exoneração extingue a relação jurídica (e seus direitos e deveres) criada pela nomeação e posse.
    * A UFPE não pode recontratar um ex-servidor exonerado a pedido sob alegação de desconhecimento da lei.
    * **Exoneração x Vacância:**
        * A exoneração a pedido é o procedimento geral para ruptura definitiva do vínculo.
        * A vacância por posse em cargo inacumulável se aplica quando o servidor assume outro cargo incompatível, mesmo sendo esta a regra geral, o servidor pode optar por pedir exoneração.
        * É recomendado que a data de vacância seja a mesma da posse no novo cargo, garantindo a continuidade da relação jurídica com a administração pública (ver Parecer AGU nº 13/GM).
    * **Afastamento:** Servidores em afastamento para estudo/missão no exterior ou pós-graduação *stricto sensu* não podem ser exonerados antes do fim do período de permanência obrigatória, a não ser que ressarçam as despesas (ver regras de Afastamento).
    * **Consequências Administrativas:** Variam conforme a situação do servidor e do novo cargo/emprego (ver Quadro 1 do documento "Exoneração de Cargo Efetivo"). Em resumo:
        * **Servidor Estável:** Pode ser reconduzido ao cargo anterior se pedir exoneração para assumir outro cargo público (e não for aprovado no estágio probatório nem obtiver estabilidade no novo cargo).
        * **Servidor Não Estável:** Não pode ser reconduzido ao cargo anterior.
        * **Assumir Emprego (Público ou Privado):** Só cabe exoneração. O servidor perde o vínculo com a UFPE, não pode ser reconduzido e será indenizado por férias e 13º salário proporcionais.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: EXONERACAO DO CARGO EFETIVO.
    * Classificação (CONARQ): 022.7 – VACANCIA.
    * Assunto Detalhado: EXONERAÇÃO A PEDIDO.
    * Código do Setor Responsável: 11.07.10.
* **Setor Responsável:** CPC – Coordenação de Provimentos e Concursos.
    * Telefone: (81) 2126-7095
    * E-mail: admissao.progepe@ufpe.br

**2. Vacância por Posse em Cargo Público Inacumulável**

* **O que é?** Desligamento do cargo público efetivo em virtude da posse em outro cargo público incompatível com o atual, independentemente da esfera de poder.
* **Público Alvo:** Servidores técnico-administrativos e docentes efetivos.
* **Requisitos:**
    * Nomeação em outro cargo público inacumulável.
* **Documentação Necessária:**
    * Requerimento de Vacância.
    * Comprovante de vinculação ao novo cargo: cópia da publicação da portaria de nomeação no Diário Oficial OU cópia do Termo de Posse.
    * Cópia do documento oficial com foto (RG, CNH, Passaporte) e CPF.
    * Declaração de bens OU cópia da Declaração de Imposto de Renda completa com recibo de entrega.
    * Se aplicável: cópias da procuração e documento oficial com foto do procurador.
* **Base Legal:**
    * Lei 8.112/90.
    * Nota Informativa nº 305/2010/COGES/DENOP/SRH/MP.
    * Nota Técnica nº 236/2009/COGES/DENOP/SRH/MP.
    * Nota Técnica nº 385/2009/COGES/DENOP/SRH/MP.
    * Nota Informativa nº 365/2010/COGES/DENOP/SRH/MP.
    * Parecer AGU nº 13/GM de 11/12/2000.
    * Parecer nº AGU/LS-04/97.
    * Ofício COGLE/DENOR/SRH/SEAP nº 67/99.
    * Ofício COGLE/DENOR/SRH/SEAP nº 117/99.
* **Informações Gerais:**
    * **Servidor em Estágio Probatório:** Pode solicitar vacância, mas não poderá ser reconduzido ao cargo anterior.
    * **Data da Vacância:** Recomenda-se que seja a mesma da posse no novo cargo para manter a continuidade jurídica com a administração pública (ver Parecer AGU nº 13/GM).
    * **Estabilidade:** O vínculo com a União só se extingue quando o servidor estável assume outro cargo inacumulável em outra esfera federativa (Nota Técnica nº 236/2009).
    * **Férias e 13º Salário:** 
        * Não é exigido novo período aquisitivo de 12 meses no novo cargo se o servidor já tiver cumprido no cargo anterior (Portaria Normativa nº 2/98-SRH/MARE, Art. 7º).
        * Se não tiver 12 meses no cargo anterior, o período deverá ser complementado no novo cargo.
    * **Assumir Emprego (Público ou Privado):**  Nesses casos, o servidor deve solicitar Exoneração.
    * **Consequências Administrativas:** Variam conforme a situação do servidor e do novo cargo/emprego (ver Quadro 1 do documento "Vacância por Posse em Cargo Público Inacumulável"). As regras são as mesmas da Exoneração a Pedido.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: VACANCIA POR POSSE EM CARGO INACUMULAVEL.
    * Classificação (CONARQ): 022.7 – VACANCIA.
    * Assunto Detalhado: Vacância por posse em cargo inacumulável.
    * Código do Setor Responsável: 11.07.10.
* **Setor Responsável:** CPC – Coordenação de Provimentos e Concursos.
    * Telefone: (81) 2126-7095
    * E-mail: admissao.progepe@ufpe.br

**3. Aposentadoria**

**3.1 Aposentadoria Voluntária**

* **O que é?** Benefício previdenciário concedido a pedido do servidor que cumpre os requisitos legais.
* **Público Alvo:** Servidores ativos da UFPE.
* **Requisitos:** Cumprir as exigências das regras de aposentadoria vigentes (preservada a opção pelas regras antigas, de transição e geral, quando pertinente).
* **Documentação Necessária:**
    * Requerimento de Aposentadoria (ver modelo em anexo no documento original).
    * Declaração de acumulação de cargos (ver modelo em anexo no documento original).
    * Se aplicável: documentos que comprovem a acumulação de cargo/emprego/benefício.
    * Ofício da chefia imediata informando se o servidor responde a inquérito administrativo.
    * Documento oficial com foto (RG, CNH, Carteira de registro profissional).
    * CPF (se não constar no documento anterior).
    * Declaração de bens OU Declaração de Imposto de Renda completa com recibo de entrega.
    * Contracheque.
    * Diploma da maior titulação.
* **Base Legal:**
    * Emenda Constitucional nº 103/2019.
    * Emenda Constitucional nº 47/2005.
    * Emenda Constitucional nº 41/2003.
    * Emenda Constitucional nº 20/1999.
    * Constituição Federal de 1988.
* **Informações Gerais:**
    * A aposentadoria compulsória é automática aos 75 anos (ver item 3.3).
    * Se o servidor solicitar aposentadoria compulsória, mas fizer jus à voluntária, será aplicada a regra mais vantajosa.
    * Se o servidor não abrir o processo de aposentadoria compulsória, a SAEP o fará.
* **Procedimento para Abertura do Processo:**
    1. Preencher e assinar os formulários de Requerimento e Declaração de Acumulação de Cargos.
    2. Digitalizar todos os documentos necessários.
    3. Abrir o processo no SIPAC:
        * Tipo de Processo: APOSENTADORIA VOLUNTÁRIA.
        * Classificação (CONARQ): 026.53 - APOSENTADORIA VOLUNTÁRIA.
        * Assunto Detalhado: APOSENTADORIA VOLUNTÁRIA.
        * Natureza do Processo: OSTENSIVO.
        * Anexar os documentos (opcional: inserir documentos como "restritos").
        * Encaminhar para a CACE (Coordenação de Acumulação de Cargos e Empregos) - Código SIPAC: 11.07.40.
* **Setor Responsável:** SAEP - Seção de Aposentadoria e Pensão.
    * Telefone: (81) 2126-8175
    * E-mail: saep.progepe@ufpe.br

**3.2 Aposentadoria por Incapacidade**

* **O que é?** Benefício previdenciário concedido ao servidor considerado incapaz para o trabalho pela Junta Médica Oficial, sem possibilidade de readaptação.
* **Público Alvo:** Servidores ativos da UFPE.
* **Requisitos:** Laudo Médico Pericial de incapacidade emitido pela Junta Médica Oficial.
* **Documentação Necessária:**
    * Declaração de acumulação de cargos (ver modelo em anexo no documento original).
    * Se aplicável: documentos que comprovem a acumulação de cargo/emprego/benefício.
    * Ofício da chefia imediata informando se o servidor responde a inquérito administrativo.
    * Documento oficial com foto (RG, CNH, Carteira de registro profissional).
    * CPF (se não constar no documento anterior).
    * Declaração de bens OU Declaração de Imposto de Renda completa com recibo de entrega.
    * Contracheque.
    * Diploma da maior titulação.
* **Base Legal:**
    * Emenda Constitucional nº 103/2019.
    * Portaria SGP/SEDGG/ME nº 10.360/2022.
    * Manual de Perícia Oficial em Saúde do Servidor Público Federal.
* **Informações Gerais:**
    * O servidor pode solicitar reconsideração da decisão da Junta Médica em até 30 dias.
    * A perícia médica definirá a periodicidade da verificação da incapacidade (não superior a 2 anos, exceto em casos excepcionais - Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 28, parágrafo único).
    * Não é necessário cumprir estágio probatório (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 30).
    * Se o servidor cumprir os requisitos para aposentadoria voluntária, poderá optar pela mais vantajosa (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 31).
    * Não é permitido acumular cargo público com aposentadoria por incapacidade (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 33).
    * É proibido exercer qualquer atividade na iniciativa privada durante a aposentadoria por incapacidade (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 34).
    * A aposentadoria será reavaliada se o servidor voltar a exercer atividade laboral ou houver possibilidade de readaptação (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 35).
    * O pagamento do benefício será suspenso se o servidor não comparecer à perícia médica quando convocado (Portaria SGP/SEDGG/ME nº 10.360/2022, Art. 35, parágrafo 1º).
* **Procedimento para Abertura do Processo:**
    * **Opção 1: Núcleo de Atenção à Saúde do Servidor (NASS)**
        * O NASS recebe a documentação digitalizada e dá andamento ao processo.
        * Enviar a documentação para o e-mail da SAEP (saep.progepe@ufpe.br).
    * **Opção 2: Abertura pelo próprio Servidor**
        1. Preencher e assinar os formulários de Requerimento e Declaração de Acumulação de Cargos.
        2. Digitalizar todos os documentos necessários.
        3. Abrir o processo no SIPAC:
            * Tipo de Processo: APOSENTADORIA POR INVALIDEZ.
            * Classificação (CONARQ): 026.51 - INVALIDEZ PERMANENTE.
            * Assunto Detalhado: APOSENTADORIA INVALIDEZ.
            * Natureza do Processo: OSTENSIVO.
            * Anexar os documentos (opcional: inserir documentos como "restritos").
            * Encaminhar para a SAEP (Seção de Aposentadoria e Pensão) - Código SIPAC: 11.07.33.
* **Setor Responsável:** SAEP - Seção de Aposentadoria e Pensão.
    * Telefone: (81) 2126-8168 / 8175
    * E-mail: saep.progepe@ufpe.br

**3.3 Aposentadoria Compulsória (Idade)**

* **O que é?**  Benefício previdenciário concedido automaticamente ao servidor que completa 75 anos de idade.
* **Público Alvo:** Servidores ativos da UFPE.
* **Requisitos:**  Completar 75 anos de idade.
* **Documentação Necessária:**
    * Declaração de acumulação de cargos (ver modelo em anexo no documento original).
    * Se aplicável: documentos que comprovem a acumulação de cargo/emprego/benefício.
    * Ofício da chefia imediata informando se o servidor responde a inquérito administrativo.
    * Documento oficial com foto (RG, CNH, Carteira de registro profissional).
    * CPF (se não constar no documento anterior).
    * Declaração de bens OU Declaração de Imposto de Renda completa com recibo de entrega.
    * Contracheque.
    * Diploma da maior titulação.
* **Base Legal:**
    * Emenda Constitucional nº 103/2019.
    * Constituição Federal de 1988.
    * Lei nº 8.112/1990 (Art. 187).
* **Informações Gerais:**
    * A aposentadoria compulsória é automática, com vigência a partir do dia seguinte ao aniversário de 75 anos do servidor.
    * Se o servidor solicitar aposentadoria compulsória, mas fizer jus à voluntária, será aplicada a regra mais vantajosa.
    * Se o servidor não abrir o processo de aposentadoria compulsória, a SAEP o fará.
* **Procedimento para Abertura do Processo:**
    1. Preencher e assinar a Declaração de Acumulação de Cargos.
    2. Digitalizar todos os documentos necessários.
    3. Abrir o processo no SIPAC:
        * Tipo de Processo: APOSENTADORIA COMPULSÓRIA.
        * Classificação (CONARQ): 026.52 - APOSENTADORIA COMPULSÓRIA.
        * Assunto Detalhado: APOSENTADORIA COMPULSÓRIA.
        * Natureza do Processo: OSTENSIVO.
        * Anexar os documentos (opcional: inserir documentos como "restritos").
        * Encaminhar para a CACE (Coordenação de Acumulação de Cargos e Empregos) - Código SIPAC: 11.07.40.
* **Setor Responsável:** SAEP - Seção de Aposentadoria e Pensão.
    * Telefone: (81) 2126-8175
    * E-mail: saep.progepe@ufpe.br

(Declaração de acúmulo de cargos, requerimento para aposentadoria, requerimento para vacância por possem em outro cargo e requerimento para exoneração do cargo efetivo podem ser encontrados no site https://www.ufpe.br/manual-do-servidor/aposentadorias-e-desligamentos)

---Fim das Informações sobre Aposentadorias e Desligamentos---

---Informações sobre Auxílios---

## Auxílios para Servidores da UFPE: Guia Completo

Este guia detalha os auxílios disponibilizados aos servidores da UFPE, com base nos documentos fornecidos.

**1. Auxílio-Saúde (Per Capita Saúde Suplementar)**

* **O que é?**  Ressarcimento parcial das despesas com planos de saúde privados para servidores ativos, inativos, pensionistas e seus dependentes. 
* **Público Alvo:**
    * Servidores ativos efetivos ou comissionados.
    * Servidores aposentados.
    * Pensionistas.
* **Requisitos:**
    * Possuir plano de saúde ou odontológico.
    * O plano deve atender ao padrão mínimo da ANS (Agência Nacional de Saúde Suplementar), conforme a Instrução Normativa SGP/SEDGG/ME nº 97/2022.
        * **Exceção:** Planos contratados antes da Lei nº 9.656/1998.
* **Base Legal:**
    * Art. 230 da Constituição Federal.
    * Lei nº 8.112/90.
    * Portaria nº 08/2016 - MPOG.
    * Instrução Normativa SGP/SEDGG/ME nº 97/2022.
* **Informações Gerais:**
    * **Dependentes:**
        * Cônjuge ou companheiro(a) em união estável.
        * Pessoa separada/divorciada ou com união estável dissolvida (judicial ou extrajudicialmente) que recebe pensão alimentícia.
        * Filhos e enteados:
            * Até 21 anos incompletos.
            * Inválidos (enquanto durar a invalidez).
            * Entre 21 e 24 anos, se dependentes economicamente do servidor e estudantes de curso regular reconhecido pelo MEC (comprovar vínculo e dependência semestral e anualmente).
        * Menor sob guarda ou tutela judicial (enquanto durar a condição).
    * **Pais e mães NÃO são dependentes, mesmo que economicamente.**
    * **Pensionistas:** Seus dependentes não têm direito ao auxílio.
    * **Cadastro de Dependentes:** Os dependentes devem estar cadastrados no assentamento funcional do servidor (SouGov - módulo "Cadastro de Dependente").
    * **Início do Benefício:** Na data do requerimento no SouGov.
    * **Pagamento:** Mensal, no contracheque do titular.
    * **Obrigações do Servidor/Pensionista:** Informar alterações no plano (titularidade, operadora, valor, inclusão/exclusão de beneficiários) e nos dados cadastrais que afetem o benefício, através do SouGov.
    * **Acompanhamento:** O servidor deve acompanhar o status da solicitação no SouGov.
    * **Planos de Autogestão (ASSEFAZ, CAPESAÚDE e GEAP):** Não requerem solicitação no SouGov. A DAQV (Divisão de Apoio em Qualidade de Vida) gerencia o benefício.
* **Concessão, Alteração e Exclusão:**
    * **Concessão:**
        * **Documentos:**
            * Contrato do plano (com titularidade).
            * Boleto mais recente com valores por pessoa + comprovante de pagamento.
            * Para filhos/enteados entre 21 e 24 anos: comprovante de matrícula e dependência econômica.
        * **Procedimento:** 
            * SouGov (web ou app) - bloco "Solicitações" - ícone "Saúde Suplementar".
            * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/saude-suplementar/como-solicitar-assistencia-a-saude-suplementar-teste
    * **Alteração:**
        * **Documentos:** Documentação referente à alteração (ex: novo boleto com comprovante, documento do plano com data de inclusão/exclusão de dependente).
        * **Procedimento:**
            * SouGov (web ou app) - bloco "Solicitações" - ícone "Saúde Suplementar".
            * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/saude-suplementar/copy_of_como-solicitar-assistencia-a-saude-suplementar
            * Para incluir/excluir dependentes, marcar/desmarcar no módulo "Saúde Suplementar".
    * **Exclusão:**
        * **Documentos:** Último boleto com comprovante OU declaração de quitação do plano com data de desligamento/último pagamento.
        * **Procedimento:**
            * SouGov - "Assistência à saúde suplementar" - "Encerrar plano".
            * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/saude-suplementar/encerrar-plano
* **Setor Responsável:** DAQV - Divisão de Apoio em Qualidade de Vida.
    * E-mail: apoio.dqv@ufpe.br
    * Telefone: (81) 2126-8190
    * WhatsApp: (81) 2126-8189

**2. Auxílio-Transporte**

* **O que é?** Indenização para cobrir parcialmente as despesas com transporte público no trajeto casa-trabalho-casa.
* **Público Alvo:** Servidores que usam transporte público municipal, intermunicipal ou interestadual.
* **Base Legal:**
    * MP nº 2.165-36/2001.
    * Decreto nº 2.880/1998.
    * Instrução Normativa nº 207/2019.
    * Nota Técnica Consolidada nº 01/2013/CGNOR/DENOP/SEGEP/MP.
    * Nota Técnica nº 1102/2019-ME.
* **Informações Gerais:**
    * Beneficiários: servidores e empregados públicos da administração federal direta, autárquica e fundacional.
    * Inclui professores substitutos e visitantes (Lei nº 8.745/1993).
    * Não cobre deslocamentos em intervalos de repouso/alimentação durante a jornada.
    * Residência: local de moradia habitual do servidor.
    * Natureza indenizatória, pago em dinheiro.
    * Não pode ser incorporado a vencimentos, remuneração, proventos ou pensão.
    * Cálculo do desconto de 6%: sobre o vencimento básico proporcional a 22 dias (VB/30 * 22).
    * Limites: o valor não pode ser menor que a despesa real nem maior que o valor da tabela de escalonamento (gasto diário * 22 - desconto de 6%).
    * Despesa inferior ao desconto de 6%: o servidor não tem direito ao auxílio.
    * Suspensão do auxílio: em ausências e afastamentos considerados efetivo exercício (ex: férias, licença-maternidade/paternidade, licença médica até 24 meses, licença capacitação, serviço militar, missão/estudo no exterior, etc.).
* **Procedimento para Abertura do Processo:**
    * SouGov.
    * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/auxilio-transporte/como-solicitar-o-auxilio-transporte-pelo-aplicativo-sougov-br
* **Setor Responsável:** DP - Divisão de Pagamento.
    * Telefone: (81) 2126-8177
    * E-mail: dp.progepe@ufpe.br

**3. Auxílio Pré-Escolar**

* **O que é?** Auxílio para educação pré-escolar de dependentes com até 5 anos, 11 meses e 29 dias (ou idade mental equivalente).
* **Público Alvo:** Servidores ativos permanentes.
* **Requisitos:**
    * Dependente(s) cadastrado(s) no SIAPE/E-siape.
    * Dependente com até 6 anos incompletos (ou idade mental equivalente, comprovada por laudo médico).
    * Acesso ao SouGov.
* **Documentação Necessária:**
    * Certidão de nascimento do(s) filho(s).
    * Acesso ao SouGov.
    * Cadastro do(s) filho(s) como dependente(s) no SouGov.
* **Base Legal:**
    * Decreto nº 977/1993.
    * Instrução Normativa nº 12/SAF/1993.
    * Portaria nº 658/1995.
    * Orientação Consultiva nº 12/97 – DENOR/SRH/MARE.
    * Nota Técnica nº 713/2009/COGES/DENOP/SRH/MP.
    * Nota Informativa nº 546/2010/CGNOR/DENOP/SRH/MP.
    * Nota Técnica nº 39/2010/COGES/DENOP/SRH/MP.
    * Portaria Interministerial nº 10/2016.
    * Ofício-Circular nº 20/2022/DAJ/COLEP/CGGP/SAA-MEC.
    * Portaria MGI nº 2.897/2024.
* **Informações Gerais:**
    * Beneficiários: dependentes de servidores ativos (efetivos e professores substitutos) da administração pública federal direta, autárquica e fundacional.
    * Dependentes: filho(s) e/ou menor(es) sob tutela do servidor.
    * Valor: R$ 489,90 por dependente, por mês.
    * Concessão:
        * Apenas para um dos cônjuges servidores públicos federais.
        * Para quem detém a guarda legal, em caso de separação.
        * A partir da data do nascimento.
    * Perda do benefício:
        * Quando o dependente completa 6 anos.
        * Em caso de falecimento do dependente.
        * Durante licença para tratar de interesses particulares.
        * Durante afastamento ou licença com perda de remuneração.
* **Procedimento para Abertura do Processo:**
    * SouGov - módulo "Cadastro de dependentes".
    * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/cadastrar-dependentes/cadastrar-dependente
* **Setor Responsável:** CASF - Coordenação de Pagamento de Pessoal.
    * Telefone: (81) 2126-8673
    * E-mail: casf.progepe@ufpe.br

**4. Auxílio-Natalidade**

* **O que é?**  Benefício pago ao servidor em caso de nascimento de filho(a), inclusive natimorto.
* **Público Alvo:** Servidores ativos e aposentados do quadro permanente.
* **Requisitos:**  Comprovar o nascimento do(s) filho(s).
* **Documentação Necessária:**
    * Certidão de nascimento do(s) filho(s) (inclusive natimorto).
    * Cadastro do(s) filho(s) como dependente(s) no SouGov.
    * Se a solicitação for feita pelo pai: informar o CPF da mãe.
* **Base Legal:**
    * Art. 196 da Lei nº 8.112/1990.
    * Nota Técnica nº 1008/2010-CGNOR/DNOP/SRH/MP.
    * Lei nº 10.855/2004 (alterada pela Lei nº 11.907/2009).
    * Ofício nº 233/2003/SRH/MP.
    * Ofício-Circular nº 11/1996/SRH/MARE.
* **Informações Gerais:**
    * O auxílio é pago ao cônjuge/companheiro(a) servidor(a) se a parturiente não for servidora pública.
    * Em caso de falecimento da parturiente, o benefício vai para os sucessores.
    * Valor: R$ 718,58.
    * Parto múltiplo ou natimorto: acréscimo de 50% por nascituro.
    * O auxílio é isento de Imposto de Renda.
    * Prescrição: 5 anos após o nascimento.
    * Adoção: pode ser requerido com base na certidão de nascimento ou termo de guarda judicial.
* **Procedimento para Abertura do Processo:**
    * **Para o Servidor Pai:**
        * **Temporariamente:** Abrir processo no SIPAC:
            * Assunto: Auxílio natalidade.
            * CONARQ: 26.3.
            * Código do Setor Responsável: 11.07.16 (Divisão de Pagamentos).
        * **Em breve:** Solicitação pelo SouGov (módulo em adaptação).
    * **Para a Servidora Mãe:** A solicitação é incluída no processo de Licença Gestante/Adotante.
* **Setor Responsável:** DP - Divisão de Pagamento.
    * Telefone: (81) 2126-8177
    * E-mail: pagamento.progepe@ufpe.br

**5. Auxílio-Funeral**

* **O que é?**  Benefício pago aos familiares ou responsável pelo funeral do servidor falecido.
* **Público Alvo:** Familiares do servidor falecido.
* **Requisitos:**  Comprovar o falecimento do servidor e as despesas com o funeral.
* **Documentação Necessária:**
    * **Para Cônjuge/Companheiro(a)/Filho(a):**
        * Requerimento.
        * Certidão de óbito.
        * Documento de identificação do requerente.
        * Documento que comprove o parentesco.
        * Nota fiscal da funerária (em nome do requerente, especificando a despesa).
        * Comprovante de residência.
        * Comprovante de dados bancários.
    * **Demais Requerentes:**
        * Requerimento.
        * Certidão de óbito.
        * Documento de identificação do requerente.
        * Nota fiscal da funerária (em nome do requerente, especificando a despesa).
        * Comprovante de residência.
        * Comprovante de dados bancários.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 226 a 228, 241 e parágrafo único).
    * Orientação Normativa DRH/SAF nº 101/1991.
    * Memorando MEC/SA/SAA s/nº de 03/05/2000.
    * Ofício COGLE/SRH/MP nº 111/2002.
    * Acórdão TCU - 1ª Câmara nº 867/2003.
    * Acórdão TCU - Plenário nº 294/2004.
    * Nota Técnica nº 60/2011/CGNOR/DNOP/SRH/MP.
    * Instrução Normativa SGP/SEDGG/ME nº 101/2021.
* **Informações Gerais:**
    * **NÃO é solicitado pelo SouGov.**
    * Valor: equivalente a um mês da remuneração/provento do servidor no mês do falecimento (limitado ao teto legal), independentemente da causa da morte.
    * Família: cônjuge, filhos e pessoas que viviam às expensas do servidor (constantes no assentamento individual).
    * Irmãos são considerados terceiros.
    * Companheiro(a) em união estável é equiparado a cônjuge.
    * Prazo de pagamento: 48 horas após a entrada do requerimento no setor responsável.
    * Acumulação de cargos: o auxílio é pago apenas pelo cargo de maior remuneração.
    * Pagamento a terceiros: limitado ao valor das despesas comprovadas por notas fiscais (até o limite da remuneração/provento do servidor).
    * Prescrição: 5 anos.
* **Procedimento para Abertura do Processo:**
    1. Enviar a documentação digitalizada para o e-mail da SAEP (saep.progepe@ufpe.br).
    2. Após análise, o Protocolo (CPG) abre o processo.
* **Setor Responsável:** SAEP - Seção de Aposentadoria e Pensão.
    * Telefone: (81) 2126-8175 / 2126-8168
    * E-mail: saep.progepe@ufpe.br

**6. Auxílio-Alimentação**

* **O que é?** Benefício para cobrir despesas com alimentação.
* **Público Alvo:**
    * Servidores efetivos.
    * Servidores comissionados.
    * Empregados públicos.
    * Contratados temporários.
    * Vinculados à administração pública federal direta, autárquica e fundacional.
* **Requisitos:** Estar em efetivo exercício ou em afastamentos/licenças considerados efetivo exercício (Art. 102 da Lei 8.112/1990).
* **Documentação Necessária:**  Requerimento.
* **Base Legal:**
    * Lei nº 8.112/1990.
    * Lei nº 8.460/1992.
    * Decreto nº 3.887/2001.
    * Instrução Normativa SGP/SEDGG/ME nº 80/2021.
    * Portaria MGI nº 2.797/2024.
* **Informações Gerais:**
    * Pagamento antecipado e em dinheiro.
    * Em caso de acumulação de cargos, o auxílio é pago apenas para um dos vínculos.
    * Caráter indenizatório (Decreto nº 3.887/2001, Art. 2º).
    * Suspensão: em licenças/afastamentos não considerados efetivo exercício (observando a jornada de trabalho e a opção em caso de acumulação de cargos).
    * Não incide Imposto de Renda nem contribuição previdenciária (Lei nº 8.460/1992, Art. 22).
    * Desconto por dia não trabalhado: proporcional a 22 dias/mês.
    * Valor: R$ 1.000,00.
* **Procedimento para Abertura do Processo:**
    * SouGov.
    * Tutorial: https://www.gov.br/servidor/pt-br/acesso-a-informacao/faq/sou-gov.br/auxilio/alimentacao-refeicao
* **Setor Responsável:** DP - Divisão de Pagamento.
    * Telefone: (81) 2126-8177
    * E-mail: pagamento.progepe@ufpe.br

---Fim das Informações sobre Auxílios---

---Informações sobre Avaliação de Desempenho---

link do site: https://www.ufpe.br/manual-do-servidor/avaliacao-de-desempenho

A Avaliação de Desempenho é a sistemática de apreciação do desempenho do servidor no cargo e do seu potencial de desenvolvimento. Tem como objetivo não somente atender às exigências da lei, como também promover o crescimento profissional e integração institucional do servidor, de forma democrática e participativa. As Avaliações de desempenho são realizadas para: 

· Avaliação de desempenho para Estágio Probatório – Docente (ver item Estágio Probatório do Manual do servidor)

· Avaliação de desempenho para Estágio Probatório – TAE (ver item Estágio Probatório do Manual do servidor)

· Avaliação de desempenho para Progressão por Mérito Profissional – TAE: A Progressão por Mérito Profissional é a mudança para o padrão de vencimento imediatamente subseqüente, a cada 18 (dezoito) meses de efetivo exercício, desde que o servidor apresente resultado fixado em programa de avaliação de desempenho e tem o objetivo de promover o desenvolvimento do servidor na carreira.

Neste período de 18 (dezoito) meses, o servidor responderá, nos primeiros 09 (nove) meses, a avaliação denominada Tipo A, e nos últimos 09 (nove) meses, a avaliação denominada Tipo B, completando assim os 18 (dezoito) meses necessários para a Progressão por Mérito Profissional.

A Avaliação terá duas dimensões: Funcional e Gerencial, tendo cada uma delas um formulário de auto-avaliarão (AA) e um formulário de avaliação pela chefia imediata (AC).

Para progredir o servidor deverá alcançar desempenho satisfatório na avaliação (ver item Progressão por Mérito Profissional do Manual do servidor).

**Base Legal**

Avaliação Desempenho de Estágio Probatório/Docente: PORTARIA NORMATIVA Nº 06, DE 09 DE MAIO DE 2006
Avaliação de Desempenho de Estágio Probatório/TAE: PORTARIA NORMATIVA Nº 07, DE 09 DE MAIO DE 2006
Manual de Avaliação de Desempenho dos Servidores da UFPE em Estágio Probatório
Lei 4.965/66 Publicação dos Atos Relativos aos Servidores Públicos Civis do Poder Executivo
Regimento Interno CADS
Avaliação de Desempenho para Progressão por Mérito de Servidores TAE: RESOLUÇÃO Nº 06/2006

A relação dos servidores com pendência, servidores sendo avaliados, o cronograma anual de abertura do Siga para Avaliação de Desemprenho podem ser encontrados no site.

---Fim das Informações sobre Avaliação de Desempenho---

---Informações sobre Jornadas Especiais, Mudanças de Regime/Jornada e Averbação na UFPE---

## Guia Completo de Jornadas Especiais, Mudanças de Regime/Jornada e Averbação na UFPE

Este guia detalha os procedimentos para solicitar jornadas especiais, alterações de regime/jornada de trabalho e averbação de tempo de contribuição na UFPE, com base nos documentos fornecidos.

**1. Jornadas Especiais de Trabalho**

**1.1 Jornada de Treinamento Regularmente Instituído (TRI) - Educação Formal**

* **O que é?** Jornada especial para servidores técnico-administrativos em educação (TAE) participarem de ações de desenvolvimento de educação formal promovidas ou apoiadas pela UFPE.
* **Público Alvo:** Servidores técnico-administrativos da UFPE.
* **Requisitos:**
    * Ser TAE da UFPE.
    * Cumprir a TRI durante a jornada regular ou atividades de teletrabalho (sem compensação de horário).
    * Participar de ações de desenvolvimento (presenciais, online ou híbridas) de educação formal, amparadas pela Política de Formação Continuada e previstas no Plano de Desenvolvimento de Pessoas (PDP) da UFPE.
    * O horário/local da ação deve inviabilizar o cumprimento da jornada regular ou do teletrabalho (exceto afastamentos previstos nos Art. 95, 96 e 96-A da Lei 8.112/1990 e licença capacitação).
    * É possível participar de ações de curta/média duração e educação formal concomitantemente, se ambas ocorrerem no expediente e no interesse da administração.
    * Não estar em jornada flexibilizada.
    * Não possuir o nível de escolarização pleiteado.
    * Não exercer função comissionada ou de confiança dos níveis FG1, CD1, CD2, CD3 ou CD4 (dedicação integral - Resolução nº 10/2021 do Conselho de Administração da UFPE, Art. 15).
* **Documentação Necessária:**
    * Requerimento geral padrão (endereçado ao Reitor).
    * Declaração do servidor de que não possui o nível de escolarização pleiteado.
    * Cópia do último contracheque.
    * Declaração/despacho de concordância da chefia imediata (informando que o servidor não está em jornada flexibilizada).
    * Declaração da instituição de ensino (pública ou privada), especificando: curso, período de integralização, período acadêmico, turno, horário das aulas ou modalidade online.
    * Se aplicável: carta do orientador indicando a etapa do trabalho de conclusão de curso (monografia, dissertação, tese).
    * **Renovação Semestral:**
        * Declaração da instituição de ensino comprovando aproveitamento e frequência.
        * Comprovante de renovação de matrícula.
        * Cópia do último contracheque.
        * Declaração do servidor de que não possui o nível de escolarização pleiteado.
        * Se aplicável: declaração do orientador sobre a etapa do trabalho de conclusão de curso.
        * Despacho do servidor solicitando a renovação (com ciência da chefia imediata).
    * **Conclusão do Curso:** Declaração de conclusão de curso.
    * **Formatos:** Documentos em PDF. Cópias digitalizadas conferidas e assinadas eletronicamente no SIPAC por outro servidor (Lei 13.726/2018).
    * **Documentos Natodigitais:** Dispensam assinatura de outro servidor.
    * **Chefia Imediata:** Assina eletronicamente a declaração de concordância e o despacho de renovação.
* **Base Legal:**
    * Decreto nº 9.991/2019.
    * Instrução Normativa SGP-ENAP/SEDGG/ME nº 21/2021.
    * Resolução nº 17/2021 - Conselho de Administração da UFPE.
    * Resolução nº 10/2021 - Conselho de Administração da UFPE.
* **Informações Gerais:**
    * A TRI é concedida quando há incompatibilidade entre o horário da UFPE e o do curso, sem prejuízo do cargo e sem compensação de horário.
    * Válida apenas durante o período do curso, respeitando o prazo de integralização.
    * Deve ser comprovada a cada período letivo no mesmo processo.
    * Suspensão: durante as férias escolares (exceto se o servidor estiver elaborando o trabalho de conclusão de curso, com atestado da coordenação do curso).
    * Elaboração de trabalho de conclusão: liberação de 10h semanais, mesmo com disciplinas remanescentes.
    * Só é concedida para o nível de escolarização que o servidor ainda não possui.
    * Suspensão da TRI:
        * A pedido do servidor.
        * Trancamento total ou parcial do curso.
        * Reprovação em duas disciplinas.
        * Frequência/aproveitamento inferior a 60% das disciplinas (em cursos com matrícula por disciplina).
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: JORNADA DE TREINAMENTO REGULARMENTE INSTITUÍDO – EDUCAÇÃO FORMAL.
    * Classificação (CONARQ): 023.5 – CONCESSÕES.
    * Código do Setor Responsável: 11.07.47.
    * Encaminhar para a SAAPQ (Seção de Acompanhamento e Avaliação das Progressões e Qualificação).
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Telefone: (81) 2126-8671 / 8669
    * E-mail: saapq.cfc@ufpe.br

**1.2 Horário Especial para Servidor Estudante**

* **O que é?** Horário especial concedido ao servidor estudante para conciliar os horários da UFPE e do curso, com compensação de horas.
* **Público Alvo:** Servidores técnico-administrativos da UFPE.
* **Requisitos:**
    * Ser TAE da UFPE.
    * Ser estudante regularmente matriculado em curso de educação formal (presencial, híbrido ou online).
    * Haver incompatibilidade entre o horário da UFPE e o do curso.
    * Cumprir 30h semanais (redução de até 25% da jornada, mediante compensação).
    * Não exercer função comissionada ou de confiança dos níveis FG1, CD1, CD2, CD3 ou CD4 (dedicação integral - Resolução nº 10/2021 do Conselho de Administração da UFPE, Art. 15).
* **Documentação Necessária:**
    * Requerimento geral padrão (endereçado ao Reitor).
    * Declaração/despacho de concordância da chefia imediata.
    * Declaração do servidor com o horário alternativo de compensação (com concordância da chefia).
    * Declaração da instituição de ensino (pública ou privada), especificando: curso, período de integralização, período acadêmico, turno, horário das aulas ou modalidade online.
    * Se aplicável: carta do orientador indicando a etapa do trabalho de conclusão de curso (monografia, dissertação, tese).
    * **Renovação Semestral:**
        * Declaração da instituição de ensino comprovando aproveitamento e frequência.
        * Comprovante de renovação de matrícula.
        * Se aplicável: declaração do orientador sobre a etapa do trabalho de conclusão de curso.
        * Despacho do servidor solicitando a renovação (com ciência da chefia imediata).
    * **Conclusão do Curso:** Declaração de conclusão de curso.
    * **Formatos:** Documentos em PDF. Cópias digitalizadas conferidas e assinadas eletronicamente no SIPAC por outro servidor (Lei 13.726/2018).
    * **Documentos Natodigitais:** Dispensam assinatura de outro servidor.
    * **Chefia Imediata:** Assina eletronicamente a declaração de concordância e o despacho de renovação.
* **Base Legal:** 
    * Lei nº 8.112/1990.
    * Decreto nº 9.991/2019.
    * Instrução Normativa SGP-ENAP/SEDGG/ME nº 21/2021.
    * Resolução nº 17/2021 - Conselho de Administração da UFPE.
    * Resolução nº 10/2021 - Conselho de Administração da UFPE.
* **Informações Gerais:**
    * Só é concedido para cursos que representam a segunda formação do servidor no mesmo nível de escolarização.
    * Válido apenas durante o período do curso, respeitando o prazo de integralização.
    * O horário especial deve ser comprovado a cada período letivo.
    * Suspensão: durante as férias escolares (exceto se o servidor estiver elaborando o trabalho de conclusão de curso, com atestado da coordenação do curso).
    * Suspensão do Horário Especial:
        * A pedido do servidor.
        * Trancamento total ou parcial do curso.
        * Reprovação em duas disciplinas.
        * Frequência/aproveitamento inferior a 60% das disciplinas (em cursos com matrícula por disciplina).
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: HORÁRIO ESPECIAL PARA SERVIDOR ESTUDANTE.
    * Classificação (CONARQ): 023.5 – CONCESSÕES.
    * Código do Setor Responsável: 11.07.47.
    * Encaminhar para a SAAPQ (Seção de Acompanhamento e Avaliação das Progressões e Qualificação).
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Telefone: (81) 2126-8671 / 8669
    * E-mail: saapq.cfc@ufpe.br

**1.3 Horário Especial para Servidor com Deficiência (ou com cônjuge, filho ou dependente com deficiência)**

* **O que é?** Horário especial que permite ao servidor se ausentar do trabalho para cuidar de si mesmo ou de familiar com deficiência, sem compensação de horário.
* **Público Alvo:** Todos os servidores públicos ativos da UFPE.
* **Requisitos:** Comprovação de deficiência física (do servidor ou familiar) por junta médica oficial.
* **Base Legal:** Lei nº 8.112/1990 (Art. 98, § 2º e § 3º).
* **Documentação Necessária:**
    * **Laudo/Parecer Médico (restrito ou apresentado na perícia):**
        * Identificação do paciente.
        * Identificação do profissional emitente.
        * Assinatura e CRM do profissional.
        * CID ou diagnóstico.
    * Documentação comprobatória do parentesco e da dependência (se aplicável).
* **Procedimento:**  Agendamento de perícia médica no NASS (Núcleo de Atenção à Saúde do Servidor).
* **Setor Responsável:** NASS - Núcleo de Atenção à Saúde do Servidor.
    * Telefone:
        * (81) 2126-3944 (Recepção)
        * (81) 2126-7578 (Junta Médica)
        * (81) 2126-8582 (Coordenação)
    * E-mail: nass.unidadesiass@ufpe.br

**2. Mudança de Regime de Trabalho Docente**

* **O que é?**  Alteração do regime de trabalho (20h, 40h ou Dedicação Exclusiva) de professores do Magistério Superior ou do Ensino Básico, Técnico e Tecnológico.
* **Público Alvo:**
    * Professores do Magistério Superior.
    * Professores do Ensino Básico, Técnico e Tecnológico.
* **Requisitos:**
    * Aprovação do Plano de Trabalho pelo departamento e conselho do centro.
    * Autorização da DDP (Diretoria de Desenvolvimento de Pessoal), com base no Banco de Professor Equivalente.
    * Pareceres favoráveis da PROGRAD (Graduação), PROEXC (Extensão e Cultura), PROPESQI (Pesquisa e Inovação) e PROPG (Pós-Graduação).
    * Compatibilidade de horário com outros cargos/empregos (CACE - Coordenação de Acumulação de Cargos e Empregos).
    * Comprovação de que falta pelo menos 5 anos para a aposentadoria (SAEP - Seção de Aposentadoria e Pensão). Se faltar menos de 5 anos para a aposentadoria voluntária ou compulsória, a mudança para Dedicação Exclusiva é vedada.
    * Análise e parecer favorável da CPPD (Comissão Permanente de Pessoal Docente).
    * Autorização do Gabinete do Reitor.
    * Aguardar a publicação da portaria para iniciar a nova carga horária.
* **Base Legal:**
    * Lei nº 12.772/2012.
    * Resolução nº 07/1993 - CEPE.
    * Resolução nº 05/1997 - CEPE.
    * Banco de Professor Equivalente da UFPE.
* **Documentação Necessária:**
    * Requerimento + Curriculum Vitae + plano de trabalho + documentos para análise da CPPD.
    * Declaração de acúmulo de cargos.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: Alteração de carga horária (docente) / Aumento de carga horária / Redução de carga horária.
    * Assunto do Processo: 029.12 – Definição do horário de expediente.
* **Setor Responsável:** PROGEPE (Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida) e DAP (Diretoria de Administração de Pessoal).
    * PROGEPE:
        * Telefone: (81) 2126-8150
        * E-mail: progepe@ufpe.br
    * DAP:
        * Telefone: (81) 2126-8670
        * E-mail: dap.progepe@ufpe.br

**3. Mudança de Jornada de Trabalho de Técnico Administrativo**

* **O que é?**  Alteração da jornada de trabalho (40h, 30h ou 20h) de TAE, com remuneração proporcional e possibilidade de reversão à jornada integral.
* **Público Alvo:** Técnicos Administrativos em Educação da UFPE.
* **Requisitos:**
    * Atender aos Art. 20 e 21 da IN nº 02/2018 (redução ou reversão da jornada, com remuneração proporcional).
    * Autorização da chefia imediata.
    * Compatibilidade de horário com outros cargos/empregos (CACE).
    * Parecer favorável da PROGEPE.
    * Análise da SAEP (se o servidor estiver a menos de 5 anos da aposentadoria integral, a redução é vedada).
    * Autorização do Gabinete do Reitor.
    * Aguardar a publicação da portaria para iniciar a nova carga horária.
* **Documentação Necessária:**
    * Requerimento com a data de início desejada e anuência da chefia imediata.
    * Declaração de acúmulo de cargos.
* **Base Legal:**
    * Instrução Normativa nº 02/2018.
    * Quadro de Referência dos Servidores Técnicos Administrativos em Educação (QRSTA) da UFPE.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: Alteração de carga horária (técnico administrativo) / Aumento de carga horária / Redução de carga horária.
    * Assunto do Processo: 029.12 – Definição do horário de expediente.
* **Setor Responsável:** PROGEPE (Pró-Reitoria de Gestão de Pessoas e Qualidade de Vida) e DAP (Diretoria de Administração de Pessoal).
    * PROGEPE:
        * Telefone: (81) 2126-8150
        * E-mail: progepe@ufpe.br
    * DAP:
        * Telefone: (81) 2126-8670
        * E-mail: dap.progepe@ufpe.br

**4. Averbação de Tempo de Contribuição**

* **O que é?** Registro nos assentamentos funcionais do tempo de contribuição em outros vínculos (públicos ou privados), desde que não tenha sido usado para outro benefício previdenciário.
* **Público Alvo:** Servidores efetivos da UFPE.
* **Requisitos:**
    * Ter trabalhado em órgãos públicos, empresas privadas ou sociedades de economia mista.
    * O período a ser averbado não pode coincidir com o período do cargo atual ou com outros períodos já averbados.
    * Não ter averbado esse tempo em outro órgão público ou no INSS.
* **Documentação Necessária (por tipo de vínculo):**
    * **Iniciativa Privada:**
        * Certidão de Tempo de Contribuição do INSS (destinada à UFPE).
        * Se o período for a partir de julho de 1994: a certidão deve conter a relação dos salários de contribuição.
        * Se as funções não constarem na certidão: anexar cópias dos contratos registrados na Carteira de Trabalho ou outro documento comprobatório.
    * **Serviço Público:** 
        * Certidão de Tempo de Contribuição do órgão de origem (destinada à UFPE).
        * Se o período for a partir de julho de 1994: a certidão deve conter a relação das bases de cálculo de contribuição.
    * **Forças Armadas:**
        * Certidão de Tempo de Serviço Militar (destinada à UFPE).
        * Para serviço militar obrigatório: Certificado de Reservista com as datas de início e término.
    * **Aluno Aprendiz:** Certidão da instituição de ensino comprovando a atuação como aluno-aprendiz em escola pública profissional, com comprovação de retribuição pecuniária (alimentação, fardamento, material escolar ou renda por encomendas).
* **Base Legal:**
    * Lei nº 8.112/90 (Art. 100 e 103).
    * Lei nº 8.213/1991 (Art. 96).
    * Portaria MPS nº 1.467/2022.
    * Nota Informativa nº 165/2014/CGNOR/DENOP/SEGEP/MP.
    * Nota Informativa SEI nº 1/2019/CONOR/CGNAL/SRPPS/SPREV-ME.
    * Nota Técnica SEI nº 15790/2020/ME.
    * Nota Técnica SEI nº 12713/2021/ME.
    * Súmula nº 096 - TCU.
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: TEMPO DE SERVIÇO: AVERBACAO.
    * Classificação (CONARQ): 026.02 - CONTAGEM E AVERBACAO DE TEMPO DE SERVICO.
    * Anexar a documentação exigida.
    * Assinar os documentos eletronicamente (primeiro adicionar o servidor como assinante).
    * Cadastrar o servidor como interessado no processo (com a opção de notificação por e-mail).
    * Encaminhar o processo para a Seção de Informações Funcionais (código 11.07.21).
    * Confirmar os dados do processo e finalizar.
* **Setor Responsável:** CASF - Coordenação de Assentamento Funcional.
    * Telefone: (81) 2126-8673
    * E-mail: casf.progepe@ufpe.br

---Fim das Informações sobre Jornadas Especiais, Mudanças de Regime/Jornada e Averbação na UFPE---

---Informações sobre Bolsas, Declarações e Dispensa Eleitoral na UFPE---

## Guia Completo de Bolsas, Declarações e Dispensa Eleitoral na UFPE

Este guia apresenta, de forma consolidada, os procedimentos relacionados a bolsas para estudantes, emissão de declarações e dispensa por serviço eleitoral na UFPE, com base nos documentos fornecidos.

**1. Bolsas para Estudantes**

**1.1 Bolsas PROMULTI**

* **O que é?** Programa de Bolsas de Iniciação à Formação Multiprofissional (ProMulti), que visa proporcionar aos estudantes a experiência prática na administração pública.
* **Público Alvo:** Estudantes de graduação da UFPE.
* **Requisitos:**
    * Matrícula com, no mínimo, 180h por semestre.
    * Ter concluído, no mínimo, o primeiro período do curso.
    * Aprovação em, no mínimo, 50% das disciplinas do semestre anterior.
    * Não participar de outros programas acadêmicos remunerados (exceto bolsa permanência - PNAES - conforme Resolução nº 11/2021, Art. 12).
    * Aprovação em processo seletivo da unidade de lotação (via edital específico).
* **Documentação Necessária:** A lista de documentos e as orientações para o processo admissional são enviadas por e-mail às unidades de lotação após a seleção dos candidatos. A responsabilidade pela documentação é da unidade e segue as etapas do edital.
* **Base Legal:** Resolução nº 11/2021 - CONSAD UFPE.
* **Informações Gerais:**
    * A PROGEPE define o processo seletivo, o número de vagas e o edital.
    * Inscrições em fluxo contínuo pelo formulário online: https://www.ufpe.br/progepe/concursos (link "Gestão de Bolsas e Estágios").
    * Permanência máxima: 2 anos.
    * Recesso remunerado: 30 dias por ano (a unidade deve informar os dias à CPC).
    * Declaração de bolsista: solicitar pelo e-mail bolsas.progepe@ufpe.br.
    * A unidade de lotação é responsável pelas comunicações, intermediação de informações e verificação dos requisitos, monitorando a permanência máxima e as ocorrências dos bolsistas.
    * ProMulti x Estágio: são programas distintos, com regras, procedimentos e legislações diferentes.
* **Procedimento:**
    1. Inscrição pelo formulário online.
    2. Composição de lista de espera (conforme edital).
    3. Unidade com vaga disponível envia ofício (via SIPAC) para a CPC (código 11.07.10) informando os dados do bolsista anterior, o e-mail da unidade e solicitando novos candidatos.
    4. A CPC envia os dados dos candidatos (por ordem de classificação) para a unidade.
    5. A unidade entrevista e seleciona o candidato.
    6. A unidade solicita a documentação admissional e abre processo no SIPAC (encaminhado à CPC), seguindo as orientações recebidas por e-mail.
    7. A CPC registra a bolsa e integra o estudante à folha de pagamento.
    8. A unidade envia mensalmente a frequência do estudante à CPC.
* **Setor Responsável:** CPC – Coordenação de Provimentos e Concursos.
    * Telefone: (81) 2126-8676
    * E-mail: bolsas.progepe@ufpe.br

**1.2 Programa Institucional de Estágio**

* **O que é?**  Programa que oferece aos estudantes a oportunidade de complementar a formação acadêmica com experiência prática.
* **Público Alvo:** Estudantes de graduação da UFPE.
* **Requisitos:**
    * Matrícula e frequência em curso de graduação (a partir do 3º período, conforme o PPC do curso).
    * Disponibilidade de 4 horas diárias (20h semanais).
    * CRA igual ou superior a 50%.
    * Não participar de outros programas acadêmicos remunerados (exceto bolsa permanência - PNAES - conforme Resolução nº 11/2021, Art. 12).
    * Aprovação em processo seletivo da unidade de lotação (via edital específico).
* **Documentação Necessária:** A lista de documentos e as orientações para o processo admissional são enviadas por e-mail às unidades após a convocação dos candidatos aprovados. A responsabilidade pela documentação é da unidade e segue as etapas do edital.
* **Base Legal:**
    * Resolução nº 11/2021 - CONSAD UFPE.
    * Lei nº 11.788/2008 (Lei de Estágios).
* **Informações Gerais:**
    * A PROGEPE define o processo seletivo, o número de vagas e o edital.
    * As atividades do estagiário devem ter relação com a área de estudo, e a unidade deve ter um servidor da mesma área para supervisioná-lo.
    * Permanência máxima: 2 anos.
    * O programa abrange estágios obrigatórios e não obrigatórios (conforme o PPC do curso), com entrega de relatórios parciais e final.
    * Declaração de estagiário: solicitar pelo e-mail bolsas.progepe@ufpe.br.
    * A unidade de lotação é responsável pelas comunicações, intermediação de informações e verificação dos requisitos, monitorando a permanência máxima e as ocorrências dos estagiários.
    * ProMulti x Estágio: são programas distintos, com regras, procedimentos e legislações diferentes.
    * Recesso remunerado: 30 dias por ano (a unidade deve informar os dias à CPC).
* **Procedimento:**
    1. Inscrição pelo site da PROGEPE (https://www.ufpe.br/progepe/concursos), link "Gestão de Bolsas e Estágios".
    2. Seleção conforme edital (o resultado é publicado no site da PROGEPE).
    3. A unidade ofertante das vagas segue as instruções enviadas por e-mail, contata os candidatos aprovados, recebe a documentação admissional e abre processo no SIPAC (encaminhado à CPC).
    4. Para vagas remanescentes, a unidade entra em contato com o próximo candidato da fila de espera (respeitando a ordem de classificação e as cotas).
    5. A CPC registra o estudante e o integra à folha de pagamento.
    6. A unidade envia mensalmente a frequência do estudante à CPC.
    7. Em caso de rescisão, finalização, renovação ou outras ocorrências, a unidade deve instruir o processo admissional e encaminhá-lo à CPC.
* **Setor Responsável:** CPC – Coordenação de Provimentos e Concursos.
    * Telefone: (81) 2126-8676 / 7095
    * E-mail: bolsas.progepe@ufpe.br

**2. Declarações**

* **Tipos de Declarações:**
    * Vínculo: informações funcionais do servidor ativo.
    * Dependentes: informações dos dependentes cadastrados.
    * Professor Substituto: informações funcionais do ex-servidor.
    * Licenças e Afastamentos: licenças e afastamentos usufruídos ou não.
    * Não estar comprometido em processo disciplinar: informação sobre a existência de sindicância ou processo administrativo disciplinar.
    * Tempo de Contribuição: informações sobre o tempo de contribuição do servidor.
* **Público Alvo:** 
    * Servidores técnico-administrativos e docentes (efetivos e temporários).
    * Ex-servidores.
    * Dependentes.
* **Procedimento:**
    * **Servidores Ativos:**
        * Abrir processo no SIPAC com requerimento especificando o tipo de declaração desejada.
        * Encaminhar para a Seção de Informações Funcionais (código 11.07.21).
    * **Ex-Servidores e Dependentes:**
        * Enviar e-mail para protocolo@ufpe.br especificando o tipo de declaração desejada.
* **Tipos de Processo no SIPAC (para servidores ativos):**
    * Vínculo: DECLARACAO DE VINCULO.
    * Dependentes: DECLARACAO DE VINCULO.
    * Não estar comprometido em processo disciplinar: DECLARACAO REF. PROCESSO DISCIPLINAR.
    * Tempo de contribuição: DECLARACAO DE TEMPO DE CONTRIBUICAO.
    * Licenças e afastamentos: SOLICITA DECLARACAO.
    * Professor substituto: DECLARACAO DE VINCULO.
* **Classificação (CONARQ):** 991 - GESTAO DE COMUNICACOES EVENTUAIS (COMUNICADOS, INFORMES).
* **Etapas da Seção de Informações Funcionais (SIF):**
    1. Analisar a solicitação e a documentação.
    2. Consultar as informações do servidor no sistema.
    3. Emitir a declaração e inserir no processo.
    4. Encaminhar:
        * Para o setor do servidor ativo.
        * Por e-mail para o ex-servidor (o processo é arquivado após o envio).
* **Setor Responsável:** CASF - Coordenação de Assentamentos Funcionais.
    * E-mail: sif.progepe@ufpe.br
    * Telefone: (81) 2126-7084

**3. Dispensa por Serviço Eleitoral**

* **O que é?**  Dispensa do trabalho pelo dobro dos dias de serviços prestados à Justiça Eleitoral.
* **Público Alvo:**
    * Servidores técnico-administrativos e docentes ativos da UFPE.
    * Servidores comissionados sem vínculo efetivo.
    * Contratados temporários (incluindo professores substitutos).
* **Requisitos:** Comprovação da prestação de serviços à Justiça Eleitoral.
* **Documentação Necessária:**
    * Comprovante emitido pela Justiça Eleitoral.
    * Atestado da chefia com os dias de usufruto na folha de ponto.
* **Base Legal:**
    * Lei nº 8.868/1994 (Art. 15).
    * Lei nº 9.504/1997 (Art. 98).
    * Resolução TSE nº 22.747/2008.
* **Informações Gerais:**
    * É necessário apresentar atestado/certidão comprovando os serviços prestados (Lei nº 9.504/1997, Art. 98).
    * A participação em cursos para mesários também gera direito à dispensa, mediante comprovação. O servidor é liberado apenas durante o curso e o deslocamento, devendo cumprir o restante da jornada.
    * O benefício só é concedido se o servidor já tinha vínculo com a UFPE na época dos serviços eleitorais (Resolução TSE nº 22.747/2008, Art. 2º).
    * O benefício se estende a servidores efetivos, contratados e estagiários.
    * Não há prazo de prescrição para usar as folgas (mediante acordo com a chefia imediata).
    * As folgas podem ser usadas em conjunto ou separadamente (com registro no processo).
    * Servidores em férias ou repouso no dia do trabalho eleitoral também têm direito à dispensa.
    * Os dias de compensação não podem ser convertidos em dinheiro.
* **Procedimento:**
    1. O servidor encaminha processo no SIPAC para a Seção de Controle de Frequência (SCF), informando o direito à dispensa, anexando o comprovante da Justiça Eleitoral e um despacho com a quantidade de dias a que tem direito.
    2. A SCF registra a solicitação no processo e o devolve à unidade.
    3. A chefia imediata gerencia o uso das folgas.
    4. Após o uso de todas as folgas, o servidor devolve o processo para a SCF.
    * **Tipos de Processo no SIPAC:** Dias trabalhados/TRE.
    * **Classificação (CONARQ):** 023.5 - CONCESSOES.
* **Setor Responsável:** SCF - Seção de Controle de Frequencia (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**Observação:** Os documentos também contêm tutoriais detalhados sobre como abrir processos no SIPAC e registrar ocorrências no SIGRH. 

---Fim das Informações sobre Bolsas, Declarações e Dispensa Eleitoral na UFPE---

---Informações sobre Estágio Probatório para servidores da UFPE---

## Guia Completo do Estágio Probatório para Servidores da UFPE

Este guia detalha os procedimentos e informações relevantes sobre o Estágio Probatório para servidores técnico-administrativos e docentes da UFPE, com base nos documentos fornecidos.

**1. Estágio Probatório - TAE (Técnico-Administrativo em Educação)**

* **O que é?** Período de avaliação de 36 meses para servidores técnico-administrativos recém-nomeados para cargos efetivos.
* **Público Alvo:** Servidores técnico-administrativos aprovados em concurso público e nomeados para cargos efetivos.
* **Requisitos:**
    * Nomeação para cargo efetivo.
    * Entrada em exercício.
* **Documentação Necessária:**
    * **Responsabilidade da PROGEPE:**
        * Portaria Normativa nº 07/2006/UFPE.
        * Ficha cadastral do servidor.
        * Ficha de licenças e afastamentos.
    * **Responsabilidade do Servidor:**
        * Declaração de Acumulação de Cargos (https://abre.ai/declaracaodeacumulacaodecargos).
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 20, alterado pela Lei nº 9.527/1997; Art. 29, inciso I; Art. 34, parágrafo único, inciso I).
    * Instrução Normativa SAF nº 10/1994.
    * Decisão TCU nº 012/1995.
    * Ofício-Circular SRH/MARE nº 42/1995.
    * Emenda Constitucional nº 19/1998.
    * Parecer nº 1 da AGU/MC/2004.
    * Portaria Normativa nº 07/2006 - UFPE.
    * Nota Técnica nº 30/12-SEGEP/MP.
    * Portaria Normativa UFPE nº 05/2021 (Art. 11, inciso III).
* **Informações Gerais:**
    * A CADMP (Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal) abre o processo de avaliação no SIPAC com 32 meses de efetivo exercício e o encaminha à chefia imediata.
    * **Tipo de Processo no SIPAC:** Avaliação de Desempenho por Estágio Probatório.
    * **Classificação (CONARQ):** 022.61 – Cumprimento de Estágio Probatório, Homologação da Estabilidade.
    * **Código do Setor Responsável:** 11.07.06 (CADMP).
* **Procedimento:**
    1. O servidor inicia o estágio probatório na data da entrada em exercício e recebe orientação e treinamento.
    2. A chefia imediata acompanha sistematicamente o servidor durante o estágio.
    3. A avaliação ocorre após 32 meses de serviço.
    4. Fatores avaliados:
        * Assiduidade.
        * Disciplina.
        * Capacidade de iniciativa.
        * Produtividade.
        * Responsabilidade.
    5. Pontuação: de 0 a 10 para cada fator (excelente: 9-10; bom: 8-8,9; regular: 7-7,9; fraco: 6-6,9; insuficiente: abaixo de 5,9).
    6. **Habilitado:** pontuação total igual ou superior a 7,0.
    7. **Inabilitado:** avaliação "insuficiente" em assiduidade ou disciplina, ou em mais de um dos outros fatores (independentemente da pontuação total).
    8. A chefia imediata preenche a ficha de avaliação, atribuindo pontos e conceitos, e faz uma avaliação global. Após a ciência do servidor, o processo é encaminhado à CADMP.
    9. A CADMP confere a documentação e a envia para a CACE (Comissão de Acumulação de Cargos e Empregos), que analisa e devolve o processo para a CADMP, que o encaminha à Comissão de Avaliação de Desempenho.
    10. O servidor pode recorrer da avaliação em até 5 dias, enviando as razões da discordância por escrito à PROGEPE.
    11. A Comissão de Avaliação de Desempenho analisa a avaliação da unidade, emite parecer, analisa recursos e submete a avaliação ao Reitor para aprovação e homologação.
    12. Composição da Comissão de Avaliação de Desempenho: Pró-Reitor de Gestão de Pessoas e Qualidade de Vida (presidente), Diretor de Desenvolvimento de Pessoal, dois TAE indicados pelo órgão de classe e um servidor do setor de avaliação de desempenho.
    13. A estabilidade dos servidores habilitados é declarada no Boletim Oficial da UFPE.
    14. O tempo de estágio probatório é suspenso durante licenças e afastamentos (Nota Técnica nº 30/12-SEGEP/MP).
    15. O servidor em estágio probatório tem os mesmos benefícios e vantagens dos demais servidores, exceto os restritos a servidores estáveis por lei.
    16. Pode exercer cargos em comissão ou funções de direção, chefia ou assessoramento na UFPE.
    17. Pode ser cedido para cargos de Natureza Especial, DAS níveis 6, 5 e 4 ou equivalentes.
    18. O tempo de estágio probatório não é aproveitado em caso de aprovação em outro concurso público. O tempo de serviço em cargo com estabilidade, enquanto em estágio probatório em novo cargo, não conta para progressão/promoção no novo cargo.
    19. O servidor que pedir vacância para assumir outro cargo inacumulável pode desistir do estágio probatório e retornar ao cargo anterior. Se for inabilitado, também pode ser reconduzido ao cargo anterior.
    20. O servidor inabilitado é exonerado de ofício ou reconduzido ao cargo anterior, sem necessidade de inquérito administrativo.
* **Setor Responsável:** CADMP - Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal e SAD - Seção de Avaliação de Desempenho.
    * Telefone: (81) 2126-8174
    * E-mail: desempenho@ufpe.br

**2. Estágio Probatório - Docente**

* **O que é?** Período de avaliação de 36 meses para servidores docentes recém-nomeados para cargos efetivos.
* **Público Alvo:** Servidores docentes aprovados em concurso público e nomeados para cargos efetivos.
* **Requisitos:**
    * Nomeação para cargo efetivo.
    * Entrada em exercício.
* **Documentação Necessária:**
    * **Responsabilidade da PROGEPE:**
        * Portaria Normativa nº 06/2006/UFPE.
        * Ficha cadastral do servidor.
        * Ficha de licenças e afastamentos.
    * **Responsabilidade do Servidor:**
        * Curriculum Vitae ou Lattes (sem comprovação).
        * Plano de Trabalho ou PAAD/RAAD do período do estágio probatório.
        * Declaração de participação no treinamento de docentes recém-ingressos.
        * Extrato da ata do departamento que aprovou o plano de trabalho ou PAAD/RAAD.
        * Declaração de Acumulação de Cargos (https://abre.ai/declaracaodeacumulacaodecargos).
* **Base Legal:** Mesma base legal do Estágio Probatório para TAE.
* **Informações Gerais:**
    * A CADMP abre o processo de avaliação no SIPAC com 32 meses de efetivo exercício e o encaminha à chefia imediata.
    * **Tipo de Processo no SIPAC:** Avaliação de Desempenho por Estágio Probatório.
    * **Classificação (CONARQ):** 022.61 – Cumprimento de Estágio Probatório, Homologação da Estabilidade.
    * **Código do Setor Responsável:** 11.07.06 (CADMP).
* **Procedimento:**
    1. O servidor inicia o estágio probatório na data da entrada em exercício e recebe orientação e treinamento.
    2. A chefia imediata acompanha e avalia sistematicamente o servidor durante o estágio.
    3. A avaliação ocorre após 32 meses de serviço.
    4. Fatores avaliados:
        * Assiduidade.
        * Disciplina.
        * Capacidade de iniciativa.
        * Produtividade.
        * Responsabilidade.
        * Outras habilidades e características relevantes para o cargo.
    5. Pontuação: de 0 a 10 para cada fator (mesma escala do Estágio Probatório para TAE).
    6. **Habilitado:** pontuação total igual ou superior a 7,0.
    7. **Inabilitado:** avaliação "insuficiente" em assiduidade ou disciplina, ou em mais de um dos outros fatores (independentemente da pontuação total).
    8. A chefia do departamento informa ao docente os critérios, normas e padrões da avaliação.
    9. A avaliação é realizada por uma comissão setorial composta por:
        * Chefe do departamento (presidente).
        * Coordenador do curso de graduação com maior número de aulas ministradas pelo docente.
        * Coordenador do curso de pós-graduação com maior número de aulas ministradas pelo docente, ou docente eleito pelo departamento com categoria superior à do avaliado.
    10. O formulário de avaliação, assinado pela comissão setorial, é enviado à CADMP em até 5 dias úteis, com os documentos do servidor anexados.
    11. O docente pode recorrer da avaliação em até 5 dias úteis, enviando um requerimento ao presidente da Comissão Superior de Avaliação.
    12. A CADMP confere a documentação e a envia para a CACE, que a analisa e a devolve para a CADMP, que a encaminha à Comissão Superior.
    13. A Comissão Superior (composta pelos Pró-Reitores de Assuntos Acadêmicos, Pesquisa e Pós-Graduação, Gestão de Pessoas e Qualidade de Vida e Extensão) confirma ou modifica a avaliação, submetendo-a à CPPD (Comissão Permanente de Pessoal Docente) para análise e homologação.
    14. A CPPD homologa ou não o resultado em até 10 dias úteis e o encaminha ao Reitor para aprovação final.
    15. A estabilidade dos servidores habilitados é declarada no Boletim Oficial da UFPE.
    16. A contagem do tempo de estágio probatório é suspensa durante licenças e afastamentos (Nota Técnica nº 30/12-SEGEP/MP).
    17. O servidor em estágio probatório tem os mesmos benefícios e vantagens dos demais servidores, exceto os restritos a servidores estáveis por lei.
    18. Pode exercer cargos em comissão ou funções de direção, chefia ou assessoramento na UFPE.
    19. Pode ser cedido para cargos de Natureza Especial, DAS níveis 6, 5 e 4 ou equivalentes.
    20. O tempo de estágio probatório não é aproveitado em caso de aprovação em outro concurso público. O tempo de serviço em cargo com estabilidade, enquanto em estágio probatório em novo cargo, não conta para progressão/promoção no novo cargo.
    21. O servidor que pedir vacância para assumir outro cargo inacumulável pode desistir do estágio probatório e retornar ao cargo anterior. Se for inabilitado, também pode ser reconduzido ao cargo anterior.
    22. O servidor inabilitado é exonerado de ofício ou reconduzido ao cargo anterior, sem necessidade de inquérito administrativo.
* **Setor Responsável:** CADMP - Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal e SAD - Seção de Avaliação de Desempenho.
    * Telefone: (81) 2126-7148
    * E-mail: desempenho@ufpe.br

---Fim das Informações sobre Estágio Probatório para servidores da UFPE---

---Informações sobre identidade Funcional---

A PROGEPE realiza a entrega do 1º lote do Cartão de Identidade Funcional a partir de 15/01/2024, através da Central de Atendimento ao Servidor, no horário das 08:30h às 12h.

 

A retirada da CIF será feita exclusivamente pelo servidor, mediante apresentação de documento de identificação com foto.

 

Local para retirada:

CAS – Central de Atendimento ao Servidor

Sala 112 – Térreo da Reitoria

Horário para retirada: das 08:30h às 12h.

Contatos: Central.servidor@ufpe.br / Whatsapp: (81)99900-8610

Os servidores que receberam os CIFs com erro de impressão devem entrega-los quando forem retirar seus novos CIFs.

Consulte a lista dos servidores que constam nesse 1º lote:

Campus Recife

CAV

CAA

Favor atentar para a leitura do termo de responsabilidade.

Para os servidores lotados nos campi Vitória e Caruaru, a PROGEPE realizará a entrega em data programada a ser divulgada posteriormente. Antes disso, o servidor poderá optar pela retirada na CAS.

**Como solicitar**

A PROGEPE retoma a emissão do Cartão de Identidade Funcional (CIF), conforme Instrução Normativa nº 02/2023, publicada no Boletim Oficial nº 152, de 01/09/2023. O cartão será emitido para servidor em exercício na UFPE, se caracterizando como documento de identificação.

Deverão ser fornecidos os seguintes dados: nome civil completo; nome social (caso se aplique); matrícula Siape; foto no tamanho 3x4 (imagem digitalizada, colorida, tirada de frente, enquadrada e centralizada, fundo branco com iluminação uniforme, sem uso de acessórios); e assinatura digitalizada (em folha branca e caneta preta), conforme instruções apresentadas no Manual de Solicitação da Identidade Funcional.

Para solicitar o seu cartão de identidade funcional o servidor deverá preencher o FORMULÁRIO DE SOLICITAÇÃO DE CARTÃO DE IDENTIDADE FUNCIONAL (CIF).

O formulário estará disponível para preenchimento no período de 09/11/2023 até 20/11/2023. Novas datas serão disponibilizadas nos próximos meses.

O primeiro lote será entregue em Dezembro/2023 e o segundo lote será entregue em Janeiro/2024. A Progepe informará o período para a retirada dos Cartões!

Os servidores que tiveram seu pedido indeferido no primeiro lote, poderão realizar nova solicitação.

Em caso de dúvidas em relação ao processo de solicitação, o servidor pode consultar o MANUAL DE SOLICITAÇÃO DA IDENTIDADE FUNCIONAL ou entrar em contato com a Central de Atendimento ao Servidor: 

E-mail - centralservidor@ufpe.br

Telefone - 2126-8176 / 2126-8166

Whatsapp - 81 - 99900-8610

 

Antes de fazer a sua solicitação, favor conferir todas as exigências contidas no manual (especialmente nos arquivos de fotos). 

O não atendimento das exigências implicará no cancelamento da solicitação.

---Fim das Informações sobre identidade Funcional---


---Informações sobre Gratificações, Pagamentos e Férias na UFPE---

## Guia Completo sobre Gratificações, Pagamentos de Substituição e Férias na UFPE

Este guia apresenta informações detalhadas sobre a Gratificação por Encargo de Curso e Concurso (GECC), Gratificação Natalina, Pagamento por Substituição de Função e Férias na UFPE.

**1. Gratificação por Encargo de Curso e Concurso (GECC)**

* **O que é?**  Gratificação paga aos servidores que realizam atividades eventuais relacionadas a cursos, concursos ou seleções, como:
    * Instrução em cursos de formação, desenvolvimento ou treinamento.
    * Participação em bancas examinadoras, comissões de análise curricular, correção de provas, elaboração de questões ou julgamento de recursos.
    * Atividades logísticas de concursos públicos (planejamento, coordenação, supervisão, execução e avaliação).
    * Aplicação, fiscalização, avaliação ou supervisão de provas de vestibulares ou concursos.
* **Público Alvo:** Servidores públicos federais efetivos.
* **Requisitos:**
    * Desempenho eventual de atividades relacionadas à GECC.
    * Não estar em férias ou outro afastamento durante a atividade.
    * Autorização prévia da chefia imediata (Anexo V da Portaria UFPE nº 04/2022).
    * Limite de horas anuais disponível registrado no formulário próprio (Anexo III da Portaria UFPE nº 04/2022).
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 76-A).
    * Decreto nº 11.069/2022.
    * Portaria UFPE nº 04/2022.
* **Informações Gerais:**
    * A unidade responsável pela atividade deve abrir processo de previsão orçamentária (Portaria UFPE nº 04/2022).
    * A documentação do servidor deve ser enviada ao setor responsável pela atividade.
    * A Gerência de Curso e Concurso (GCC) da PROGEPE analisa os processos, executa os procedimentos financeiros e encaminha os pagamentos.
* **Setores Responsáveis (por tipo de atividade):**
    * **Cursos:** Coordenação de Formação Continuada - PROGEPE.
        * Telefone: (81) 2126-8669
        * E-mail: coordenacao.cfc@ufpe.com
    * **Concursos para Técnicos Administrativos:** Comissão Executora de Concurso - PROGEPE.
        * Telefone: (81) 2126-8171
        * E-mail: concurso2022@ufpe.br
    * **Concursos para Docentes:** Coordenação de Provimento Concurso - PROGEPE.
        * Telefone: (81) 2126-8042
        * E-mail: gcc.progepe@ufpe.com
        * Site: https://covest.com.br/cec/
    * **Seleção de Pós-Graduação:** Gerência Financeira - PROPG.
        * Telefone: (81) 2126-8144 (WhatsApp Business)
        * E-mail: financeiro.propg@ufpe.br
    * **Vestibulares e SISU:** Divisão de Finanças – PROGRAD.
        * Telefone: (81) 2126-8106
        * E-mail: financeiro.prograd@ufpe.br
    * **Pagamento da GECC:** GCC - Gerência de Cursos e Concursos.
        * Telefone: (81) 2126-8042
        * E-mail: gcc.progepe@ufpe.com

**2. Gratificação Natalina (13º Salário)**

* **O que é?** Gratificação paga aos servidores em dezembro, correspondente a 1/12 da remuneração por mês de exercício no ano.
* **Público Alvo:** Servidores ativos, aposentados e pensionistas.
* **Requisitos:** Ter exercido as funções por mais de 14 dias no ano civil.
* **Base Legal:**
    * Decreto-Lei nº 2.310/1986 (Art. 9º, § 2º).
    * Lei nº 8.112/1990 (Art. 63 a 66).
    * Lei nº 10.887/2004.
    * Nota Técnica nº 1093/2010/CGNOR/DENOP/SRH/MP.
* **Informações Gerais:**
    * O pagamento é feito integralmente em novembro, com desconto da antecipação de 50% paga em junho.
    * O servidor pode solicitar a antecipação de 50% nas férias.
    * Frações de 15 dias ou mais contam como mês integral.
    * A antecipação não é tributada.
    * Em caso de exoneração, o servidor recebe o valor proporcional aos meses trabalhados.
    * A Gratificação Natalina não é base de cálculo para outras vantagens.
    * Há incidência de contribuição previdenciária (PSS) e Imposto de Renda (IRRF) sobre o pagamento em novembro.
* **Setor Responsável:** CPP - Coordenação de Pagamento de Pessoal.
    * Telefone: (81) 2126-8035
    * E-mail: cpp.progepe@gmail.com

**3. Pagamento por Substituição de Função**

* **O que é?**  Retribuição paga ao servidor que substitui, de forma eventual, o titular de cargo em comissão, função comissionada ou função gratificada, durante afastamento ou impedimento legal.
* **Público Alvo:** Servidores ativos da UFPE.
* **Requisitos:** Ser designado previamente como substituto eventual em portaria publicada no Boletim de Serviços da UFPE.
* **Documentação Necessária:** Portaria de designação do substituto eventual.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 38 e 39, alterados pela Lei nº 9.527/1997).
    * Ofício-Circular SRH/MP nº 01/2005.
* **Informações Gerais:**
    * O pagamento é feito após o término do período de substituição (solicitações mensais para substituições superiores a 30 dias).
    * Titular e substituto não podem se afastar no mesmo período, exceto em casos excepcionais e justificados.
    * O valor da substituição integra a base de cálculo da Gratificação Natalina.
    * Não há pagamento por substituição em afastamentos do titular a serviço da UFPE.
    * São considerados afastamentos/impedimentos legais: férias, estudo/missão no exterior, ausências previstas no Art. 97 da Lei nº 8.112/1990, participação em treinamento, júri, licenças (maternidade/paternidade, médica, por acidente de trabalho, etc.), afastamento preventivo, participação em comissões de sindicância, processos administrativos disciplinares ou inquéritos.
    * **Substituições superiores a 30 dias:**
        * Nos primeiros 30 dias, há acumulação de funções, com o substituto recebendo a remuneração mais vantajosa (Lei nº 8.112/1990, Art. 38, § 1º).
        * Após 30 dias, o substituto exerce apenas as funções do cargo substituído.
    * O início do exercício da função substituída ocorre no primeiro dia útil após o fim do impedimento do titular (no máximo 30 dias após a publicação da designação).
* **Procedimento:**
    * Abrir processo no SIPAC.
    * **Tipo de Processo:** Pagamento de Substituto Eventual.
    * **Classificação (CONARQ):** 022.5 - SUBSTITUICAO.
    * **Código do Setor Responsável:** 11.07.26 (Seção de Funções de Confiança).
* **Setor Responsável:** SFC/CAPP – Seção de Funções de Confiança.
    * Telefone: (81) 2126-3170 / 2126-8660
    * E-mail: funcoes.progepe@ufpe.br

**4. Férias**

* **O que é?** Período de descanso remunerado a que o servidor tem direito.
* **Público Alvo:**
    * Servidores técnico-administrativos e docentes ativos da UFPE.
    * Servidores comissionados sem vínculo efetivo.
    * Contratados temporários (incluindo professores substitutos).
* **Requisitos:** Ter adquirido o direito ao gozo de férias (conforme normas da UFPE).
* **Documentação Necessária:**
    * Ofício de solicitação atestado pela chefia imediata.
    * Documentos comprobatórios, se necessário.
* **Base Legal:**
    * Lei nº 8.112/1990.
    * Orientação Normativa SRH nº 2/2011.
* **Informações Gerais:**
    * Duração: 30 dias por ano civil (parceláveis em até 3 etapas, a depender do interesse da administração).
    * As férias devem ser homologadas pela chefia imediata.
    * A remuneração inclui 1/3 de adicional.
    * As férias não podem coincidir com outros afastamentos ou licenças.
    * A homologação formaliza as férias para todos os efeitos legais, inclusive o pagamento.
    * O pagamento é feito na folha do mês anterior ao gozo das férias.
* **Procedimento:**
    * **Programação/Alteração de Férias pelo SouGov:**
        1. O servidor solicita a programação/alteração pelo SouGov.
        2. A chefia imediata homologa a solicitação.
        * **Tutorial:** O site da SCF contém um tutorial completo com imagens sobre como usar o SouGov para programar, visualizar e alterar as férias.
    * **Alteração/Interrupção de Férias em Casos Excepcionais (fora do prazo do SouGov):**
        1. O servidor abre processo no SIPAC e o encaminha à Seção de Controle de Frequência (SCF), solicitando a alteração/interrupção e anexando os documentos necessários.
        2. A chefia imediata atesta ou recusa a solicitação.
        3. A SCF realiza a alteração/interrupção e devolve o processo para ciência e arquivamento.
        * **Tipos de Processo no SIPAC:** FERIAS: ALTERACAO.
        * **Classificação (CONARQ):** 023.2 - FERIAS.
        * **Modelos de Texto para o Ofício:** É possível encontrar modelos no site da SCF.
* **Setor Responsável:** SCF - Seção de Controle de Frequencia (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

---Fim das Informações sobre Gratificações, Pagamentos de Substituição e Férias na UFPE---

---Informações sobre Incentivos, Isenções e Dependentes na UFPE---

## Guia Completo sobre Incentivos, Isenções e Dependentes na UFPE

Este guia consolida as informações sobre Incentivo à Qualificação, Isenção de Imposto de Renda e Inclusão de Dependentes para servidores da UFPE, com base nos documentos fornecidos.

**1. Incentivo à Qualificação - TAE**

* **O que é?** Percentual adicional sobre o vencimento concedido aos servidores técnico-administrativos que concluírem cursos de educação formal (nível médio, técnico, graduação ou pós-graduação) superiores à exigência do cargo.
* **Público Alvo:** Servidores técnico-administrativos da UFPE.
* **Requisitos:**
    * Ser TAE da UFPE.
    * Concluir curso de educação formal superior ao exigido para o cargo.
    * Abrir processo administrativo no SIPAC, com a documentação exigida.
* **Documentação Necessária:**
    * Requerimento de Incentivo à Qualificação (preenchido e assinado eletronicamente no SIPAC; servidores sem acesso ao SIPAC assinam manualmente).
    * Cópia do último contracheque.
    * Cópia do termo de posse (para servidores com área de atuação específica).
    * **Documentação por Nível de Escolaridade:**
        * **Ensino Médio Técnico:** Diploma + histórico escolar.
        * **Ensino Médio Profissionalizante:** Certificado de conclusão (com nome da instituição, nome e período do curso, declaração de conclusão e aprovação) + histórico escolar.
        * **Ensino Médio:** Declaração de conclusão (com nome da instituição, nome e período do curso, declaração de conclusão e aprovação) + histórico escolar.
        * **Graduação, Mestrado ou Doutorado:** 
            * Diploma (frente e verso).
            * **Comprovante Provisório (na ausência do diploma):**
                * Declaração da instituição de ensino (conclusão do curso, aprovação e ausência de pendências).
                * Comprovante de início de expedição do diploma.
        * **Especialização (Lato Sensu):**
            * Certificado de conclusão + histórico escolar (conforme Resolução nº 1/2018 do Conselho Nacional de Educação, Art. 8º).
            * **Comprovante Provisório (na ausência do certificado):**
                * Declaração da instituição de ensino (conclusão do curso, aprovação e ausência de pendências).
                * Comprovante de início de expedição do certificado.
                * Histórico escolar (conforme Resolução nº 1/2018 do CNE, Art. 8º).
    * **Formatos:** Documentos em PDF. Cópias digitalizadas conferidas e assinadas eletronicamente no SIPAC por outro servidor (Lei 13.726/2018). Documentos natodigitais dispensam assinatura de outro servidor.
    * Despacho com a descrição das atividades do servidor na unidade (assinado pela chefia e pelo servidor; não colocar apenas as atribuições do cargo).
* **Base Legal:**
    * Lei nº 8.112/1990.
    * Lei nº 11.091/2005.
    * Lei nº 12.772/2012.
    * Decreto nº 5.824/2006.
    * Decreto nº 5.825/2006.
    * Decreto nº 9.991/2019.
    * Resolução CNE/CES nº 1/2018.
    * Ofício Circular SEI nº 39/2019/GAB/SAA/SAA-MEC.
    * Ofício Circular CFC PROGEPE nº 27/2022.
    * Parecer nº 83/2022/PF-UFPE/PRF5/AGU.
* **Informações Gerais:**
    * A análise leva em conta a relação entre a área do curso e o ambiente de trabalho do servidor (Decreto nº 5.824/2006).
    * Os percentuais não são acumuláveis e são incorporados aos proventos de aposentadoria e pensão (desde que os certificados tenham sido obtidos até a data da aposentadoria ou pensão).
    * O cálculo é feito sobre o padrão de vencimento do servidor.
    * Cursos em áreas com relação direta ao trabalho do servidor têm percentuais maiores.
    * Ensino fundamental e médio contam como conhecimento relacionado diretamente ao trabalho, se excederem a escolaridade mínima do cargo.
    * Cursos no exterior: aceitos apenas com revalidação/reconhecimento no Brasil (o diploma deve ser apostilado por uma universidade brasileira).
    * O percentual do incentivo não pode ser reduzido (Decreto nº 5.824/2006, Art. 1º, § 8º).
    * O benefício é pago a partir da data de abertura do processo, se os requisitos forem cumpridos.
    * O servidor pode recorrer da decisão, reenviando o processo à SAAPQ com um despacho justificando o pedido e anexando os documentos que julgar necessários.
* **Tabela de Percentuais (Lei nº 11.091/2005, alterada pela Lei nº 12.772/2012):**
    | Nível de Escolaridade | Área de Conhecimento Direta | Área de Conhecimento Indireta |
    |---|---|---|
    | Ensino fundamental completo | 10% | - |
    | Ensino médio completo | 15% | - |
    | Ensino médio profissionalizante ou técnico | 20% | 10% |
    | Graduação | 25% | 15% |
    | Especialização (360h ou mais) | 30% | 20% |
    | Mestrado | 52% | 35% |
    | Doutorado | 75% | 50% |
* **Procedimento para Abertura do Processo:**
    * Sistema: SIPAC.
    * Tipo de Processo: Incentivo à Qualificação.
    * Classificação (CONARQ): 023.157 – TITULAÇÃO.
    * Código do Setor Responsável: 11.07.47.
    * Encaminhar para a SAAPQ.
    * Especificar o nível de escolaridade em "Assuntos Detalhados".
    * Abrir um único processo por nível de escolarização.
    * Classificar documentos com informações pessoais como "restritos".
    * Incluir o requerente como interessado (nome completo e SIAPE ou CPF).
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Telefone: (81) 2126-8671 / 8669
    * E-mail: saapq.cfc@ufpe.br

**2. Isenção de Imposto de Renda para Aposentados e Pensionistas**

* **O que é?** Exclusão do desconto de Imposto de Renda (IR) sobre os proventos de aposentados e pensionistas portadores de doenças graves ou ocupacionais.
* **Público Alvo:** Servidores aposentados e pensionistas da UFPE.
* **Requisitos:** Possuir doença grave ou ocupacional listada na legislação (Inciso XIV, Art. 6º da Lei nº 7.713/1988).
* **Documentação Necessária:**
    * Requerimento geral (presencial no Protocolo da UFPE ou por e-mail: protocolo@ufpe.br).
    * Laudo médico (apresentar na perícia).
* **Base Legal:**
    * Lei nº 7.713/1988.
    * Lei nº 8.541/1992.
* **Informações Gerais:**
    * O requerimento pode ser feito por e-mail (protocolo@ufpe.br), sem a necessidade de enviar o laudo médico inicialmente.
    * A perícia médica deve ser agendada no NASS.
    * A isenção só é aplicada após a perícia médica.
* **Procedimento:**
    1. Enviar e-mail para protocolo@ufpe.br com o requerimento (próprio ou geral).
    2. Agendar perícia médica no NASS.
* **Setor Responsável:** CAS - Central de Atendimento ao Servidor.
    * Telefone: (81) 2126-8176 / 2126-8166
    * E-mail: centralservidor@ufpe.br

**3. Inclusão de Dependentes**

* **O que é?**  Inclusão de dependentes no assentamento funcional do servidor para fins de dedução no Imposto de Renda.
* **Público Alvo:**
    * Servidores técnico-administrativos.
    * Servidores docentes (efetivos e temporários).
    * Aposentados.
* **Requisitos e Documentação (por tipo de dependente):**
    * **Cônjuge:** Certidão de casamento + CPF do dependente + declaração de dependência econômica (Anexo I do documento original).
    * **Companheiro(a):** 
        * Identidade e CPF do(a) companheiro(a).
        * Declaração de dependência econômica (Anexo I do documento original).
        * Cópia da certidão de casamento com averbação da separação/divórcio (se aplicável) ou de óbito.
        * Pelo menos dois dos documentos listados nos § 6º-A e § 8º do Art. 16 do Decreto nº 3.048/1999 (com redação do Decreto nº 10.410/2020), como: certidão de nascimento de filho em comum, certidão de casamento religioso, declaração de IR com o(a) companheiro(a) como dependente, disposições testamentárias, declaração perante tabelião, comprovante de residência em comum, comprovante de encargos domésticos, procuração ou fiança outorgada, conta bancária conjunta, registro em associação, etc.
    * **Pais, Padrasto e Madrasta (sem rendimentos tributáveis ou não superiores ao limite de isenção):** Certidão de nascimento do servidor + CPF do dependente + declaração de dependência econômica.
    * **Filhos e Enteados (até 21 anos):** Certidão de nascimento + CPF + comprovante de parentesco com o servidor (para enteados).
    * **Filhos e Enteados (entre 21 e 24 anos, estudantes de curso superior ou técnico):** Certidão de nascimento + CPF + comprovante de matrícula + comprovante de parentesco com o servidor (para enteados).
    * **Filho(a) ou Enteado(a) Incapacitado(a):** Certidão de nascimento + CPF + laudo médico + comprovante de parentesco com o servidor (para enteados).
    * **Irmão(ã), Neto(a) ou Bisneto(a) sob Guarda Judicial (até 22 anos ou incapacitado(a)):** Certidão de nascimento + CPF + termo de guarda judicial + laudo médico (se incapacitado(a)).
    * **Irmão(ã), Neto(a) ou Bisneto(a) sob Guarda Judicial (até 25 anos, estudantes de curso superior ou técnico):** Certidão de nascimento + CPF + termo de guarda judicial + comprovante de matrícula + laudo médico (se incapacitado(a)).
    * **Menor Pobre sob Guarda Judicial (até 21 anos):** Certidão de nascimento + CPF + termo de guarda judicial.
    * **Pessoa Absolutamente Incapaz sob Tutela ou Curatela:** Certidão de nascimento + CPF + termo de tutela ou curatela.
* **Observação:** Apenas um dos pais servidores públicos pode incluir o dependente.
* **Base Legal:**
    * Instrução Normativa RFB nº 1500/2014.
    * Decreto nº 3.048/1999.
* **Procedimento:**
    * **Opção 1: SouGov**
        1. Acessar o SouGov (aplicativo ou web).
        2. No menu "Solicitações", clicar em "Cadastro de Dependente".
        3. Editar o vínculo de dependentes já cadastrados (ícone "lápis") ou excluí-los (ícone "lixeira").
        4. Para incluir um novo dependente, clicar em "Cadastrar Novo Dependente".
        5. Preencher as 4 etapas:
            * Dados da Solicitação.
            * Benefícios (selecionar "Dedução Imposto de Renda").
            * Documentos.
            * Conferência.
        6. Clicar em "Solicitar" para enviar o requerimento à unidade de gestão de pessoas. O requerimento pode ser salvo como rascunho.
        * **Observação:** O tutorial no documento "INCLUSÃO DE DEPENDENTES" contém imagens ilustrativas.
    * **Opção 2: SIPAC**
        1. Abrir processo no SIPAC.
        2. Tipo de Processo: INCLUSÃO DE DEPENDENTE.
        3. Classificação (CONARQ): 023.185 - IMPOSTO DE RENDA.
        4. Anexar a documentação digitalizada em PDF/A.
        5. Assinar os documentos eletronicamente.
        6. Incluir o servidor como interessado (com a opção de notificação por e-mail).
        7. Encaminhar o processo para a Coordenação de Assentamento Funcional (código 11.07.19).
        8. Confirmar os dados e finalizar o processo.
* **Etapas da Coordenação de Assentamentos Funcionais (CASF):**
    1. Analisar a solicitação e a documentação.
    2. Se a documentação estiver incompleta, devolver o processo ao servidor e solicitar os ajustes.
    3. Se a documentação estiver completa, incluir o dependente no Assentamento Funcional Digital do Servidor.
* **Arquivamento:** A Seção de Arquivamento Pessoal (SAP) arquiva o processo na pasta funcional digital do servidor (se aberto pelo SIPAC).
* **Setor Responsável:** CASF - Coordenação de Assentamento Funcional.
    * Telefone: (81) 2126-8673
    * E-mail: casf.progepe@ufpe.br

**Observação:** Os documentos também contêm tutoriais detalhados sobre como usar o SouGov e o SIPAC. 

---Fim das Informações sobre Incentivos, Isenções e Dependentes na UFPE---

---Informações sobre Licenças Adotante, Gestante, Paternidade, Gala e Nojo---

## Guia Completo de Licenças para Servidores da UFPE

Este guia detalha os procedimentos para solicitar diferentes tipos de licenças na UFPE, com base nos documentos fornecidos.

**1. Licença Nojo (Falecimento)**

* **O que é?** Licença remunerada de 8 dias consecutivos em caso de falecimento de familiar.
* **Público Alvo:** Todos os servidores da UFPE.
* **Requisitos:** Falecimento de cônjuge, companheiro(a), pais, madrasta ou padrasto, filhos, enteados, menor sob guarda ou tutela e irmãos.
* **Documentação Necessária:**
    * Certidão de óbito.
    * Documento comprovando o vínculo familiar.
* **Base Legal:** Lei nº 8.112/1990 (Art. 97 e 102).
* **Informações Gerais:** A licença é concedida a partir da data do falecimento.
* **Procedimento:**
    * **Opção 1: SouGov**
        1. Acessar o SouGov (aplicativo ou web).
        2. Em "Solicitações", clicar em "Ver todas as opções" e depois em "Informar Afastamentos".
        3. Selecionar "Falecimento de familiar".
        4. Informar a data de início e clicar em "Avançar".
        5. Anexar a certidão de óbito, clicar em "Avançar" e confirmar a solicitação.
        * **Observação:** O documento "LICENÇA NOJO (Falecimento)" contém um tutorial com imagens ilustrativas do SouGov.
    * **Opção 2: SIPAC (se o SouGov não puder ser usado)**
        1. Abrir processo no SIPAC.
        2. Tipo de Processo: LICENÇA NOJO.
        3. Classificação (CONARQ): 023.3 - LICENÇA.
        4. Anexar a documentação digitalizada em PDF/A.
        5. Assinar os documentos eletronicamente.
        6. Incluir o servidor como interessado (com a opção de notificação por e-mail).
        7. Encaminhar o processo para a Seção de Controle de Frequência (código 11.07.24).
        8. Confirmar os dados e finalizar o processo.
* **Etapas da Seção de Controle de Frequência (SCF):**
    1. Analisar a solicitação e a documentação.
    2. Se a documentação estiver incompleta, indeferir ou devolver o processo ao servidor, solicitando os ajustes.
    3. Se a documentação estiver completa, autorizar a licença e registrar no sistema (SIGEPE).
* **Arquivamento:** A Seção de Arquivamento de Pessoal (SAP) arquiva o processo.
* **Setor Responsável:** SCF - Seção de Controle de Frequência (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**2. Licença Gala (Casamento)**

* **O que é?** Licença remunerada de 8 dias consecutivos em caso de casamento.
* **Público Alvo:** Todos os servidores da UFPE.
* **Requisitos:** Comprovação do casamento.
* **Documentação Necessária:** Certidão de casamento.
* **Base Legal:** Lei nº 8.112/1990 (Art. 97 e 102).
* **Informações Gerais:**
    * A licença é concedida a partir da data do casamento.
    * É recomendado avisar a chefia imediata com antecedência, se possível.
* **Procedimento:**
    * **Opção 1: SouGov**
        1. Acessar o SouGov (aplicativo ou web).
        2. Em "Solicitações", clicar em "Ver todas as opções" e depois em "Informar Afastamentos".
        3. Selecionar "Casamento".
        4. Informar a data de início e clicar em "Avançar".
        5. Anexar a certidão de casamento, clicar em "Avançar" e confirmar a solicitação.
        * **Observação:** O documento "LICENÇA GALA (Casamento)" contém um tutorial com imagens ilustrativas do SouGov.
    * **Opção 2: SIPAC (se o SouGov não puder ser usado)**
        1. Abrir processo no SIPAC.
        2. Tipo de Processo: LICENÇA GALA.
        3. Classificação (CONARQ): 023.3 - LICENÇA.
        4. Anexar a documentação digitalizada em PDF/A.
        5. Assinar os documentos eletronicamente.
        6. Incluir o servidor como interessado (com a opção de notificação por e-mail).
        7. Encaminhar o processo para a Seção de Controle de Frequência (código 11.07.24).
        8. Confirmar os dados e finalizar o processo.
* **Etapas da Seção de Controle de Frequência (SCF):**
    1. Analisar a solicitação e a documentação.
    2. Se a documentação estiver incompleta, indeferir ou devolver o processo ao servidor, solicitando os ajustes.
    3. Se a documentação estiver completa, autorizar a licença e registrar no sistema (SIGEPE).
* **Arquivamento:** A SAP arquiva o processo.
* **Setor Responsável:** SCF - Seção de Controle de Frequência (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**3. Licença Paternidade**

* **O que é?** Licença remunerada de 5 dias (prorrogável por mais 15 dias), contados da data do nascimento ou adoção.
* **Público Alvo:** Todos os servidores ativos (efetivos ou temporários) em efetivo exercício.
* **Requisitos:** Ser pai natural ou adotivo (com registro em cartório).
* **Documentação Necessária:** Certidão de nascimento, termo de adoção ou termo de guarda e responsabilidade.
* **Base Legal:**
    * Constituição Federal (Art. 227).
    * Lei nº 8.112/1990.
    * Lei nº 8.069/1990.
    * Decreto nº 8.737/2016.
    * Nota Técnica nº 16.295/2016-MP.
    * Nota Técnica nº 959/2017-MP.
* **Informações Gerais:**
    * A solicitação deve ser feita pelo SouGov (https://sougov.economia.gov.br/sougov/).
    * O servidor não pode trabalhar durante a licença, sob pena de cancelamento e registro de falta.
    * A licença é considerada efetivo exercício para todos os fins.
    * A adoção de adolescentes maiores de 12 anos não dá direito à licença.
    * A solicitação (incluindo a prorrogação) deve ser feita em até 2 dias úteis após o nascimento ou adoção.
* **Procedimento:**
    * **SouGov:**
        1. Acessar o SouGov (aplicativo ou web).
        2. Em "Solicitações", clicar em "Licença Gestante, Adotante e Paternidade".
        3. Selecionar "Licença Paternidade" e clicar em "Solicitar Licença".
        4. Informar a data do parto (o sistema inclui automaticamente a opção de prorrogação para 20 dias) e clicar em "Avançar".
        5. Clicar em "Solicito Cadastro de Dependente" e preencher os dados do dependente.
            * Para não solicitar a prorrogação, desmarcar a opção.
            * Para solicitar outros benefícios (auxílio-natalidade, acompanhamento de familiar, dedução de IR), clicar nos botões correspondentes e adicionar o dependente.
        6. Anexar a certidão de nascimento, clicar em "Avançar" e confirmar a solicitação.
        * **Observação:** O documento "LICENÇA PATERNIDADE" contém um tutorial com imagens ilustrativas do SouGov.
* **Etapas da Seção de Controle de Frequência (SCF):**
    1. Analisar a solicitação e a documentação.
    2. Se a documentação estiver incompleta, devolver o processo ao servidor, solicitando os ajustes.
    3. Se a documentação estiver completa, autorizar a licença e registrar no Assentamento Funcional Digital.
* **Setor Responsável:** SCF - Seção de Controle de Frequência.
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**4. Licença Gestante**

* **O que é?** Licença remunerada de 120 dias (prorrogável por mais 60 dias), concedida à servidora gestante.
* **Público Alvo:** Todas as servidoras da UFPE (técnico-administrativas, docentes, comissionadas, contratadas e professoras substitutas).
* **Requisitos:** Nascimento do bebê.
* **Documentação Necessária:** Certidão de nascimento.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 207, 209 e 210).
    * Decreto nº 6.690/2008.
    * Nota Informativa nº 759/2012/CGNOR/DENOP/SEGEP/MP.
* **Informações Gerais:**
    * **Início da Licença:**
        * **Na data do parto:** solicitar pelo SouGov, sem necessidade de perícia médica.
        * **Antes do parto (casos excepcionais):** agendar perícia no NASS (telefones: (81) 2126-3944, (81) 2126-8582 ou (81) 2126-7578).
    * **Prorrogação:**
        * Solicitar pelo SouGov.
        * A prorrogação é registrada após o término da licença inicial (o status no SouGov fica como "em análise" até o registro).
        * A servidora deve solicitar a prorrogação até o final do primeiro mês após o parto.
* **Procedimento:**
    * **Opção 1: SouGov**
        1. Acessar o SouGov (aplicativo ou web).
        2. Em "Solicitações", clicar em "Licença Gestante, Adotante e Paternidade".
        3. Selecionar "Licença Gestante" e clicar em "Solicitar Licença".
        4. Informar a data do parto (o sistema inclui automaticamente a opção de prorrogação para 180 dias) e clicar em "Avançar".
        5. Clicar em "Solicito Cadastro do Dependente" e preencher os dados do dependente.
            * Para solicitar outros benefícios (auxílio-natalidade, acompanhamento de familiar, dedução de IR), clicar nos botões correspondentes e adicionar o dependente.
        6. Anexar a certidão de nascimento, clicar em "Avançar" e confirmar a solicitação.
        * **Observação:** O documento "LICENÇA GESTANTE" contém um tutorial com imagens ilustrativas do SouGov.
* **Etapas da Seção de Controle de Frequência (SCF):**
    1. Buscar os processos de licença gestante no sistema.
    2. Analisar a solicitação e a documentação.
    3. Se a documentação estiver completa, autorizar a licença e registrar no Assentamento Funcional Digital.
    4. Se a documentação estiver incompleta, indeferir ou devolver o processo ao servidor, solicitando os ajustes.
* **Registro da Licença no Ponto Eletrônico:**
    * **TAE:**
        * Se a licença não constar automaticamente na frequência mensal, a servidora deve anexar a resposta da solicitação eletrônica ou o despacho do processo no ponto eletrônico, no último dia do mês.
        * Se a licença ainda não constar no SIGRH, registrar a ocorrência "Afastamentos Sigepe/Siass/Siape" no ponto eletrônico mensalmente até que a informação seja atualizada.
        * Se a informação já constar no ponto, apenas cientificar a chefia imediata.
    * **Docente:** Apresentar a resposta da solicitação eletrônica ou o despacho à chefia imediata para ciência.
* **Chefia Imediata:**
    * **TAE:** Homologar a licença no ponto eletrônico.
    * **Docente:** Tomar ciência da licença.
* **Setor Responsável:** SCF - Seção de Controle de Frequência.
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**5. Licença Adotante**

* **O que é?** Licença remunerada de 120 dias (prorrogável por mais 60 dias) concedida ao servidor que adotar ou obtiver guarda judicial de criança.
* **Público Alvo:** Servidores ativos permanentes da UFPE.
* **Requisitos:** Adoção ou guarda judicial de criança.
* **Documentação Necessária:** Certidão de nascimento, termo de adoção ou termo de guarda.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 210).
    * Decreto nº 6.690/2008.
    * Nota Técnica nº 150/2014/CGNOR/DENOP/SEGEP/MP.
    * Nota Técnica nº 162/2014/DENOP/SEGEP/MP.
    * Ofício Circular nº 14/2017-MP.
* **Informações Gerais:**
    * A solicitação deve ser feita pelo SouGov (https://sougov.economia.gov.br/sougov/).
    * A licença deve ser usufruída imediatamente após a adoção.
    * A prorrogação deve ser solicitada até o final do primeiro mês após a adoção.
    * A licença pode ser concedida a qualquer um dos adotantes, independentemente do gênero.
    * **Casal Homoafetivo (ambos servidores públicos federais):**
        * A licença adotante é concedida a apenas um dos adotantes. O outro adotante recebe licença paternidade (Lei nº 8.112/1990, Art. 208).
        * O adotante que solicitar a licença adotante deve declarar que o(a) companheiro(a) não a solicitou.
    * **Casal Heterosexual (ambos servidores públicos federais):** A licença adotante é concedida preferencialmente à mulher.
* **Procedimento:**
    * **Opção 1: SouGov**
        1. Acessar o SouGov (aplicativo ou web).
        2. Em "Solicitações", clicar em "Licença Gestante, Adotante e Paternidade".
        3. Selecionar "Licença Adotante" e clicar em "Solicitar Licença".
        4. Informar a data da adoção (o sistema inclui automaticamente a opção de prorrogação para 180 dias) e clicar em "Avançar".
        5. Clicar em "Solicito Cadastro do Dependente" e preencher os dados do dependente.
            * Para solicitar outros benefícios (auxílio-natalidade, acompanhamento de familiar, dedução de IR), clicar nos botões correspondentes e adicionar o dependente.
        6. Anexar a certidão de nascimento/termo de adoção, clicar em "Avançar" e confirmar a solicitação.
* **Etapas da Seção de Controle de Frequência (SCF):**
    1. Buscar os processos de licença adotante no sistema.
    2. Analisar a solicitação e a documentação.
    3. Se a documentação estiver completa, registrar a licença no sistema (SIGEPE).
    4. Se a documentação estiver incompleta, indeferir ou devolver o processo ao servidor, solicitando os ajustes.
* **Registro da Licença no Ponto Eletrônico:**
    * **TAE:**
        * Se a licença não constar automaticamente na frequência mensal, a servidora deve anexar a resposta da solicitação eletrônica ou o despacho do processo no ponto eletrônico, no último dia do mês.
        * Se a licença ainda não constar no SIGRH, registrar a ocorrência "Afastamentos Sigepe/Siass/Siape" no ponto eletrônico mensalmente até que a informação seja atualizada.
        * Se a informação já constar no ponto, apenas cientificar a chefia imediata.
    * **Docente:** Apresentar a resposta da solicitação eletrônica ou o despacho à chefia imediata para ciência.
* **Chefia Imediata:**
    * **TAE:** Homologar a licença no ponto eletrônico.
    * **Docente:** Tomar ciência da licença.
* **Setor Responsável:** SCF - Seção de Controle de Frequência.
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br


---Fim das Informações sobre Licenças Adotante, Gestante, Paternidade, Gala e Nojo---


---Informações sobre Licenças Para Acompanhar Conjuge, Atividade Política, Capacitação, Tratamento de Saúde, Prêmio e Interesse particular ---

## Guia Completo de Licenças para Servidores da UFPE (Parte 2)

Este guia detalha os procedimentos para solicitar diferentes tipos de licenças na UFPE, continuando a partir do guia anterior.

**6. Licença Prêmio por Assiduidade (LPA)**

* **O que é?** Licença remunerada de até três meses, concedida como prêmio por assiduidade a cada cinco anos ininterruptos de exercício.
* **Público Alvo:** Servidores ativos permanentes da UFPE.
* **Requisitos:**
    * Ter completado cinco anos de efetivo exercício até 15/10/1996 (conforme Lei nº 8.112/1990, Art. 15 e 102, e Instrução Normativa nº 08/1993).
    * O tempo de serviço em outros órgãos federais (União, autarquias e fundações) é considerado.
* **Procedimento:**
    * Fazer requerimento com manifestação e assinatura da chefia imediata.
    * Abrir processo no SIPAC (ver tutorial no documento "LICENÇA PRÊMIO POR ASSIDUIDADE").
    * Solicitar a licença com pelo menos 60 dias de antecedência (Deliberação CODEP nº 11/2000, Art. 10).
    * **Docentes:** A licença é concedida pelo departamento, e a ata da reunião deve constar no processo (Deliberação CODEP nº 11/2000, Art. 4º).
* **Informações Gerais:**
    * O tempo de LPA conta em dobro para Abono de Permanência/Aposentadoria, se o servidor tiver completado o tempo para aposentadoria até a publicação da Emenda Constitucional nº 20 (Lei nº 9.527/1997, Art. 7º, e Orientação Normativa nº 01/1999).
    * Em caso de acumulação de cargos na UFPE, a licença é concedida para cada cargo.
    * A licença pode ser gozada em um único período ou em três períodos (mínimo de 30 dias cada - Orientação Normativa nº 04/1994).
    * A interrupção da licença só é possível em casos de calamidade pública, comoção interna, convocação para júri/serviço militar/eleitoral ou interesse da administração (Instrução Normativa nº 04/1994).
    * Servidores em cargos em comissão ou funções de confiança recebem apenas a remuneração do cargo efetivo durante a licença (Instrução Normativa nº 08/1993 e Ofício-Circular nº 69/1995).
    * As gratificações por insalubridade, periculosidade e raios X são suspensas durante a licença (Lei nº 8.112/1990, Art. 68, § 2º).
    * Servidores com dois períodos de férias a gozar (sem programação) não podem gozar da LPA no segundo semestre (Deliberação CODEP nº 11/2000, Art. 13).
* **Base Legal:**
    * Decreto nº 38.204/1955 (alterado pelo Decreto nº 50.408/1961).
    * Lei nº 8.112/1990 (Art. 87, 97, 102, VIII, "e", 245).
    * Parecer nº 526/MARE/1992.
    * Orientações Normativas DRH/SAF nº 26/1990, 34/1990, 36/1990, 38/1990, 40/1991 e 94/1991.
    * Parecer DRH/SAF nº 162/1991.
    * Instrução Normativa SAF nº 08/1993.
    * Instrução Normativa SAF nº 04/1994.
    * Instrução Normativa nº 12/MARE/1996.
    * Lei nº 9.527/1997.
    * Orientação Normativa nº 01/1999 - DENOR/SEAP.
    * Ofício Circular nº 69/MARE/1995.
    * Ofício Circular nº 43/MARE/1996.
    * Emenda Constitucional nº 20/1998.
    * Deliberação nº 11/2000 – CODEP/FURG.
* **Setor Responsável:** CASF - Coordenação de Assentamentos Funcionais.
    * Telefone: (81) 2126-7084
    * E-mail: sif.progepe@ufpe.br

**7. Licença por Motivo de Pessoa na Família**

* **O que é?** Licença concedida em caso de doença do cônjuge, companheiro(a), pais, filhos, padrasto ou madrasta, enteado ou dependente que viva às expensas do servidor (e conste no assentamento funcional), mediante perícia médica.
* **Público Alvo:** Servidores públicos federais ativos e comissionados da UFPE.
* **Requisitos:**
    * O dependente deve estar cadastrado no SIGRH e no SIAPE.
    * A assistência do servidor deve ser indispensável e incompatível com o trabalho (mesmo com compensação de horário).
* **Documentação Necessária:**
    * Número de SIAPE e CPF do servidor.
    * Documento comprovando o vínculo familiar ou a dependência.
    * Atestado médico ou odontológico com:
        * Identificação do servidor e do profissional emitente.
        * Assinatura e registro no conselho de classe (CRM ou CRO).
        * CID ou diagnóstico.
        * Período recomendado de afastamento (não pode ser indeterminado).
    * Justificativa da necessidade do acompanhamento, com identificação do servidor e do familiar.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 83).
    * Manual de Perícia Oficial em Saúde do Servidor Público Federal (2017).
    * Decreto nº 7.003/2009.
* **Informações Gerais:**
    * A licença só é concedida se a assistência for indispensável e incompatível com o trabalho.
    * Duração:
        * **Remunerada:** até 60 dias (consecutivos ou não), em 12 meses.
        * **Não remunerada:** até 90 dias (consecutivos ou não), após o período remunerado.
    * O período de 12 meses conta a partir do deferimento da primeira licença.
    * A soma das licenças (remunerada + não remunerada) não pode ultrapassar 5 meses (incluindo prorrogações).
    * É possível solicitar perícia domiciliar, se justificado pelo médico assistente.
* **Procedimento:**
    * Usar a ferramenta "Atestado Web" (disponível no aplicativo ou site do SouGov).
    * **Tutorial Atestado Web:** https://www.ufpe.br/documents/3783589/0/MANUAL_ATESTADO+WEB+-+VF.pdf/c1d1cf22-506a-42f0-ae8d-4ad9096273b1
    * **Perguntas Frequentes sobre Perícias:** https://drive.google.com/file/d/1HL8Jz7X0EhxZjeHVI8jLkNFguBCYQmTx/view?usp=sharing
* **Setor Responsável:** NASS - Núcleo de Atenção à Saúde do Servidor (www.ufpe.br/nass).
    * Telefone:
        * (81) 2126-3944 / 2126-7578 (Recepção)
        * (81) 2126-8582 (Coordenação)
    * E-mail: nass.unidadesiass@ufpe.br

**8. Licença para Tratar de Interesse Particular**

* **O que é?** Licença não remunerada concedida a servidores estáveis, mediante análise do interesse da administração.
* **Público Alvo:** Servidores estáveis da UFPE.
* **Requisitos:**
    * Ter concluído o estágio probatório.
    * Preencher o formulário (Anexo III da IN nº 34/2021).
* **Documentação Necessária:** Formulário de solicitação de licença (Anexo III da Instrução Normativa SGP/SEDGG/ME nº 34/2021).
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 81 e 91).
    * Resolução nº 5/2018 - CEPE.
    * Instrução Normativa SGP/SEDGG/ME nº 34/2021.
* **Informações Gerais:**
    * Duração: 12 meses, prorrogável por mais dois períodos (total máximo de 3 anos).
    * A licença pode ser interrompida a qualquer tempo (a pedido do servidor ou por necessidade do serviço).
    * A solicitação deve ser feita com até 60 dias de antecedência.
    * O período da licença não conta para nenhum fim (exceto para aposentadoria, se houver contribuição previdenciária).
    * O servidor pode contribuir para o Plano de Seguridade Social (PSS) durante a licença.
    * No primeiro dia útil após o término da licença, o servidor deve preencher o Termo de Apresentação (Anexo II da Resolução nº 5/2018) e enviá-lo à Seção de Movimentação de Pessoal.
    * O servidor tem direito às férias proporcionais ao período trabalhado no ano de retorno.
    * Servidores que solicitarem a licença para trabalhar no setor privado devem observar a Lei nº 12.813/2013 (conflito de interesses).
    * Não é permitida a concessão retroativa da licença.
* **Procedimento:**
    * Abrir processo no SIPAC.
    * Tipo de Processo: LICENCA PARA TRATAR DE INTERESSE PARTICULAR.
    * Classificação (CONARQ): 023.3 – LICENCAS.
    * Código do Setor Responsável: 11.07.30.
* **Setor Responsável:** SMP - Seção de Movimentação de Pessoal.
    * Telefone: (81) 2126-8165
    * E-mail: smp.progepe@ufpe.br

**9. Licença para Tratamento de Saúde**

* **O que é?** Licença remunerada concedida ao servidor mediante avaliação da perícia médica oficial.
* **Público Alvo:** Todos os servidores públicos federais da UFPE.
* **Requisitos:**
    * O servidor deve estar doente.
    * Ter acompanhamento médico ou odontológico.
* **Documentação Necessária:**
    * Número de SIAPE e CPF do servidor.
    * Atestado médico ou odontológico com:
        * Identificação do servidor e do profissional emitente.
        * Assinatura e registro no conselho de classe (CRM ou CRO).
        * CID ou diagnóstico.
        * Período recomendado de afastamento (não pode ser indeterminado).
* **Base Legal:** Lei nº 8.112/1990 (Art. 202, 203 e 204).
* **Procedimento:**
    * Usar a ferramenta "Atestado Web" (disponível no aplicativo ou site do SouGov).
    * **Tutorial Atestado Web:** https://www.ufpe.br/documents/3783589/0/MANUAL_ATESTADO+WEB+-+VF.pdf/c1d1cf22-506a-42f0-ae8d-4ad9096273b1
    * **Perguntas Frequentes sobre Perícias:** https://drive.google.com/file/d/1HL8Jz7X0EhxZjeHVI8jLkNFguBCYQmTx/view?usp=sharing
* **Setor Responsável:** NASS - Núcleo de Atenção à Saúde do Servidor (www.ufpe.br/nass).
    * Telefone:
        * (81) 2126-3944 / 2126-7578 (Recepção)
        * (81) 2126-8582 (Coordenação)
    * E-mail: nass.unidadesiass@ufpe.br

**10. Licença para Capacitação - TAE**

* **O que é?** Licença remunerada de até 3 meses, concedida a cada 5 anos de efetivo exercício para ações de capacitação profissional.
* **Público Alvo:** Servidores técnico-administrativos da UFPE que completaram 5 anos de efetivo exercício.
* **Requisitos:**
    * Completar 5 anos de efetivo exercício.
    * Obter autorização da chefia imediata.
    * A ação deve ser relacionada ao cargo/função/ambiente organizacional.
    * A carga horária mínima da ação deve ser de 30h semanais.
    * A licença não pode coincidir com férias ou outros afastamentos.
    * Estar dentro do limite de 2% dos servidores da UFPE em licença capacitação simultaneamente.
    * O horário da ação deve ser incompatível com a jornada de trabalho na UFPE.
* **Documentação Necessária:**
    * Requerimento.
    * Documento do SouGov com a programação de férias do servidor.
    * Termo de compromisso.
    * Plano de estudo.
    * Autorização da chefia imediata.
    * Carta de aceite ou declaração de vínculo com a instituição promotora.
    * Se aplicável: comprovante de solicitação de exoneração/dispensa de cargo em comissão ou função de confiança (para afastamentos superiores a 30 dias), ou declaração de que não exerce essas funções.
    * Documento da instituição promotora comprovando a carga horária mínima de 30h semanais. Para elaboração de monografia/dissertação/tese, o orientador deve se pronunciar sobre a necessidade de carga horária superior a 30h.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 87).
    * Decreto nº 9.991/2019 (alterado pelo Decreto nº 10.506/2020).
    * Instrução Normativa nº 21/2021.
    * Resolução nº 13/2019 - CONSUNI/UFPE.
* **Informações Gerais:**
    * A licença pode ser parcelada em até 6 períodos (mínimo de 15 dias cada, totalizando no máximo 90 dias).
    * O período da licença é considerado efetivo exercício para fins de aposentadoria.
    * Os períodos não são acumuláveis e devem ser usados antes do próximo quinquênio.
    * Deve haver um intervalo mínimo de 60 dias entre as parcelas da licença.
    * O tempo de faltas não justificadas, pena privativa de liberdade (crime comum), licença médica superior a 2 anos (exceto por acidente de trabalho ou doenças previstas em lei), licença para tratar de interesse particular e licença para acompanhar cônjuge ou por doença em pessoa da família (sem remuneração) não conta para o cálculo do quinquênio.
    * O servidor deve anexar o relatório circunstanciado e os documentos de conclusão da ação ao processo original em até 30 dias após o término da licença, encaminhando-o à SAAPQ com um despacho assinado pelo servidor e com ciência da chefia.
* **Procedimento:**
    * Abrir processo no SIPAC.
    * Assunto: Licença Capacitação.
    * Classificação (CONARQ): 023.3.
    * Código do Setor Responsável: 11.07.47 (SAAPQ).
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação/CFC-DDP (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8671 / 2126-8669
    * E-mail: saapq.cfc@ufpe.br

**11. Licença para Capacitação - Docentes**

* **O que é?** Licença remunerada de até 3 meses, concedida a cada 5 anos de efetivo exercício para ações de capacitação profissional.
* **Público Alvo:** Servidores docentes da UFPE que completaram 5 anos de efetivo exercício.
* **Requisitos:** Os mesmos requisitos da Licença para Capacitação para TAE.
* **Documentação Necessária:**
    * Requerimento.
    * Documento do SouGov com a programação de férias do servidor.
    * Termo de compromisso.
    * Plano de estudo.
    * Documento de aprovação do conselho do centro e do departamento.
    * Carta de aceite ou declaração de vínculo com a instituição promotora.
    * Últimos PAAD e RAAD homologados.
    * Indicação do professor substituto.
    * Se aplicável: comprovante de solicitação de exoneração/dispensa de cargo em comissão ou função de confiança (para afastamentos superiores a 30 dias), ou declaração de que não exerce essas funções.
    * Documento da instituição promotora comprovando a carga horária mínima de 30h semanais. Para elaboração de monografia/dissertação/tese, o orientador deve se pronunciar sobre a necessidade de carga horária superior a 30h.
* **Base Legal:** A mesma base legal da Licença para Capacitação para TAE.
* **Informações Gerais:** As mesmas informações gerais da Licença para Capacitação para TAE.
* **Procedimento:**
    * Abrir processo no SIPAC.
    * Assunto: Licença Capacitação.
    * Classificação (CONARQ): 023.3.
    * Código do Setor Responsável: 11.07.47 (SAAPQ).
* **Setor Responsável:** SAAPQ - Seção de Acompanhamento e Avaliação das Progressões e Qualificação/CFC-DDP (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8671 / 2126-8669
    * E-mail: saapq.cfc@ufpe.br

**12. Licença para Atividade Política**

* **O que é?** Licença concedida para candidatura a cargo eletivo.
    * **Sem remuneração:** do período entre a escolha em convenção partidária e a véspera do registro da candidatura.
    * **Com remuneração:** do registro da candidatura até o 10º dia após a eleição.
* **Público Alvo:** Servidores da UFPE que desejam se candidatar a cargo eletivo.
* **Requisitos:**
    * **Sem remuneração:** interesse em se candidatar.
    * **Com remuneração:** ser candidato(a).
* **Documentação Necessária:**
    * Formulário de Licença para Atividade Política (IN nº 34/2021).
    * Ata da convenção partidária.
    * **Licença com remuneração:** certidão da Justiça Eleitoral comprovando o deferimento do registro da candidatura.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 20, § 5º, e Art. 86).
    * Lei Complementar nº 64/1990 (Art. 1º, II).
    * Nota Técnica Consolidada nº 01/2014/CGNOR/DENOP/SEGEP/MP.
    * Nota Informativa SEI nº 7/2019/DIDLA/CGDIM/DEPRO/SGP/SEDGG-ME.
    * Parecer nº 343/2016/PFG/PF/UFES.
    * Site do TSE: https://www.tse.jus.br/.
* **Informações Gerais:**
    * Servidores que exercem cargos de direção, chefia, assessoramento, arrecadação ou fiscalização na mesma localidade da candidatura são afastados sem remuneração a partir do registro da candidatura (Lei nº 8.112/1990, Art. 86, § 1º, e Orientação Consultiva nº 38/1998/DENOR/SRH/MARE).
    * A licença com remuneração tem duração máxima de 3 meses (Lei nº 8.112/1990, Art. 86, § 2º).
    * O período da licença remunerada conta para aposentadoria e disponibilidade (Lei nº 8.112/1990, Art. 103, III).
    * A licença pode ser concedida a servidores em estágio probatório, que fica suspenso durante o período (Lei nº 8.112/1990, Art. 20, § 4º e § 5º).
    * Durante a licença remunerada, o servidor continua recebendo auxílio pré-escolar e auxílio-saúde, mas perde o direito a auxílio-transporte, auxílio-alimentação e adicional de periculosidade (Nota Técnica Consolidada nº 01/2014/CGNOR/DENOP/SEGEP/MP).
* **Procedimento:**
    1. O servidor abre processo no SIPAC.
    2. Anexa o formulário de licença (IN nº 34/2021) e a documentação exigida.
    3. A Seção de Controle de Frequência (SCF) analisa a documentação, emite portaria, registra o afastamento no sistema (SIGEPE) e envia a portaria à unidade para ciência. O processo é encaminhado à Divisão de Pagamentos (CPP) para ajustes financeiros.
    4. A Diretoria de Administração de Pessoal (DAP) assina a portaria.
    5. A CPP realiza os ajustes financeiros.
    6. O processo é enviado à Seção de Arquivamento de Pessoal (SAP) para registro e arquivamento.
    * **Tipos de Processo no SIPAC:**
        * Licença sem remuneração: AFASTAMENTO P/EXERCER ATIVIDADE POLÍTICA: SEM ÔNUS PARA A INSTITUIÇÃO.
        * Licença com remuneração: AFASTAMENTO P/EXERCER ATIVIDADE POLÍTICA: COM ÔNUS PARA A INSTITUIÇÃO.
    * **Classificação (CONARQ):** 023.3 - LICENÇAS.
* **Setor Responsável:** SCF - Seção de Controle de Frequência (https://www.ufpe.br/progepe/frequencia).
    * Telefone: (81) 2126-8039
    * E-mail: frequencia.progepe@ufpe.br

**13. Licença para Acompanhar Cônjuge - Exercício Provisório**

* **O que é?** Licença remunerada por prazo indeterminado concedida ao servidor para acompanhar cônjuge ou companheiro(a) que foi deslocado(a) para outro local do Brasil, para o exterior ou para exercer mandato eletivo.
* **Público Alvo:** Servidores ativos permanentes da UFPE.
* **Requisitos:**
    * O cônjuge/companheiro(a) deve ser servidor público (civil ou militar) de qualquer esfera de governo ou ter sido eleito(a) para mandato no Executivo ou Legislativo.
    * Deve haver possibilidade de exercício provisório em órgão ou entidade federal (com atividade compatível com o cargo do servidor).
* **Documentação Necessária:**
    * Requerimento.
    * Ato de deslocamento do cônjuge/companheiro(a).
    * Documento comprovando que o cônjuge/companheiro(a) é servidor público ou militar, ou diploma de mandato eletivo (TSE).
    * Certidão de casamento ou declaração de união estável (com data anterior ao deslocamento).
    * Anuências dos órgãos/entidades envolvidos.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 84, § 2º).
    * Orientação Normativa nº 5/2012.
    * Instrução Normativa SGP/SEDGG/ME nº 34/2021.
* **Procedimento:**
    * Abrir processo no SIPAC.
    * Tipo de Processo: EXERCÍCIO PROVISÓRIO.
    * Classificação (CONARQ): 022.21 - LOTAÇÃO, EXERCÍCIO E PERMUTA.
    * Código do Setor Responsável: 11.07.30.
* **Setor Responsável:** SMP - Seção de Movimentação de Pessoal.
    * Telefone: (81) 2126-8165
    * E-mail: smp.progepe@ufpe.br

**14. Licença para Acompanhar Cônjuge ou Companheiro(a) (Sem Remuneração)**

* **O que é?** Licença não remunerada por prazo indeterminado concedida ao servidor para acompanhar cônjuge ou companheiro(a) que foi deslocado(a) para outro local do Brasil, para o exterior ou para exercer mandato eletivo.
* **Público Alvo:** Servidores ativos permanentes da UFPE.
* **Requisitos:**
    * O cônjuge/companheiro(a) deve ter sido deslocado(a) por motivo alheio à sua vontade (no setor público ou privado).
* **Documentação Necessária:**
    * Certidão de casamento ou declaração de união estável (com data anterior ao deslocamento).
    * Ato de deslocamento do cônjuge/companheiro(a).
    * Diploma de mandato eletivo (TSE), se for o caso.
* **Base Legal:**
    * Lei nº 8.112/1990 (Art. 84, § 1º).
    * Instrução Normativa SGP/SEDGG/ME nº 34/2021.
* **Procedimento:**
    * Abrir processo no SIPAC.
    * Tipo de Processo: LICENCA POR MOTIVO DE AFASTAMENTO DO CÔNJUGE/COMPANHEIRO.
    * Classificação (CONARQ): 023.3 - LICENÇAS.
    * Código do Setor Responsável: 11.07.30.
* **Setor Responsável:** SMP - Seção de Movimentação de Pessoal.
    * Telefone: (81) 2126-8165
    * E-mail: smp.progepe@ufpe.br

---Fim das Informações sobre Licenças Para Acompanhar Conjuge, Atividade Política, Capacitação, Tratamento de Saúde, Prêmio e Interesse particular---

---Informações sobre Afastamentos e Movimentações de Servidores na UFPE---

## Tipos de Afastamentos e Movimentação de Servidores na UFPE:

Este guia detalha os tipos de afastamentos e movimentações disponíveis para servidores técnico-administrativos da UFPE, com base nos documentos fornecidos. 

**1. REQUISIÇÃO:**

* **O que é:** Transferência irrecusável de um servidor público para outro órgão ou entidade requisitante, sem alteração da lotação original. O servidor requisitado passa a exercer suas funções no novo órgão, mas mantém vínculo com o de origem.
* **Público Alvo:** Servidor ativo permanente.
* **Requisitos:**
    * Ser servidor ativo permanente.
    * O órgão requisitante deve possuir prerrogativa expressa para requisitar servidores.
    * A requisição não é nominal, o órgão requisitado indica o servidor. 
    * A requisição independe de cargo em comissão ou função de confiança.
* **Documentação necessária:**  Pedido de requisição (Anexo III da Portaria nº 6.066/2022).
* **Base Legal:**
    * Lei nº 8.112/1990 (art. 93);
    * Decreto nº 10.835/2021; 
    * Lei nº 13.328/2016 (art. 105 a 108);
    * Lei nº 6.999/1982;
    * Portaria SEDGG/ME nº 6.066/2022.
* **Informações Gerais:**
    * A requisição, em geral, tem prazo indeterminado, salvo disposição legal em contrário.
    * Não pode ser encerrada unilateralmente pelo órgão requisitado.
    * O Reitor é a autoridade competente para efetivar a requisição.
    *  É vedada a retroatividade nas portarias de requisição e a convalidação de atos com efeitos  exauridos.
* **Procedimentos:**
    * Abertura de processo no SIPAC - Tipo: REQUISICAO. CESSAO.
    * Classificação (CONARQ): 022.22 - CESSAO. REQUISICAO DE SERVIDOR.
    * Código do setor responsável: 11.07.30.
* **Setor responsável:** SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br.

**2. REMOÇÃO POR PERMUTA:**

* **O que é:**  Deslocamento de dois servidores, com a troca de suas respectivas lotações, a pedido e com concordância de ambas as partes e autorização da administração.
* **Público Alvo:** Servidores técnico-administrativos ativos permanentes da UFPE.
* **Requisitos:**
    * Ser servidor ativo.
    * Equivalência de atribuições entre os cargos dos servidores envolvidos.
    * Acordo entre as Chefias dos servidores.
    * Autorização da Diretora da DDP.
* **Documentação necessária:** Não especificada nos documentos, recomenda-se contato com o setor responsável. 
* **Base Legal:** Lei nº 8.112/1990.
* **Informações Gerais:** Não constam nos documentos analisados.
* **Procedimentos:**
    * Abertura de processo no SIPAC - Assunto: Permuta de Funcionários.
    * Classificação (CONARQ): 022.21.
    * Código do setor responsável: 11.07.30.
* **Setor responsável:** SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br.

**3. REMOÇÃO A PEDIDO DO SERVIDOR (MOTIVO SAÚDE):**

* **O que é:** Remoção concedida a pedido do servidor, independentemente do interesse da administração, por motivo de saúde do próprio servidor, cônjuge, companheiro(a) ou dependente que viva às suas expensas e conste em assentamento funcional.
* **Público Alvo:** Servidores ativos permanentes.
* **Requisitos:**
    * Ser servidor ativo.
    * Laudo médico emitido por Junta Médica Oficial comprovando a enfermidade. 
* **Documentação necessária:**
    * Requerimento de remoção.
    * Documentos que comprovem a doença motivadora do pedido.
* **Base Legal:** Lei nº 8.112/1990.
* **Informações Gerais:**
    *  A remoção para acompanhar cônjuge não concede ajuda de custo.
    *  A lotação do servidor removido deve respeitar as atribuições do cargo, exceto em casos de readaptação comprovada por Junta Médica Oficial.
* **Procedimentos:**
    * Abertura de processo no SIPAC - Assunto: Remoção de Servidor.
    * Classificação (CONARQ): 022.3.
    * Código do setor responsável: 11.07.30.
* **Setor responsável:** SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br.

**4. REDISTRIBUIÇÃO:**

* **O que é:** Deslocamento definitivo de um cargo efetivo para outro órgão ou entidade do mesmo poder. 
* **Público Alvo:** Servidor Ativo Permanente.
* **Requisitos:**
    * Interesse da Administração (art. 37, inciso I da Lei nº 8.112/90);
    * Equivalência de vencimentos (art. 37, inciso II da Lei nº 8.112/90);
    * Manutenção da essência das atribuições do cargo (art. 37, inciso III da Lei nº 8.112/90);
    * Vinculação entre graus de responsabilidade e complexidade das atividades (art. 37, inciso IV da Lei nº 8.112/90);
    * Mesmo nível de escolaridade, especialidade ou habilitação profissional (art. 37, inciso V da Lei nº 8.112/90);
    * Compatibilidade entre as atribuições do cargo e as finalidades do órgão/entidade (art. 37, inciso VI da Lei nº 8.112/90).
* **Documentação necessária:**
    * Formulário de Redistribuição (específico para este fim).
    * Documentos listados no Formulário de Redistribuição.
* **Base Legal:**
    * Lei nº 8.112/1990 (art. 18, 37, 53 e 99);
    * Lei nº 9.527/1997;
    * Portaria SEGRT/MGI nº 619/2023;
    * Nota Técnica nº 70/2023/MOV/COLEP/CGGP/SAA;
    * Ofício-Circular nº 2/2023/GABINETE/CGGP/SAA-MEC;
    * Ofício Circular nº 24/1996 (Processo administrativo/impedimento);
    * Decreto 9.262/2018 (Extinção de cargos);
    * Lei 8.270/1991 (art. 7, 8 e 26);
    * Lei n. 11.091/2005 (Art. 26-B);
    * Nota Técnica nº 69/2014/CGNOR/DENOP/SEGEP/MP (Certidão de tempo de contribuição).
* **Informações Gerais:**
    * Tipo de Processo: Redistribuição.
    * Classificação (CONARQ): 022.4 – Redistribuição.
    * Código do setor responsável: 11.07.30 - Seção de Movimentação de Pessoal da CADMP.
* **Procedimentos:**
    *  Abertura do processo:
        * Órgão/Departamento interessado: via ofício.
        * Servidor interessado: preenchimento do formulário de redistribuição + documentos.
    *  Envio do processo:
        * Sem indicação de permuta com código de vaga: DDP (verificar disponibilidade e interesse da UFPE).
        * Cargos extintos: DDP (análise), mesmo sem contrapartida (Decreto 9.262/2018 e Ofício-Circular nº 2/2017/CGRH/DIFES/SESU-MEC).
        *  Departamento e Centro interessados: para ciência e pronunciamento.
        * DDP: apreciação e envio ao Gabinete do Reitor (GR) para anuência do Reitor.
        * MEC: publicação da redistribuição no DOU, com anuência dos órgãos envolvidos.
        * Órgão: solicitar anuência na redistribuição e enviar ao MEC para publicação no DOU.
* **Setor responsável:** 
    * CADMP - Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal.
    * SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br.

**5. COLABORAÇÃO TÉCNICA:**

* **O que é:** Afastamento de servidor da UFPE para trabalho técnico em campus diferente, outra instituição federal de ensino/pesquisa no Brasil, ou de servidores de outras instituições que venham colaborar com a UFPE. 
* **Público Alvo:** Servidor ativo permanente.
* **Requisitos:**
    * Ser servidor ativo e estável.
    * Estar vinculado a um projeto ou convênio com prazos e finalidades bem definidos.
    * Concordância dos dirigentes máximos de cada órgão/campus envolvido.
* **Documentação necessária:**
    * Requerimento do interessado (modelo geral disponível no site da UFPE ou solicitar a protocolo@ufpe.br) ou Ofício da instituição de destino.
    * Projeto ou Convênio de colaboração técnica com prazos e finalidades bem definidos.
    * Cópia da Portaria de aprovação em estágio probatório. 
    * Declaração de que o servidor não responde a Processo Administrativo Disciplinar ou Sindicância.
    *  Termo de Cooperação Técnica assinado pela autoridade máxima da instituição de destino (se houver).
* **Base Legal:**
    * Lei 12.772/2012.
    * Lei 11.091/2005.
* **Informações Gerais:**
    * Demanda iniciada via processo no SIPAC (servidor da UFPE) ou Protocolo Geral (protocolo@ufpe.br) para servidor de outra instituição.
    * Servidores não estáveis não podem participar, conforme  § 4º do art. 20 da Lei 8112/90.
    * A autoridade máxima da instituição de origem emite Portaria, publicada no DOU, cedendo o servidor.
    *  Tempo máximo: 4 anos, podendo ser interrompida a qualquer momento (administração ou servidor).
    *  Remuneração: responsabilidade da instituição de origem.
    * Prazo para início: 30 dias a partir da publicação do ato. 
    *  Frequência: enviada pela instituição recebedora à de origem até o 5º dia útil do mês subsequente.
* **Procedimentos:**
    * Abertura de processo no SIPAC - Tipo: Colaboração Técnica.
    * Classificação (CONARQ): 023.4 - AFASTAMENTOS.
    * Código do setor responsável: 11.07.30.
* **Setor responsável:** SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br.

**6. CESSÃO PARA OUTRO ÓRGÃO:**

* **O que é:**  Ato autorizativo que permite ao servidor público, sem suspender ou interromper o vínculo com o órgão de origem, exercer suas funções em outro órgão ou entidade. 
* **Público Alvo:** Servidor ativo permanente.
* **Requisitos:**
    * Pedido do servidor a ser cedido.
    * Concordância do órgão cedente.
    * Concordância do órgão cessionário.
    * O pedido deve ser apresentado conforme Anexo I da Portaria nº 6.066/2022.
* **Documentação necessária:**  Pedido de cessão (Anexo I da Portaria nº 6.066/2022).
* **Base Legal:**
    * Lei nº 8.112/1990 (art. 93); 
    * Decreto nº 10.835/2021;
    * Portaria SEDGG/ME nº 6.066/2022.
* **Informações Gerais:**
    * A cessão, em geral, tem prazo indeterminado.
    *  Aplica-se a outros órgãos da União, Estados, Distrito Federal e Municípios, para cargos em comissão, função de confiança ou casos de leis específicas.
    * Para outros Poderes, órgãos autônomos ou entidades federativas: apenas para cargos em comissão ou função de confiança (nível mínimo 4 do Grupo-DAS).
    *  Servidor em estágio probatório: somente para cargos de Natureza Especial, DAS nível 6, 5 e 4, ou equivalentes.
    *  Mudança de sede: o servidor tem de 10 a 30 dias para assumir o cargo na nova sede.
    *  A cessão pode ser encerrada a qualquer momento (cedente, cessionário ou servidor).
    *  O tempo em cargo em comissão ou equivalente em outros órgãos (União, Estados, Municípios e DF) conta como efetivo exercício.
    *  O Reitor autoriza a cessão.
    *  É vedada a retroatividade nas portarias de cessão e a convalidação de atos com efeitos  exauridos.
* **Procedimentos:**
    * Abertura de processo no SIPAC - Tipo: CESSAO DE SERVIDOR.
    * Classificação (CONARQ): 022.22 - CESSAO. REQUISICAO DE SERVIDOR
    * Código do setor responsável: 11.07.30
* **Setor responsável:** SMP - Seção de Movimentação de Pessoal.
    * Contato: (21) 2681-65 / smp.progepe@ufpe.br. 

---Fim das Informações sobre Afastamentos e Movimentações de Servidores na UFPE---

---Informações sobre Processo Administrativo Disciplinar - PAD---

Para informações sobre PAD entrar em contato com a SOPAD

Unidade Responsável:
 
SOPAD - Serviço de Corregedoria e Organização de Processo Disciplinar
Telefone:(81) 2126.8167
Contato: servicocorregedoria@ufpe.br
 
Equipe:
 
Tereza Cristina Tarragô Souza Rodrigues
Maria Alexsandra Prado de Oliveira
Fernando Cavalcanti de Souza
 
Manual Prático do SOPAD link:https://www.ufpe.br/documents/3803744/4374088/Manual+Pra%C2%B4tico+do+SOPAD.pdf/c21d4be4-948a-4865-b3cd-d6ed43c47899

---Fim das Informações sobre Processo Administrativo Disciplinar - PAD---

---Informações sobre Serviço Voluntário, Progressão por Mérito, Progressão por Capacitação e Pensão por Morte---

## Tipos de Afastamentos e Movimentações na UFPE (Continuação):

**7. SERVIÇO VOLUNTÁRIO:**

* **O que é:** Programa que permite a cidadãos prestar serviços, sem remuneração, em atividades de ensino, pesquisa, extensão, técnica, administrativa e/ou assistenciais na UFPE.
* **Público Alvo:** Comunidade interna e externa à UFPE.
* **Requisitos:** Interesse em prestar serviço voluntário (sem remuneração).
* **Documentação necessária:**
    * Plano de atividades (especificando serviços, datas de início e fim, e carga horária semanal).
    * *Curriculum vitae*.
    * Aprovação do Colegiado do Curso, Departamento e Conselho Departamental (atividades de ensino, pesquisa e extensão).
    * Aprovação da Pró-Reitoria ou Conselho Técnico-Administrativo (atividades administrativas e assistenciais). 
* **Base Legal:**
    * Resolução nº 3/2007 – Conselho Universitário/UFPE.
    * Lei nº 9.608/1998.
* **Informações Gerais:**
    * Locais de atuação: centros/departamentos acadêmicos, Pró-Reitorias ou órgãos suplementares.
    * Duração inicial: até 2 anos (renovável).
    * Vedações aos voluntários: exercer função gratificada, funções administrativas privativas de servidores efetivos e participação em processos eleitorais. 
    *  Voluntários em ensino, pesquisa e extensão: podem orientar alunos, participar de grupos de trabalho, bancas examinadoras, etc. 
    *  Não gera vínculo empregatício, obrigações trabalhistas, previdenciárias ou afins. 
* **Procedimentos:**
    *  Abertura de processo no SIPAC pela unidade interessada.
    *  Tipo do Processo: SERVICO VOLUNTARIO.
    *  Classificação (CONARQ): 020.12 – SERVIDORES TEMPORARIOS.
    *  Assunto Detalhado: Participação no Programa de Serviço Voluntário da UFPE.
    *  Unidade de Destino: 11.07.51 (Divisão de Apoio em Qualidade de Vida).
* **Setor responsável:** DAQV - Divisão de Apoio em Qualidade de Vida.
    * Contato: 2126-8190/8189 (WhatsApp) / apoiodqv.progepe@ufpe.br 

**8. PROGRESSÃO POR MÉRITO PROFISSIONAL:**

* **O que é:** Mudança para o padrão de vencimento subsequente a cada 18 meses de efetivo exercício, mediante resultado positivo em avaliação de desempenho. Objetivo: promover o desenvolvimento do servidor na carreira.
* **Público Alvo:** Servidores Técnico-Administrativos em Educação (TAE).
* **Requisitos:**
    *  18 meses de efetivo exercício (para primeira progressão).
    *  18 meses entre cada progressão. 
    *  Obter resultado definido no Programa de Avaliação de Desempenho da UFPE. 
* **Documentação necessária:**
    * Formulário de Autoavaliação.
    * Formulário de Avaliação pela Chefia Imediata. 
* **Base Legal:**
    * Lei nº 8.112/1990.
    * Lei nº 11.091/2005.
    * Lei nº 11.784/2008.
    * Decreto nº 5.825/2006.
    * Resolução nº 6/2006 – UFPE.
* **Informações Gerais:**
    * Tipo de Processo: Avaliação de Desempenho.
    * Classificação (CONARQ): 022.6 – Avaliação de Desempenho.
    * Código do setor responsável: 11.07.06 – Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal.
    *  Processo avaliativo: envolve servidores e chefias.
    *  Avaliação Tipo A: primeiros 9 meses.
    *  Avaliação Tipo B: últimos 9 meses. 
    *  Formulários: disponibilizados no SIGA.
    *  Dimensões da avaliação: Funcional e Gerencial (cada uma com autoavaliação e avaliação pela chefia).
    *  Requisitos para progressão: desempenho satisfatório na avaliação e ausência de sanções disciplinares durante os 18 meses.
    *  Variação salarial: 3,9% sobre o vencimento básico. 
    *  Indicadores da Avaliação: descritos no documento (pág. 3 e 4).
    *  Conceitos: Abaixo do Esperado (AbE), Parcialmente Esperado (PE), Dentro do Esperado (DE) e Acima do Esperado (AE) – com pontuações.
    *  Progressão: concedida para quem obtiver DE ou AE.
    *  Servidores cedidos, requisitados, etc.: avaliação com os mesmos critérios, processo formalizado pela CADMP/PROGEPE (não pelo SIGA).
* **Setor responsável:** CADMP – Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal.
    * Contato: 2126-8173 / cadmp.progepe@ufpe.br. 

**9. PROGRESSÃO POR CAPACITAÇÃO (TAE):**

* **O que é:** Mudança de nível de capacitação no mesmo cargo e nível de classificação, mediante certificação em programa de capacitação compatível.
* **Público Alvo:** Servidores técnico-administrativos em Educação (TAE) da UFPE.
* **Requisitos:**
    * Ser TAE da UFPE.
    *  18 meses de efetivo exercício (para primeira progressão).
    *  18 meses entre cada progressão. 
    *  Realizar ações de desenvolvimento de curta duração (mínimo 20h por certificado) compatíveis com o cargo, ambiente organizacional (Portaria MEC nº 9/2006), e carga horária mínima total (Anexo III da Lei nº 11.091/2005).
* **Documentação necessária:**
    * Requerimento de Progressão por Capacitação (preenchido e assinado eletronicamente no SIPAC).
    *  Certificado do curso/ação (carga horária mínima de 20h, contendo: nome completo, nome do curso/ação, instituição, carga horária total, período de realização, código de autenticação (para cursos EAD)). 
    *  Cópia da Portaria da última progressão por capacitação (se estiver no nível II ou III). 
    *  Termo de posse (para servidores com área de atuação específica).
    *  Documento comprobatório de aproveitamento de disciplina de Mestrado ou Doutorado cursada como aluno especial (para cargos nível E), contendo: nome completo, instituição, curso, área de conhecimento, carga horária, período cursado, ementa, declaração de conclusão com aproveitamento como aluno especial (conforme Parecer CNE/CES n° 607/2020).
    *  Despacho descrevendo as atividades diárias do servidor na unidade (assinado pela chefia imediata e pelo servidor).
    *  Documentos em PDF, cópias digitalizadas conferidas administrativamente e assinadas eletronicamente via SIPAC (exceto nato-digitais). 
* **Base Legal:** (lista completa na página 2 do documento)
    * Lei nº 8.112/1990;
    * Lei nº 11.091/2005;
    * Lei nº 11.784/2008;
    * Lei nº 12.772/2012;
    *  Decretos, Portarias, Pareceres e Instruções Normativas relacionadas (verificar documento).
* **Informações Gerais:** 
    *  Servidor posicionado no nível de capacitação seguinte, no mesmo nível de classificação, mantendo a distância entre o padrão anterior e o inicial do novo nível.
    *  Somatório de cargas horárias permitido (verificar regras na página 3 do documento).
    *  Cursos com menos de 20h não são válidos.
    *  Não se aplica a cursos de educação formal.
    *  Certificados de cursos ministrados pelo próprio servidor não são válidos.
    *  Certificados em língua estrangeira:  exigem tradução juramentada (art. 224 da Lei nº 10.406/2002). 
    * Cursos EAD: permitidos se a instituição tiver autorização e o certificado, código de verificação.
    *  "Aluno regular de disciplinas isoladas" (art. 10, §6º, Lei nº 11.091/2008 e art. 2º, II, Portaria MEC nº 11.091/2008):  refere-se a aluno especial (Parecer CNE/CES 607/2020).
    *  Progressão: efetivada após publicação do ato, com efeitos financeiros a partir da data de entrada do requerimento no SIPAC, se cumpridas as exigências. 
    *  Recurso:  via mesmo processo reenviado à SAAPQ com despacho justificando o pedido e novos documentos. 
    *  Tabela de cargas horárias mínimas por nível de classificação e capacitação (pág. 4 e 5 do documento).
* **Procedimentos:**
    *  Abertura de processo no SIPAC.
    * Tipo: Progressão por Capacitação.
    *  Classificação (CONARQ): 023.12 – Reestruturação e Alteração Salarial.
    * Código do setor responsável: 11.07.47.
    *  Processo: único para cada tipo e nível de progressão.
    *  Processos: ostensivos (em geral), documentos com dados pessoais: restritos.
    *  Servidor: cadastrado como interessado com nome completo e SIAPE.
    *  Não abrir mais de um processo simultâneo. 
    *  Responsabilidades: servidor (abertura, acompanhamento e resolução de pendências). 
* **Setor responsável:** Núcleo de Acompanhamento e Avaliação das Progressões e Qualificação.
    * Contato: 2126-8671 / desenvolvimento.progepe@ufpe.br 

**10. PENSÃO POR MORTE:**

* **O que é:** Benefício previdenciário concedido aos dependentes de servidor falecido (em atividade ou aposentado).
* **Público Alvo:** Dependentes do servidor falecido (verificar lista completa no Art. 3º da Portaria SGP/SEDGG/ME Nº 4645/2022, pág. 1 e 2 do documento).
* **Requisitos:**
    * Possuir a condição de dependente (conforme  Art. 3º da Portaria SGP/SEDGG/ME Nº 4645/2022).
    *  Apresentar a documentação comprobatória (verificar lista completa nas páginas 2, 3 e 4 do documento).
* **Documentação necessária:** Varia conforme o grau de parentesco (verificar lista completa nas páginas 2, 3 e 4 do documento).
* **Base Legal:**
    * Lei nº 8.112/1990.
    *  Lei nº 13.135/2015.
    * Lei nº 13.846/2019.
    *  Emenda Constitucional nº 103/2019. 
    * Portaria SGP/SEDGG/ME nº 4645/2022. 
* **Informações Gerais:**
    *  A invalidez está sujeita à avaliação da Junta Médica Oficial.
    *  Invalidez, deficiência grave, intelectual ou mental e dependência econômica:  devem ser anteriores ao óbito do servidor. 
    *  Menos de 18 meses de contribuição ou casamento/união estável inferior a 2 anos na data do óbito:  4 meses de pensão (exceção: filho menor de 16 anos, até 180 dias).
    *  Retroativos: pagos a partir da data do óbito se solicitados em até 90 dias (180 dias para filho menor de 16 anos). 
    *  Tempo de recebimento:  varia conforme a idade do cônjuge/companheiro (verificar tabela na página 5 do documento). 
* **Procedimentos:**
    *  Envio da documentação digitalizada para o email do setor responsável (saep.progepe@ufpe.br). 
    *  Análise e validação da documentação.
    *  Abertura do processo pelo Protocolo Geral (CPG).
* **Setor responsável:** CAPE - Coordenação de Aposentadoria e Pensão.
    * Contato: 2126-8675 


**Observação:** É fundamental que o servidor consulte os documentos completos e atualizados junto aos setores responsáveis para obter informações precisas sobre os procedimentos, prazos e legislação vigente. 

---Fim das Informações sobre Serviço Voluntário, Progressão por Mérito, Progressão por Capacitação e Pensão por Morte---

---Informações de contato ---
(se perguntarem quem te criou informe que foi o servidor Luiz Emanoel da CASF)
(Caso seja solicitada alguma informação abaixo você pode dar a informação sem problema)
(o servidor docente só pode participar do PGD quando ocupantes de função gratificada ou cargo de direção no âmbito da Universidade Federal de Pernambuco — UFPE, e apenas quanto às atividades dedicadas à gestão e quando a sua unidade tiver aderido ao PGD.)
##  Setores e Unidades da PROGEPE - Contatos e Descrições:

**Gabinete da Pró-Reitoria:**

* **Gabinete do Pró-reitor(a):** 
    * **Telefone:** 2126-8150
    * **Email:** progepe@ufpe.br
    * **Descrição:** Secretaria do Pró-Reitor(a). 
(unidades diretamente ligadas à PROGEPE)
* **Gerência de Legislação e Controle de Processos (GLCP):**
    * **Telefone:** 2126-8112
    * **Email:** glcp.progepe@ufpe.br
    * **Descrição:** Controle dos atendimentos aos processos judiciais, de Ouvidoria e de órgãos de controle (CGU, TCU, MPF).

* **Gerência de Curso e Concurso (GCC):**
    * **Telefone:** 2126-8042
    * **Email:** gcc.progepe@ufpe.br
    * **Descrição:** Pagamento de GECC; bolsa de desenvolvimento e execução de contratações de cursos e formação.

* **Coordenação de Acumulação de Cargos e Emprego (CACE):**
    * **Telefone:** 2126-8172 e 2126-8003
    * **Email:** cace.progepe@ufpe.br
    * **Descrição:** Análise de acumulação de cargo no mesmo ou em outro órgão.

* **Comissão de Raio X e Substâncias Radioativas (CoraX):**
    * **Telefone:** 2126-8003
    * **Email:** corax.progepe@ufpe.br
    * **Descrição:** Orientação e análise das solicitações de adicionais de Raio X e radiação ionizante dos servidores que trabalham expostos às radiações ionizantes.

* **Comissão Interna de Supervisão de Atividades Insalubres e Perigosas (COSAIP):**
    * **Telefone:** 2126-8003
    * **Email:** seccosaip.progepe@ufpe.br
    * **Descrição:** Orientações sobre solicitação dos adicionais de insalubridade e de periculosidade, no que se refere à instrução dos processos administrativos.

* **Divisão de Tecnologia da Informação e Comunicação (DTIcom):**
    * **Telefone:** 2126-8169
    * **Email:** dticom.progepe@ufpe.br
    * **Descrição:**  Gestão de unidades já existentes e cadastro de novas unidades; Gestão dos níveis de responsabilidade (Secretário, gerente, vice-chefe, chefe); Configuração dos vínculos (designação) no SIGRH (coordenador, chefe, vice, etc); Habilitação dos Usuários no SIAPE/SIASS; Habilitação de Homologador de Férias; Extração de relatórios funcionais; Habilitação nos Módulos do SIPAC e SIGRH (Almoxarifado, Infraestrutura, Compras, etc); Cadastro/Atribuição de unidade extra.

(Diretoria subordinada à PROGEPE) 
**Diretoria de Administração de Pessoal [DAP]:**

* **Diretoria:**
    * **Telefone:** 2126-8670
    * **Email:** dap.progepe@ufpe.br

* **Central de Atendimento ao Servidor:** (unidade subortinada à DAP)
    * **Telefone:** 2126-8166
    * **Whatsapp:** 2126-8176
    * **Email:** centralservidor@ufpe.br
    * **Descrição:** Desbloqueio sigepe, prova de vida, contracheques, informe de rendimentos, plataformas de gestão (Gov,Sou Gov,Sigac), etc. 

(coordenação subordinada à DAP)
* **Coordenação de Pagamento de Pessoal (CPP):**
    * **Telefone:** 2126-8177
    * **Email:** cpp.progepe@ufpe.br
    * **Descrição:** Folha de Pagamento; alteração de conta bancária; pagamento de exercícios anteriores; isenção de IRRF; inclusão de vale transporte etc. 
(Números da CPP por assunto)
* **Divisão de Pagamentos:**
    * **Telefone:** 2126-8177
    * **Email:** pagamento.progepe@ufpe.br
    * **Descrição:**  

* **Exercícios Anteriores:**
    * **Telefone:** 2126-8177
    * **Email:** exanterior.progepe@ufpe.br
    * **Descrição:**  

* **Reposição ao Erário e Resíduos Remuneratórios:**
    * **Telefone:** 2126-8678
    * **Descrição:**  
(Fim dos números da CPP por assunto)

(Coordenação subortinada à DAP)
* **Coordenação de Assentamento Funcional (CASF):**
    * **Email:** casf.progepe@ufpe.br
    * **Descrição:** Arquivo funcional físico. Arquivo funcional digital. PGD. Frequência. Informações funcionais. Implantação e prorrogação de licença maternidade, emissão e solicitação de averbação de tempo de serviço, licença paternidade/nojo; gala; auxílio pré-escolar.    
(Números da CASF por assunto)

* **Secretaria:**
    * **Telefone:** 2126-8673
* **Arquivo de Pessoal:**
    * **Telefone:** 2126-8147
    * **Email:** arquivodepessoal.progepe@ufpe.br
    * **Descrição:**  

* **Controle de Frequência:**
    * **Telefone:** 2126-8039
    * **Email:** frequencia.progepe@ufpe.br
    * **Descrição:**  

* **Tempo de Serviço:**
    * **Telefone:** 2126-7084
    * **Email:** tempodeservico.progepe@ufpe.br
    * **Descrição:**  
(Fim dos números da CASF por assunto)

(coordenação subortinada à DAP)    
* **Coordenação de Aposentadoria e Pensão (CAPE):**
    * **Telefone:** 2126-8675
    * **Email:** cape.progepe@ufpe.br
    * **Descrição:** Aposentadoria, abono de permanência, revisões, pensão e auxílio funeral. 
(Números da CAPE por assunto)   
* **Aposentadoria:**
    * **Telefone:** 2126-8175
    * **Email:** aposentadoria.progepe@ufpe.br
    * **Descrição:**  

* **Pensão:**
    * **Telefone:** 2126-8674
    * **Email:** pensao.progepe@ufpe.br
    * **Descrição:**  

* **Núcleo de Análise Funcional (NAF):**
    * **Telefone:** 2126-8168
    * **Email:** naf.progepe@ufpe.br
    * **Descrição:** Análise do acervo funcional, dos sistemas corporativos e instrução dos processos de Abono, Aposentadoria, Pensão e Revisões. 
(Fim dos Números da CAPE por assunto)    

(coordenação subortinada à DAP)    
* **Coordenação Administrativa de Portarias e Publicações (CAPP):**
    * **Telefone:** 2126-7057
    * **Email:** capp.progepe@ufpe.br

(Números da CAPP por assunto)    

* **Apoio à Adicionais e Progressões:**
    * **Telefone:** 2126-7094
    * **Email:** portarias.progepe@ufpe.br
    * **Descrição:** Emissão de portarias e implantação de progressões de docentes, adicionais ocupacionais e alterações de carga horária. Emissão de portarias de comissões de inquérito, designações coletivas, autorizações, delegações de poderes, penalidades e elogios.

* **Funções de Confiança:**
    * **Telefone:** 2126-3170/8660
    * **Email:** funcoes.progepe@ufpe.br
    * **Descrição:** Emissão de portarias de substituição, nomeação, exoneração, designação e dispensa de função. 

* **Publicações e Registros:**
    * **Telefone:** 2126-8179
    * **Email:** publicacao.progepe@ufpe.br
    * **Descrição:** Publicações oficiais no Boletim Oficial e Diário Oficial da União (D.O.U) 

(Fim dos números da CAPP por assunto)
    
(Diretoria subortinada à PROGEPE) 
**Desenvolvimento de Pessoas [DDP]:**

* **Diretoria:**
    * **Telefone:** 2126-8698
    * **Email:** ddp.progepe@ufpe.br

(Unidades subordinadas à DDP) 
* **Coordenação de Avaliação, Dimensionamento e Movimentação de Pessoal (CADMP):**
    * **Telefone:** 2126-8173
    * **Email:** cadmp.progepe@ufpe.br
    * **Descrição:** Avaliação de Desempenho e Progressão de Mérito (Progressão por mérito funcional - TAE); Avaliação de Desempenho por Estágio Probatório (Estágio Probatório Docente e TAE); Movimentação de Pessoal (Redistribuição, cessão, licença para tratar de interesse particular, licença para acompanhar cônjuge, licença prêmio, licença para mandato eletivo, exercício provisório e remoção); Dimensionamento de Pessoal (Análise e parecer do Dimensionamento da Força de Trabalho-DFT). 
(numeros por assunto CADMP)
* **Avaliação de Desempenho e Progressão de Mérito:**
    * **Telefone:** 2126-8174
    * **Email:** desempenho.progepe@ufpe.br
    * **Descrição:**  

* **Avaliação de Desempenho por Estágio Probatório:**
    * **Telefone:** 2126-7148
    * **Email:** desempenho.progepe@ufpe.br
    * **Descrição:**  

* **Movimentação de Pessoal:**
    * **Telefone:** 2126-8165
    * **Email:** movimentacao.progepe@ufpe.br
    * **Descrição:**  

* **Dimensionamento de Pessoal:**
    * **Telefone:** 2126-7148
    * **Descrição:**  
(fim dos numeros por assunto CADMP)

(coordenação subordinada À DDP)
* **Coordenação de Provimentos e Concursos (CPC):**
    * **Telefone:** 2126-8672
    * **Email:** cpc.progepe@ufpe.br
    * **Descrição:** Demandas judiciais, de Ouvidoria, Acesso à Informação e órgãos de controle relativas a Provimentos e Concursos, solicitações ainda não autorizadas.  

* **Bolsas:**
    * **Telefone:** 2126-8676
    * **Email:** bolsas.progepe@ufpe.br
    * **Descrição:**  

* **Concursos:**
    * **Telefone:** 2126-7095
    * **Email:** admissao.progepe@ufpe.br
    * **Descrição:** Editais finalizados e em andamento para técnicos e docentes, validade de concursos e seleções, abertura e homologação de concursos. 

* **Provimentos:**
    * **Telefone:** 2126-7095
    * **Email:** admissao.progepe@ufpe.br
    * **Descrição:** Contratação, nomeação, posse, implantação de novos servidores no SIAPE, Aproveitamentos, reintegração, recondução, vacância, exoneração e demissão. 
(Fim de números relacionados a CPC)

* **Escola de Formação dos Servidores da UFPE - FORMARE:**
    * **Telefone:** 2126-8669/8671
    * **Email:** formare.progepe@ufpe.br
    * **Descrição:** Gestão técnico-administrativa e pedagógica da Formare; análise das solicitações de pedidos de ofertas de ações formativas e gerenciamento de editais voltados à formação e ao desenvolvimento de servidores; viabilização de ações de educação formal, gestão de parcerias, convênios de cooperação técnica e científica com instituições afins, etc.

* **Núcleo de Formação Continuada:**
    (ligada à FORMARE)
    * **Telefone:** 2126-8669
    * **Email:** formacaocontinuada.progepe@ufpe.br
    * **Descrição:** Elaboração, monitoramento, execução e avaliação do Plano de Desenvolvimento de Pessoas (PDP) da UFPE; planejamento, avaliação, oferta e certificação de ações formativas de curta e de média duração previstas no PDP da UFPE; formação de formadores da PROGEPE.

* **Núcleo Acompanhamento e avaliação das progressões e qualificação:**
    (ligada à FORMARE)
    * **Telefone:** 2126-8671
    * **Email:** desenvolvimento.progepe@ufpe.br
    * **Descrição:** Análise para concessão, emissão de documentos concessórios, solicitação de publicação e implantação de Progressão por capacitação profissional, de incentivo à qualificação, de jornada especial de Treinamento Regularmente Instituído (TRI) – educação formal e de horário especial de servidor estudante de técnicos administrativos em educação – TAE’s; análise para concessão, emissão de documentos concessórios, solicitação de publicação e implantação de licenças para capacitação, de afastamentos para estudo de longa duração e de curta duração, no Brasil e no Exterior, para servidores docentes e TAE’s.

(Fim das Unidades subordinadas à DDP)

(Diretoria subordinada à PROGEPE) 
**Diretoria de Qualidade de Vida [DQV]:**

* **Diretoria:**
    * **Telefone:** 2126-7341
    * **Email:** dqv.progepe@ufpe.br

* **Divisão de Apoio em Qualidade de Vida:**
    * **Whatsapp:** 2126-8189
    * **Telefone:** 2126-8190
    * **Email:** apoiodqv.progepe@ufpe.br
    * **Descrição:** Planos de saúde, auxílio-saúde, CMEI Paulo Rosas, Serviço Voluntário e Clube do Desconto. 

* **Núcleo de Atenção à Saúde do Servidor (NASS):**
    * **Email:** nass.siass.progepe@ufpe.br
    * **Descrição:** Licença para tratamento de saúde e Licença para acompanhar pessoa da família (Inserir atestado no Sougov). Outros tipos de perícia oficial em saúde ligar para receber orientação e/ou acessar o manual do servidor. 
(Abaixo números do NASS)
* **Assistência médica e nutricional:**
    * **Telefone:** 2126-3944/8582/7578
    * **Descrição:** Agendamento presencial ou por telefone em data específica do mês para consultas no mês seguinte. Ligue antes para confirmar o dia da marcação de consultas. 

* **Saúde Mental/Serviço Social:**
    * **Telefone:** 2126-7577
    * **Email:** saudemental.nass@ufpe.br
    * **Descrição:**  
(Fim dos números do NASS)
* **Serviço de Saúde e Segurança do Trabalho (SESST):**
    * **Telefone:** 2126-3992
    * **Email:** sesst.siass.progepe@ufpe.br
    * **Descrição:** Avaliação de riscos ambientais; Laudos técnicos para licitação; Laudos técnicos das condições ambientais de trabalho; Apoio à perícia médica; Treinamentos de assuntos relacionados à segurança do trabalho. 

* **Comitê de Ergonomia:**
    * **Telefone:** 2126-3992
    * **Email:** comiteergonomia.progepe@ufpe.br
    * **Descrição:**      

* **Coordenação de Qualidade de Vida:**
    * **Telefone:** 2126-7341
    * **Email:** qualidadevida.progepe@ufpe.br
    * **Descrição:** Política de Qualidade de Vida - Projetos e ações relacionados à qualidade de vida. 

* **Divisão de Prevenção e Promoção em Saúde Mental:**
    * **Email:** divsaudemental.progepe@ufpe.br
    * **Descrição:** Apoio a ações e projetos universitários de promoção à saúde mental. 
(Fim das Unidades subordinadas à DQV)
--- 

**Observação:**  É importante observar que alguns telefones podem não estar atualizados. Recomendo consultar o site da PROGEPE ou entrar em contato com a central de atendimento para confirmar os números.

---fim das informações dos contatos-----

---Fim das informações---

Aqui termina as informações e observações, de exemplo e vai começar o chat em si. O chat consiste em uma pergunta iniciando com "pergunta:". Você deverá analisar o contexto das perguntas feitas para dar a resposta mais adequada. Você deve se concentrar na pergunta mais recente então se o chat tiver:
"pergunta: bom dia! resposta: (sua resposta para o bom dia...) pergunta: Como faço para solicitar a aposentadoria?" você não precisa repetir o olá como posso ajudar em cada pergunta subsequente e pode variar essa introdução."""

pergunta += st.session_state.diff + "\n" + "--Início do Chat--\n"

for message in st.session_state.messages:
    if message["role"] == "user":
        pergunta += f"\npergunta:\n{message['content']}"
    else:
        pergunta += f"\nresposta:\n{message['content']}"
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua dúvida sobre o PGD..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(sheet, "Usuário", prompt)
    pergunta += f"\npergunta:\n{prompt}"
    result = llm.invoke(pergunta)
    response = result.content
    pergunta += f"\nresposta:\n{response}"
    if response:
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_message(sheet, "Sistema", response)
