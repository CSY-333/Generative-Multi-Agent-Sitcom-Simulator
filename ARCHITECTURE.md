# Neon Society: Generative Agent RPG 아키텍처 개요

Neon Society는 다중 에이전트가 공간을 이동하며 상호작용하는 시뮬레이터로, 인지 아키텍처, 시간·공간 시뮬레이션, 상태 스냅샷(DVR) 세 축을 중심으로 설계된다. 아래 내용은 핵심 엔진의 작동 원리를 정리한 것이다.

## 1. 인지 모델: Gemini 기반의 생각 엔진 (`geminiService.ts`)
- **컨텍스트 주입(Prompt Engineering)**: 에이전트의 성격(Traits), 목표(Goal), 현재 위치, 최근 기억(Memories), 주변 에이전트 정보를 페이로드에 포함해 모델이 일관된 자아와 상황 인식을 유지하도록 한다.
- **구조화된 출력(JSON)**: `responseMimeType: "application/json"`과 `responseSchema`를 지정해 항상 일정한 필드를 받는다.
  - `thought`: 에이전트의 속마음(마인드 뷰에 노출).
  - `action`: 이동 방향(`UP`/`DOWN`/`LEFT`/`RIGHT`/`STAY`).
  - `plan`: 단기 계획.
- **호출 간격 제어(THINK_INTERVAL)**: `ticksUntilNextThink`를 사용해 약 8틱마다 한 번만 “깊은 생각”을 수행하고, 그 사이에는 이전 계획을 따라 무작위/관성 이동으로 비용을 절감한다.

## 2. 시뮬레이션 루프: 틱(Tick) 기반 처리 (`App.tsx`)
- setInterval로 틱을 돌리며 매 틱마다 아래 순서로 처리한다.
  1) **공간 근접도 계산**: 모든 에이전트 좌표를 비교해 반경 1.5칸 이내에 상대가 있는지 확인.
  2) **사회적 상호작용**: 근접 시 두 에이전트를 대화 상태로 전환하고, Gemini가 두 성격/목표를 대조해 시트콤 스타일 대화 및 요약을 생성한다. 결과는 즉시 **기억 스트림**에 저장된다.
  3) **이동·인지 단계**: 대화 중이 아닌 에이전트는 `ticksUntilNextThink`를 소모하며 이동하고, 타이머가 0이 되면 다음 이동을 Gemini에 질의한다.
  4) **상태 스냅샷**: 모든 월드 상태(위치, 생각, 대화 기록)를 `history` 배열에 push한다.

## 3. 기억 시스템 (Memory Stream)
- **LRU 유지**: 컨텍스트 길이와 성능을 위해 최신 기억 20개만 보존한다.
- **중요도 스코어**: 각 기억에 1~10 중요도를 부여(대화 기본 7점)하여 향후 회상/가중치에 활용한다.

## 4. DVR 기능: 타임머신
- **상태 스냅샷**: 매 틱의 `WorldState`를 `history`에 복제해 저장한다.
- **DVR 모드**: 사용자가 슬라이더를 움직이면 시뮬레이션을 일시 정지하고 `worldState`를 선택한 스냅샷으로 교체해 과거 상태를 재현한다.

## 5. 안정성: Mock Mode (Local Brain)
- **콜 실패 대비**: Gemini 호출 실패(예: 429)나 Mock Mode 활성화 시 내부 규칙 기반(Random Walk + 템플릿 텍스트) 로직으로 즉시 전환해 시뮬레이션을 유지한다.

## 6. 시각화 (`WorldMap.tsx`)
- **20x20 그리드**를 CSS Grid로 그린 뒤 에이전트를 absolute 좌표 + transition으로 배치해 부드럽게 이동한다.
- **상태 아이콘**으로 TALKING/THINKING 등을 표시해 현재 행위를 직관적으로 보여준다.
