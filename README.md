# 🏪 레스토랑 관리 시스템

**1인 사장님**부터 **중견 그룹/프랜차이즈**까지 유연하게 대응하는 레스토랑 관리 시스템입니다.

## 🚀 주요 기능

### 📊 대시보드 모드
- **1인 사장님 모드**: 모든 업무 메뉴에 접근 가능
- **그룹/프랜차이즈 모드**: 최고관리자 전용 메뉴만 표시
- **일반 관리자 모드**: 기본 관리 기능

### 👥 사용자 관리
- 직원 가입 승인/거절
- 권한별 메뉴 접근 제어
- 팀별 관리

### 📅 스케줄 관리
- 근무 스케줄 (직원별 배정)
- 청소 스케줄 (팀별 담당)
- 탭으로 구분된 직관적인 UI

### 📦 발주 관리
- 물품 발주 신청
- 승인/거절 프로세스
- 처리 시간 측정

### 📊 출퇴근 관리
- GPS 기반 출퇴근 기록
- 지각/조퇴/야근 관리
- 근태 평가 및 리포트

### 🔔 알림 시스템
- 실시간 알림
- 권한별 알림 발송
- Slack 연동

## 🛠️ 설치 및 설정

### 1. 환경 설정

```bash
# 환경 설정 파일 복사
cp env_example.txt .env

# .env 파일에서 대시보드 모드 설정
DASHBOARD_MODE=solo  # 'solo' 또는 'franchise'
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 설정

```bash
flask db upgrade
```

### 4. 관리자 계정 생성

```bash
flask create-admin admin password123
```

### 5. 서버 실행

```bash
python app.py
```

## ⚙️ 대시보드 모드 설정

### 1인 사장님 모드 (`DASHBOARD_MODE=solo`)
- 모든 업무 메뉴 표시
- 발주, 스케줄, 재고, 예약, 정산, 고객 관리
- 직원 승인, 권한 관리, 권한 변경 이력
- 매장별 관리자/직원 업무 바로가기

### 그룹/프랜차이즈 모드 (`DASHBOARD_MODE=franchise`)
- 최고관리자 전용 메뉴만 표시
- 직원 승인, 권한 관리
- 알림 발송, 공지/운영방침
- 통합 리포트, 시스템/오류 보고
- 백엔드 관리

### 모드 전환 방법
1. **환경 변수로 전환**: `.env` 파일에서 `DASHBOARD_MODE` 변경
2. **실시간 전환**: 관리자 설정에서 모드 변경 (추후 구현 예정)

## 📁 프로젝트 구조

```
restaurant_project/
├── app.py                 # 메인 애플리케이션
├── config.py             # 설정 파일
├── models.py             # 데이터베이스 모델
├── templates/            # HTML 템플릿
│   ├── dashboard.html    # 대시보드 (모드별 분기)
│   ├── admin_dashboard.html  # 관리자 대시보드
│   └── schedule.html     # 스케줄 관리
├── routes/               # 라우트 블루프린트
├── utils/                # 유틸리티 함수
├── static/               # 정적 파일
└── migrations/           # 데이터베이스 마이그레이션
```

## 🔧 개발 가이드

### 새로운 기능 추가 시
1. 모델 정의 (`models.py`)
2. 라우트 구현 (`routes/` 또는 `app.py`)
3. 템플릿 생성 (`templates/`)
4. 대시보드 모드별 메뉴 분기 추가

### 권한 관리
- `User` 모델의 `permissions` 필드 활용
- `is_solo_mode()`, `is_franchise_mode()` 메서드 활용
- 템플릿에서 `DASHBOARD_MODE` 변수로 분기

## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 있거나 기능 요청이 있으시면 이슈를 생성해 주세요.

---

**개발자**: AI Assistant  
**버전**: 1.0.0  
**최종 업데이트**: 2024년

## 주요 변경점 및 권장사항 (2024-06)

- 불필요 파일/캐시/중복 코드 정리
- 모든 print 문 → logger로 통합
- PayTransfer, Payroll 모델 추가 및 DB 마이그레이션
- requirements.txt 최신화 및 패키지 업그레이드
- 전체 테스트 자동화 및 통과
- DeprecationWarning(향후 호환성 경고) 점진적 개선 필요
- 운영 환경에서는 Flask-Limiter 외부 스토리지(예: Redis) 연동 권장

---

## 프로젝트 실행/운영 가이드

### 1. 환경 변수 설정
- `.env` 파일 또는 운영 환경 변수에 아래 항목 필수 설정
  - `SECRET_KEY`, `DATABASE_URL`, `SMTP_SERVER`, `SMTP_USERNAME`, `SMTP_PASSWORD`

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션
```bash
flask db upgrade
```

### 4. 관리자 계정 생성
```bash
python create_admin.py
```

### 5. 서버 실행
```bash
python app.py
```

---

## 테스트 실행 방법
```bash
pytest tests/ -v
```

---

## 운영/배포 체크리스트
- [x] 환경 변수 설정 및 보안 점검
- [x] 의존성 설치 및 최신화
- [x] DB 마이그레이션 및 관리자 계정 확인
- [x] 로그 파일 자동 정리/압축 스케줄러 점검
- [x] logger 레벨 환경별 분리 적용
- [x] 전체 테스트 통과
- [ ] DeprecationWarning 코드 점진적 개선
- [ ] Flask-Limiter 외부 스토리지(운영 환경) 적용

---

## 문의 및 지원
- 시스템/배포/운영 관련 문의: 관리자 또는 개발팀에 연락
