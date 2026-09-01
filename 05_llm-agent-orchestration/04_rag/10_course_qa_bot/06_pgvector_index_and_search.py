"""2026 AI 캠퍼스 OT 지식을 pgvector에 저장하고 검색합니다."""

from typing import Any

from _pgvector_store import delete_collection, similarity_search, upsert_text


COLLECTION = "ai_campus_ot_2026"
SOURCE = "[OT] 2026_AI캠퍼스_OT_AI오케스트레이션 캠프 1기.pdf"
KNOWLEDGE_VERSION = "2026-ai-campus-ot-v3"
SCORE_THRESHOLD = 0.44

# PDF의 표와 안내문을 질문 하나에 답하기 좋은 크기로 직접 검수한 지식입니다.
# 노트북 비밀번호와 예시 생년월일 같은 민감정보는 포함하지 않습니다.
DOCUMENTS: list[dict[str, Any]] = [
    {
        "title": "교육 일정과 시간",
        "content": (
            "전체 교육 기간과 하루 교육 시간 안내입니다. 교육 기간은 "
            "2026년 7월 9일부터 2027년 1월 4일까지 총 120일, 960시간입니다. "
            "수업은 주중 09:00부터 18:00까지 진행하며 하루 교육 시간은 "
            "8시간입니다."
        ),
        "page_number": 4,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "과정명과 교육 방식",
        "content": (
            "과정명은 '멀티 에이전트 워크플로우 기반 AI 오케스트레이션 "
            "애플리케이션 개발자 과정'입니다. 교육은 오프라인이 원칙이며 "
            "긴급 상황에는 온·오프라인을 병행할 수 있습니다."
        ),
        "page_number": 4,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "수강 철회 기간",
        "content": (
            "수강 철회는 개강일부터 7일간 가능하며 최종 기한은 "
            "2026년 7월 15일 10:00입니다. 행정 처리를 위해 철회 요청은 "
            "7월 14일 13:00까지 전달해 달라고 안내되어 있습니다."
        ),
        "page_number": 4,
        "section": "행정",
        "time_sensitive": True,
    },
    {
        "title": "교육 운영진과 상담",
        "content": (
            "교육 운영진은 PM 김세미 매니저, 캠퍼스 총괄 손승진 팀장, "
            "APM 박숙경 매니저입니다. 정기 상담은 개강 후, 개강 2개월 차, "
            "개강 4개월 차에 진행하며 정기 상담 외에도 운영진에게 상담할 수 있습니다."
        ),
        "page_number": 5,
        "section": "운영",
        "time_sensitive": True,
    },
    {
        "title": "전체 커리큘럼 구성",
        "content": (
            "교육은 5개 교과목, 5번의 평가, 5개의 프로젝트로 구성됩니다. "
            "웹 서비스 기초 및 AI 백엔드 개발 192시간, 단일 에이전트 추론 및 "
            "AI 오케스트레이션 160시간, 멀티 에이전트 협업 및 서비스 운영 "
            "152시간, 노코드 멀티 에이전트 워크플로우 설계 및 운영 152시간, "
            "최종 프로젝트 304시간으로 총 960시간입니다."
        ),
        "page_number": 6,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "웹 서비스 기초 및 AI 백엔드 개발",
        "content": (
            "첫 번째 교과목은 총 24일, 192시간입니다. 파이썬 백엔드 개발 및 "
            "Vibe Coding 10일 80시간, DB 연동 및 세션 관리 5일 40시간, "
            "AI 인터페이스 및 UX 설계 6일 48시간, 단위 프로젝트 3일 "
            "24시간으로 구성됩니다."
        ),
        "page_number": 8,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "단일 에이전트 추론 및 AI 오케스트레이션",
        "content": (
            "두 번째 교과목은 총 20일, 160시간입니다. 고급 프롬프트 및 추론 "
            "전략 4일 32시간, Function Calling 및 오케스트레이션 5일 40시간, "
            "지식 저장소 및 장기 기억 4일 32시간, 상태 기계 기반 흐름 제어 "
            "4일 32시간, 단위 프로젝트 3일 24시간으로 구성됩니다."
        ),
        "page_number": 8,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "멀티 에이전트 협업 및 서비스 운영",
        "content": (
            "세 번째 교과목은 총 19일, 152시간입니다. 멀티 에이전트 협업 설계 "
            "5일 40시간, 서비스 배포 및 자동화 운영 6일 48시간, AI 보안 및 "
            "가드레일 설계 5일 40시간, 단위 프로젝트 3일 24시간으로 구성됩니다."
        ),
        "page_number": 8,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "노코드 멀티 에이전트 워크플로우 설계 및 운영",
        "content": (
            "네 번째 교과목은 총 19일, 152시간입니다. AI 워크플로우 개념 및 "
            "구성 요소 이해 2일 16시간, AI 워크플로우 설계 및 구현 2일 "
            "16시간, 운영·확장 관점의 AI 워크플로우 설계 고도화 6일 48시간, "
            "AI 워크플로우 운영 및 관리 역량 강화 6일 48시간, 단위 프로젝트 "
            "3일 24시간으로 구성됩니다."
        ),
        "page_number": 8,
        "section": "교육과정",
        "time_sensitive": False,
    },
    {
        "title": "최종 프로젝트 기간",
        "content": "최종 프로젝트는 38일, 304시간으로 편성되어 있습니다.",
        "page_number": 8,
        "section": "프로젝트",
        "time_sensitive": False,
    },
    {
        "title": "교과목 프로젝트 주제",
        "content": (
            "교과목 프로젝트는 고정 주제로 진행합니다. 웹 서비스 기초는 실시간 "
            "로그 대시보드 인터페이스, 단일 에이전트는 복합 API 연계 일정 조정 "
            "에이전트, 멀티 에이전트는 에러 자가 치유 AutoHealing 워크플로우, "
            "노코드 교과목은 노코드·로코드 기반 기업형 지능형 기술 지원 자동화 "
            "Tech Support 워크플로우를 구축합니다."
        ),
        "page_number": 9,
        "section": "프로젝트",
        "time_sensitive": False,
    },
    {
        "title": "최종 프로젝트 방식과 멘토링",
        "content": (
            "최종 프로젝트는 6개 주제 중 팀별로 1개를 선택합니다. 현직자 멘토와 "
            "20시간의 멘토링을 진행하며 팀 프로젝트가 원칙입니다. 개인 프로젝트는 "
            "진행할 수 없고, 개인 프로젝트에는 멘토링과 리소스가 지원되지 않습니다."
        ),
        "page_number": 10,
        "section": "프로젝트",
        "time_sensitive": False,
    },
    {
        "title": "교재와 실습 리소스",
        "content": (
            "교과목 수업에는 훈련 교재가 배부되고 교과목 및 최종 프로젝트에 "
            "리소스가 지원됩니다. 교재에는 파이썬, LangChain 기반 RAG, AI 에이전트, "
            "프롬프트 엔지니어링, 벡터 데이터베이스 관련 도서가 포함됩니다. "
            "교과목별로 Codex, OpenAI API, AWS 계정이 지원될 수 있으며 제공 유형과 "
            "금액은 변동될 수 있습니다."
        ),
        "page_number": 7,
        "section": "지원",
        "time_sensitive": True,
    },
    {
        "title": "코딩 테스트 지원",
        "content": (
            "취업 역량 강화를 위해 유료 코딩 테스트를 제공합니다. 개강 후 "
            "1개월 차에는 전체 교육생이 필수로 참여하며, 수강 중부터 수료 후까지 "
            "프로그래머스 코딩역량 인증 시험을 지원합니다."
        ),
        "page_number": 11,
        "section": "취업 지원",
        "time_sensitive": True,
    },
    {
        "title": "수료 후 취업 지원",
        "content": (
            "수료 후 6개월 동안 취업률을 조사하며 같은 기간 코딩 테스트와 취업 "
            "특강을 지원합니다. 과정 진행 중이나 수료 후 취업한 경우 담당 매니저에게 "
            "공유해야 합니다."
        ),
        "page_number": 12,
        "section": "취업 지원",
        "time_sensitive": True,
    },
    {
        "title": "커뮤니케이션 채널",
        "content": (
            "과정 공지는 Discord로 전달됩니다. 모바일 Discord 앱과 노트북의 웹 "
            "Discord를 설치하고 모바일·웹 알림을 모두 켜야 합니다. 공지에는 반응을 "
            "남기는 것이 필수라고 안내되어 있습니다."
        ),
        "page_number": 13,
        "section": "학습 안내",
        "time_sensitive": True,
    },
    {
        "title": "주간 및 월간 회고",
        "content": (
            "주간 회고는 매주 월요일부터 일요일 사이에 강의 요약이 아니라 그 주에 "
            "배운 내용에 대한 회고를 KPT 또는 4L 형식으로 작성합니다. 월간 회고는 "
            "매월 말일에 학습 기술, 느낀 점, Keep·Problem·Try를 작성합니다. 작성한 "
            "글은 과정 전용 시트에 업로드합니다."
        ),
        "page_number": 15,
        "section": "학습 안내",
        "time_sensitive": True,
    },
    {
        "title": "고용24 출석 앱",
        "content": (
            "출석을 위해 고용24 직업훈련 출석 앱을 설치하고 기기 1대를 등록해야 "
            "합니다. 비콘이 인식되지 않으면 즉시 인포 매니저에게 방문해 QR 출석으로 "
            "대체합니다. 시스템 오류 때는 신분증과 사진 촬영으로 출석을 대체할 수 "
            "있으므로 09:00 전에 도착해야 합니다."
        ),
        "page_number": 21,
        "section": "출결",
        "time_sensitive": True,
    },
    {
        "title": "출결 기준과 지각 환산",
        "content": (
            "하루 출석 시간이 4시간 미만이면 결석으로 처리됩니다. 지각은 13:59까지 "
            "입실하고 18:00에 퇴실하면 인정되며, 조퇴는 09:00~13:00 수강 후 "
            "퇴실한 경우 인정됩니다. 지각·조퇴·외출을 합해 3회가 되면 결석 1회로 "
            "처리되고 하루에 지각과 조퇴를 모두 하면 2회가 누적됩니다."
        ),
        "page_number": 25,
        "section": "출결",
        "time_sensitive": True,
    },
    {
        "title": "지각·조퇴·외출 사전 공유",
        "content": (
            "지각·조퇴·외출·결석은 매니저에게 사전에 공유해야 합니다. 외출 전과 "
            "복귀 때 앱 처리를 하지 않거나 4시간 이상 외출하면 결석 처리됩니다. "
            "사전 공유 없이 외출하거나 수업 중 장시간 자리를 비우면 사후 외출로 "
            "처리될 수 있습니다."
        ),
        "page_number": 26,
        "section": "출결",
        "time_sensitive": True,
    },
    {
        "title": "지정좌석과 출석 확인",
        "content": (
            "과정은 지정좌석제로 운영됩니다. 매 교시 강사가 출석을 확인하고 오전과 "
            "오후에는 운영 매니저가 불시에 출석을 확인합니다. 부정훈련 방지를 위해 "
            "지정 좌석 기준으로 매일 주기적인 모니터링을 진행합니다."
        ),
        "page_number": 28,
        "section": "출결",
        "time_sensitive": True,
    },
    {
        "title": "공가 증빙서류",
        "content": (
            "공가 사유에 따라 훈련·시험 확인서, 면접확인서, 예비군·민방위 증빙, "
            "청첩장·가족관계증명서, 사망진단서·가족관계증명서, 출생증명서·입원확인서, "
            "진료확인서·입퇴원확인서, 휴가신청서, 분실신고증, 단말기 고장 증빙, "
            "현장훈련 출석부 등이 필요합니다. 서류 제출만으로 자동 인정되지 않으며 "
            "고용센터가 점검 후 보완을 요청할 수 있습니다."
        ),
        "page_number": 29,
        "section": "공가",
        "time_sensitive": True,
    },
    {
        "title": "공가 처리 절차",
        "content": (
            "공가를 사용하려면 사전에 매니저에게 DM을 보내고 다음 출석일에 서류를 "
            "제출합니다. 플레이데이터가 서류를 취합·점검해 주 1회 시스템에 올리면 "
            "고용센터가 확인해 출석 처리합니다. 완료까지 약 7~10일이 걸리며 서류가 "
            "늦으면 전체 반의 출석 반영과 훈련장려금 지급이 지연될 수 있습니다."
        ),
        "page_number": 30,
        "section": "공가",
        "time_sensitive": True,
    },
    {
        "title": "수료 기준",
        "content": (
            "수료하려면 전체 120일 중 80% 이상인 96일 이상을 이수해야 합니다. "
            "수료 기준은 월별 장려금 충족 여부가 아니라 전체 훈련 일수의 전체 "
            "출석률로 계산합니다. 수료하면 플레이데이터 수료증이 발급됩니다."
        ),
        "page_number": 31,
        "section": "수료",
        "time_sensitive": True,
    },
    {
        "title": "미수료 및 제적 기준",
        "content": (
            "전체 훈련 일수의 20%를 초과해 결석하거나 한 단위기간의 결석이 해당 "
            "기간 훈련일수의 50% 이상이면 미수료 또는 제적 대상입니다. 부정 출석, "
            "불량한 수강 태도, 수강 포기, 절도·폭행·폭언 등도 제적 사유입니다. "
            "전체 기간의 80% 이상 출석한 뒤 취업하면 조기취업 수료로 인정됩니다."
        ),
        "page_number": 32,
        "section": "수료",
        "time_sensitive": True,
    },
    {
        "title": "중도탈락 패널티",
        "content": (
            "불가피한 사유 없이 중도탈락하면 국민내일배움카드 계좌에서 최초 "
            "20만원, 2회 50만원, 3회 이상 100만원이 차감될 수 있습니다. 최초 "
            "중도탈락 때는 참여 일수에 해당하는 금액도 차감되며 K-디지털 트레이닝 "
            "과정을 5년간 수강할 수 없다고 안내되어 있습니다. 부정 출석으로 "
            "제적되면 계좌 잔액 전액이 차감될 수 있습니다."
        ),
        "page_number": 33,
        "section": "수료",
        "time_sensitive": True,
    },
    {
        "title": "훈련장려금 지급 기준",
        "content": (
            "단위기간 출석률이 80% 이상이면 훈련장려금 지급 대상입니다. OT 기준 "
            "훈련장려금 20만원과 AI캠퍼스 특별훈련수당 20만원을 합해 최대 40만원이며, "
            "출석 인정 일수당 2만원으로 계산합니다. 단위기간 출석률이 80% 미만이면 "
            "지급되지 않습니다. 실업급여나 청년수당 등과는 이중 수급할 수 없습니다."
        ),
        "page_number": 34,
        "section": "훈련장려금",
        "time_sensitive": True,
    },
    {
        "title": "훈련장려금 미지급 사례",
        "content": (
            "재직자, 고용보험 미가입 재직자, 특수형태근로자, 영세자영업자는 고용형태를 "
            "실업자로 변경하고 개강 후 2주 이내 관련 서류를 제출해야 지급 대상이 될 "
            "수 있습니다. 고용보험 가입 후 주 15시간 이상 근로하거나 일용직 근로가 "
            "한 달에 10일 이상이면 미지급될 수 있습니다. 자격증 응시료 지원을 받은 "
            "일수만큼 장려금이 차감될 수 있으므로 근무 병행자는 매니저에게 알려야 합니다."
        ),
        "page_number": 35,
        "section": "훈련장려금",
        "time_sensitive": True,
    },
    {
        "title": "최신 FAQ 확인",
        "content": (
            "동작 캠퍼스 FAQ는 실시간으로 바뀌는 내용을 반영하기 위해 별도 Notion에 "
            "정리되어 있으며 내용이 변경될 수 있습니다. 행정·출결·장려금·시설 관련 "
            "답변은 OT PDF의 안내이므로 최신 FAQ 또는 담당 매니저에게 다시 확인해야 합니다."
        ),
        "page_number": 36,
        "section": "운영",
        "time_sensitive": True,
    },
    {
        "title": "교육센터 운영시간",
        "content": (
            "교육센터는 평일 월요일부터 금요일까지 08:30~22:00에 운영합니다. "
            "주말과 공휴일에는 문을 열지 않습니다."
        ),
        "page_number": 38,
        "section": "시설",
        "time_sensitive": True,
    },
    {
        "title": "공용공간과 흡연 규정",
        "content": (
            "공용공간 사용 후에는 테이블을 정리하고 오래 사용한 뒤에는 다른 "
            "교육생에게 자리를 양보해야 합니다. 소지품 분실은 교육센터가 책임지지 "
            "않습니다. 강의실·화장실 등 센터 내외부와 교육장 주차장은 금연이며 위반하면 "
            "과태료가 부과될 수 있습니다."
        ),
        "page_number": 39,
        "section": "시설",
        "time_sensitive": True,
    },
    {
        "title": "노트북 및 장비 사용 규정",
        "content": (
            "교육용 노트북에는 불법 소프트웨어, 게임, 라이선스 없는 개인용 "
            "소프트웨어를 설치할 수 없습니다. 파일은 별도 저장장치나 온라인 저장소에 "
            "백업해야 하며 장비 고장·파손·이상은 즉시 사무실 또는 매니저에게 알립니다. "
            "장비와 비품에는 스티커를 붙이거나 낙서할 수 없습니다."
        ),
        "page_number": 40,
        "section": "장비",
        "time_sensitive": True,
    },
    {
        "title": "노트북 대여와 운영체제",
        "content": (
            "교육에 필요한 개인 장비가 없으면 노트북을 대여할 수 있습니다. 전체 "
            "교육은 Windows 기반으로 진행되므로 Mac 사용자는 Windows와 다른 환경의 "
            "소프트웨어 설치 문제 등을 스스로 해결해야 합니다."
        ),
        "page_number": 41,
        "section": "장비",
        "time_sensitive": True,
    },
    {
        "title": "부정훈련 예방",
        "content": (
            "결석·지각·조퇴·외출자를 정상 출석으로 처리하거나 QR 코드를 외부에 "
            "유출하고 스마트폰을 두고 외출하는 행위는 부정훈련입니다. 계획과 다른 "
            "내용을 가르치거나 약속한 교재·재료를 지급하지 않는 경우, 평가 없이 "
            "평가했다고 응답하게 하는 경우, 강사가 빈번하게 자리를 비우는 경우도 "
            "부정훈련 사례로 안내되어 있습니다."
        ),
        "page_number": 46,
        "section": "훈련 규정",
        "time_sensitive": True,
    },
    {
        "title": "교육생 경고와 제적",
        "content": (
            "팀 프로젝트·실습에 비협조적이거나 지각·결석으로 다른 교육생에게 피해를 "
            "주는 경우, 과정 관계자 사이에 갈등을 일으키는 경우, 근거 없이 비방하는 "
            "경우, 운영 방침을 따르지 않는 경우 경고 대상이며 경고 3회 누적 시 "
            "제적됩니다. 절도·폭행·성적 자율권 침해 행위는 경고 및 제적 대상입니다."
        ),
        "page_number": 47,
        "section": "훈련 규정",
        "time_sensitive": True,
    },
    {
        "title": "서약서 작성",
        "content": (
            "작성 대상 서류는 개인정보 수집·이용 동의서, 입과 서약서, 제적경고 "
            "서약서입니다. 서약서는 사전에 발송되었으며 미작성자가 작성합니다. "
            "생년월일은 주민등록번호 앞 6자리 형식으로 기재하되 실제 개인정보는 "
            "공개된 채널에 공유하지 않습니다."
        ),
        "page_number": 48,
        "section": "서약",
        "time_sensitive": True,
    },
]


def index_documents() -> None:
    """기존 캠프 지식을 교체하고 검수된 청크를 저장합니다."""
    delete_collection(COLLECTION)
    for chunk_index, document in enumerate(DOCUMENTS):
        upsert_text(
            collection=COLLECTION,
            title=document["title"],
            content=document["content"],
            source=SOURCE,
            chunk_index=chunk_index,
            metadata={
                "page_number": document["page_number"],
                "section": document["section"],
                "time_sensitive": document["time_sensitive"],
                "knowledge_version": KNOWLEDGE_VERSION,
            },
        )
        print(
            f"저장: chunk={chunk_index:02d} | p.{document['page_number']} | "
            f"{document['title']}"
        )


if __name__ == "__main__":
    index_documents()

    question = "최종 프로젝트를 개인으로 진행할 수 있나요?"
    print("\n질문:", question)
    results = similarity_search(
        question,
        collection=COLLECTION,
        top_k=4,
        score_threshold=SCORE_THRESHOLD,
    )
    if not results:
        print("관련 OT 근거를 찾지 못했습니다.")

    for item in results:
        page = item["metadata"].get("page_number", "?")
        print(
            f"{item['score']:.3f} | {item['source']} p.{page} | "
            f"{item['content']}"
        )
