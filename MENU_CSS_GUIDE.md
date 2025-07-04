# 🎯 메뉴/버튼 겹침 방지 CSS 가이드

## 📋 개요
이 가이드는 Flask 템플릿에서 메뉴/버튼이 겹치지 않도록 하는 최신 flex 레이아웃 CSS 스타일을 제공합니다.

## 🎨 적용된 CSS 파일
- `static/css/common.css` - 공통 메뉴 스타일

## 🔧 사용법

### 1. 기본 메뉴 바 (가장 많이 사용)

```html
<!-- 메뉴 영역(로그아웃/권한관리/기타) -->
<div class="menu-bar">
  <a class="menu-link" href="/dashboard">대시보드</a>
  <a class="menu-link" href="/admin/user_permissions">직원 권한 관리</a>
  <a class="menu-link" href="/admin/approval_logs">권한 변경 이력</a>
  <a class="menu-link" href="/notifications">알림센터</a>
  <a class="menu-link" href="/logout" style="color:#d32f2f;">로그아웃</a>
</div>
```

### 2. 헤더 메뉴 (반투명 배경)

```html
<div class="header-menu">
  <a class="header-menu-link" href="/dashboard">🏠 대시보드</a>
  <a class="header-menu-link" href="/admin/user_permissions">👥 권한 관리</a>
  <a class="header-menu-link" href="/admin/approval_logs">📋 변경 이력</a>
  <a class="header-menu-link" href="/notifications">🔔 알림센터</a>
  <a class="header-menu-link logout" href="/logout">🚪 로그아웃</a>
</div>
```

### 3. 버튼 그룹

```html
<div class="button-group">
  <button class="btn btn-primary">저장</button>
  <button class="btn btn-secondary">취소</button>
  <button class="btn btn-success">승인</button>
  <button class="btn btn-danger">삭제</button>
</div>
```

## 🎯 CSS 특징

### ✅ 자동 줄바꿈
- `flex-wrap: wrap` - 메뉴가 많으면 자동으로 다음 줄로 이동
- `gap: 16px` - 메뉴 간 일정한 간격 유지

### ✅ 반응형 디자인
- 700px 이하: 간격과 폰트 크기 자동 조정
- 480px 이하: 더 작은 간격과 폰트 크기

### ✅ 겹침 방지
- `white-space: nowrap` - 메뉴 텍스트가 한 줄로 유지
- `flex-wrap: wrap` - 공간이 부족하면 자동 줄바꿈

### ✅ 시각적 효과
- hover 효과 - 마우스 오버 시 배경색 변경
- 부드러운 전환 - `transition` 효과

## 📱 반응형 동작

### 데스크탑 (768px 이상)
```
[대시보드] [직원 권한 관리] [권한 변경 이력] [알림센터] [로그아웃]
```

### 태블릿 (700px 이하)
```
[대시보드] [직원 권한 관리]
[권한 변경 이력] [알림센터] [로그아웃]
```

### 모바일 (480px 이하)
```
[대시보드]
[직원 권한 관리]
[권한 변경 이력]
[알림센터]
[로그아웃]
```

## 🔧 적용된 템플릿

### ✅ 이미 적용된 템플릿
1. `templates/dashboard.html` - 메인 대시보드
2. `templates/core_dashboard.html` - 코어 대시보드

### 📝 적용 방법
1. 템플릿 `<head>`에 CSS 링크 추가:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/common.css') }}">
```

2. 기존 메뉴를 새로운 클래스로 감싸기:
```html
<!-- 기존 -->
<a href="/logout">로그아웃</a>

<!-- 개선 -->
<div class="menu-bar">
  <a class="menu-link" href="/logout">로그아웃</a>
</div>
```

## 🎨 스타일 변형

### 색상 커스터마이징
```css
.menu-link:last-child {
  background: #ffeaea;
  color: #d32f2f;
}
```

### 간격 조정
```css
.menu-bar {
  gap: 20px; /* 간격 증가 */
}
```

### 배경색 변경
```css
.menu-bar {
  background: #e3f2fd; /* 파란색 계열 */
}
```

## ✅ 장점

1. **절대 겹치지 않음** - flex-wrap으로 자동 줄바꿈
2. **반응형** - 모든 디바이스에서 최적화
3. **일관성** - 모든 메뉴에서 동일한 스타일
4. **유지보수** - CSS 파일 하나로 전체 관리
5. **성능** - 최신 CSS로 빠른 렌더링

## 🚀 빠른 적용

기존 템플릿에서 메뉴 겹침 문제가 있다면:

1. `static/css/common.css` 파일이 있는지 확인
2. 템플릿에 CSS 링크 추가
3. 메뉴를 `<div class="menu-bar">`로 감싸기
4. 각 링크에 `class="menu-link"` 추가

이렇게 하면 즉시 메뉴 겹침 문제가 해결됩니다! 🎉
