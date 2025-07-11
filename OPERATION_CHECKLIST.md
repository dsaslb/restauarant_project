# 🚀 운영 환경 최종 점검 체크리스트

## 📋 **1. 운영 환경 변수 설정**

### ✅ 환경 변수 확인
- [ ] `SECRET_KEY` 설정 (강력한 랜덤 키)
- [ ] `SQLALCHEMY_DATABASE_URI` 설정
- [ ] `FLASK_ENV=production` 설정
- [ ] `DEBUG=False` 설정

### ✅ .env 파일 분리
- [ ] `.env.development` (개발용)
- [ ] `.env.production` (운영용)
- [ ] `.env.test` (테스트용)

### ✅ 보안 설정
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `SESSION_COOKIE_HTTPONLY=True`
- [ ] `PERMANENT_SESSION_LIFETIME=3600`

## 🗄️ **2. 데이터베이스 및 백업**

### ✅ DB 백업 스크립트
- [ ] `backup_db.py` 스크립트 준비
- [ ] 정기 백업 스케줄 설정
- [ ] 백업 파일 무결성 검사

### ✅ 백업 명령어
```bash
# 백업
python backup_db.py backup --db prod_db.sqlite3

# 복원
python backup_db.py restore --backup-file backup/db_backup_20241201_120000.sqlite3

# 백업 목록
python backup_db.py list

# 오래된 백업 정리
python backup_db.py cleanup --keep-days 30
```

## 👥 **3. 사용자 계정 관리**

### ✅ 관리자 계정
- [ ] 관리자 계정 생성 확인
- [ ] 비밀번호 강도 확인
- [ ] 권한 설정 확인

### ✅ 테스트 계정
- [ ] 일반 사용자 계정 생성
- [ ] 테스트용 계정 준비
- [ ] 계정 상태 확인

## 🎨 **4. UI/템플릿 최신화**

### ✅ 템플릿 파일
- [ ] `templates/` 폴더 최신 상태 확인
- [ ] `login.html` 정상 동작
- [ ] `dashboard.html` 정상 동작
- [ ] `admin_attendance.html` 정상 동작

### ✅ 정적 파일
- [ ] CSS/JS 파일 최신화
- [ ] 이미지 파일 확인
- [ ] 폰트 파일 확인

## 🧹 **5. 불필요 파일/코드 정리**

### ✅ 삭제할 파일들
- [ ] 개발용 임시 파일 삭제
- [ ] 테스트용 파일 정리
- [ ] 백업 파일 정리
- [ ] 로그 파일 정리

### ✅ 코드 정리
- [ ] 주석 처리된 코드 정리
- [ ] 사용하지 않는 import 제거
- [ ] 디버그 코드 제거

## 🚀 **6. 배포 스크립트 정리**

### ✅ 실행 스크립트
- [ ] `run_production.bat` (Windows)
- [ ] `run_production.sh` (Linux/Mac)
- [ ] `requirements.txt` 최신화

### ✅ 운영 서버 설정
- [ ] gunicorn 설치 및 설정
- [ ] nginx 설정 (선택사항)
- [ ] SSL 인증서 설정 (선택사항)

## 🧪 **7. 운영 테스트**

### ✅ 로그인/로그아웃 테스트
- [ ] 관리자 로그인
- [ ] 일반 사용자 로그인
- [ ] 로그아웃 기능
- [ ] 세션 관리

### ✅ 핵심 기능 테스트
- [ ] 출근 버튼 동작
- [ ] 퇴근 버튼 동작
- [ ] 근태 기록 확인
- [ ] 통계 조회 기능

### ✅ 관리자 기능 테스트
- [ ] 관리자 대시보드 접근
- [ ] 직원 근태 조회
- [ ] 통계 차트 확인
- [ ] 데이터 필터링

### ✅ 예외 상황 테스트
- [ ] 잘못된 로그인 시도
- [ ] 권한 없는 페이지 접근
- [ ] 404 에러 페이지
- [ ] 500 에러 처리

## 📱 **8. 호환성 테스트**

### ✅ 브라우저 호환성
- [ ] Chrome 최신 버전
- [ ] Firefox 최신 버전
- [ ] Safari 최신 버전
- [ ] Edge 최신 버전

### ✅ 모바일 호환성
- [ ] 모바일 브라우저 테스트
- [ ] 반응형 디자인 확인
- [ ] 터치 인터페이스 확인

## 📊 **9. 성능 테스트**

### ✅ 로딩 속도
- [ ] 페이지 로딩 시간 < 3초
- [ ] API 응답 시간 < 1초
- [ ] 이미지 로딩 최적화

### ✅ 동시 접속
- [ ] 다중 사용자 접속 테스트
- [ ] 동시 출근/퇴근 테스트
- [ ] 데이터베이스 동시성 확인

## 🔒 **10. 보안 점검**

### ✅ 인증/인가
- [ ] 세션 관리 보안
- [ ] 권한 검증 확인
- [ ] CSRF 보호 확인

### ✅ 데이터 보안
- [ ] SQL Injection 방지
- [ ] XSS 공격 방지
- [ ] 파일 업로드 보안

## 📝 **11. 로깅 및 모니터링**

### ✅ 로그 설정
- [ ] 로그 레벨 설정
- [ ] 로그 파일 경로 확인
- [ ] 로그 로테이션 설정

### ✅ 모니터링
- [ ] 서버 상태 모니터링
- [ ] 데이터베이스 모니터링
- [ ] 에러 알림 설정

## 🚨 **12. 비상 대응**

### ✅ 백업 및 복구
- [ ] 데이터베이스 백업 절차
- [ ] 파일 백업 절차
- [ ] 복구 절차 문서화

### ✅ 장애 대응
- [ ] 서버 다운 대응 절차
- [ ] 데이터 손실 대응 절차
- [ ] 연락처 및 담당자 명시

---

## ✅ **최종 확인 사항**

### 🎯 **운영 준비 완료 체크**
- [ ] 모든 기능 정상 동작
- [ ] 보안 설정 완료
- [ ] 백업 절차 준비
- [ ] 테스트 완료
- [ ] 문서화 완료

### 📞 **운영 시작**
- [ ] 운영 서버 시작
- [ ] 모니터링 시작
- [ ] 사용자 안내
- [ ] 정기 점검 스케줄 설정

---

**운영 환경 점검 완료일: ___________**  
**점검 담당자: ___________**

# 운영/복구/백업 체크리스트

## 1. 서비스 점검
- [ ] docker-compose ps로 컨테이너 상태 확인
- [ ] docker-compose logs로 에러/경고 확인
- [ ] Sentry/Slack 알림 확인

## 2. 장애/오류 발생 시
- [ ] docker-compose restart [서비스명]으로 재시작
- [ ] 로그/알림 분석 후 원인 파악
- [ ] 필요시 개발자/운영자에게 문의

## 3. 데이터 백업/복구
- [ ] DB/파일 정기 백업(cron, 스크립트 등)
- [ ] 복구 절차 문서화 및 테스트

## 4. 신규 매장/그룹 확장
- [ ] docker-compose scale, DB 마이그레이션 등 적용
- [ ] 신규 매장 온보딩/설정 지원 