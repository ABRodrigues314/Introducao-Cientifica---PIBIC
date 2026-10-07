# 🚀 30 Desafios para Dominar o opencode

> Trinta projetos de programação, em dificuldade crescente (de ~1.000 a ~100.000 linhas), desenhados para transformar quem **já sabe programar** em quem **domina o opencode** como ferramenta de engenharia de software assistida por IA.

---

## 📖 Sobre este repositório

Saber programar e saber **conduzir um agente de código** são habilidades diferentes. O segundo exige:

- especificar bem o que você quer (e o que você *não* quer);
- decompor problemas grandes em passos que o agente consegue executar com confiança;
- gerenciar o contexto (que é finito);
- verificar, revisar e corrigir o que o agente produz;
- automatizar o seu próprio fluxo de trabalho (comandos, agentes, permissões, scripts).

Cada um dos 30 desafios abaixo é um **projeto diferente**, e cada um carrega uma **meta de aprendizado do opencode** além da meta técnica. A ideia não é só "terminar o projeto", e sim terminá-lo **com método**.

**Nível de referência da dificuldade**

| Rótulo | O que significa aqui |
|---|---|
| **Média** | Média-alta, nível FGV EMAp: boa disciplina de graduação avançada (Algoritmos, Estatística, Aprendizado de Máquina, Estruturas de Dados). Exige raciocínio matemático/algorítmico, não só "juntar bibliotecas". |
| **Alta** | Nível Harvard: sistemas ou algoritmos em que o **design** é o difícil, com invariantes sutis, trade-offs e corretude não trivial. |
| **Altíssima** | Projeto de pesquisa/engenharia de equipe. Sem rede de segurança. |

> ⚠️ **Sobre as linhas de código:** as estimativas incluem testes, mas excluem código gerado, dependências e arquivos de dados. Use `cloc` para medir. Considere uma margem de ±30%. Se o seu projeto ficou bem menor porque o design ficou mais elegante, ótimo.

---

## 🗂️ Como usar

1. Crie uma pasta por desafio: `exercicios/01-algebra-linear/`, `exercicios/02-diff-simbolica/`, etc. Cada pasta é um repositório git independente (ou uma subpasta com histórico próprio).
2. Faça os desafios **em ordem**. As habilidades de opencode são cumulativas.
3. Em cada desafio:
   1. Leia o enunciado completo antes de abrir o opencode.
   2. Escreva (você mesmo) um `SPEC.md` curto com decisões de design.
   3. Rode `/init` e refine o `AGENTS.md`.
   4. Trabalhe em ciclos: **planejar → construir → verificar → commitar**.
   5. Ao terminar, preencha a retrospectiva (template abaixo) em `RETRO.md`.
4. Marque o checklist no fim deste arquivo.

### Linguagens
Cada desafio traz uma **stack sugerida**, mas você pode trocar. Recomendação: use **Python** nas fases iniciais para focar na ferramenta, e **Rust / Go / C++ / TypeScript** quando o desafio pedir desempenho ou tipagem forte.

---

## 🧭 Regras de ouro

1. **Você é o arquiteto, o agente é a equipe.** Decisões de design são suas. Delegue a execução.
2. **Especificação antes de código.** Use o modo *Plan* para discutir e só depois mude para *Build*.
3. **Commit a cada passo verde.** Git é o seu `Ctrl+Z` de longo prazo. `/undo` ajuda, mas não substitui commits.
4. **Testes são o contrato.** Peça testes junto (ou antes) do código, e rode-os sempre.
5. **Leia os diffs.** Código que você não entende é dívida técnica com juros altos.
6. **O `AGENTS.md` é um documento vivo.** Sempre que o agente errar duas vezes do mesmo jeito, registre a regra ali.
7. **Sessões curtas e focadas.** Contexto longo degrada qualidade. Use `/compact`, nova sessão e documentos de handoff.
8. **Registre o que funcionou.** Mantenha um `LOG.md` com prompts bons, armadilhas e descobertas.
9. **(Modo hardcore, opcional)** Não digite código de produção manualmente. Só edite à mão para depurar ou entender. O objetivo é dominar a ferramenta.

---

## 🛠️ Cheat sheet do opencode

> Os comandos e caminhos podem mudar entre versões. Confira sempre a documentação oficial em **https://opencode.ai/docs**.

| Recurso | Para que serve |
|---|---|
| `opencode` | Abre a interface de terminal (TUI) no diretório atual. |
| `/connect` | Configura o provedor/credenciais de modelo. |
| `/models` | Troca o modelo. Modelos mais fortes para planejar, mais rápidos para tarefas mecânicas. |
| `/init` | Analisa o projeto e cria/atualiza o `AGENTS.md` com instruções para o agente. |
| **Tab** | Alterna entre os agentes **Plan** (só lê/planeja) e **Build** (edita arquivos e roda comandos). |
| `@arquivo` | Referencia arquivos (busca fuzzy) no prompt. |
| `!comando` | Executa um comando de shell e leva a saída para a conversa. |
| `/undo` e `/redo` | Desfaz/refaz a última rodada de alterações do agente. |
| `/compact` | Resume a conversa para liberar contexto. |
| `/new`, `/sessions` | Nova sessão / retomar sessões anteriores. |
| `/share` | Gera link compartilhável da conversa. |
| `/export` | Exporta a conversa. |
| `opencode run "prompt"` | Modo não interativo, útil para scripts e CI. |
| `opencode serve` | Sobe o servidor headless para integrações. |
| `opencode.json` | Configuração do projeto: modelos, permissões, MCP servers, agentes, comandos. |
| `.opencode/` | Pasta para **comandos customizados** (markdown), **agentes customizados** e extras do projeto. |
| Subagentes | Agentes especializados invocados pelo agente principal (ex.: `@general`) ou criados por você. |
| MCP servers | Dão ferramentas externas ao agente (docs, banco de dados, browser, etc.). |
| Permissões | Controlam o que o agente pode fazer sem perguntar (`edit`, `bash`, `webfetch`, ...). |
| LSP | O opencode usa servidores de linguagem para dar feedback de tipos/erros ao agente. |

### Um fluxo de trabalho padrão

```text
1. Escrever SPEC.md (você)                       → o "o quê" e o "porquê"
2. /init + ajustar AGENTS.md                     → convenções, comandos de build/test
3. [Plan] "Proponha o plano de implementação em milestones"
4. Revisar e editar o plano (você)               → salve como PLAN.md
5. [Build] "Implemente o milestone 1 e rode os testes"
6. Ler o diff → rodar testes → git commit
7. Repetir 5-6. Ao poluir o contexto: /compact ou nova sessão
8. Atualizar AGENTS.md / LOG.md com o que aprendeu
```

### Template de retrospectiva (`RETRO.md`)

```markdown
# Retrospectiva — Desafio NN: <nome>

- Tempo total:
- Nº de sessões / modelos usados:
- Linhas finais (cloc):
- O que o agente fez muito bem:
- Onde o agente errou ou travou (e como destravei):
- O melhor prompt que escrevi:
- Uma regra que adicionei ao AGENTS.md por causa deste projeto:
- O que farei diferente no próximo desafio:
```

---

## 📊 Visão geral da progressão

| Fase | Desafios | Complexidade | Tamanho estimado | Foco no opencode |
|---|---|---|---|---|
| 1 | 01–06 | Média | ~1.000 linhas | Fundamentos: Plan vs Build, `AGENTS.md`, `@`, `/undo`, ciclos curtos |
| 2 | 07–12 | Média | ~5.000 linhas | Milestones, testes como contrato, comandos customizados |
| 3 | 13–18 | Alta | ~6.000 linhas | Spec-driven, TDD com agente, subagentes, verificação independente |
| 4 | 19–22 | Média | ~25.000 linhas | Arquitetura multi-módulo, gestão de contexto e sessões, MCP |
| 5 | 23–26 | Alta | ~25.000 linhas | Agentes customizados, permissões, trabalho paralelo, refatorações grandes |
| 6 | 27–30 | Média → Altíssima | ~100.000 linhas | Orquestração em escala, automação headless, CI, engenharia de longo prazo |

---

# 🟢 FASE 1 — Fundamentos (6 projetos · Média · ~1.000 linhas)

**Habilidades do opencode treinadas nesta fase:** alternar Plan/Build, escrever bons prompts, usar `@arquivo`, manter `AGENTS.md`, usar `/undo`, commitar a cada passo.

**Regra da fase:** o projeto cabe em poucas sessões. Se o contexto estourou, o seu prompt estava grande demais.

---

## 01 · Biblioteca de Álgebra Linear Numérica (sem NumPy)

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Python puro (NumPy só nos testes)

**O projeto.** Implemente do zero uma biblioteca de álgebra linear numérica com classes `Matrix` e `Vector`, focando em **estabilidade numérica**, não só em "dar o resultado".

**Requisitos**
- Operações básicas, transposição, norma (1, 2, ∞, Frobenius) e número de condição.
- Decomposição **LU com pivoteamento parcial**, **Cholesky** e **QR** (Householder).
- Resolução de sistemas lineares, inversa e determinante a partir das decomposições.
- Autovalores via **iteração QR com shifts** e **SVD** (Jacobi unilateral).
- Mínimos quadrados via QR e via SVD, com comparação de estabilidade em matrizes mal condicionadas (ex.: Hilbert).

**🎯 Foco no opencode.** Aprender o ciclo Plan → Build. No modo Plan, peça ao agente para **listar os riscos numéricos** antes de codificar. Use `/undo` deliberadamente pelo menos uma vez para sentir como ele funciona.

**✅ Critérios de aceite**
- Testes comparando com `numpy.linalg` com tolerâncias justificadas (documentadas).
- Um script mostrando o erro versus número de condição.
- `AGENTS.md` com comando de teste e convenções de estilo.

---

## 02 · Diferenciação Simbólica e Simplificador de Expressões

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Python, OCaml, Haskell ou Rust

**O projeto.** Um mini sistema de álgebra computacional: parseia expressões, constrói a AST, simplifica, deriva e exibe em texto e LaTeX.

**Requisitos**
- Parser com precedência e associatividade corretas (recursivo descendente ou Pratt).
- Funções: `sin`, `cos`, `exp`, `log`, potências, raízes e composições.
- Derivada simbólica (regra da cadeia, produto, quociente), derivadas parciais e gradiente.
- Simplificação por regras de reescrita até ponto fixo (`x*1 → x`, `x+0 → x`, constantes, fatoração simples).
- Saída em LaTeX e avaliação numérica; verificação por **diferenças finitas**.

**🎯 Foco no opencode.** Prompts com **exemplos de entrada/saída** (few-shot na especificação). Use `@arquivo` para pedir alterações cirúrgicas em módulos específicos.

**✅ Critérios de aceite**
- Testes baseados em propriedades (ex.: derivada simbólica ≈ derivada numérica em pontos aleatórios).
- Simplificador idempotente (`simplify(simplify(e)) == simplify(e)`), testado.

---

## 03 · Micro-framework de Autodiff e Redes Neurais

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Python (NumPy permitido)

**O projeto.** Um autodiff em modo reverso sobre tensores, com camadas e otimizadores, treinando redes pequenas.

**Requisitos**
- Grafo computacional dinâmico, `backward()` com acumulação de gradientes e broadcasting correto.
- Operações: `matmul`, ativações (ReLU, tanh, sigmoid, softmax), perdas (MSE, cross-entropy estável).
- Módulos `Linear`, `Sequential`, dropout, e otimizadores SGD (momentum) e Adam.
- Treino em dois datasets: `make_moons` e um subconjunto do MNIST.
- **Gradient checking** numérico para todas as operações.

**🎯 Foco no opencode.** Fazer o agente **escrever primeiro o gradient checker** e só depois cada operação. Observe como o agente reage a testes que falham.

**✅ Critérios de aceite**
- Todas as operações passam no gradient check (erro relativo < 1e-5 em float64).
- Acurácia ≥ 90% no subconjunto de MNIST escolhido.

---

## 04 · Motor de Busca com BM25 e Avaliação Quantitativa

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Python ou Go

**O projeto.** Indexador e buscador full-text com ranking probabilístico, mais um módulo de **avaliação de recuperação de informação**.

**Requisitos**
- Tokenização, normalização, remoção de stopwords e stemming (implemente um Porter simplificado).
- Índice invertido persistido em disco com compressão de postings (delta + variable-byte).
- Ranking **TF-IDF** e **BM25** (com parâmetros ajustáveis).
- Consultas booleanas (AND/OR/NOT), frases entre aspas e CLI.
- Avaliação: Precision@k, MAP e nDCG com um dataset pequeno e julgamentos de relevância (ex.: Cranfield).

**🎯 Foco no opencode.** Criar o seu **primeiro comando customizado** (ex.: `/avaliar`, que roda a avaliação e resume as métricas).

**✅ Critérios de aceite**
- Relatório comparando TF-IDF vs. BM25 no dataset, com a análise escrita por você.
- Índice recarregável sem reindexar.

---

## 05 · Biblioteca de MCMC com Diagnósticos de Convergência

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Python + NumPy + Matplotlib

**O projeto.** Amostradores MCMC e as ferramentas para saber **se eles funcionaram**.

**Requisitos**
- Metropolis-Hastings (com adaptação do passo), Gibbs e **Hamiltonian Monte Carlo** (leapfrog) com gradientes fornecidos pelo usuário.
- Múltiplas cadeias em paralelo.
- Diagnósticos: **R-hat**, **ESS** e autocorrelação, além de trace plots.
- Casos de teste: gaussiana multivariada correlacionada, "banana" de Rosenbrock, mistura bimodal e regressão logística bayesiana.
- Comparação de eficiência (ESS/segundo) entre os amostradores.

**🎯 Foco no opencode.** Aprender a **pedir verificação estatística** ao agente e a desconfiar dela: valide os resultados contra soluções analíticas conhecidas.

**✅ Critérios de aceite**
- Médias e covariâncias recuperadas dentro do erro de Monte Carlo esperado.
- Um relatório curto explicando onde o MH falha e o HMC funciona.

---

## 06 · Resolvedor SAT (DPLL → CDCL) e Aplicações

**Nível:** Média · **Tamanho:** ~1.000 linhas · **Stack sugerida:** Rust, C++ ou Python

**O projeto.** Um solver SAT que evolui de DPLL para CDCL, mais *encoders* que reduzem problemas reais a SAT.

**Requisitos**
- Parser DIMACS CNF.
- DPLL com propagação unitária e eliminação de literais puros.
- Evolução para **CDCL**: *watched literals*, análise de conflito (1-UIP), backjumping não cronológico e heurística VSIDS.
- Encoders: **Sudoku**, **N-rainhas** e coloração de grafos.
- Verificador independente do modelo retornado.

**🎯 Foco no opencode.** **Refatorar com segurança**: transforme o DPLL em CDCL em passos pequenos, sempre com a suíte verde. Pratique `git diff` + revisão + commit entre as rodadas.

**✅ Critérios de aceite**
- Resolve instâncias do SATLIB (ex.: `uf50`–`uf250`) em tempo razoável.
- Todo modelo retornado é validado pelo verificador.

---

# 🔵 FASE 2 — Projetos Médios (6 projetos · Média · ~5.000 linhas)

**Habilidades do opencode treinadas nesta fase:** decompor em **milestones**, `SPEC.md` + `PLAN.md`, testes como contrato, **comandos customizados** de rotina, `AGENTS.md` robusto, sessões separadas por módulo.

**Regra da fase:** nenhum prompt pode pedir "o projeto inteiro". Cada rodada entrega um milestone verificável.

---

## 07 · Banco de Dados Chave-Valor LSM-Tree

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Go ou Rust

**O projeto.** Um armazenamento chave-valor persistente no estilo LevelDB/RocksDB.

**Requisitos**
- **WAL** com recuperação após *crash*, **memtable** (skiplist) e **SSTables** imutáveis.
- *Bloom filters*, índice esparso e compressão por blocos.
- **Compaction** leveled (ou size-tiered), com iteradores *merge* e *snapshots*.
- API: `Put`, `Get`, `Delete`, `Scan(range)` e batch atômico.
- Teste de *crash injection*: matar o processo em pontos aleatórios e verificar a consistência.

**🎯 Foco no opencode.** Escreva um `PLAN.md` com 6–8 milestones e execute **um por sessão**. Crie o comando `/milestone`, que recebe o número do milestone e instrui o agente a ler `PLAN.md` e implementar só aquele.

**✅ Critérios de aceite**
- Teste *fuzz* comparando contra um `map` em memória (modelo de referência).
- Benchmark de escrita/leitura publicado no README do projeto.

---

## 08 · Framework de Backtesting de Estratégias Financeiras

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Python (pandas permitido)

**O projeto.** Um motor *event-driven* de backtest sem *look-ahead bias*, com relatórios.

**Requisitos**
- Ingestão de dados OHLCV (CSV/Parquet) e alinhamento de calendários.
- Engine orientada a eventos: dados → sinais → ordens → execuções (com **custos e *slippage***).
- Portfólio com posições, *margin* simples e rebalanceamento.
- Métricas: retorno, volatilidade, **Sharpe, Sortino, max drawdown, Calmar**, VaR histórico.
- **Walk-forward** e *purged cross-validation* para evitar vazamento de informação.
- Relatório HTML com gráficos e CLI.

**🎯 Foco no opencode.** Fazer o agente **auditar o próprio código** à procura de *look-ahead bias*, em uma sessão separada e limpa (revisor independente).

**✅ Critérios de aceite**
- Um teste que *prova* a ausência de look-ahead (ex.: alterar o futuro não muda decisões passadas).
- Três estratégias de exemplo (cruzamento de médias, mean reversion, momentum).

---

## 09 · Compilador + Máquina Virtual para uma Linguagem Imperativa

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Rust, OCaml, Go ou Java

**O projeto.** Projete uma linguagem pequena (variáveis, funções, recursão, arrays, closures simples) e implemente o pipeline completo até uma VM.

**Requisitos**
- *Lexer* e *parser* com recuperação de erros e mensagens com linha/coluna.
- **Verificador de tipos** (estático, com inferência local).
- Geração de **bytecode** e VM baseada em pilha (ou registradores).
- Coletor de lixo *mark-and-sweep*.
- REPL, `--dump-bytecode` e programas de exemplo (fibonacci, quicksort, N-rainhas).

**🎯 Foco no opencode.** **Desenvolvimento guiado por exemplos:** crie uma pasta `tests/programas/` com programas e saídas esperadas ANTES da implementação e deixe o agente trabalhar até tudo passar.

**✅ Critérios de aceite**
- Erros de tipo e de sintaxe com mensagens legíveis.
- Teste de estresse do GC (sem vazamentos nem *use-after-free* lógico).

---

## 10 · Biblioteca de Machine Learning Clássico "estilo scikit-learn"

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Python + NumPy (sem scikit-learn)

**O projeto.** Reimplemente o coração do ML clássico com uma API coerente (`fit`/`predict`/`transform`).

**Requisitos**
- Regressão linear (ridge/lasso), logística, **SVM linear** (SGD) e naive Bayes.
- **Árvores de decisão**, *random forest* e **gradient boosting**.
- **k-means++**, GMM (EM), **PCA** e t-SNE (versão simples).
- `Pipeline`, `GridSearchCV`, *k-fold* estratificado e métricas (ROC-AUC, F1, log-loss).
- Serialização de modelos.

**🎯 Foco no opencode.** Definir **convenções de API no `AGENTS.md`** para que o agente mantenha consistência entre dezenas de classes. Observe como regras escritas reduzem divergências.

**✅ Critérios de aceite**
- Cada estimador testado contra o scikit-learn em *datasets* reais (diferenças dentro de tolerância documentada).
- Documentação gerada a partir das *docstrings*.

---

## 11 · Sistema de Build com Cache por Conteúdo e Execução Paralela

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Go, Rust ou Python

**O projeto.** Um sistema de build (estilo Make/Bazel-lite) com DAG de tarefas.

**Requisitos**
- DSL declarativa de tarefas (YAML ou linguagem própria) com dependências e saídas.
- Ordenação topológica e detecção de ciclos com mensagem clara.
- **Cache por hash de conteúdo** (entradas + comando + ambiente) e *cache* remoto opcional via diretório compartilhado.
- Execução **paralela** com limite de *workers* e propagação correta de falhas.
- Modo `--watch` (rebuild incremental) e `--explain` (por que esta tarefa reconstruiu?).

**🎯 Foco no opencode.** **Concorrência é onde agentes mais erram.** Peça ao agente para escrever testes que forcem *race conditions* (`-race`, `loom`, ou repetição) e para explicar os invariantes.

**✅ Critérios de aceite**
- Builds reproduzíveis: mesma entrada → mesmo hash → *cache hit*.
- Teste com um grafo aleatório de 1.000 tarefas comparado com execução serial.

---

## 12 · Engine de Xadrez Compatível com UCI

**Nível:** Média · **Tamanho:** ~5.000 linhas · **Stack sugerida:** Rust, C++ ou Go

**O projeto.** Uma engine de xadrez completa que conversa com GUIs pelo protocolo UCI.

**Requisitos**
- Representação por **bitboards** e geração de lances legais (*magic bitboards* ou equivalente).
- Validação por **perft** em posições conhecidas.
- Busca: *iterative deepening*, **alpha-beta**, tabelas de transposição (Zobrist), *quiescence*, *null-move*, LMR e *move ordering*.
- Avaliação: material, tabelas peça-casa, estrutura de peões e segurança do rei.
- Protocolo UCI, controle de tempo e *opening book* simples.

**🎯 Foco no opencode.** **Loop de verificação objetiva:** o `perft` é a "verdade". Configure um comando customizado que roda o perft e devolve a primeira posição divergente, deixando o agente depurar sozinho.

**✅ Critérios de aceite**
- `perft` correto até a profundidade 6 nas posições-padrão (inclui *Kiwipete*).
- Mini torneio contra uma versão anterior da própria engine, mostrando ganho de Elo.

---

# 🟠 FASE 3 — Projetos de Alta Complexidade (6 projetos · Alta · ~6.000 linhas)

**Habilidades do opencode treinadas nesta fase:** desenvolvimento **spec-driven**, TDD com agente, **subagentes** para revisão independente, uso de **LSP/tipos** como feedback, prompts que exigem **provas e invariantes**, não só código.

**Regra da fase:** projetos pequenos em linhas, mas densos em ideias. Antes de qualquer código, escreva por você mesmo as **invariantes** do sistema em `SPEC.md`. O agente deve ser capaz de citá-las.

---

## 13 · Otimização Convexa: Simplex, Pontos Interiores e uma DSL de Modelagem

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** Python + NumPy, Julia ou Rust

**O projeto.** Um solver de programação linear e convexa com uma linguagem de modelagem no estilo CVXPY.

**Requisitos**
- **Simplex revisado** (duas fases, regra de Bland contra ciclagem) e **método de pontos interiores** primal-dual (preditor-corretor) para LP e QP.
- **ADMM** para problemas com estrutura separável (ex.: LASSO).
- DSL algébrica (`x = Variable(n)`, `minimize(...)`, `constraints`) com **verificação DCP** (*Disciplined Convex Programming*) e mensagens de erro úteis.
- Reformulação automática para a forma canônica do solver (*canonicalization*).
- Certificados de otimalidade: dualidade forte, folga complementar e *gap*.
- Detecção de infactibilidade/ilimitação, com certificados de Farkas.

**🎯 Foco no opencode.** Peça ao agente, no modo Plan, uma **lista de invariantes matemáticas** de cada algoritmo e **transforme-as em testes**. Depois use um subagente (ou sessão limpa) como revisor adversarial.

**✅ Critérios de aceite**
- Resultados idênticos (dentro da tolerância) aos do SciPy/CVXPY em ao menos 30 problemas, incluindo os da NETLIB (subconjunto).
- Teste de *fuzz*: LPs aleatórios cuja solução ótima é conhecida por construção.

---

## 14 · Linguagem de Programação Probabilística (PPL)

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** Python (com autodiff próprio ou JAX) ou Julia

**O projeto.** Uma PPL embutida: o usuário escreve o modelo generativo e o sistema infere a posteriori.

**Requisitos**
- Primitivas `sample`, `observe` e `factor`, com distribuições (Normal, Beta, Gamma, Bernoulli, Categórica, etc.).
- Execução de modelos por **rastros (traces)** e *effect handlers*.
- Inferência: *importance sampling*, **SMC** (filtro de partículas), **MCMC** (MH por traço) e **HMC/NUTS** com autodiff.
- **Inferência variacional** (ADVI) com *reparametrization trick*.
- Transformações de suporte (restrito → irrestrito) com Jacobianos corretos.
- Diagnósticos e *posterior predictive checks*.

**🎯 Foco no opencode.** **Corretude estatística é difícil de testar.** Use *Simulation-Based Calibration (SBC)* como teste de aceite e faça o agente implementá-lo. Registre no `AGENTS.md` as armadilhas encontradas.

**✅ Critérios de aceite**
- Cinco modelos clássicos (regressão, mistura, HMM, modelo hierárquico "oito escolas", processo de Poisson) com posteriores conferidas contra Stan/PyMC ou soluções analíticas.
- SBC passando para os modelos conjugados.

---

## 15 · Consenso Raft com Simulador Determinístico e Verificador de Linearizabilidade

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** Go, Rust ou Python

**O projeto.** Uma implementação do **Raft** testada não por "rodar na máquina", mas por um **simulador determinístico de rede** (estilo Jepsen/FoundationDB).

**Requisitos**
- Eleição de líder, replicação de log, *commit*, **snapshots/compaction**, e mudanças de configuração (*joint consensus* ou single-server).
- Máquina de estados replicada: um KV store com `Get/Put/CAS`.
- **Simulador**: relógio lógico, rede com atraso, perda, duplicação, reordenação e **partições**, injeção de *crashes* e reinícios, sempre reproduzíveis por *seed*.
- **Verificador de linearizabilidade** do histórico de operações (algoritmo estilo Wing & Gong/Porcupine).
- Checagem de invariantes do Raft (Election Safety, Log Matching, State Machine Safety).

**🎯 Foco no opencode.** Peça ao agente para **achar bugs com o simulador** (rodar milhares de *seeds*) e reproduzir cada um como teste de regressão. Treine o ciclo: *bug* → *seed* → teste → correção.

**✅ Critérios de aceite**
- 10.000 *seeds* com falhas agressivas sem violação de invariante nem de linearizabilidade.
- Documento mostrando ao menos um bug real que o simulador encontrou na sua própria implementação.

---

## 16 · Motor de Consultas SQL Colunar com Otimizador

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** Rust, C++, Go ou Java

**O projeto.** Um engine analítico em memória (estilo DuckDB-lite) com formato colunar próprio.

**Requisitos**
- Parser SQL (SELECT, JOIN, GROUP BY, HAVING, ORDER BY, LIMIT, subconsultas, CTEs, *window functions* básicas).
- Plano lógico → **otimizador** com regras (*predicate/projection pushdown*, reordenação de joins) e **modelo de custo** com estatísticas (histogramas).
- Execução **vetorizada** por lotes; joins *hash*, *sort-merge* e *nested loop*; agregações por hash.
- Formato de arquivo colunar com compressão (RLE, dicionário) e *zone maps*.
- `EXPLAIN` e `EXPLAIN ANALYZE`.

**🎯 Foco no opencode.** **Teste diferencial:** gere consultas aleatórias e compare os resultados com **SQLite** ou **DuckDB**. Peça ao agente para montar o gerador de consultas e interpretar as divergências.

**✅ Critérios de aceite**
- Mais de 1.000 consultas aleatórias idênticas ao SQLite.
- Pelo menos 10× mais rápido que a execução linha a linha da sua própria base em consultas analíticas (TPC-H subconjunto).

---

## 17 · Provador de Teoremas e Verificador de Programas (Lógica de Hoare)

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** OCaml, Haskell, Rust ou Python

**O projeto.** Um sistema de verificação formal em duas camadas: um provador automático para lógica de primeira ordem e um verificador de programas imperativos anotados.

**Requisitos**
- Lógica proposicional e de primeira ordem: parser, forma normal conjuntiva e **skolemização**.
- **Unificação** e **resolução** (com estratégias: *set of support*, subsunção).
- Linguagem imperativa com `requires/ensures/invariant`.
- Gerador de **condições de verificação** via *weakest precondition*.
- Backend: seu provador e (opcionalmente) integração com Z3 para comparação.
- Verificação de programas como busca binária, *insertion sort* e *gcd*, incluindo **terminação** (variantes).

**🎯 Foco no opencode.** **Verificar o verificador:** peça ao agente para escrever *testes de soundness* (nenhuma fórmula inválida deve ser "provada") usando contraexemplos gerados por força bruta em domínios pequenos.

**✅ Critérios de aceite**
- Provador resolve problemas do TPTP de dificuldade baixa/média.
- Programas incorretos (bug sutil em invariante) são rejeitados com contraexemplo.

---

## 18 · Transformer do Zero: Tokenizer BPE, Treino e Geração

**Nível:** Alta · **Tamanho:** ~6.000 linhas · **Stack sugerida:** Python + NumPy (ou Rust/C++ para o núcleo)

**O projeto.** Um modelo de linguagem estilo GPT construído sobre **seu próprio** autodiff e kernels, sem PyTorch/JAX.

**Requisitos**
- **Tokenizer BPE** treinável (a nível de bytes), com serialização.
- Autodiff tensorial com *broadcasting*, `matmul` em lote, LayerNorm, softmax estável e dropout.
- Bloco Transformer: *multi-head attention* causal, MLP, resíduos, **embeddings posicionais** (RoPE ou aprendidos).
- Treino: AdamW, *warmup + cosine decay*, *gradient clipping*, *checkpointing*.
- Geração: *temperature*, top-k/top-p e **KV cache**.
- Treinar num corpus pequeno (ex.: Shakespeare/contos em português) e plotar curvas de perda.

**🎯 Foco no opencode.** **Pensar em tensores com o agente:** peça documentação de *shapes* em cada função e testes de *shape/gradiente*. Rode experimentos longos em segundo plano via `!` e reporte as métricas para o agente analisar.

**✅ Critérios de aceite**
- Gradientes do modelo inteiro verificados numericamente em uma configuração minúscula.
- Perda de validação decrescente e amostras de texto coerentes no nível do corpus escolhido.
- Geração com KV cache idêntica à geração sem cache.

---

# 🟣 FASE 4 — Sistemas Grandes de Complexidade Média (4 projetos · Média · ~25.000 linhas)

**Habilidades do opencode treinadas nesta fase:** arquitetura **multi-módulo**, gestão agressiva de **contexto** (`/compact`, sessões por módulo, documentos de *handoff*), **MCP servers**, `AGENTS.md` hierárquico, `ADRs` (Architecture Decision Records) para o agente respeitar decisões passadas.

**Regra da fase:** nenhuma sessão deve tocar em mais de um ou dois módulos. Crie **contratos de interface** (tipos/APIs) antes das implementações.

---

## 19 · Plataforma Acadêmica Full-Stack (estilo "Moodle-lite")

**Nível:** Média · **Tamanho:** ~25.000 linhas · **Stack sugerida:** TypeScript (Node + React) ou Python (FastAPI) + frontend à escolha, PostgreSQL

**O projeto.** Um sistema de gestão de cursos, turmas, entregas e notas, com múltiplos perfis de usuário.

**Requisitos**
- Autenticação (JWT + *refresh*), **RBAC** (aluno, monitor, professor, admin) e auditoria.
- Cursos, turmas, matrículas, atividades, entregas (upload), correção e **boletim** com regras de média configuráveis.
- Fóruns/mural, notificações e fila de *jobs* (e-mails, correção automática de código).
- **Correção automática** de exercícios de programação em *sandbox* (container ou processo restrito).
- Migrações de banco, *seed data*, testes unitários, de integração e **e2e**.
- Documentação OpenAPI e pipeline de CI.

**🎯 Foco no opencode.** Configurar um **MCP server** útil (ex.: acesso ao esquema do banco ou à documentação das libs) e comparar a qualidade do código do agente com e sem ele. Mantenha `AGENTS.md` por pasta (`backend/`, `frontend/`).

**✅ Critérios de aceite**
- Cobertura de testes ≥ 70% no backend e fluxos críticos cobertos por e2e.
- Qualquer pessoa sobe o sistema inteiro com `docker compose up`.

---

## 20 · Plataforma Local de MLOps (tracking, registry e pipelines)

**Nível:** Média · **Tamanho:** ~25.000 linhas · **Stack sugerida:** Python (SDK/CLI/servidor) + frontend leve (React/HTMX)

**O projeto.** Uma alternativa enxuta ao MLflow + DVC + Airflow, rodando localmente.

**Requisitos**
- **Experiment tracking:** runs, parâmetros, métricas por passo, artefatos, tags e comparação entre runs.
- **Registry** de modelos com versões, estágios e *lineage* (dados → código → modelo).
- **Versionamento de dados** por hash de conteúdo, com *deduplicação*.
- **Pipelines** como DAG (decoradores Python), cache de etapas, execução local paralela e *retries*.
- **Serving** de modelos via API com *schema validation* e *shadow deploy*.
- UI web para explorar runs, gráficos e diffs entre experimentos; CLI completa.
- Detecção de *data drift* (PSI, KS) em dados de entrada.

**🎯 Foco no opencode.** Trabalhar em **monorepo com contratos**: defina `schemas/` primeiro e faça cada módulo (SDK, servidor, UI, CLI) consumir os mesmos tipos. Exercite o *handoff* entre sessões com um `STATUS.md` atualizado ao fim de cada uma.

**✅ Critérios de aceite**
- Reprodutibilidade: reexecutar um run antigo gera os mesmos artefatos (dado *seed* e dados versionados).
- Um projeto de ML real (ex.: previsão de séries temporais) rodando inteiro sobre a sua plataforma.

---

## 21 · Engine de Jogos 2D com ECS, Física e Editor

**Nível:** Média · **Tamanho:** ~25.000 linhas · **Stack sugerida:** Rust (wgpu/winit), C++ (SDL), ou TypeScript (WebGL/Canvas)

**O projeto.** Uma engine 2D reutilizável com um jogo de demonstração completo.

**Requisitos**
- **ECS** (*Entity-Component-System*) com armazenamento eficiente (*archetypes* ou *sparse sets*) e *queries* tipadas.
- Renderizador 2D com *batching*, atlas de sprites, câmera, camadas e partículas.
- **Física 2D**: broadphase (grade/BVH), colisões SAT, resolução de impulsos, atrito e *joints* simples.
- Sistema de cenas, **serialização** e *hot reload* de recursos.
- Scripting embutido (Lua ou uma mini-linguagem sua).
- **Editor de níveis** (GUI) com *undo/redo*.
- Áudio, entrada e *input mapping*.

**🎯 Foco no opencode.** **Visual não se testa só com `assert`:** monte um fluxo em que o agente gera *screenshots* determinísticos e compara com imagens de referência (*golden tests*). Aprenda a pedir ao agente para olhar o resultado e iterar.

**✅ Critérios de aceite**
- 10.000 entidades com física a 60 FPS em hardware comum.
- Um jogo jogável (plataforma, *shooter* ou puzzle) com 3 fases, feito com o editor.

---

## 22 · Editor de Texto Modal para Terminal com LSP e Syntax Highlighting

**Nível:** Média · **Tamanho:** ~25.000 linhas · **Stack sugerida:** Rust, Go ou C++ (TUI)

**O projeto.** Um editor no estilo Vim/Helix, com cliente LSP e extensibilidade.

**Requisitos**
- Estrutura de dados para texto: **rope** ou *piece table*, com desempenho em arquivos de centenas de MB.
- Modos (normal/insert/visual/comando), *motions*, *text objects*, macros, registradores e **undo tree**.
- *Syntax highlighting* incremental (gramáticas regulares próprias ou tree-sitter).
- **Cliente LSP** (JSON-RPC): diagnósticos, *completion*, *go-to-definition*, *hover* e *rename*.
- Múltiplos *buffers/splits/tabs*, busca com regex e *fuzzy finder* de arquivos.
- Sistema de **plugins/configuração** (Lua, WASM ou script próprio).

**🎯 Foco no opencode.** Use o próprio **opencode como cliente do seu editor**: integre-o ao fluxo (ex.: abrir o editor com `$EDITOR` a partir do opencode). Treine o uso de `opencode run` para tarefas automatizadas (ex.: gerar *testes de motion*).

**✅ Critérios de aceite**
- Abre e edita um arquivo de 200 MB sem travar a interface.
- Suíte de testes de *keystrokes → buffer final* com mais de 300 cenários.

---

# 🔴 FASE 5 — Sistemas Grandes de Alta Complexidade (4 projetos · Alta · ~25.000 linhas)

**Habilidades do opencode treinadas nesta fase:** **agentes customizados** (revisor, arquiteto, depurador), **permissões** finas em `opencode.json`, trabalho **paralelo** com `git worktree`, refatorações de larga escala guiadas por testes, **benchmarks** como juiz objetivo.

**Regra da fase:** configure o seu ambiente de agentes ANTES de começar: pelo menos um agente de *code review* somente leitura e um comando `/verificar` que roda toda a bateria de checagens.

---

## 23 · Biblioteca de Deep Learning (tensores, autodiff, kernels e treinamento)

**Nível:** Alta · **Tamanho:** ~25.000 linhas · **Stack sugerida:** C++/Rust (núcleo) + bindings Python, ou Python + Numba/Triton

**O projeto.** Um mini PyTorch/tinygrad com núcleo de alto desempenho.

**Requisitos**
- Tensor N-dimensional com *strides*, *views*, *broadcasting* e *dtypes*.
- **Autodiff** reverso com grafo dinâmico, *checkpointing* de ativações e *higher-order gradients* (ao menos para um subconjunto de operações).
- Kernels otimizados em CPU (SIMD, *blocking*, multithreading) para `matmul` e convolução; **fusão de operações** (*elementwise fusion*).
- Camadas: Linear, Conv2d, BatchNorm, LayerNorm, atenção, LSTM/GRU, embeddings.
- Otimizadores (SGD, Adam, AdamW, Lion), *schedulers*, *mixed precision* simulada e DataLoader com paralelismo.
- Serialização de modelos e **exemplos reproduzindo resultados** (ResNet pequena em CIFAR-10, um GPT pequeno).

**🎯 Foco no opencode.** Crie **dois agentes**: um *implementador* (edita) e um *revisor* (somente leitura, com permissões `edit: deny`). Use `git worktree` para tentar duas estratégias de otimização em paralelo e deixar o **benchmark** escolher a melhor.

**✅ Critérios de aceite**
- Todas as operações verificadas por *gradcheck* e por comparação com PyTorch.
- `matmul` dentro de um fator razoável (ex.: ≤ 3×) do BLAS de referência, com análise de *roofline* simples.

---

## 24 · Banco de Dados Relacional com MVCC, B+Tree e Recuperação ARIES

**Nível:** Alta · **Tamanho:** ~25.000 linhas · **Stack sugerida:** Rust, C++ ou Go

**O projeto.** Um SGBD relacional completo no estilo **BusTub/PostgreSQL-lite**, com transações ACID.

**Requisitos**
- Camada de armazenamento: páginas, **buffer pool** (LRU-K), *heap files* e **B+Tree** concorrente (*latch crabbing*).
- **WAL** e recuperação estilo **ARIES** (*analysis/redo/undo*, CLRs, *checkpoints* fuzzy).
- **MVCC** com *snapshot isolation* e, como extensão, **SSI** (*Serializable Snapshot Isolation*) ou 2PL com detecção de *deadlock*.
- SQL: parser, planner, otimizador básico, executores (Volcano), índices e *constraints*.
- Cliente e protocolo de rede simples (compatível com `psql` é bônus).
- Ferramenta de **testes de isolamento** (anomalias: *dirty read*, *write skew*, *lost update*).

**🎯 Foco no opencode.** **Refatoração grande e arriscada:** troque o 2PL por MVCC com o agente, usando a bateria de testes de isolamento como rede de segurança. Defina permissões em `opencode.json` para que comandos destrutivos peçam confirmação.

**✅ Critérios de aceite**
- Testes de *crash recovery* aleatórios: após qualquer falha, o estado converge ao esperado.
- Transações concorrentes passam em um teste estilo *Jepsen* local (ex.: *bank transfer* com invariante de soma).

---

## 25 · Compilador Otimizante para Linguagem Funcional (Hindley-Milner → SSA → Código)

**Nível:** Alta · **Tamanho:** ~25.000 linhas · **Stack sugerida:** OCaml, Haskell ou Rust

**O projeto.** Um compilador de uma linguagem estilo ML com tipos algébricos e *pattern matching*, gerando código nativo ou WebAssembly.

**Requisitos**
- **Inferência de tipos Hindley-Milner** com polimorfismo, *type classes* simples (ou módulos) e mensagens de erro de qualidade.
- ADTs, *pattern matching* com **verificação de exaustividade** e compilação eficiente de *matches* (árvores de decisão).
- Sistema de módulos simples e biblioteca padrão mínima.
- IRs em camadas: AST → *Core* → **ANF/CPS** → **SSA**.
- Otimizações: *inlining*, *constant folding*, **eliminação de código morto**, *common subexpression*, *tail-call optimization* e **otimização de closures** (*closure conversion*, *lambda lifting*).
- Backend: **WebAssembly** (ou x86-64/LLVM IR) e *runtime* com GC.
- Ferramentas: REPL, formatter e *language server* básico.

**🎯 Foco no opencode.** Escreva **ADRs** (`docs/adr/`) para cada decisão de IR e referencie-os no `AGENTS.md`. Observe como o agente respeita (ou viola) decisões documentadas. Pratique `/compact` e retomadas de sessão em fases longas.

**✅ Critérios de aceite**
- Teste diferencial: programas aleatórios (*QuickCheck*-like) dão o mesmo resultado no interpretador de referência e no código compilado, com e sem otimizações.
- Um conjunto de *benchmarks* mostrando ganho das otimizações.

---

## 26 · Plataforma de Busca Semântica e RAG com Índice ANN (HNSW)

**Nível:** Alta · **Tamanho:** ~25.000 linhas · **Stack sugerida:** Rust/C++/Go (núcleo) + Python (avaliação)

**O projeto.** Um sistema completo de recuperação: crawler, indexação híbrida (léxica + vetorial) e pipeline RAG avaliável.

**Requisitos**
- **Crawler** educado (robots.txt, *rate limit*, deduplicação por *simhash*) e *parsing* de HTML/PDF.
- Índice **léxico** (BM25, com *skip lists* e compressão) e índice **vetorial HNSW** próprio, com inserção/remoção, persistência e filtros por metadados.
- **Quantização** (PQ/scalar) para reduzir memória, e análise do *trade-off* recall × latência.
- *Chunking* inteligente, *embeddings* (via modelo local ou API) e **fusão híbrida** (RRF).
- **Reranking** e pipeline RAG com citações de fonte.
- Harness de **avaliação** (recall@k, nDCG, *faithfulness*, *answer relevance*) e relatórios.
- API HTTP, observabilidade (métricas e *tracing*).

**🎯 Foco no opencode.** **Experimentos guiados por métricas:** deixe o agente propor melhorias, mas só aceite o que **melhora a métrica no conjunto de validação**. Use `opencode run` em *scripts* para rodar *sweeps* de hiperparâmetros e resumir os resultados.

**✅ Critérios de aceite**
- Recall@10 do HNSW ≥ 95% frente à busca exata em 1M de vetores, com latência p95 documentada.
- Relatório mostrando o ganho da busca híbrida sobre cada método isolado.

---

# ⚫ FASE 6 — Projetos Monumentais (4 projetos · ~100.000 linhas)

**Habilidades do opencode treinadas nesta fase:** **orquestração em escala** (dezenas de sessões coordenadas por documentos), **automação headless** (`opencode run`/`serve`), integração com **CI e GitHub**, engenharia de longo prazo: **arquitetura evolutiva, dívida técnica, observabilidade do próprio processo**.

**Regras da fase**
- **Cada projeto tem de ser conduzido como um programa de engenharia:** `ARCHITECTURE.md`, `ROADMAP.md` com milestones, ADRs, `AGENTS.md` por subsistema e um `STATUS.md` de *handoff*.
- **Nunca peça "faça o projeto".** Cada sessão tem uma tarefa com critério de aceite objetivo.
- **Invista cedo em infraestrutura de verificação:** testes diferenciais, *fuzzing*, *benchmarks* e CI vêm **antes** das *features*.
- 100k linhas por agente só é viável se a arquitetura for **modular e fortemente testada**. Se o projeto estiver ficando intratável, o problema é de arquitetura, não de prompt.
- Aceite escopo menor: o critério final é a **qualidade da base e a capacidade de evoluí-la**, não o número de linhas.

---

## 27 · Plataforma de Business Intelligence Self-Service (estilo Metabase)

**Nível:** Média · **Tamanho:** ~100.000 linhas · **Stack sugerida:** TypeScript/Go/Python + React, PostgreSQL

**O projeto.** Uma plataforma de BI multiusuário que se conecta a bancos de dados de terceiros e permite explorar dados sem escrever SQL.

**Requisitos**
- **Conectores** para múltiplos SGBDs (PostgreSQL, MySQL, SQLite, BigQuery-like via interface comum) e CSV/Parquet.
- **Construtor de consultas visual** que compila para SQL por dialeto, com *joins* automáticos por chaves estrangeiras.
- **Dashboards** com dezenas de tipos de gráficos, filtros cruzados, *drill-down* e exportação.
- Camada semântica (métricas e dimensões reutilizáveis), **cache** e agendamento de atualizações.
- Multi-tenant, **RBAC**, permissões a nível de linha/coluna, SSO (OIDC/SAML).
- Alertas, relatórios agendados por e-mail e *embedding* de dashboards.
- **Assistente de linguagem natural → SQL**, com validação e execução segura.
- Observabilidade, **migrações**, importação/exportação de configuração e documentação de API.

**🎯 Foco no opencode.** **Coordenar muitas sessões:** organize o trabalho em *épicos* com um `ROADMAP.md`; use `opencode run` em um script para rodar tarefas repetitivas (ex.: gerar conectores/dialetos a partir de um *template*). Compare resultados entre modelos com tarefas idênticas.

**✅ Critérios de aceite**
- Testes de integração contra ao menos 3 bancos reais (via containers), e e2e do fluxo "conectar → explorar → dashboard → compartilhar".
- Teste de segurança: nenhuma consulta de um usuário vaza linhas fora de suas permissões (teste de propriedade).

---

## 28 · Motor de Processamento Distribuído (estilo Spark)

**Nível:** Alta · **Tamanho:** ~100.000 linhas · **Stack sugerida:** Rust, Go, Scala ou Java

**O projeto.** Uma plataforma de processamento de dados em *cluster* com APIs de alto nível.

**Requisitos**
- **Cluster manager**: *driver*, *workers*, registro, *heartbeats*, alocação de recursos e **tolerância a falhas** (reexecução por *lineage*).
- **Scheduler de DAG** com *stages*, **shuffle** distribuído (hash e sort-based, com *spill* em disco) e *speculative execution*.
- **API DataFrame** e **SQL** sobre o seu engine colunar (reaproveite ideias do desafio 16), com otimizador de consultas e **execução adaptativa**.
- Formatos de arquivo (CSV, Parquet-like), particionamento e **predicate pushdown**.
- **Streaming** (micro-batch) com janelas, *watermarks* e semântica *exactly-once* via *checkpointing*.
- Biblioteca de ML distribuído (regressão, k-means, ALS) sobre o engine.
- Gerenciamento de memória, *serialization* eficiente, UI de monitoramento e *job history*.
- Suporte a UDFs.

**🎯 Foco no opencode.** **Integração com CI e GitHub:** configure um fluxo em que *pull requests* disparam testes e revisão automatizada via opencode em modo não interativo. Faça **sessões de revisão adversarial** em subsistemas críticos (scheduler, shuffle).

**✅ Critérios de aceite**
- Simulador de falhas: matar *workers* aleatoriamente durante um TPC-H não altera o resultado final.
- Escalabilidade demonstrada (ganho de velocidade com mais *workers*) em *benchmark* reproduzível, e resultados idênticos a um engine de referência.

---

## 29 · Ecossistema Completo de uma Linguagem de Programação

**Nível:** Alta · **Tamanho:** ~100.000 linhas · **Stack sugerida:** Rust, C++ ou Zig

**O projeto.** Não apenas um compilador, e sim **o ecossistema inteiro** de uma linguagem moderna de sistemas/aplicações.

**Requisitos**
- **Linguagem** com sistema de tipos rico (genéricos, *traits/interfaces*, ADTs, **ownership/borrowing** ou GC opcional), módulos e macros higiênicas.
- Compilador com **IR de múltiplos níveis**, otimizações (*inlining*, SROA, *loop opts*) e **backends**: *interpretador/JIT* e **código nativo** (x86-64/ARM64 via LLVM ou próprio) e/ou WebAssembly.
- **Runtime**: GC (geracional ou concorrente), *threads*/*async*, FFI.
- **Biblioteca padrão**: coleções, strings/Unicode, I/O, rede, JSON, regex, concorrência.
- **Ferramentas**: gerenciador de pacotes com resolução de dependências (SAT/PubGrub), *formatter*, **LSP completo**, *linter*, gerador de documentação, **depurador** (DWARF) e *test runner*.
- **Especificação** da linguagem e *test suite* de conformidade.
- Um conjunto de **programas reais** escritos na linguagem (ex.: servidor HTTP, o próprio formatter reescrito nela).

**🎯 Foco no opencode.** **Gestão de dívida técnica:** programe *sprints* de refatoração explícitos. Use agentes customizados (arquiteto, revisor de *soundness*, escritor de testes de conformidade) e **automatize o regression testing** com `opencode run` + CI.

**✅ Critérios de aceite**
- Autocompilação parcial (*bootstrapping*) ou ao menos uma ferramenta real escrita na própria linguagem.
- *Fuzzing* contínuo do *parser* e do verificador de tipos sem *crashes*, e testes diferenciais entre backends.

---

## 30 · Sistema Operacional Unix-like para RISC-V (Altíssima complexidade)

**Nível:** **Altíssima** · **Tamanho:** ~100.000 linhas · **Stack sugerida:** Rust (ou C) + assembly RISC-V, rodando em QEMU

**O projeto.** Um sistema operacional do zero, com **kernel, drivers, sistema de arquivos, rede e espaço de usuário**, capaz de rodar programas reais.

**Requisitos**
- **Boot** (firmware/SBI, *early init*), **gerenciamento de memória** (paginação Sv39/Sv48, alocador físico *buddy*, *slab*, *copy-on-write*, *demand paging*, `mmap`).
- **Processos e threads**, *scheduler* **SMP** preemptivo (com prioridades/CFS-like), *syscalls*, sinais e IPC (pipes, sockets Unix, *shared memory*).
- **Sistema de arquivos**: camada **VFS**, um FS com *journaling* (estilo ext4/xv6-log estendido), *page cache* e *devfs/procfs*.
- **Drivers** *virtio* (bloco, rede, console, GPU opcional), *interrupt controller* (PLIC), temporizadores e *UART*.
- **Pilha de rede TCP/IP** própria (ARP, IPv4, ICMP, UDP, **TCP** com controle de congestionamento), *sockets* e DHCP/DNS cliente.
- **Espaço de usuário**: *libc* mínima, *shell* com *pipes*/redirecionamento/*job control*, utilitários (`ls`, `cat`, `grep`, `ps`…), e um **editor** simples.
- **Port de programas reais** (um mini compilador C, um servidor HTTP) rodando sobre o seu SO.
- **Infraestrutura de depuração**: GDB stub, *tracing*, *panic* com *backtrace*, *test harness* em QEMU e **fuzzing de syscalls**.
- *Security basics*: modo usuário/supervisor isolados, *capabilities* ou permissões, ASLR/NX.

**🎯 Foco no opencode.** **Autonomia com guarda-corpos.** Em um domínio onde um erro derruba tudo silenciosamente, a estratégia é: *harness* de testes em QEMU com saída serial determinística, **logs estruturados** que o agente consiga ler, permissões restritas em `opencode.json` e um agente depurador que usa GDB/*traces*. Use `git worktree` para explorar subsistemas em paralelo (rede, FS, memória) e **integre via PRs revisados**.

**✅ Critérios de aceite**
- Boot automatizado no CI (QEMU) e suíte de testes de integração que roda os utilitários em espaço de usuário.
- `iperf`-like entre duas instâncias do SO e entre o SO e o host; um programa C compilado dentro do próprio SO executando com sucesso.
- Teste de estresse de *fork/exec/mmap/IO* por horas sem *panic*, com SMP ativo.

---

# ✅ Checklist de progresso

| # | Projeto | Fase | Concluído | Retro escrita |
|---|---|---|---|---|
| 01 | Álgebra Linear Numérica | 1 | ☐ | ☐ |
| 02 | Diferenciação Simbólica | 1 | ☐ | ☐ |
| 03 | Autodiff e Redes Neurais | 1 | ☐ | ☐ |
| 04 | Motor de Busca BM25 | 1 | ☐ | ☐ |
| 05 | Biblioteca MCMC | 1 | ☐ | ☐ |
| 06 | Solver SAT (CDCL) | 1 | ☐ | ☐ |
| 07 | KV Store LSM-Tree | 2 | ☐ | ☐ |
| 08 | Backtesting Financeiro | 2 | ☐ | ☐ |
| 09 | Compilador + VM | 2 | ☐ | ☐ |
| 10 | ML Clássico "scikit-learn" | 2 | ☐ | ☐ |
| 11 | Sistema de Build | 2 | ☐ | ☐ |
| 12 | Engine de Xadrez UCI | 2 | ☐ | ☐ |
| 13 | Otimização Convexa + DSL | 3 | ☐ | ☐ |
| 14 | Linguagem Probabilística | 3 | ☐ | ☐ |
| 15 | Raft + Simulador | 3 | ☐ | ☐ |
| 16 | SQL Colunar | 3 | ☐ | ☐ |
| 17 | Provador + Lógica de Hoare | 3 | ☐ | ☐ |
| 18 | Transformer do Zero | 3 | ☐ | ☐ |
| 19 | Plataforma Acadêmica | 4 | ☐ | ☐ |
| 20 | Plataforma MLOps | 4 | ☐ | ☐ |
| 21 | Engine de Jogos 2D | 4 | ☐ | ☐ |
| 22 | Editor Modal com LSP | 4 | ☐ | ☐ |
| 23 | Biblioteca de Deep Learning | 5 | ☐ | ☐ |
| 24 | SGBD com MVCC e ARIES | 5 | ☐ | ☐ |
| 25 | Compilador Funcional Otimizante | 5 | ☐ | ☐ |
| 26 | Busca Semântica e RAG (HNSW) | 5 | ☐ | ☐ |
| 27 | Plataforma de BI | 6 | ☐ | ☐ |
| 28 | Processamento Distribuído | 6 | ☐ | ☐ |
| 29 | Ecossistema de Linguagem | 6 | ☐ | ☐ |
| 30 | Sistema Operacional RISC-V | 6 | ☐ | ☐ |

---

## 🧪 Rubrica de autoavaliação (por projeto)

Pontue de 0 a 5 e registre em `RETRO.md`:

| Critério | Pergunta |
|---|---|
| **Corretude** | Os critérios de aceite passam? Há testes que provam isso? |
| **Compreensão** | Consigo explicar cada módulo e decisão de design sem olhar o código? |
| **Condução do agente** | Decompus bem as tarefas? Detectei os erros dele? Registrei o que aprendi no `AGENTS.md`? |
| **Verificação** | Usei testes, *fuzzing*, *benchmarks* e revisão independente, em vez de "parece certo"? |
| **Qualidade** | O código é legível, modular e sem duplicação? |
| **Documentação** | Alguém roda e entende o projeto só pelo README e pelos ADRs? |

> 💡 **Dica final:** a ordem é uma sugestão, não uma lei, mas **não pule as fases iniciais**. Os projetos pequenos treinam exatamente o fluxo (planejar → construir → verificar → commitar) que vai sustentar os gigantes. Bons commits! 🚀
