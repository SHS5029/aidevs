# Stateful Weather CI CD와 AWS EC2 배포 준비

CI와 CD는 Application 3개(Weather MCP·Backend·Frontend)만 다룹니다. PostgreSQL과 Redis는
Pipeline에서 실행하지 않고, 외부 관리형 저장소의 접속 URL을 서버의 `.env.docker`에 입력해
사용합니다. 저장소를 준비하기 전에는 URL을 빈 값으로 두고 CI까지만 통과시킵니다.

## 1. EC2 준비

Amazon Linux 2023 EC2에 Docker와 Docker Compose Plugin을 설치합니다. Security Group은 SSH
22와 Frontend 8501만 허용합니다. Backend 8000은 Compose가 `127.0.0.1`에만 공개하므로
인터넷에서 접근할 수 없습니다. MCP 8010은 Container 사이에서만 열립니다.

배포 폴더와 환경 파일을 최초 한 번 준비합니다. 이 파일은 Git에 없으므로 배포할 때마다
덮어써지지 않습니다.

```bash
mkdir -p ~/weather-stateful
cd ~/weather-stateful
nano .env.docker
chmod 600 .env.docker
```

```ini
DATABASE_URL=
REDIS_URL=
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
WEATHER_CACHE_TTL_SECONDS=600
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
```

`DATABASE_URL`과 `REDIS_URL`은 관리형 PostgreSQL·Redis를 만든 뒤에 채웁니다.

```ini
DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<database>
REDIS_URL=rediss://:<password>@<host>:6380/0
```

두 URL이 비어 있으면 Backend의 `/health/ready`가 503을 돌려주므로 배포 Job의 마지막 확인
단계가 실패합니다. 이는 잘못된 상태를 성공으로 표시하지 않기 위한 의도된 동작입니다.
`weather_agent.runs` Table은 `database/init.sql`을 관리형 PostgreSQL에 한 번 실행해 만듭니다.
Workflow는 `.env.docker`를 GitHub에서 복사하거나 로그로 출력하지 않습니다.

로컬에서 관리형 저장소 대신 Container를 쓰고 싶을 때만 `compose.infrastructure.yml`을
사용하고, `.env.docker`의 두 URL을 `postgresql://postgres:postgres@database:5432/agent_db`와
`redis://redis:6379/0`으로 바꿉니다. 이 Compose는 CI와 CD에서 실행하지 않습니다.

## 2. GitHub production Environment

Repository `Settings → Environments → New environment`에서 `production`을 만듭니다. 가능한
계정에서는 Required reviewers와 `main` Branch 제한을 설정합니다.

다음 Environment Secret을 등록합니다.

| Secret | 내용 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 IP |
| `AWS_USER` | Amazon Linux의 `ec2-user` |
| `AWS_SSH_PRIVATE_KEY` | 배포용 Private Key 전체 |
| `AWS_SSH_KNOWN_HOSTS` | 관리자가 지문을 확인한 EC2 known_hosts 항목 |

저장소 접속 URL은 Secret이 아니라 서버의 `.env.docker`에 둡니다. Workflow가 Runner에서
관리형 저장소에 접속하지 않으므로 Runner에 저장소 자격 증명을 두지 않습니다.

### AWS_SSH_KNOWN_HOSTS 생성

앞 단계에서 로컬 PC의 SSH 접속이 이미 성공했으므로 Host Key도 Windows 사용자의
`known_hosts`에 저장되어 있습니다. 서버에 다시 접속하거나 서버의 `.ssh`를 수정하지 않고
로컬 PowerShell에서 `ssh-ed25519` 한 줄 전체를 Clipboard에 복사합니다. Fingerprint
`SHA256:...`만 Secret에 넣지 않습니다.

```powershell
$knownHost = ssh-keygen -F <PUBLIC_IPV4_OR_DNS> `
  -f "$env:USERPROFILE\.ssh\known_hosts" |
  Select-String "ssh-ed25519" |
  ForEach-Object { $_.Line }

$knownHost
$knownHost | Set-Clipboard
```

출력 형식은 다음과 같으며 `...`가 아니라 실제 긴 값 전체를 등록합니다.

```text
<PUBLIC_IPV4_OR_DNS> ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA...
```

05와 같은 EC2·주소·`production` Environment를 재사용하면 기존 Secret을 그대로 사용하고
06용으로 다시 등록하지 않습니다. EC2 Public IP가 바뀌면 `AWS_HOST`와 이 Secret을 함께
갱신합니다. GitHub-hosted Runner에서 EC2 SSH로 접근 가능한 네트워크 정책이 별도로 필요하며,
이를 해결하려고 22번 Port를 `0.0.0.0/0`으로 열지 않습니다. 실제 운영에서는 SSM, VPN,
Bastion 또는 보안 정책에 맞는 self-hosted Runner를 사용합니다.

## 3. Workflow 구성

`.github/workflows/07-weather-stateful-cicd.yml` 한 파일이 CI와 CD를 모두 담당합니다.
`backend`, `frontend`, `mcp_server`, `compose.application.yml`, `.env.docker.example`이
바뀐 Push와 Pull Request에서만 실행합니다.

| Job | 조건 | 내용 |
| --- | --- | --- |
| `test-and-build` | 모든 Push·PR·수동 실행 | Fake Store Test → `.env.docker.example` 복사 → Compose 검사 → Image 3개 Build |
| `deploy-application` | `main` Push 또는 수동 실행에서 `deploy: true` | `production` 승인 → Source 복사 → Application Compose 재배포 → `/health/ready` 확인 |

`test-and-build`는 실제 Key와 저장소 없이 실행합니다. Backend Test가 Redis·PostgreSQL·MCP·LLM을
모두 Fake로 교체하고, Compose 검사에는 Secret이 없는 `.env.docker.example`을 복사해 사용합니다.
Image는 Build만 하고 Registry에 Push하지 않습니다.

```text
개인 브랜치 Push 또는 Pull Request
→ Fake Store·MCP·LLM Backend Test
→ Application Compose 검사
→ MCP·Backend·Frontend Image Build
→ main 병합
→ 같은 CI 재실행·성공
→ production 승인
→ EC2 Source 복사·Application Compose만 실행
→ /health/ready 성공
```

## 4. EC2 확인과 복구

```bash
cd ~/weather-stateful
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/ready
```

`/health/ready`는 `redis`, `database`, `database_schema`, `mcp`를 구분해 알려 주므로 어떤
의존성이 끊겼는지 응답만 보고 판단합니다. 배포 후 문제가 있으면 GitHub에서 마지막 정상
Commit으로 되돌린 새 Commit을 만든 뒤 같은 승인 절차로 다시 배포합니다. 이 입문 예제는
Blue/Green이나 자동 Rollback을 구현하지 않습니다.
