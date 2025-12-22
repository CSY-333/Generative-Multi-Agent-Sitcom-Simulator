PRD v1.0 (상세): Generative Multi-Agent Sitcom Simulator (MVP)
0. 문서 목적

본 PRD는 2-Agent 대화 시뮬레이터를 Generative Agents 핵심 로직(기억·반성·계획) 기반으로 구현하는 MVP 사양서다.

목표는 “그럴싸한 대화”가 아니라, 왜 그런 발화가 나왔는지 설명 가능한 시스템을 만드는 것이다.

1. 목표 및 비목표
1.1 목표 (Goals)

두 에이전트가 턴 기반으로 대화하며, 각 턴마다:

관련 기억을 검색하고

(조건부) 반성을 생성하고

계획을 세우고

발화를 생성하고

(조건부) 기억을 저장한다.

UI에서 각 발화에 대해:

어떤 기억이 검색됐는지

최종 스코어(유사도/최신성/중요도 가중)

반성/계획이 무엇이었는지
를 확인할 수 있다.

실행 재현성(부분적):

동일한 설정 + 동일한 seed(선택)일 때 유사한 흐름이 나오도록 구조를 설계한다.

importance는 캐시로 안정화한다.

1.2 비목표 (Non-goals)

3명 이상 에이전트, 공간 내 이동/경로 계획, 정교한 감정 모델, RL/학습, 외부 툴(브라우저/파일) 사용

대규모 장기 운영(수만 메모리) 최적화

프로덕션 배포/권한/멀티유저

2. 사용자(페르소나) & 사용 시나리오
2.1 사용자

연구/엔지니어링 포트폴리오 제작자

멀티에이전트 아키텍처 데모를 만들고 싶은 지원자

“설명 가능성”을 강조해야 하는 발표자

2.2 핵심 시나리오 (Happy Path)

사용자가 사이드바에서 철수/영희 프로필을 입력

“Reset & Initialize”로 초기 메모리/DB 생성

“Run 1 Turn”을 여러 번 눌러 대화 진행

각 메시지 아래 Debug Expander를 열어:

Retrieval 결과(Top-k), score breakdown, reflection/plan 확인

필요 시 “Export Session”으로 로그/대화/메모리 스냅샷 저장

3. 사용자 경험(UX) 요구사항
3.1 화면 구성

Sidebar

Agent A: name / traits / goal

Agent B: name / traits / goal

Model 설정: model_name, temperature

Memory 설정: k, topN, weights(w_sim,w_rec,w_imp), reflection_period

버튼: Reset, Run 1 Turn, Run N Turns(선택), Export

Main

Chat transcript (말풍선 형태, 좌/우)

각 턴 메시지 아래:

Debug Expander: Retrieved Memories, Reflection, Plan, Score breakdown, Store decision

3.2 UX 제약

Streamlit rerun 특성상 상태는 전부 st.session_state에 유지해야 한다.

“Run N Turns”는 느려질 수 있으므로 MVP에서는 기본적으로 “Run 1 Turn” 중심.

4. 시스템 구성 요소 (Modules)
4.1 파일/모듈 구조 (제안)
project/
  app.py
  models.py
  memory_stream.py
  agent.py
  prompts.py
  scoring.py
  utils.py
  config.py
  storage/
    chroma/
  exports/
    sessions/
  tests/
    test_scoring.py
    test_memory.py
    test_agent.py

5. 데이터 모델 (models.py)
5.1 Memory (단일 기억 단위)

필드:

id: str (uuid4)

content: str

memory_type: Literal["observation","reflection","plan"]

created_at: datetime

importance: int (1~10)

source: Optional[str] (e.g., “agent_said”, “agent_reflection”)

tags: list[str] (선택: goal 관련 키워드)

embedding: Optional[list[float]] (저장 필요 시)

검증 규칙:

content 길이 제한(예: 1~2000 chars)

importance 범위 1~10 강제

5.2 AgentProfile

name: str

traits: str (최소 20자 권장)

goal: str (한 문장 권장)

5.3 AgentState

turn_index: int

current_context: str (최근 대화 요약/상황)

last_plan: Optional[str]

last_utterance: Optional[str]

mood_hint: Optional[str] (MVP optional; 단순 텍스트)

5.4 TurnRecord (UI 디버그용)

turn_id: str

speaker: str

listener: str

context_in: str

retrieved: list[ScoredMemory]

reflection: Optional[str]

plan: str

utterance: str

store_events: list[StoreEvent]

timestamps: dict

5.5 ScoredMemory / StoreEvent

ScoredMemory: memory + similarity + recency_score + importance_score + final_score

StoreEvent: memory_type, content, importance, stored(bool), reason

6. 기억 시스템 설계 (memory_stream.py + scoring.py)
6.1 저장소 요구사항

ChromaDB 로컬 영구 저장(디렉토리 지정)

collection 이름은 에이전트별로 분리:

memories_agent_{name}

저장되는 metadata:

memory_type

created_at(timestamp)

importance

source

6.2 Importance 산정 (중요)

LLM 전권 금지. MVP 규칙:

importance_rule_score(text): 1~10

사건성 키워드(“결정”, “약속”, “실수”, “고백”) +2

감정 키워드(“화남”, “기쁨”, “불안”) +1

goal 단어 포함 +2

사람 이름/관계 단서 +1

기본값 3, 상한 10

(선택) LLM 보정은 “옵션”으로만:

temperature=0

output 스키마 고정(JSON)

캐시 키: sha256(text) → importance 저장

6.3 Retrieval 파이프라인 (2-Stage)

입력: query, 파라미터: topN=20, k=5

Vector search: ChromaDB에서 topN

Re-rank:

similarity: (Chroma distance → similarity 변환 필요)

recency_score:

age_hours = (now - created_at).total_seconds()/3600

예: recency = exp(-age_hours / tau) 형태 권장(0~1)

importance_score:

importance_norm = (importance - 1) / 9 (0~1)

final_score:

final = w_sim*sim + w_rec*rec + w_imp*imp


출력: 상위 k개의 ScoredMemory

6.4 스토어 정책 (Noise 방지)

Observation 저장:

기본: 모든 발화를 저장하지 않음

저장 조건(예시):

importance_rule_score >= 6

또는 “새로운 사실/약속/갈등” 감지

Reflection 저장:

항상 저장 (단, 짧게)

Plan 저장:

기본은 저장하지 않음 (선택 옵션)

7. 에이전트 인지 구조 (agent.py + prompts.py)
7.1 Agent 초기화

입력:

profile: AgentProfile

state: AgentState

memory_stream: MemoryStream

llm_client: OpenAI wrapper (단순화)

7.2 Turn Loop: run_step()

입력:

context: (현재 상황 텍스트; UI가 유지)

other_agent_name

recent_dialogue: 최근 N턴 transcript(선택)

출력:

TurnRecord

단계 A: Query 구성

query = f"{context}\n상대:{other_agent_name}\n내 목표:{goal}"

goal을 query에 넣어 retrieval이 “목표 지향”이 되게 함

단계 B: Retrieve

scored_memories = memory_stream.retrieve(query)

단계 C: Reflect (조건부)

reflection_period = 6 (기본)

if turn_index % reflection_period == 0:

입력: 최근 observation 일부 + retrieved 요약

출력: reflection 1~3문장

저장: memory_type="reflection", importance=7(고정 또는 규칙)

단계 D: Plan

입력: profile + context + reflection + top memories

출력: plan 한 문장 (행동 지향)

단계 E: Act (Utterance)

입력: system 프롬프트(페르소나), developer(규칙), user(상황+계획+기억)

출력: utterance 1~2문장

금지: 장문 독백, 메타발언(“나는 AI라서…”)

단계 F: Store

store observation 후보:

“내 발화” + “상대 발화(최근)” 중 중요 이벤트만

store_events 기록(왜 저장/왜 미저장)

8. 프롬프트 설계 (prompts.py)
8.1 시스템 프롬프트(고정)

너는 {name}이다.

traits를 지켜 말투/성격 유지

목표(goal)를 의식적으로 추구

말은 1~2문장, 자연어

메타 발언 금지

안전/혐오/불법 지침 포함

8.2 플래너 프롬프트

“다음 턴에서 달성할 구체 행동을 한 문장으로”

JSON 출력(optional): { "plan": "..." }

8.3 리플렉션 프롬프트

최근 관찰/대화 요약을 바탕으로:

핵심 1~3개를 추려 교훈화

감정/관계/목표 진행을 짧게 정리

JSON 출력(optional)

8.4 임포턴스 보정 프롬프트(옵션)

입력 텍스트를 보고 1~10 점수

출력은 JSON 스키마 고정

temperature=0 고정

9. 앱 동작(상태 관리) (app.py)
9.1 세션 상태 키

session_state.agents: dict[name] -> Agent

session_state.transcript: list[TurnRecord]

session_state.turn_idx: int

session_state.config: weights, k, topN, reflection_period

session_state.db_paths: chroma directory

9.2 버튼 동작

Reset:

transcript 초기화

chroma collection 초기화(또는 새 collection suffix)

turn_idx=0

Run 1 Turn:

speaker = A if turn_idx even else B

listener = other

context = summarize(transcript last N) or simple concat

record = speaker.run_step(...)

transcript append

turn_idx += 1

Export:

transcript를 JSON으로 저장

memory snapshot(선택)

10. 로깅 & 디버깅 요구사항
10.1 로그 레벨

INFO: turn 시작/끝, 저장 이벤트 수, 토큰/시간

DEBUG: retrieval topN raw + rerank 점수표

ERROR: API 실패, rate limit, parsing 실패

10.2 UI 디버그 표시(반드시)

Retrieved memories 테이블:

content(앞 120자)

type, importance, age, sim, rec, imp, final

Reflection 텍스트

Plan 텍스트

Store events(저장 여부 + 이유)

11. 에러/예외 처리
11.1 OpenAI 실패

재시도 1~2회(지수 백오프)

실패 시:

utterance를 “(잠시 생각이 끊겼다…)” 같은 placeholder로 처리하고, 다음 턴 진행 가능하게 유지

UI에 에러 표시

11.2 임베딩 실패/DB 실패

DB 생성 실패 시: in-memory fallback(리스트 + sklearn cosine) 옵션(정말 최후)

메모리 저장은 실패해도 대화는 지속

11.3 JSON 파싱 실패

“자유 텍스트” fallback

하지만 reflection/plan은 길이 제한으로 강제

12. 보안/비용/성능
12.1 키 관리

OPENAI_API_KEY는 환경변수에서만

UI에 키 입력 받지 않음(권장)

12.2 비용 제어

각 턴 호출:

act 1회 필수

plan 1회(가능하면 act에 포함해 1회로 줄일 수도 있음)

reflection은 주기적(예: 6턴마다)

임베딩은 저장 이벤트 발생 시에만

12.3 성능 목표

Run 1 Turn 평균 2~6초(네트워크에 따라)

topN=20, k=5 기본

13. 테스트 계획 (tests/)
13.1 단위 테스트

scoring:

recency 함수 값 범위(0~1)

final_score 가중치 합산 검증

importance:

규칙 기반 점수 예제 고정

캐시 적용 여부

memory_stream:

add/retrieve 호출 시 메타데이터 포함 여부

13.2 통합 테스트(간단)

3턴 실행 후 transcript 길이=3

각 턴에 retrieved 길이=k

reflection_period 도달 시 reflection 생성 확인

14. 수용 기준 (Acceptance Criteria)
필수

앱이 streamlit run app.py로 실행된다.

최소 10턴 대화가 누적된다.

각 턴에 Debug Expander가 존재하고, score breakdown이 보인다.

reflection이 주기적으로 생성되어 저장된다.

observation은 조건부 저장으로 noise가 억제된다.

실패로 간주

발화는 나오는데 “왜 그런지”가 UI에서 추적 불가

기억이 무한히 쌓여 retrieval이 랜덤처럼 보임

importance가 매번 흔들려 재현성 붕괴

15. 구현 순서(권장)

models.py (Memory/TurnRecord)

scoring.py (recency/final score)

memory_stream.py (Chroma + rerank)

agent.py (retrieve→plan→act→store; reflection은 후순위)

app.py (턴 기반 UI)

reflection 추가 + export + 테스트

16. “재밌는 요소” 체크리스트 (요청 반영)

 Debug Expander로 “왜 그런 말” 공개

 Reflection으로 캐릭터 성장/변화 연출

 Plan 공개로 “머릿속” 연출

 기억 점수표(랭킹)로 엔지니어링 재미

 무한 저장 방지로 시스템이 무너지지 않게 함