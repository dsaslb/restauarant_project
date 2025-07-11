# Your Program - 통합 관리 시스템

![Your Program Logo](static/favicon.svg)

## 📋 개요

Your Program은 현대적인 웹 기반 통합 관리 시스템으로, 백엔드 API, 프론트엔드 웹 애플리케이션, 모바일 앱, AI/ML 모듈을 포함한 완전한 솔루션입니다.

## 🏗️ 아키텍처

```
Your Program/
├── your_program_frontend/     # Next.js 프론트엔드
├── mobile_app/               # React Native 모바일 앱
├── api/                      # Flask 백엔드 API
├── ai_modules/               # AI/ML 모듈
├── scripts/                  # 자동화 스크립트
├── kubernetes/               # K8s 배포 설정
├── docs/                     # 문서
└── tests/                    # 테스트
```

## 🚀 빠른 시작

### 1. 전체 프로젝트 시작 (권장)

```bash
# Windows
scripts\start_all.bat

# Linux/Mac
./scripts/start_all.sh
```

### 2. 개별 서비스 시작

#### 백엔드 API
```bash
# 가상환경 생성 및 의존성 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 데이터베이스 마이그레이션
flask db upgrade

# 서버 시작
python app.py
```

#### 프론트엔드
```bash
cd your_program_frontend
npm install
npm run dev
```

#### 모바일 앱
```bash
cd mobile_app
npm install
npx expo start
```

#### AI 서버
```bash
pip install -r ai_requirements.txt
python ai_server.py
```

## 📦 주요 기능

### 🔐 인증 및 권한 관리
- 다중 권한 레벨 (최고관리자, 매장관리자, 직원)
- JWT 기반 인증
- 권한별 메뉴 자동 분기
- 실시간 권한 변경

### 📊 대시보드
- 권한별 맞춤 대시보드
- 실시간 데이터 동기화
- 반응형 디자인
- 다크모드 지원

### 👥 직원 관리
- 직원 등록/수정/삭제
- 근무표 관리
- 출퇴근 관리
- 평가 시스템

### 📦 재고 관리
- 재고 현황 모니터링
- 자동 발주 알림
- 재고 예측 (AI)
- 바코드/QR코드 스캔

### 🍽️ 주문 관리
- 실시간 주문 처리
- 주문 상태 추적
- 결제 통합
- 주문 히스토리

### 📈 분석 및 리포트
- 매출 분석
- 고객 분석
- 직원 성과 분석
- AI 기반 예측

### 📱 모바일 앱
- 출퇴근 체크
- 재고 확인
- 주문 처리
- 푸시 알림

### 🤖 AI/ML 기능
- 매출 예측
- 재고 최적화
- 고객 행동 분석
- 자연어 처리

## 🛠️ 기술 스택

### 백엔드
- **Framework**: Flask 3.0
- **Database**: PostgreSQL + SQLAlchemy
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT
- **Real-time**: WebSocket
- **Testing**: pytest
- **Documentation**: Swagger/OpenAPI

### 프론트엔드
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **UI Components**: shadcn/ui
- **Testing**: Jest + React Testing Library
- **E2E Testing**: Playwright

### 모바일
- **Framework**: React Native + Expo
- **Navigation**: React Navigation
- **State Management**: Zustand
- **UI**: React Native Paper
- **Testing**: Jest

### AI/ML
- **Framework**: FastAPI
- **ML Libraries**: TensorFlow, PyTorch, scikit-learn
- **NLP**: Transformers, spaCy
- **Computer Vision**: OpenCV, MediaPipe
- **Monitoring**: Prometheus + Grafana

### DevOps
- **Container**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

## 📁 프로젝트 구조

```
your_program/
├── your_program_frontend/          # Next.js 프론트엔드
│   ├── app/                       # App Router
│   ├── components/                # 재사용 컴포넌트
│   ├── hooks/                     # 커스텀 훅
│   ├── store/                     # Zustand 스토어
│   ├── lib/                       # 유틸리티
│   └── src/__tests__/            # 테스트
├── mobile_app/                    # React Native 모바일 앱
│   ├── src/
│   │   ├── screens/              # 화면 컴포넌트
│   │   ├── components/           # 재사용 컴포넌트
│   │   ├── contexts/             # React Context
│   │   ├── services/             # API 서비스
│   │   └── types/                # TypeScript 타입
│   └── assets/                   # 이미지, 폰트 등
├── api/                          # Flask 백엔드
│   ├── models/                   # 데이터베이스 모델
│   ├── routes/                   # API 라우트
│   ├── services/                 # 비즈니스 로직
│   ├── utils/                    # 유틸리티
│   └── templates/                # HTML 템플릿
├── ai_modules/                   # AI/ML 모듈
│   ├── prediction_engine/        # 예측 엔진
│   ├── analytics_engine/         # 분석 엔진
│   ├── nlp_processor/           # 자연어 처리
│   └── computer_vision/         # 컴퓨터 비전
├── scripts/                      # 자동화 스크립트
│   ├── start_all.sh             # 전체 서비스 시작
│   ├── cleanup_all.sh           # 프로젝트 정리
│   ├── deploy.sh                # 배포 스크립트
│   └── backup.sh                # 백업 스크립트
├── kubernetes/                   # K8s 배포 설정
│   ├── deployments/             # 배포 설정
│   ├── services/                # 서비스 설정
│   ├── ingress/                 # 인그레스 설정
│   └── monitoring/              # 모니터링 설정
├── docs/                         # 문서
│   ├── API.md                   # API 문서
│   ├── DEPLOYMENT.md            # 배포 가이드
│   └── DEVELOPMENT.md           # 개발 가이드
└── tests/                        # 테스트
    ├── unit/                    # 단위 테스트
    ├── integration/             # 통합 테스트
    └── e2e/                     # E2E 테스트
```

## 🔧 개발 환경 설정

### 필수 요구사항
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker (선택사항)

### 환경 변수 설정

#### 백엔드 (.env)
```env
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/your_program
SECRET_KEY=your-secret-key-here
API_URL=http://localhost:5001
WS_URL=ws://localhost:5001
AI_SERVER_URL=http://localhost:8002
```

#### 프론트엔드 (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:5001
NEXT_PUBLIC_WS_URL=ws://localhost:5001
NODE_ENV=development
```

#### AI 서버 (.env.ai)
```env
DATABASE_URL=postgresql://user:password@localhost/your_program_ai
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-ai-secret-key-here
MODEL_PATH=./models
```

## 🧪 테스트

### 전체 테스트 실행
```bash
# 백엔드 테스트
pytest tests/ --cov=app --cov-report=xml

# 프론트엔드 테스트
cd your_program_frontend
npm test

# E2E 테스트
npm run test:e2e
```

### 테스트 커버리지
- 백엔드: 70% 이상
- 프론트엔드: 70% 이상
- E2E: 주요 플로우 커버

## 🚀 배포

### 개발 환경
```bash
./scripts/start_all.sh dev
```

### 스테이징 환경
```bash
./scripts/start_all.sh staging
```

### 프로덕션 환경
```bash
# Docker 배포
docker-compose -f docker-compose.prod.yml up -d

# Kubernetes 배포
kubectl apply -f kubernetes/
```

## 📊 모니터링

### 로그 확인
```bash
# 실시간 로그
tail -f logs/*.log

# 특정 서비스 로그
tail -f logs/backend.log
tail -f logs/frontend.log
tail -f logs/ai_server.log
```

### 메트릭 확인
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001
- API 문서: http://localhost:5001/docs

## 🔄 자동화 스크립트

### 프로젝트 정리
```bash
# 전체 정리
./scripts/cleanup_all.sh

# 특정 타입만 정리
./scripts/cleanup_all.sh cache
./scripts/cleanup_all.sh node_modules
./scripts/cleanup_all.sh python
```

### 백업 및 복원
```bash
# 백업 생성
./scripts/backup.sh

# 백업 복원
./scripts/restore.sh backup_20250101_120000
```

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 지원

- **이슈 리포트**: [GitHub Issues](https://github.com/your-username/your-program/issues)
- **문서**: [docs/](docs/)
- **이메일**: support@yourprogram.com

## 🔄 업데이트 로그

### v1.0.0 (2025-01-01)
- 초기 릴리즈
- 기본 CRUD 기능
- 권한 관리 시스템
- 실시간 알림
- 모바일 앱
- AI/ML 모듈

---

**Your Program** - 현대적인 통합 관리 시스템의 새로운 기준
