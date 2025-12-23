# 🎯 Project Vision: Generative Agent RPG (Sitcom Simulator)

우리가 만들고자 하는 것은 단순한 챗봇이 아닌, **"스스로 생각하고 살아가는 작은 사회(Living World)"**입니다.

## 1. 핵심 컨셉 (Core Concept)
10명의 AI 에이전트가 주어진 성격(Traits)과 목표(Goal)를 가지고 20x20 크기의 지도 위에서 자유롭게 돌아다니며, 마주치면 대화하고 관계를 맺는 **"관찰형 시뮬레이션 게임"**입니다. 사용자는 이들의 삶을 신처럼 관조하거나 개입할 수 있습니다.

## 2. 주요 목표 (Key Objectives)

### 🌍 1. 공간과 시간의 시뮬레이션 (Spatial & Temporal)
- **2D World**: 에이전트는 좌표(x, y)를 가지며 매 턴마다 이동합니다.
- **Proximity Interaction**: 억지로 대화를 시키는 것이 아니라, **"길 가다 마주치면(반경 2칸 이내)"** 대화 그룹이 형성되고 이야기가 시작됩니다.
- **Auto-Play**: 사용자가 클릭하지 않아도 시간이 자동으로 흐르며 세상이 돌아갑니다.

### 🧠 2. 깊이 있는 인지 모델 (Deep Configuration)
- **Memory Stream**: 모든 경험은 벡터 DB(ChromaDB)에 저장되고, 관련성/최신성/중요도에 따라 회상됩니다.
- **Reflection & Planning**: 단순히 반응하는 것이 아니라, 과거를 회고(Reflection)하고 미래를 계획(Planning)하여 행동합니다.
- **Transparent Mind**: 사용자는 언제든 에이전트의 뇌를 열어(Debug Mode) 지금 무슨 생각을 하는지 볼 수 있습니다.

### ⏪ 3. 타임 트래블 (Time Travel)
- **DVR 기능**: 시뮬레이션의 과거 특정 시점으로 시간을 되돌려, 그때 그 에이전트가 **"왜 그런 말을 했는지"** 당시의 기억과 상태를 뜯어볼 수 있습니다.

### 🎮 4. 게임 같은 경험 (Gamification)
- **RPG UI**: 딱딱한 관리자 화면이 아닌, 네온 스타일의 다크 모드, 말풍선, 캐릭터 카드 등 게임 같은 몰입감을 제공합니다.
- **Mock Mode**: API 비용 걱정 없이 로직을 검증할 수 있는 가상 LLM 모드를 지원합니다.

## 3. 기술 스택 (Tech Stack)
- **UI/Engine**: Streamlit (Python) + Custom CSS/Layout
- **Brain**: OpenAI API (GPT-4) OR Mock LLM (Rule-based)
- **Memory**: ChromaDB (Vector Search)
- **Logic**: Pydantic (Data Validation), NetworkX (Graphs - planned)
