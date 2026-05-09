# Frontend Structure

## src/pages
각 화면(페이지) 단위를 관리하는 폴더

- HomePage.jsx  
  메인 대시보드 홈 화면

- EducationPage.jsx  
  교육 관리 화면

- EmployeePage.jsx  
  직원 관리 화면

---

## src/components
재사용 가능한 UI 컴포넌트 관리

### ui/
공통 버튼, 카드, 입력창 등

### dashboard/
대시보드 전용 컴포넌트

### auth/
로그인/회원가입 관련 컴포넌트

---

## src/data
현재 backend API 연결 전 사용되는 mock 데이터 관리

---

## src/services
backend API 연결을 위한 API 레이어

- apiClient.js  
  공통 API 클라이언트

- authApi.js  
  로그인/인증 관련 API

- surveyApi.js  
  교육 생성/설문 관련 API
