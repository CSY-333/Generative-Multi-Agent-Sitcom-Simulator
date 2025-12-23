---
marp: true
theme: default
paginate: true
backgroundColor: #0a0e27
color: #e0e0e0
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  section {
    font-family: 'Inter', 'Malgun Gothic', sans-serif;
    font-size: 24px;
    line-height: 1.6;
    letter-spacing: -0.02em;
    color: #e0e0e0;
    background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
    padding: 60px 80px;
  }

  /* Headings with Gradient */
  h1 { 
    font-size: 56px; 
    font-weight: 800;
    background: linear-gradient(120deg, #00d9ff 0%, #a855f7 50%, #ff006e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.4em 0;
    letter-spacing: -0.03em;
  }

  h2 { 
    font-size: 36px; 
    font-weight: 700;
    color: #00d9ff;
    margin: 0.8em 0 0.3em 0;
    border-left: 4px solid #00d9ff;
    padding-left: 20px;
  }

  h3 { 
    font-size: 28px; 
    font-weight: 600;
    color: #a855f7;
    margin: 0.5em 0 0.25em 0;
  }

  /* Lists with custom bullets */
  ul { 
    margin: 0.5em 0; 
    padding-left: 1.5em;
  }

  li { 
    margin: 0.3em 0;
    position: relative;
  }

  li::marker {
    color: #00d9ff;
  }

  /* Code blocks - Cyberpunk style */
  code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85em;
    color: #ff006e;
    background: rgba(255, 0, 110, 0.1);
    border: 1px solid rgba(255, 0, 110, 0.3);
    border-radius: 4px;
    padding: 3px 8px;
  }

  pre {
    margin: 1em 0;
    border-radius: 12px;
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(0, 217, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
  }

  pre code {
    font-size: 0.75em;
    line-height: 1.5;
    padding: 20px;
    display: block;
    background: transparent;
    color: #06ffa5;
    border: none;
  }

  /* Blockquotes - Neon alert style */
  blockquote {
    font-size: 22px;
    font-style: italic;
    color: #00d9ff;
    border-left: 4px solid #00d9ff;
    background: rgba(0, 217, 255, 0.05);
    padding: 16px 20px;
    margin: 0.8em 0;
    border-radius: 0 8px 8px 0;
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.1);
  }

  /* Tables - Modern glass style */
  table { 
    font-size: 20px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    overflow: hidden;
    backdrop-filter: blur(10px);
  }

  th {
    background: linear-gradient(135deg, #00d9ff 0%, #8338ec 100%);
    color: white;
    font-weight: 600;
    padding: 12px 16px;
  }

  td {
    padding: 10px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  /* Custom classes */
  .muted { 
    color: #6b7785;
    font-size: 0.9em;
  }

  .tight { 
    line-height: 1.3;
  }

  .pill {
    display: inline-block;
    padding: 6px 16px;
    border: 2px solid #00d9ff;
    border-radius: 999px;
    font-size: 18px;
    color: #00d9ff;
    background: rgba(0, 217, 255, 0.1);
    font-weight: 600;
    box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
  }

  .highlight {
    background: linear-gradient(120deg, rgba(255, 0, 110, 0.2), rgba(168, 85, 247, 0.2));
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
  }

  /* Lead slide - Special cover style */
  section.lead {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #1a1a2e 100%);
  }

  section.lead h1 {
    font-size: 72px;
    margin-bottom: 0.2em;
  }

  section.lead h3 {
    font-size: 32px;
    color: #a855f7;
  }

  /* Page numbers */
  section::after {
    color: #6b7785;
    font-size: 16px;
    text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
  }

  /* Emphasis - Neon glow */
  strong {
    color: #ff006e;
    font-weight: 700;
  }

  em {
    color: #00d9ff;
    font-style: normal;
    font-weight: 600;
  }
---

<!-- _class: lead -->

# Multi-Agent Sitcom Simulator

### Demo-first MVP (Explainable Conversation)

**Goal:** “그럴싸한 대화”가 아니라 **“왜 저 말이 나왔는지”가 보이는 데모**

---

## 오늘 데모에서 보여줄 것 (3가지)

- **1) Speaker Selection**: 누가 말할지 자동 결정
- **2) Memory Retrieval**: 어떤 기억을 꺼냈는지 확인
- **3) Traceability UI**: “근거(기억/점수/계획)”을 말풍선 아래에서 공개

> 관객이 믿어야 하는 건 대사가 아니라 **근거**입니다.

---

## 데모 흐름 (운영자 체크리스트)

1. 사이드바에서 **에이전트 4명** 로드 (미리 프리셋)
2. `Run 1 Turn`을 **3번** 눌러 대화 생성
3. 각 메시지 아래 `Debug Expander` 열기
4. `Export`로 세션 로그 저장

<div class="muted">※ 10명도 가능하지만 데모는 4명이 제일 깔끔합니다.</div>

---

## 화면 구성: 관객이 보는 것

| 영역           | 관객이 체감하는 가치                  |
| :------------- | :------------------------------------ |
| Sidebar        | 설정이 “원인”, 결과가 “대화”로 연결됨 |
| Main Chat      | 시트콤처럼 자연스럽게 흘러감          |
| Debug Expander | **왜 저 말이 나왔는지** 공개          |
| Controls       | Reset / Run 1 Turn / Export           |

---

## 0) 준비: 에이전트 프리셋 (4명 권장)

- A: 갈등 유발(목표: 이슈 던지기)
- B: 중재(목표: 합의/정리)
- C: 농담(목표: 분위기 전환)
- D: 사실 확인(목표: 검증/반박)

<div class="muted">프리셋은 “성격”보다 “목표” 차이를 크게 두는 게 시연에 유리합니다.</div>

---

## 1) Controls: 데모에서 누를 버튼 3개

- `Reset` : 세션 초기화 (관객 앞에서 깔끔하게 시작)
- `Run 1 Turn` : **1스텝 실행** (시연의 리듬 유지)
- `Export` : 결과 저장 (재현 가능성 어필)

> “한 번에 길게 돌리기”는 데모에서 거의 항상 망합니다.

---

## 2) Speaker Selection: “누가 말하나?”가 핵심

### 의도

- 대화가 순번이 아니라 **상황 기반으로 진행**
- “말해야 할 이유”를 점수로 공개

### Debug에서 보여줄 것

- 후보 에이전트별 **speaker score**
- 선택된 에이전트의 **selection rationale (1~2줄)**

---

## Speaker Selection: 점수 예시 (UI에 표시)

| Agent | Score 구성                     | 최종 |
| :---- | :----------------------------- | ---: |
| A     | urgency + goal-fit             | 0.78 |
| B     | coherence + conflict-reduction | 0.72 |
| C     | novelty + timing               | 0.55 |
| D     | verification trigger           | 0.61 |

<div class="muted">※ 숫자가 정확할 필요는 없고, “왜 선택됐는지”가 보여야 합니다.</div>

---

## 3) Memory Retrieval: “무슨 기억을 꺼냈나?”

### Retrieval 원칙

- 현재 상황(Query)과 기억을 매칭해서 Top-k 반환
- **최종 점수**로 랭킹하고 UI에 공개

$$
Score = w_{sim}\cdot Sim + w_{rec}\cdot Rec + w_{imp}\cdot Imp
$$

---

## Memory Score 구성(관객용 한 줄 버전)

- **Sim**: 지금 상황과 비슷한가?
- **Rec**: 최근인가?
- **Imp**: 중요한 사건인가?

> 대화가 아니라 **검색 결과**가 설득력을 만듭니다.

---

## 4) Debug Expander: 이 데모의 ‘킬 스위치’

각 메시지 아래에 아래 4개를 고정으로 보여줍니다.

1. **Retrieved Memories (Top-k)**
2. **Scores**: Sim/Rec/Imp + 최종 점수
3. **Plan**: 다음 행동 계획(한 줄)
4. **Why this utterance**: 발화 선택 근거(한 줄)

<div class="muted">관객은 긴 설명을 안 읽습니다. “짧은 근거”가 필요합니다.</div>

---

## Debug Expander: 출력 포맷 예시

```text
[Plan]
- Defuse conflict, summarize stakes, propose next topic.

[Retrieved Top-3]
1) (0.82) "A와 B가 지난번에 예산 문제로 충돌함"  [Imp:9, Rec:0.63]
2) (0.77) "D는 사실 검증을 선호함"              [Imp:6, Rec:0.91]
3) (0.69) "C는 갈등 직후 농담으로 전환함"        [Imp:5, Rec:0.58]

[Why]
- Selected: B (coherence high) / Use #1 to reference conflict safely
```
