# 06 Stateful Weather MCP Deployment

05 Weather MCP Agent에 PostgreSQL 영구 이력과 Redis 진행 상태·날씨 Cache를 추가한
완성형 상태 기반 배포 프로젝트입니다. 인프라는 한 번 준비하고 Application만 반복 배포합니다.

## 학습 목표와 05와의 차이

| 구분 | 05 Stateless | 06 Stateful |
| --- | --- | --- |
| 실행 진행 상태 | 저장하지 않음 | Redis에 저장하고 Frontend가 Polling |
| 같은 날씨 재조회 | 매번 MCP 호출 | Redis Cache 사용(기본 600초) |
| 완료 이력 | 저장하지 않음 | PostgreSQL에 영구 저장 |
| Compose | 하나 | Infrastructure와 Application 분리 |
| 재배포 | 전체 실행 가능 | Application만 교체하고 데이터 유지 |

이 과정의 핵심은 Redis와 PostgreSQL의 역할을 구분하는 것입니다. Redis에는 자주 읽지만 오래
보관할 필요가 없는 진행 상태와 Cache를 저장하고, PostgreSQL에는 운영 이력으로 남겨야 하는
완료 결과를 저장합니다.

```text
Browser → Frontend → Backend Agent → Weather MCP → Open-Meteo
                         ├→ Redis: 진행 상태·날씨 Cache
                         ├→ PostgreSQL: 완료 실행 이력
                         └→ OpenAI 또는 Gemini
```

## 시나리오

사용자가 “서울 내일 날씨와 옷차림을 알려 줘”라고 입력합니다. Backend Agent는 MCP의
`get_weather` Tool로 실제 날씨 근거를 가져온 뒤 Cloud LLM이 답변을 만듭니다. Tool 결과 없이
온도·강수 정보를 만들어 내지 않습니다.

## 범위

| 포함 | 제외 |
| --- | --- |
| OpenAI 또는 Gemini, Open-Meteo, MCP | Ollama |
| PostgreSQL 실행 이력·Redis 상태와 Cache | Worker Queue, Multi-Agent |
| Health Check, CI, EC2 배포 | 실제 예약·결제 |

PostgreSQL·Redis·MCP는 외부에 공개하지 않습니다. CI는 실제 저장소 대신 Fake Store를
사용하며, CD는 인프라 Container를 재시작하지 않고 Application만 교체합니다.

## 구현 순서

1. Backend·MCP·Frontend 구현
2. 로컬 Compose와 Health Check
3. CI: Test·Application Compose 검사·Image Build
4. 05에서 사용한 EC2와 Docker 실행 환경 재사용
5. 05 Application을 직접 확인한 뒤 중지
6. EC2 자원과 06 전용 `.env.docker` 준비
7. production 승인형 GitHub Actions로 Application 자동 배포
8. Application 재배포 후 PostgreSQL·Redis 상태 보존 검증

## 프로젝트 구조

```text
backend/app.py              Weather Agent API, MCP Client, Cloud LLM
backend/Dockerfile
frontend/app.py             왼쪽 메뉴가 있는 Streamlit 화면
frontend/Dockerfile
mcp_server/server.py        Open-Meteo get_weather MCP Tool
mcp_server/Dockerfile
database/init.sql           실행 이력 Schema와 Table
compose.infrastructure.yml 로컬 전용 PostgreSQL·Redis·Volume, CI/CD에서 제외
compose.application.yml    Frontend·Backend·MCP와 Network 생성
backend/.dockerignore       Build Context에서 제외할 파일
frontend/.dockerignore
mcp_server/.dockerignore
.env.example                로컬 Infrastructure Compose 값
.env.docker.example         Application Container 환경 Template
.github/workflows/07-weather-stateful-cicd.yml (저장소 루트) CI와 CD
```

환경 파일은 두 개로 나뉩니다. `.env`는 로컬에서만 쓰는 `compose.infrastructure.yml`의
PostgreSQL 계정 값이고, `.env.docker`는 Application Container가 받는 환경 변수입니다.
Redis와 PostgreSQL은 CI와 CD에서 실행하지 않고 `.env.docker`의 접속 URL로만 연결합니다.

## 1단계: 실행 준비

### 사전 확인

Docker Desktop을 실행하고 다음 명령이 정상인지 확인합니다.

```powershell
docker version
docker compose version
Get-NetTCPConnection -LocalPort 8000,8501 -ErrorAction SilentlyContinue
```

출력이 있는 Port는 `docker ps`로 어떤 Container가 사용하는지 확인합니다. Database와 Redis는
Host Port를 공개하지 않으므로 기존 Host의 `5432`, `6379`와 충돌하지 않습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment
Copy-Item .env.example .env
Copy-Item .env.docker.example .env.docker
```

`.env.docker`에 사용할 Provider의 API Key를 입력합니다. OpenAI와 Gemini를 모두 사용할 경우
두 Key를 모두 설정합니다. 이 파일은 Git과 Image에 포함되지 않습니다.

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
```

`DATABASE_URL`과 `REDIS_URL`은 Template에서 비어 있습니다. 저장소를 어디에 두는지에 따라
값을 직접 입력합니다. 로컬 Container를 쓸 때의 `database`, `redis`, `weather-mcp`는 Compose
서비스 이름입니다. Container 안에서 `127.0.0.1`로 바꾸면 자기 자신을 가리키므로 연결되지
않습니다.

```ini
# 로컬 compose.infrastructure.yml을 사용할 때
DATABASE_URL=postgresql://postgres:postgres@database:5432/agent_db
REDIS_URL=redis://redis:6379/0

# 관리형 PostgreSQL·Redis를 사용할 때
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
REDIS_URL=rediss://:<password>@<host>:6380/0
```

```ini
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
WEATHER_CACHE_TTL_SECONDS=600
```

두 URL이 비어 있으면 `/health/ready`가 503을 돌려주므로 Frontend Container도 기동하지
않습니다. 값을 먼저 채운 뒤 Application을 실행합니다. 두 파일이 Git에 포함되지 않는지
`git check-ignore .env .env.docker`로 확인합니다.

## 2단계: Infrastructure 최초 실행 (로컬 전용)

이 단계는 로컬 실습에서만 사용합니다. CI와 CD는 `compose.infrastructure.yml`을 실행하지
않으며, 서버에서는 `.env.docker`에 입력한 관리형 PostgreSQL·Redis URL을 사용합니다.
관리형 저장소로 바로 실습한다면 이 단계를 건너뛰고 3단계로 갑니다.

```powershell
docker compose -f .\compose.infrastructure.yml config --quiet
docker compose -f .\compose.infrastructure.yml up -d
docker compose -f .\compose.infrastructure.yml ps
```

PostgreSQL과 Redis는 `weather-stateful` Network에 연결되고 각 Volume에 데이터를 유지합니다.

두 서비스가 `healthy`가 될 때까지 기다립니다. 최초 실행 시 새 PostgreSQL Volume에만
`database/init.sql`이 자동 적용되어 `weather_agent.runs` Table이 생성됩니다. 기존 Volume에는
Container를 재시작해도 초기화 SQL이 다시 실행되지 않습니다.

## 3단계: Application 실행

```powershell
docker compose -f .\compose.application.yml config --quiet
docker compose -f .\compose.application.yml up -d --build
docker compose -f .\compose.application.yml ps
```

Application Compose가 `weather-stateful` Network를 직접 만듭니다. Infrastructure Compose가
먼저 실행되어 같은 이름의 Network를 만들어 둔 경우에는 그것을 그대로 사용하며, 다른
Project가 만들었다는 경고만 출력하고 동작에는 문제가 없습니다.

접속 주소:

| 대상 | 주소 | 공개 여부 |
| --- | --- | --- |
| Frontend | `http://127.0.0.1:8501` | Browser에 공개 |
| Backend 문서 | `http://127.0.0.1:8000/docs` | 로컬 확인용 |
| Backend Readiness | `http://127.0.0.1:8000/health/ready` | 로컬 확인용 |
| Weather MCP | `http://weather-mcp:8010/mcp` | Docker 내부 전용 |
| PostgreSQL | `database:5432` | Docker 내부 전용 |
| Redis | `redis:6379` | Docker 내부 전용 |

코드나 `.env.docker`를 수정한 뒤에는 Container를 다시 만듭니다.

```powershell
docker compose -f .\compose.application.yml up -d --build --force-recreate weather-mcp backend frontend
```

이 명령은 Database·Redis Container와 Volume을 재생성하지 않습니다.

## 4단계: 상태 기반 기능 실습

### 화면 실습 순서

1. `http://127.0.0.1:8501`을 열고 도시 `서울`, 날짜 `내일`을 선택합니다.
2. 실행 버튼을 누르고 Progress Bar와 현재 단계가 변하는지 확인합니다.
3. 최종 답변과 MCP Tool Result의 온도·강수 정보를 비교합니다.
4. 실행 이력 화면에서 PostgreSQL에 저장된 완료 기록을 확인합니다.
5. 같은 도시·날짜를 다시 실행하여 Redis Cache 사용 표시를 확인합니다.

Frontend가 Agent 단계를 실행하는 것은 아닙니다. Backend에 실행을 요청한 뒤 실행 ID를 받아
상태 API를 주기적으로 조회합니다. 첫 요청은 MCP와 Open-Meteo를 호출하고, 같은 Cache Key의
두 번째 요청은 TTL이 남아 있으면 Redis 결과를 사용합니다. LLM 답변과 실행 이력은 두 요청
모두 새로 생성됩니다.

### 상태를 직접 확인하기

Backend Process 생존과 의존 서비스 준비 상태를 구분합니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

Liveness가 성공해도 Readiness는 MCP·PostgreSQL·Schema·Redis 중 하나가 실패하면 실패할 수
있습니다. API 전체 목록은 `http://127.0.0.1:8000/docs`에서 확인합니다.

PostgreSQL 실행 이력을 직접 조회합니다.

```powershell
docker compose -f .\compose.infrastructure.yml exec database psql -U postgres -d agent_db -c "SELECT run_id, city, day, provider, model, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"
```

Redis가 가진 날씨 관련 Key도 확인할 수 있습니다.

```powershell
docker compose -f .\compose.infrastructure.yml exec redis redis-cli --scan --pattern "weather:*"
```

`FLUSHALL`은 다른 실습 데이터까지 삭제할 수 있으므로 사용하지 않습니다.

### Schema가 없을 때

기존 Volume이 `init.sql` 추가 전에 만들어졌다면 다음 명령으로 SQL을 적용합니다.

```powershell
Get-Content .\database\init.sql | docker compose -f .\compose.infrastructure.yml exec -T database psql -U postgres -d agent_db
docker compose -f .\compose.application.yml up -d --build --force-recreate backend frontend
```

운영에서는 초기화 SQL을 반복 실행하기보다 버전이 기록되는 Migration 도구를 사용합니다.

### 로컬 실행에서 자주 발생하는 오류

| 증상 | 확인 | 해결 방향 |
| --- | --- | --- |
| Backend가 DB·Redis에 연결 못 함 | `.env.docker`의 두 URL | 빈 값이면 접속 URL 입력 |
| Backend가 healthy가 되지 않음 | Application의 Backend 로그 | MCP·DB·Redis Readiness 확인 |
| Database Schema가 false | PostgreSQL 직접 조회 | 위 초기화 SQL 적용 |
| 진행률이 멈춤 | Backend·Frontend 로그 | 실행 실패 또는 Polling API 확인 |
| 매번 Cache miss | Redis Key·TTL | 도시·날짜 변경 또는 TTL 만료 확인 |
| LLM 설정 오류 | Backend 로그 | 선택 Provider API Key 확인 |
| 코드 변경 미반영 | Image 생성 시간 | `--build --force-recreate` 실행 |

### 로그와 안전한 종료

```powershell
docker compose -f .\compose.application.yml logs --tail=100 weather-mcp backend frontend
docker compose -f .\compose.application.yml down
```

이 명령은 PostgreSQL·Redis를 중지하거나 Volume을 삭제하지 않습니다. 전체 실습을 끝낼 때만
`docker compose -f .\compose.infrastructure.yml down`을 실행합니다. `down -v`는 저장 데이터를
삭제하므로 초기화 목적이 아니면 사용하지 않습니다.

Application의 `down`은 상태 인프라를 중지하지 않습니다. Infrastructure의 일반 `down`도
Volume은 유지합니다. `down -v`는 PostgreSQL 이력과 Redis 데이터를 삭제하며 복구할 수
없으므로 완전 초기화가 명확히 필요할 때만 사용합니다.

## 5단계: 로컬에서 CI 명령 실행

CI는 **Continuous Integration(지속적 통합)**입니다. 코드가 Push되거나 Pull Request가
변경될 때 Test, Compose 검사, Docker Image Build를 자동 실행합니다. CD는 CI를 통과한
Application을 EC2에 반영하는 단계입니다.

GitHub에 Push하기 전에 로컬 PowerShell에서 CI와 같은 검사를 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest
python -m pytest .\backend\test_app.py -q
Copy-Item .env.docker.example .env.docker -Force   # 이미 값을 채웠다면 생략
docker compose -f .\compose.application.yml config --quiet
docker compose -f .\compose.application.yml build
```

Python 가상환경은 Test 패키지를 프로젝트별로 분리합니다. Docker Compose는 Python
가상환경의 기능이 아니라 Docker Engine을 사용하는 명령이므로 같은 PowerShell에서 그대로
실행하면 됩니다.

### CI가 확인하는 범위

```text
Source Checkout
→ Python 3.12 준비
→ Backend 패키지와 pytest 설치
→ Fake MCP·Fake LLM·Fake Store Test
→ Secret 없는 .env.docker.example 복사
→ Application Compose 문법 검사
→ Weather MCP·Backend·Frontend Image Build
```

| 검사 | 확인하는 것 | 확인하지 않는 것 |
| --- | --- | --- |
| Backend Test | API 계약·진행 상태·이력 처리 | 실제 Cloud LLM 요청 |
| Fake MCP | Tool 결과 처리 계약 | 실제 Open-Meteo 요청 |
| Fake Store | Redis·PostgreSQL 인터페이스 | 실제 DB 연결·Volume |
| Compose config | Application YAML의 문법·환경 파일 참조 | 장시간 Container 운영 |
| Application Build | 세 Application Image 생성 | PostgreSQL·Redis 실행 |

CI는 `.env.docker.example`을 그대로 복사해 사용하므로 실제 저장소 URL과 API Key가 Runner에
올라가지 않습니다. GitHub Runner에는 수강생 PC의 `.env.docker`, Database, Redis, Docker
Volume이 없습니다. 따라서 CI는
실제 외부 저장소 대신 Fake Store로 코드 계약을 검사합니다. CI 성공은 실제 통합 환경까지
성공했다는 의미가 아니므로 로컬과 EC2에서 별도 확인해야 합니다.

## 6단계: GitHub Actions Workflow 준비

Workflow는 Git 저장소 루트의 다음 위치에 있어야 GitHub가 인식합니다.

```text
.github/workflows/07-weather-stateful-cicd.yml
```

### 6-1. 05 Workflow를 비활성화하고 06으로 전환

05와 06은 같은 EC2의 Host Port `8000`, `8501`을 사용합니다. 두 Workflow가 동시에 배포하면
한 프로젝트가 다른 프로젝트를 덮어쓰거나 Port 충돌이 발생할 수 있습니다. 06 실습을
시작하기 전에 05 Workflow를 GitHub UI에서 비활성화합니다.

```text
GitHub 저장소
→ Actions
→ 07 Weather MCP CI CD
→ 오른쪽 위 ···
→ Disable workflow
```

`Disable workflow`는 `.github/workflows/07-weather-mcp-cicd.yml` 파일을 삭제하지 않습니다.
GitHub에서 실행만 잠시 중지하므로 05 수업 자료와 Git 이력은 그대로 남습니다. 비활성화된
Workflow는 Push Trigger와 `Run workflow` 모두 실행하지 않습니다.

06 Workflow는 다음 경로에서 활성화 상태인지 확인합니다.

```text
Actions
→ 07 Stateful Weather CI CD
```

`Enable workflow` 버튼이 보이면 눌러 활성화합니다. 버튼이 없고 실행 목록과 `Run workflow`
버튼이 보이면 이미 활성화된 상태입니다.

수업 단계별 권장 상태는 다음과 같습니다.

| 현재 실습 | 05 Workflow | 06 Workflow |
| --- | --- | --- |
| 05 Stateless 배포 | Enabled | 아직 실행하지 않음 |
| 06 Stateful 배포 | Disabled | Enabled |
| 다시 05로 전환 | Enabled | Disabled |

Workflow 파일을 삭제하거나 이름을 바꾸는 방식은 사용하지 않습니다. 프로젝트를 전환할 때는
실행 중인 Container를 먼저 내리고 다음 Workflow를 활성화합니다.

### 6-2. 자동 실행과 수동 실행 구분

Workflow는 다음 두 실행 방식을 모두 지원합니다.

```text
Application·Compose 변경을 main에 Push → CI/CD 자동 실행
Actions에서 Run workflow 선택       → 사용자가 CI 또는 CI/CD 수동 실행
```

README와 배포 설명서만 수정하면 실제 서버를 다시 배포할 필요가 없으므로 자동 Trigger에서
제외했습니다. 따라서 문서만 수정한 Commit을 Push했을 때 `deploy-application`이 실행되지
않는 것은 정상입니다.

수동 실행은 `deploy` 선택값에 따라 달라집니다.

| Run workflow 선택 | `test-and-build` | `deploy-application` |
| --- | --- | --- |
| `deploy=false` | 실행 | `Skipped` |
| `deploy=true` | 실행 | CI 성공 후 실행 또는 승인 대기 |

06을 처음 자동 배포할 때는 다음과 같이 실행합니다.

```text
Actions
→ 07 Stateful Weather CI CD
→ Run workflow
→ Use workflow from: main
→ Deploy 06 application to AWS EC2: 체크
→ Run workflow
```

Job 상태의 의미는 다음과 같습니다.

| 상태 | 의미 |
| --- | --- |
| `Skipped` | `deploy=false`이거나 배포 조건이 일치하지 않음 |
| `Waiting` | `production` Environment 승인 대기 |
| `Queued` | GitHub Runner 할당 대기 |
| `In progress` | Test·Build 또는 EC2 배포 실행 중 |
| `Failure` | 처음 실패한 Step의 Log 확인 필요 |
| `Success` | Backend Readiness까지 성공 |

`Waiting`이면 `Review deployments → production → Approve and deploy` 순서로 승인합니다.
GitHub 요금제나 Environment 설정에 Required reviewer 기능이 없다면 승인 없이 바로 실행될
수 있습니다.

### 6-3. 자동 Trigger 범위

다음 Trigger는 README 같은 문서 변경을 제외하고 06 Application·Infrastructure 파일이
변경될 때 자동 실행되도록 제한합니다. Workflow 파일 자체를 수정한 직후에는 Actions의
`Run workflow`로 검사합니다.

```yaml
on:
  push:
    paths:
      - ".../06_weather-mcp-stateful-deployment/backend/**"
      - ".../06_weather-mcp-stateful-deployment/frontend/**"
      - ".../06_weather-mcp-stateful-deployment/mcp_server/**"
      - ".../06_weather-mcp-stateful-deployment/compose.application.yml"
      - ".../06_weather-mcp-stateful-deployment/.env.docker.example"
      - ".github/workflows/07-weather-stateful-cicd.yml"
  pull_request:
    paths:
      - ".../06_weather-mcp-stateful-deployment/backend/**"
      - ".../06_weather-mcp-stateful-deployment/frontend/**"
      - ".../06_weather-mcp-stateful-deployment/mcp_server/**"
      - ".../06_weather-mcp-stateful-deployment/compose.application.yml"
      - ".../06_weather-mcp-stateful-deployment/.env.docker.example"
      - ".github/workflows/07-weather-stateful-cicd.yml"
  workflow_dispatch:
    inputs:
      deploy:
        type: boolean
        default: false
```

`database/**`와 `compose.infrastructure.yml`은 Trigger에 없습니다. PostgreSQL·Redis는
Pipeline이 만들지 않고 `.env.docker`의 URL로 연결하는 외부 저장소이기 때문입니다.

| 이벤트 | Test·Build CI | AWS Application 배포 |
| --- | --- | --- |
| 개인 Branch Push | 실행 | 실행하지 않음 |
| Pull Request 생성·갱신 | 실행 | 실행하지 않음 |
| `main` Push·병합 | 실행 | CI 성공 후 실행 가능 |
| Actions의 `Run workflow`, `deploy=false` | 실행 | 실행하지 않음 |
| Actions의 `Run workflow`, `deploy=true` | 실행 | CI 성공 후 실행 |
| 로컬 `git pull` | 실행하지 않음 | 실행하지 않음 |

Deploy Job의 핵심 조건은 다음과 같습니다.

```yaml
deploy-application:
  if: >-
    (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
    (github.event_name == 'workflow_dispatch' && inputs.deploy)
  needs: test-and-build
  environment: production
```

- `if`: `main` Branch의 Push에서만 배포합니다.
- `needs`: Test·Build가 실패하면 배포하지 않습니다.
- `environment`: `production` 승인 규칙과 Secret을 사용합니다.
- 매 실행은 Application 세 Container만 Build·재생성하며 저장소는 건드리지 않습니다.

### 6-4. 개인 Branch에서 CI 실행

저장소 루트에서 실행합니다.

```powershell
git switch -c weather-stateful-lab
git add 07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment
git add .github/workflows/07-weather-stateful-cicd.yml
git commit -m "Add stateful weather deployment lab"
git push -u origin weather-stateful-lab
```

GitHub 저장소의 `Actions` 탭에서 **07 Stateful Weather CI CD**를 선택합니다. Branch와 Commit을
확인하고 `test-and-build` Job을 엽니다. 실패한 경우 처음 빨간색이 된 Step의 첫 오류부터
확인합니다.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Test backend contract | Python 버전, requirements, 최초 실패 Test |
| Prepare Docker environment file | `.env.docker.example`이 Git에 포함되었는지 |
| Validate application Compose | YAML 들여쓰기, `env_file` 경로 |
| Build application images | Dockerfile의 Base Image·COPY 경로, `.dockerignore` |

## 7단계: 05 EC2를 06 실행 환경으로 전환

이 문서는 05를 완료한 수강생이 같은 EC2에서 바로 06을 진행하는 경로를 기본으로 합니다.
새 EC2를 만들지 않으므로 VPC, Security Group, Key Pair, Ubuntu, Docker와 GitHub
`production` Environment를 재사용합니다. 06만 독립적으로 진행하는 수강생을 위한 새 EC2
절차도 7-5절에 같은 내용으로 다시 제공합니다.

### 이번 강의 환경 검증 기록

다음 내용은 실제 강의 준비 과정에서 확인한 진행 흐름입니다. Public IP, Instance ID, Key와
API Key 같은 개인·계정 값은 문서에 기록하지 않습니다.

```text
[x] Seoul Region(ap-northeast-2)에서 default VPC 생성
[x] Ubuntu Server 24.04 LTS EC2 생성
[x] SSH 22와 Streamlit 8501을 관리자 My IP/32로 제한
[x] Windows PEM 파일 권한 수정 후 SSH 접속
[x] Docker Engine·Compose·Git·curl 설치
[x] hello-world Container 실행 확인
[x] 05 GitHub Actions 배포와 세 Container Health 확인
[x] 05 Container와 전용 Network 중지
[x] 05 Source와 .env는 복구용으로 보존
[x] EC2 자원 확인 명령과 판단 기준 검증
[ ] 05 생성 단계부터 사용한 t3.small(약 2 GiB) 여부 확인
[ ] Public IP 변경 시 SSH와 GitHub Environment Secret 갱신
[ ] 06 전용 .env.docker 준비
[ ] 06 GitHub Actions 첫 자동 배포
[ ] Application 재배포 후 PostgreSQL·Redis 상태 보존 확인
```

### 7-1. 05 완료 상태 확인

로컬 PowerShell에서 실제 PEM 경로와 EC2 Public IP로 접속합니다. Ubuntu를 사용했다면
사용자는 `ubuntu`입니다.

```powershell
$keyPath = "C:\mini\weather-mcp-key.pem"
$server = "ubuntu@<PUBLIC_IPV4_OR_DNS>"
ssh -i $keyPath $server
```

EC2에서 05 Container 상태를 직접 확인합니다.

```bash
cd ~/weather-mcp-deployment
docker compose ps
curl --fail http://127.0.0.1:8000/health/ready
```

Frontend, Backend, Weather MCP가 실행 중이고 Readiness가 성공하는 것을 확인한 뒤
중지합니다. 확인 없이 바로 삭제하면 05 배포가 실제로 성공했는지 학습자가 알 수 없습니다.

### 7-2. 05 Application 중지

EC2에서 다음 명령을 직접 입력합니다.

```bash
cd ~/weather-mcp-deployment
docker compose down --remove-orphans
```

정상 출력에서는 Frontend, Backend, Weather MCP Container와 05 전용 Network가 순서대로
중지·제거됩니다. 실행 중인 Container가 없는지 확인합니다.

```bash
docker ps
```

이 명령은 EC2, Ubuntu, Docker Image, Source와 `.env`를 삭제하지 않습니다. 05 Source는
비교와 복구를 위해 다음 위치에 그대로 둡니다.

```text
/home/ubuntu/weather-mcp-deployment
```

05와 06은 Host Port `8000`, `8501`을 같이 사용하므로 동시에 실행하지 않습니다.

### 7-3. EC2 자원 확인

EC2에는 Weather MCP·Backend·Frontend 세 Container만 실행합니다. PostgreSQL과 Redis는
관리형 저장소를 사용하므로 EC2에 올리지 않습니다. 배포 전에 메모리, Disk와 Docker 사용량을
확인합니다.

```bash
free -h
df -h /
docker system df
```

| 확인 결과 | 판단 |
| --- | --- |
| Memory 약 `2 GiB` | 05부터 선택한 `t3.small`, 기본 실습 진행 |
| Memory 약 `4 GiB` | 선택형 `t3.medium`, 반복 Build에 더 여유 있음 |
| Memory 약 `1 GiB` | 05 생성 시 `t3.micro`를 잘못 선택했는지 확인 필요 |
| Root Disk 여유 `8 GiB` 이상 | 기본 실습 진행 가능 |
| Root Disk 여유 부족 | 불필요한 Build Cache 확인 또는 EBS 확장 |

정상적인 기본 경로에서는 05 생성 단계부터 `t3.small`을 사용하므로 여기서 Instance Type을
변경하지 않습니다. 약 1 GiB만 표시된다면 05 생성 시 `t3.micro`를 잘못 선택한 예외입니다.
이때만 AWS Console에서 Instance를 `Stop`한 뒤 `Actions → Instance settings → Change
instance type`으로 이동하여 `t3.small`로 변경합니다. 반복 Build와 수업 중 안정성을 더
우선하면 선택형으로 `t3.medium`을 사용할 수 있습니다.

Instance를 Stop·Start하면 Elastic IP가 없는 Public IPv4는 바뀔 수 있습니다. 다시 시작한
후 다음 항목을 모두 갱신합니다.

```text
로컬 SSH 접속 주소
GitHub production의 AWS_HOST
AWS_SSH_KNOWN_HOSTS
Browser의 http://<PUBLIC_IP>:8501 주소
```

Security Group과 EBS는 같은 Instance에 계속 연결됩니다.

### 7-4. 기존 EC2의 Docker 확인

05에서 설치한 Docker를 다시 설치하지 않고 정상 동작만 확인합니다.

```bash
docker version
docker compose version
docker run --rm hello-world
```

`Hello from Docker!`가 출력되면 06을 위한 실행 환경이 준비된 것입니다.

### 7-5. 대안: 06을 새 EC2에서 독립 실행

05를 진행하지 않은 수강생은 서울 Region `ap-northeast-2`에서 Ubuntu Server 24.04 LTS
x86_64, `t3.small`, Root EBS `16 GiB gp3`로 새 EC2를 만듭니다. 현재 Region에
default VPC가 없다면 VPC Console의 `Create default VPC`를 먼저 실행합니다.

| Port | Source | 목적 |
| ---: | --- | --- |
| `22` | `My IP/32` | 관리자 SSH |
| `8501` | `My IP/32` | Streamlit Frontend |

Backend `8000`, MCP `8010`, PostgreSQL `5432`, Redis `6379`는 공개하지 않습니다. Public
IPv4를 Enable하고 EFS 같은 추가 File system은 만들지 않습니다. Ubuntu 접속 후 다음을
실행합니다.

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git curl
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu
exit
```

재접속 후 `docker run --rm hello-world`까지 확인합니다. Windows에서 PEM 권한 오류가 나면
상속을 제거하고 현재 사용자에게만 읽기 권한을 부여합니다. 이 독립 경로도 이후 단계에서는
기존 EC2 재사용 경로와 합쳐집니다.

### 7-6. 06 전용 환경 파일 준비

EC2에 `.env.docker` 한 파일만 만듭니다. 프로젝트 전체 Source와 `.venv`는 전송하지 않습니다.
Source는 GitHub Actions가 Checkout하여 전송합니다. `.env.docker`는 Git에 없으므로 배포할
때마다 덮어써지지 않습니다.

```powershell
$keyPath = "C:\mini\weather-mcp-key.pem"
$server = "ubuntu@<PUBLIC_IPV4_OR_DNS>"

ssh -i $keyPath $server "mkdir -p ~/weather-stateful"
ssh -i $keyPath $server "nano ~/weather-stateful/.env.docker"
ssh -i $keyPath $server "chmod 600 ~/weather-stateful/.env.docker && ls -l ~/weather-stateful/.env.docker"
```

EC2에서 `.env.docker` 권한이 `-rw-------`인지 확인합니다. API Key와 Password 값을 화면이나
Actions Log에 출력하지 않습니다.

```ini
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
REDIS_URL=rediss://:<password>@<host>:6380/0
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
WEATHER_CACHE_TTL_SECONDS=600
OPENAI_API_KEY=<실제 OpenAI API Key>
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=<실제 Gemini API Key>
GEMINI_MODEL=gemini-3.5-flash
```

관리형 저장소를 아직 만들지 않았다면 두 URL을 빈 값으로 두고 CI까지만 확인합니다. 이
상태로 배포하면 `/health/ready`가 503이 되어 배포 Job의 마지막 단계가 실패합니다.
저장소를 만든 뒤에는 `database/init.sql`을 관리형 PostgreSQL에 한 번 실행해
`weather_agent.runs` Table을 만듭니다.

Workflow는 EC2의 `.env.docker`를 복사하거나 덮어쓰지 않습니다. 이 파일과 API Key를 Actions
로그에 출력하지 않습니다.

## 8단계: GitHub Production Environment

GitHub 저장소에서 다음 순서로 설정합니다.

1. `Settings → Environments`로 이동합니다.
2. `New environment`에서 `production`을 생성합니다.
3. 가능한 계정에서는 `Required reviewers`를 설정합니다.
4. Deployment Branch를 `main`으로 제한합니다.
5. 다음 Environment Secret 네 개를 등록합니다.

05에서 사용한 같은 EC2와 같은 `production` Environment를 재사용한다면 아래 네 Secret도
그대로 재사용합니다. 06을 위해 중복 등록하지 않습니다. 이 절은 06을 새 EC2에서 독립적으로
시작하거나 Public IP가 바뀐 경우를 위해 전체 절차를 다시 설명합니다.

| Secret | 값 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 Public IPv4 |
| `AWS_USER` | Ubuntu는 `ubuntu`, Amazon Linux는 `ec2-user` |
| `AWS_SSH_PRIVATE_KEY` | 배포용 Private Key 전체 내용 |
| `AWS_SSH_KNOWN_HOSTS` | Fingerprint를 검증한 EC2 known_hosts 한 줄 |

Private Key는 시작·끝 줄과 줄바꿈을 포함하여 저장하고 따옴표를 추가하지 않습니다.
known_hosts 값은 앞 단계에서 EC2 SSH 접속에 성공하면서 로컬 PC에 이미 저장된 Host Key를
사용합니다.

### AWS_SSH_KNOWN_HOSTS 만드는 방법

`AWS_SSH_KNOWN_HOSTS`에는 처음 SSH 접속 때 보이는 `SHA256:...` Fingerprint만 넣는
것이 아닙니다. SSH `known_hosts` 파일이 사용하는 다음 세 부분의 한 줄 전체를 넣습니다.

```text
<EC2 주소> ssh-ed25519 <긴 서버 공개 Host Key>
```

예시의 `...`를 직접 입력하지 않습니다. 실제 명령이 출력한 긴 문자열 전체가 필요합니다.
이미 최초 SSH 접속을 완료했으므로 서버에 다시 접속하거나 서버의 `.ssh`를 수정하지 않고
로컬 PowerShell에서 바로 조회합니다.

```powershell
ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts"
```

출력 중 `ssh-ed25519`가 있는 한 줄만 선택해 Clipboard로 복사합니다.

```powershell
$knownHost = ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts" |
  Select-String "ssh-ed25519" |
  ForEach-Object { $_.Line }

$knownHost
$knownHost | Set-Clipboard
```

GitHub의 `Settings → Environments → production → Environment secrets → Add environment
secret`에서 다음처럼 등록합니다.

```text
Name: AWS_SSH_KNOWN_HOSTS
Secret: Clipboard에 복사한 한 줄 전체
```

다음 값들은 등록하지 않습니다.

```text
SHA256:...                 # Fingerprint만 있는 값
# Host ... found: line 1   # ssh-keygen의 설명 주석
StrictHostKeyChecking=no   # Host 검증을 끄는 설정
```

Windows의 `ssh-keyscan`에서 `unsupported KEX method`가 발생해도 첫 수동 접속으로
저장된 `known_hosts`를 `ssh-keygen -F`로 조회하면 됩니다. EC2를 재생성하거나 Elastic
IP 없이 Stop·Start하여 Public IP가 바뀌면 `AWS_HOST`와 `AWS_SSH_KNOWN_HOSTS`를 모두
새 주소 기준으로 갱신합니다.

조회 결과가 없다면 이 PC에서 해당 주소로 접속한 기록이 없거나 Public IP가 바뀐
예외입니다. 이때만 새 주소와 Fingerprint를 확인하며 SSH로 한 번 접속한 다음 다시
조회합니다. 같은 EC2·같은 주소를 05에서 사용했다면 기존 Secret을 그대로 사용합니다.

검증 없이 Host Key 검사를 끄거나 `StrictHostKeyChecking=no`를 사용하지 않습니다.

## 9단계: main 병합과 Application 자동 배포

```text
개인 Branch Push
→ Fake Store 기반 CI
→ Pull Request·CI
→ main 병합
→ main CI 재실행
→ production 승인
→ EC2로 Source 복사
→ Application Compose Build·재생성
→ Backend Readiness 검증
```

Deploy Job이 EC2에서 수행하는 핵심 명령은 다음과 같습니다.

```bash
cd ~/weather-stateful
test -f .env.docker
docker compose -f compose.application.yml config --quiet
docker compose -f compose.application.yml up -d --build --force-recreate weather-mcp backend frontend
curl --fail --retry 18 --retry-delay 5 http://127.0.0.1:8000/health/ready
```

배포는 Application 세 Container만 교체합니다. PostgreSQL·Redis Container를 만들지도, 내리지도
않으므로 저장된 실행 이력과 Cache는 배포와 무관하게 유지됩니다. `.env.docker`는 EC2에만
있으므로 Source 복사 단계에서 덮어써지지 않습니다.

따라서 기본 수업 흐름에서는 Application을 EC2에서 미리 수동 실행하지 않습니다. 05에서
Docker와 06 전용 `.env.docker` 준비까지 마친 뒤 `Run workflow`에서 `deploy=true`를 선택하면
Build부터 Health 확인까지 Workflow가 수행합니다.

### 선택 진단: 자동 배포 후 EC2에서 직접 확인

자동 배포가 실패했거나 내부 상태를 학습하려는 경우에만 다음 명령을 사용합니다.

```bash
cd ~/weather-stateful
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/ready
curl --fail http://127.0.0.1:8000/api/runs
```

`/health/ready`는 `redis`, `database`, `database_schema`, `mcp`를 구분해 돌려주므로 어떤
의존성이 끊겼는지 응답만으로 판단합니다.

## 10단계: 배포 후 데이터 보존 검증

EC2에서 Application 상태를 확인합니다.

```bash
cd ~/weather-stateful
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/ready
```

실행 이력은 관리형 PostgreSQL에 있으므로 Backend API로 조회합니다.

```bash
curl --fail http://127.0.0.1:8000/api/runs
```

배포 전 실행 이력이 남아 있고, 배포 후 새 요청도 추가되면 상태 보존 배포가 성공한 것입니다.
저장소가 Application Container 바깥에 있으므로 Container를 몇 번 교체해도 데이터는
영향을 받지 않습니다. 로컬에서 `compose.infrastructure.yml`로 실습 중이라면 같은 내용을
다음 명령으로도 확인할 수 있습니다.

```bash
docker compose -f compose.infrastructure.yml exec database psql -U postgres -d agent_db -c "SELECT run_id, city, provider, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"
docker compose -f compose.infrastructure.yml exec redis redis-cli --scan --pattern "weather:*"
```

## 11단계: 배포 실패 진단과 복구

| 증상 | 먼저 확인 | 해결 방향 |
| --- | --- | --- |
| CI가 시작되지 않음 | Workflow 위치·`paths` | 저장소 루트와 변경 경로 확인 |
| Fake Store Test 실패 | 최초 빨간 Test | 로컬 pytest로 재현 |
| SSH timeout | Security Group·배포 Network | 승인된 Runner 접근 경로 준비 |
| Host Key 오류 | known_hosts Secret | EC2 재생성 여부·Fingerprint 재검증 |
| `.env.docker` 없음 | `~/weather-stateful/.env.docker` | EC2에서 최초 환경 파일 생성 |
| DB·Redis 연결 실패 | `.env.docker`의 두 URL | 빈 값·오타·Network 접근 권한 확인 |
| Database Schema 실패 | `to_regclass` 조회 | 관리형 PostgreSQL에 init.sql 1회 적용 |
| Backend Readiness 실패 | `/health/ready` 응답의 `checks` | 실패한 의존 서비스부터 복구 |
| 배포 후 이력 사라짐 | 연결된 저장소 주소 | `.env.docker`의 URL이 바뀌지 않았는지 확인 |

입문 예제에는 Blue/Green과 자동 Rollback이 없습니다. 마지막 정상 Commit으로 되돌리는 새
Commit을 만들고 CI와 승인을 다시 거쳐 배포합니다. EC2에서 Application 코드를 직접 수정하면
다음 배포에서 덮어써지고 변경 이력도 남지 않습니다.

AWS 비용을 중단하려면 수업 정책에 따라 EC2와 관리형 저장소를 함께 확인합니다. EC2를
삭제해도 관리형 PostgreSQL·Redis는 따로 남아 요금이 계속 발생하므로 저장소 Console에서
직접 중지하거나 삭제합니다. 로컬 실습의 Docker Volume은 PC Disk 안에 있으므로 필요한 실행
이력은 삭제 전에 Export합니다.

## 완료 체크

```text
[ ] Frontend에서 실제 Open-Meteo Tool Result를 확인했다.
[ ] 같은 도시·날짜를 다시 조회해 Redis Cache 사용 표시를 확인했다.
[ ] Application을 다시 배포해도 PostgreSQL 실행 이력이 남는 것을 확인했다.
[ ] Backend Readiness에서 MCP·PostgreSQL·Schema·Redis 상태를 구분했다.
[ ] 로컬 pytest, Application Compose 검사, Image Build를 통과했다.
[ ] Fake MCP·LLM·Store를 CI에서 사용하는 이유를 설명할 수 있다.
[ ] 개인 Branch와 Pull Request에서 CI 결과를 확인했다.
[ ] `.env.docker`에 저장소 URL을 입력하고 `/health/ready`가 성공하는 것을 확인했다.
[ ] 첫 `deploy=true` 실행으로 Application 세 Container가 자동 배포되었다.
[ ] GitHub production Environment와 네 개의 Secret을 설정했다.
[ ] 개인 브랜치와 Pull Request에서는 배포되지 않음을 확인했다.
[ ] 배포가 저장소를 건드리지 않고 Application만 교체함을 확인했다.
[ ] Application 재배포 전후의 실행 이력을 `/api/runs`로 비교했다.
[ ] 저장소 URL이 Git이 아닌 서버의 `.env.docker`에만 있는 이유를 설명할 수 있다.
```
