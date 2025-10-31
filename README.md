# Fofoquinha

Sistema de mensagens anônimas com análise de sentimento em tempo real.

## Objetivo

Permitir que pessoas recebam mensagens anônimas que são automaticamente classificadas quanto ao tom (positivo, neutro ou negativo). O sistema atribui um "score" para cada pessoa baseado nas mensagens recebidas, criando uma representação visual do sentimento geral através de cores, títulos e animações.

## Funcionamento

### Fluxo Principal

1. **Cadastro de Pessoas**: Admin cria perfis com nome e foto
2. **Envio de Mensagens**: Usuários escrevem mensagens anônimas (máx. 150 caracteres)
3. **Classificação Automática**: IA analisa o sentimento e atribui score (0-1)
4. **Visualização**: Mensagem aparece com cor correspondente ao sentimento
5. **Score Médio**: Perfil exibe média de todas as mensagens recebidas

### Arquitetura

**Backend (FastAPI + Python)**
- `models`: Estrutura das tabelas (Person, Message)
- `schemas`: Validação de dados (Pydantic)
- `repositories`: Acesso ao banco de dados (SQLite)
- `services`: Lógica de negócio
- `routers`: Endpoints da API
- `ai/inferir.py`: Classificação de sentimento
- `websocket_manager.py`: Conexões em tempo real

**Frontend (SvelteKit + TypeScript)**
- Página inicial: Lista de pessoas cadastradas
- Página de perfil: Visualização de mensagens e formulário
- Preview em tempo real: Score da mensagem enquanto digita (debounce 400ms)
- WebSocket: Atualização automática de mensagens e score médio

## Algoritmo de Classificação

### Metodologia

O sistema utiliza **Análise de Sentimento Supervisionada** com Machine Learning clássico. O modelo é treinado previamente com dados rotulados e depois usado para classificar mensagens em tempo real.

### Pipeline de Treinamento (`backend/app/ai/treinar.py`)

1. **Preparação de Dados**
   - Dataset: CSV com colunas `text` (mensagem) e `sentiment` (rótulo)
   - Classes: `positive`, `neutral`, `negative`

2. **Vetorização (Bag of Words)**
   - **CountVectorizer** converte texto em matriz numérica
   - Cria vocabulário de todas as palavras únicas do dataset
   - Cada mensagem vira um vetor de contagens de palavras
   - Exemplo: "oi amor" → [1, 0, 1, 0, ...] onde cada posição representa uma palavra do vocabulário
   - Resultado: Matriz esparsa (documento × palavra)

3. **Classificador (Naive Bayes Multinomial)**
   - Algoritmo probabilístico baseado no Teorema de Bayes
   - **Por que Naive Bayes?**
     - Eficiente para classificação de texto
     - Funciona bem com datasets pequenos/médios
     - Rápido para inferência em tempo real
   - Calcula P(classe|mensagem) para cada classe

4. **Serialização**
   - Pipeline completo (vetorizador + classificador) salvo como `sentiment_model.joblib`
   - Carregado uma vez na inicialização do servidor

### Pipeline de Inferência (`backend/app/ai/inferir.py`)

1. **Entrada**: String da mensagem

2. **Vetorização**: Texto convertido usando o CountVectorizer treinado
   - Mensagem é transformada no mesmo espaço vetorial do treinamento
   - Palavras desconhecidas são ignoradas

3. **Predição**: Modelo retorna probabilidades para cada classe
   ```python
   probabilities = model.predict_proba([message])[0]
   # Exemplo: {'positive': 0.7, 'neutral': 0.2, 'negative': 0.1}
   ```

4. **Conversão para Score Contínuo (0-1)**
   - Mapeia 3 classes discretas em escala contínua
   - Fórmula de gradiente linear:
   ```python
   score = (p_neutral * 0.5) + (p_negative * 1.0)
   ```
   - **Interpretação**:
     - `positive` contribui 0.0 (melhor)
     - `neutral` contribui 0.5 (meio termo)
     - `negative` contribui 1.0 (pior)
   - Exemplo: se modelo retorna 60% positive, 30% neutral, 10% negative:
     ```
     score = (0.3 * 0.5) + (0.1 * 1.0) = 0.15 + 0.1 = 0.25
     ```

5. **Saída**: Float entre 0.0 (totalmente positivo) e 1.0 (totalmente negativo)

### Títulos por Faixa
- **0 - 0.25**: Santo (verde)
- **0.25 - 0.4**: Bacana (verde-claro)
- **0.4 - 0.6**: Normal (branco)
- **0.6 - 0.75**: Babaca (vermelho-claro)
- **0.75 - 1.0**: Arrombado (vermelho)

### Efeitos Visuais
**Mensagens:**
- Gradiente verde→branco→vermelho
- Texto branco se score > 0.75 ou < 0.25
- Shake (tremor) se > 0.75
- Bounce (pulo) se < 0.25

**Foto de Perfil (WebSocket):**
- Flash vermelho + tremor violento (score > 0.75)
- Flash verde + bounce feliz (score < 0.25)

## Tecnologias

### Backend
- FastAPI (API REST + WebSocket)
- SQLModel/SQLAlchemy (ORM)
- SQLite (Banco de dados)
- scikit-learn + joblib (ML)
- Uvicorn (ASGI server)

### Frontend
- SvelteKit (Framework)
- TypeScript
- WebSocket API (tempo real)
- CSS Animations

## Execução

Na raiz do projeto:
```bash
start.bat
```

Ou:
```bash
.\start.ps1
```

**URLs:**
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Admin: http://localhost:5173/admin (senha: edson123)

## Estrutura de Dados

**Person**
- id, name, pfp_image
- average_score (calculado)

**Message**
- id, message, message_score (0-1), person_id
- Limite: 150 caracteres
- Exibição: Últimas 8 mensagens por pessoa

