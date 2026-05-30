ROTEIRO DO VÍDEO — PI UNIVESP Grupo 11
========================================
Duração prevista: 7-8 minutos
Apresentador: Diego Beran Ribeiro


═══════════════════════════════════════════════
BLOCO 1 — Identificação (30 segundos)
═══════════════════════════════════════════════

[ABRE TELA COM SLIDE DE TÍTULO]

"Olá, somos o Grupo 11 do Projeto Integrador em Computação da UNIVESP.
Meu nome é Diego Beran Ribeiro, e junto com o Narci Edson Venturini,
desenvolvemos a plataforma Pós-Graduação Brasil.

Nosso orientador é a professora Carla Maria da Silva Diaz,
e o polo é Campinas."

[TRANSIÇÃO PARA O MAPA]


═══════════════════════════════════════════════
BLOCO 2 — O Problema (1 minuto)
═══════════════════════════════════════════════

[SLIDE SIMPLES COM 3 TÓPICOS]

"Hoje, quem quer fazer uma pós-graduação enfrenta uma dificuldade:
as informações sobre os cursos estão espalhadas em vários lugares.

Os cursos de especialização você consulta no portal e-MEC.
Os cursos de mestrado e doutorado, na plataforma Sucupira da CAPES.
São sites diferentes, com interfaces diferentes, e nenhum deles
permite fazer uma busca por localização — tipo 'quais programas de
mestrado em engenharia tem num raio de 100 km da minha casa?'

A gente decidiu resolver isso construindo uma plataforma que unifica
esses dados e coloca tudo num mapa interativo."


═══════════════════════════════════════════════
BLOCO 3 — Demonstração da Solução (4-5 minutos)
═══════════════════════════════════════════════

[ABRE O SISTEMA NO NAVEGADOR — PÁGINA DO MAPA]

"Essa é a página principal. Aqui temos um mapa do Brasil com todas
as instituições de ensino superior que oferecem pós-graduação.
São 576 IES e quase 7.500 cursos cadastrados.

Os pontos estão clusterizados — quando você dá zoom, eles se abrem
e mostram as instituições separadas."

[DÁ ZOOM NO MAPA, CLICA EM ALGUNS PONTOS]

"Clicando em qualquer ponto, aparece o nome da instituição, endereço,
status jurídico e quais modalidades oferece: mestrado, doutorado
ou especialização. Também tem link pra página de detalhes."

[MOSTRA OS FILTROS]

"Do lado de cima temos filtros: posso filtrar por estado, por tipo
de instituição — federal, estadual, privada — e por modalidade.
Também tem busca por nome."

[FAZ UMA BUSCA — EX: DIGITA 'USP' E MOSTRA RESULTADO]

"Digitando 'USP', o mapa já filtra só as unidades da USP."

[AGORA VAI PRA FUNCIONALIDADE DE BUSCA POR ENDEREÇO]

"Essa é a funcionalidade que mais faz diferença e que não existe
nos portais oficiais. Aqui em cima eu posso digitar um endereço
ou CEP e o mapa vai até o local."

[DIGITA UM CEP — EX: '13083-970' (UNICAMP)]

"Vou digitar o CEP da Unicamp, em Campinas. O sistema consulta
a API gratuita do OpenStreetMap, acha as coordenadas e move
o mapa automaticamente.

O círculo verde mostra o raio de busca — 100 quilômetros.
Todas as IES dentro desse raio aparecem no mapa com a distância
em quilômetros calculada pela Fórmula de Haversine."

[MUDA O RAIO NO DROPDOWN]

"Se eu mudar o raio para 200 quilômetros, o círculo aumenta
e os marcadores atualizam na hora. Não precisa fazer nova busca."

[AUMENTA O RAIO, DEPOIS DIMINUI]

"Posso ir de 50 quilômetros até 500. Isso é útil pra quem quer
estudar perto de casa e não sabe o que tem disponível na região."

[NAVEGA PARA O DASHBOARD]

"Vamos agora pro dashboard estatístico. Aqui a plataforma mostra
os dados de forma consolidada."

[MOSTRA O DASHBOARD]

"Temos gráfico de IES por estado — São Paulo lidera com folga.
Gráfico de rosca por status jurídico — a maioria é federal.
As 15 áreas de conhecimento com mais programas.

E aqui um dado importante: a nota média da CAPES por estado.
Essa nota é calculada a partir dos conceitos reais dos cursos,
que vão de 1 a 7.

Lá no início do projeto, a gente usava uma nota fixa que vinha
do CSV. Durante o desenvolvimento, percebemos que era um bug
e corrigimos pra usar os dados reais. Agora São Paulo aparece
com média 4,94, Rio de Janeiro com 4,81, e assim por diante."

[NAVEGA PARA CONSULTA]

"Por último, a página de consulta. Aqui os dados estão em formato
de tabela, com filtros mais detalhados — posso filtrar por nota
mínima da CAPES, por exemplo."

[FAZ UMA CONSULTA]

"E tem o botão de exportar CSV. Isso permite que qualquer pessoa
baixe os dados e faça suas próprias análises."

[VOLTA BREVEMENTE PRO MAPA]


═══════════════════════════════════════════════
BLOCO 4 — Implementação e Comunidade (30 segundos)
═══════════════════════════════════════════════

[SLIDE COM INFO TÉCNICA]

"A plataforma foi feita em Django, com Leaflet.js pro mapa,
Bootstrap pra interface e Chart.js pros gráficos.
O código está todo público no GitHub.

Mostramos o protótipo pra colegas que estão pensando em fazer
pós-graduação. O feedback principal foi que a busca por CEP
e o raio de distância são o grande diferencial — ninguém
conhecia uma ferramenta que fizesse isso com dados oficiais.

O sistema está publicado e funcionando."


═══════════════════════════════════════════════
BLOCO 5 — Encerramento (30 segundos)
═══════════════════════════════════════════════

[VOLTA AO SLIDE DE TÍTULO]

"Esse foi o Projeto Integrador do Grupo 11.
A plataforma resolve o problema de fragmentação da informação
sobre pós-graduação no Brasil colocando tudo num mapa só.

Obrigado por assistir."


═══════════════════════════════════════════════
CHECKLIST DO QUE PRECISA ESTAR NA TELA
═══════════════════════════════════════════════

□ Slide inicial com nome do projeto + integrantes
□ Mapa com zoom mostrando pontos
□ Filtros funcionando (UF, status, modalidade)
□ Busca por CEP funcionando
□ Raio sendo alterado e atualizando marcadores
□ Dashboard com gráficos
□ Nota média CAPES por estado
□ Tabela de consulta
□ Exportação CSV
□ Slide do GitHub
□ Slide final de agradecimento


═══════════════════════════════════════════════
DICAS PRÁTICAS
═══════════════════════════════════════════════

- Use OBS Studio (gratuito) pra gravar a tela
- Grave o áudio junto, falando pausado e claro
- Não leia o roteiro — use como guia, fale naturalmente
- Faça um ensaio rápido antes de gravar (5 min)
- Se errar, continua e edita depois (ou regrava)
- Tempo ideal: 7 minutos
- Suba como "Não listado" no YouTube
- Coloque o link na tabela do relatório final
