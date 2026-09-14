# LLM Agent Orchestration 핵심 개념 평가 — 2차 정답·해설

대상 문제지: [QUIZ.md](./QUIZ.md)

## 정답표

| 문항 | 정답 | 핵심 개념 |
| ---: | :---: | --- |
| 1 | ③ | LLM 기반 AI Agent |
| 2 | ① | Fixed Workflow |
| 3 | ④ | Structured Output 검증 |
| 4 | ② | Prompt의 지시·데이터 경계 |
| 5 | ③ | 공통 Provider 계약 |
| 6 | ① | 필수 정보 재질문 |
| 7 | ④ | Tool Allowlist |
| 8 | ② | MCP Tool과 Resource |
| 9 | ③ | MCP stdio 전송 |
| 10 | ① | RAG Chunk와 출처 |
| 11 | ④ | Embedding과 벡터 검색 |
| 12 | ② | RAG Cache |
| 13 | ③ | Memory·RAG·단기 상태 |
| 14 | ① | Redis와 PostgreSQL |
| 15 | ④ | 사용자 Memory 격리 |
| 16 | ② | 실패 관찰과 종료 조건 |
| 17 | ③ | LangGraph의 역할 |
| 18 | ① | 행동 위험도와 승인 |
| 19 | ④ | 승인 Snapshot과 중복 방지 |
| 20 | ② | 행동 평가와 Trace |

## 문항별 해설

### 1번 — 정답 ③

AI Agent의 핵심은 LLM 사용 여부만이 아니라 **LLM이 목표와 State를 바탕으로 다음 행동이나 종료를 선택하는 것**입니다. Backend는 Tool을 검증·실행하고 그 Result를 다음 판단에 반영합니다. 단일 생성은 일반 LLM 호출이고, 고정된 실행 순서는 Workflow입니다.

학습 근거: [LLM과 Agent](./01_llm-to-agent/README.md), [Workflow와 AI Agent](./06_agent-workflow/README.md)

### 2번 — 정답 ①

입력과 중간 결과에 상관없이 미리 정한 순서로 실행되므로 Fixed Workflow입니다. 조건 분기나 매 단계의 행동 재선택이 없습니다.

학습 근거: [Workflow와 AI Agent](./06_agent-workflow/README.md)

### 3번 — 정답 ④

JSON 파싱 성공은 데이터 형식을 읽을 수 있다는 뜻일 뿐입니다. Backend는 필드 타입, 값의 범위, 필수 필드, 추가 필드 정책을 Schema로 다시 검증해야 합니다. 값을 임의로 고치는 것은 사용자 의도를 왜곡할 수 있습니다.

학습 근거: [Prompt와 Structured Output](./02_prompt-and-structured-output/README.md)

### 4번 — 정답 ②

사용자 입력 안의 명령은 시스템이 따를 지시가 아니라 요약할 데이터입니다. 역할과 데이터 경계를 명확히 하고 입력 내부의 명령을 따르지 않도록 해야 합니다. 구분자는 방어의 한 요소이므로 Backend 권한 검사와 입력 검증을 대신하지 않습니다.

학습 근거: [구분자와 Prompt Injection](./02_prompt-and-structured-output/03_delimiters_and_prompt_injection.py)

### 5번 — 정답 ③

공통 요청·응답 Schema와 업무 규칙을 유지하고 Provider 차이를 Adapter에서 처리하면 호출 대상을 바꾸기 쉽습니다. Provider의 원본 출력은 형식이 다를 수 있으므로 정규화와 검증이 필요합니다.

학습 근거: [과정의 Provider 비교 원칙](./README.md), [Prompt와 Structured Output](./02_prompt-and-structured-output/README.md)

### 6번 — 정답 ①

필수 정보가 없으면 Agent가 값을 추측해 Tool을 실행해서는 안 됩니다. 출발일을 사용자에게 질문하고, 유효한 인자가 준비된 뒤 실행해야 합니다.

학습 근거: [Tool Use](./03_tool-use/README.md)

### 7번 — 정답 ④

Tool Call은 LLM의 제안이며 실행 권한이 아닙니다. Backend는 Tool 이름이 Allowlist에 포함되는지 확인하고, 허용되지 않은 요청은 실행하지 않은 채 Trace에 남겨야 합니다.

학습 근거: [Tool Use의 안전한 실행](./03_tool-use/README.md)

### 8번 — 정답 ②

호텔 검색은 조회 동작을 수행하므로 Tool이 적합합니다. 수하물 정책처럼 URI로 식별해 읽는 Context는 Resource로 제공할 수 있습니다. MCP는 두 기능을 설명·발견·호출하기 위한 규약입니다.

학습 근거: [MCP Tool과 Resource](./03_mcp/README.md)

### 9번 — 정답 ③

stdio 방식에서는 Client가 MCP Server를 자식 프로세스로 시작하고 표준 입력과 출력으로 JSON-RPC 메시지를 교환할 수 있습니다. 프로토콜이 표준 출력을 사용하므로 임의 로그를 섞으면 통신에 방해가 될 수 있습니다.

학습 근거: [MCP stdio 실행 흐름](./03_mcp/README.md)

### 10번 — 정답 ①

Chunk의 출처 Metadata는 검색 결과가 어느 문서에서 왔는지 추적하고 답변의 근거를 표시하는 데 사용됩니다. Chunking은 긴 문서를 검색 가능한 단위로 나누는 과정이며 원본의 모든 문맥을 자동으로 완벽하게 보존하지는 않습니다.

학습 근거: [RAG](./04_rag/README.md), [Document Chunk 예제](./04_rag/02_document_chunk.py)

### 11번 — 정답 ④

Embedding은 텍스트의 특징을 수치 벡터로 표현합니다. 이를 이용하면 단어가 정확히 일치하지 않아도 의미가 가까운 문서를 찾을 수 있습니다. Embedding 자체는 암호화나 접근 통제 수단이 아닙니다.

학습 근거: [RAG의 벡터 검색](./04_rag/README.md), [Vector Search 예제](./04_rag/04_vector_search.py)

### 12번 — 정답 ②

Cache는 같은 조건의 반복 요청에서 검색과 생성 비용을 줄일 수 있습니다. 정책 문서가 바뀌거나 TTL이 만료되는 상황을 고려해 Cache Key와 무효화 정책을 설계해야 합니다. Cache는 검색과 Grounding을 대신하지 않습니다.

학습 근거: [RAG Cache](./04_rag/README.md)

### 13번 — 정답 ③

사용자별 선호는 장기 Memory, 여러 사용자가 참고하는 정책은 RAG 문서, 현재 실행의 단계와 임시 결과는 단기 상태입니다. 저장소가 아니라 정보의 목적과 보관 기간을 기준으로 구분합니다.

학습 근거: [Memory의 네 가지 구분](./05_memory/README.md)

### 14번 — 정답 ①

이 과정에서는 TTL이 필요한 Session 상태에 Redis를, 장기 Memory에 PostgreSQL을 사용합니다. PostgreSQL에 저장했다고 모든 항목을 Prompt에 넣는 것은 아니며, 현재 질문과 관련된 안전한 Memory만 선택해야 합니다.

학습 근거: [Memory 저장소 비교](./05_memory/README.md)

### 15번 — 정답 ④

화면이나 요청 Body의 `user_id`는 조작될 수 있습니다. 운영 환경에서는 Backend가 인증된 Session이나 Token에서 확인한 사용자 ID로 조회·수정·삭제 범위를 제한해야 합니다.

학습 근거: [Memory의 사용자 식별과 격리](./05_memory/README.md)

### 16번 — 정답 ②

Agent는 Tool Result를 관찰해 State를 갱신한 뒤 다음 행동을 정해야 합니다. 실패 시에도 정책에 따라 재시도, 다른 Tool 사용 또는 중단을 결정하고, 최대 반복 횟수로 무한 Loop를 막아야 합니다.

학습 근거: [Agent Loop](./06_agent-workflow/README.md), [Rule-based Agent 예제](./06_agent-workflow/03_rule_based_agent_loop.py)

### 17번 — 정답 ③

LangGraph는 State, Node, Edge, Conditional Edge와 Loop로 실행 구조를 표현하는 Framework입니다. LangGraph 사용 자체가 AI Agent나 Multi-Agent를 의미하지 않으며, 권한과 승인 정책도 애플리케이션이 설계해야 합니다.

학습 근거: [LangGraph의 역할](./06_agent-workflow/README.md)

### 18번 — 정답 ①

이 과정에서는 읽기와 외부 변경 없는 초안을 자동 처리합니다. 캘린더 저장 같은 변경은 구체적인 승인 후 실행하고, 현재 Agent에 금지된 행동은 승인이 있어도 실행하지 않습니다.

학습 근거: [Human Approval과 행동 위험도](./07_human-approval-and-safety/README.md)

### 19번 — 정답 ④

승인은 Tool 이름이 아니라 구체적인 실행 대상에 연결됩니다. 날짜가 달라졌으므로 새 승인이 필요합니다. 같은 `run_id`의 처리가 완료된 경우에는 재전송으로 인한 중복 변경도 차단해야 합니다.

학습 근거: [승인 대상과 안전한 재개](./07_human-approval-and-safety/README.md)

### 20번 — 정답 ②

Agent가 실행됐다는 사실과 올바르게 행동했다는 사실은 다릅니다. 다양한 시나리오에 기대 Tool, Status와 Arguments를 정의해 실제 행동과 비교하고, 실패하면 Trace에서 최초 오류 지점을 찾아야 합니다. 수정 후에는 같은 시나리오로 회귀를 확인합니다.

학습 근거: [Agent Evaluation and Tracing](./08_agent-evaluation-and-tracing/README.md)
