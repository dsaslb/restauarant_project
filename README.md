# 🏪 레스토랑 관리 시스템

Flask 기반의 레스토랑 직원 관리 및 출퇴근 시스템입니다.

## ✨ 주요 기능

### 👥 사용자 관리
- **회원가입/로그인**: 직원 계정 생성 및 관리
- **권한 관리**: 관리자/직원 역할 분리
- **승인 시스템**: 관리자 승인 후 계정 활성화
- **프로필 관리**: 개인정보 수정 및 비밀번호 변경

### ⏰ 출퇴근 관리
- **출퇴근 기록**: 실시간 출퇴근 처리
- **개인 출퇴근 내역**: 본인 근무 기록 조회
- **상태 관리**: 정상/지각/조퇴/결근 자동 판정

### 📊 관리자 기능
- **전체 출퇴근 내역**: 직원별/날짜별 필터링 조회
- **월별 통계**: 근무시간 집계 및 급여 계산
- **CSV 다운로드**: 출퇴근 내역 및 통계 데이터 내보내기
- **실시간 대시보드**: 지점별/직원별 통계 및 차트
- **승인 관리**: 신규 직원 승인/거절 처리

### 💰 급여 관리
- **월별 급여 계산**: 근무시간 기반 급여 산정
- **시급 설정**: 사용자별 급여 정책 적용
- **초과근무 수당**: 8시간 초과 근무 시 1.5배 수당
- **급여 보고서**: CSV 형태로 급여 명세서 생성

## 🚀 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 패키지 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정
```bash
# 환경변수 설정 (.env 파일 생성)
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/restaurant_dev.sqlite3

# 데이터베이스 초기화
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. 관리자 계정 생성
```bash
# 관리자 계정 생성
python create_admin.py

# 또는 CLI 명령어 사용
flask create-admin
```

### 4. 애플리케이션 실행
```bash
python app.py
# 또는
flask run
```

## 📁 프로젝트 구조

```
restaurant_project/
├── app.py                 # 메인 애플리케이션
├── models.py             # 데이터베이스 모델
├── config.py             # 설정 파일
├── extensions.py         # Flask 확장
├── requirements.txt      # 패키지 의존성
├── utils/
│   ├── payroll.py        # 급여 계산 유틸리티
│   ├── logger.py         # 로깅 시스템
│   └── sample_data.py    # 샘플 데이터 생성
├── templates/
│   ├── admin/
│   │   ├── attendances.html      # 출퇴근 관리
│   │   ├── attendance_stats.html # 월별 통계
│   │   └── action_logs.html      # 액션 로그
│   ├── admin_dashboard.html      # 관리자 대시보드
│   └── ...
└── instance/             # 데이터베이스 파일
```

## 🔧 주요 API 엔드포인트

### 인증 관련
- `GET/POST /login` - 로그인
- `GET /logout` - 로그아웃
- `GET/POST /register` - 회원가입
- `GET/POST /change_password` - 비밀번호 변경

### 출퇴근 관리
- `GET /dashboard` - 개인 대시보드
- `GET /clock_in` - 출근 처리
- `GET /clock_out` - 퇴근 처리
- `GET /attendance` - 개인 출퇴근 내역

### 관리자 기능
- `GET /admin` - 관리자 대시보드
- `GET /admin/attendance` - 전체 출퇴근 내역
- `GET /admin/attendance/csv` - 출퇴근 내역 CSV 다운로드
- `GET /admin/attendance/stats` - 월별 통계
- `GET /admin/attendance/stats/csv` - 급여 통계 CSV 다운로드
- `GET /admin/users` - 직원 관리
- `GET /approve_users` - 승인 관리

## 💡 사용 예시

### 1. 직원 출퇴근
```python
# 출근 처리
GET /clock_in

# 퇴근 처리  
GET /clock_out

# 개인 내역 조회
GET /attendance
```

### 2. 관리자 통계 조회
```python
# 월별 통계 조회
GET /admin/attendance/stats?year=2024&month=12

# 급여 CSV 다운로드
GET /admin/attendance/stats/csv?year=2024&month=12&wage=12000
```

### 3. 급여 계산
```python
from utils.payroll import calc_wage, calc_overtime_pay

# 기본 급여 계산
wage = calc_wage(user, work_hours, wage_table)

# 초과근무 수당 포함
base_pay, overtime_pay, total_pay = calc_overtime_pay(work_hours, hourly_wage)
```

## 🔒 보안 기능

- **비밀번호 해싱**: Werkzeug의 `generate_password_hash` 사용
- **세션 관리**: Flask-Login을 통한 안전한 세션 처리
- **권한 제어**: 역할 기반 접근 제어 (RBAC)
- **입력 검증**: SQL Injection 방지를 위한 파라미터 바인딩

## 📈 확장 가능한 기능

### 급여 시스템 확장
- 사용자별 급여 정책 설정
- 월급제/시급제/주급제 분기
- 세금 및 공제 자동 계산
- 급여 명세서 PDF 생성

### 통계 및 분석
- 주별/분기별 통계
- 근무 패턴 분석
- 지점별 비교 분석
- 예측 분석 (AI/ML)

### 알림 시스템
- 지각/결근 자동 알림
- 급여 지급 알림
- 정기 보고서 이메일 발송

## 🐛 문제 해결

### 일반적인 문제들
1. **데이터베이스 연결 오류**: `instance/` 폴더 권한 확인
2. **패키지 설치 오류**: 가상환경 활성화 상태 확인
3. **템플릿 오류**: `templates/` 폴더 경로 확인

### 로그 확인
```bash
# 애플리케이션 로그
tail -f logs/restaurant.log

# Flask 디버그 모드
export FLASK_ENV=development
flask run --debug
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**개발자**: Restaurant Management Team  
**버전**: 2.0.0  
**최종 업데이트**: 2024년 12월
