# wanted_pre_onboarding

서비스 개요
본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.
유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.

## 요구사항

- [ ] 상품 등록 : `제목`, `게시자명`, `상품설명`, `목표금액`, `펀딩종료일`, `1회펀딩금액`로 구성
- [ ] 상품 수정 : 단, 모든 내용이 수정 가능하나 `목표금액`은 수정이 불가능합니다.
- [ ] 상품 삭제 : DB에서 삭제됩니다.
- [ ] 상품 목록 : `제목`, `게시자명`, `총펀딩금액`, `달성률` 및 `D-day(펀딩 종료일까지)` 가 포함되어야 합니다.
  - [ ] 상품 검색 : (상품 리스트 API 에 ?search=취미 조회 시 ,제목에  ‘내 취미 만들..’  ‘취미를 위한 ..’ 등 검색한 문자 포함된 상품 리스트만 조회)
  - [ ] 상품 정렬 : `생성일기준`, `총펀딩금액` 두 가지 정렬이 가능해야합니다. `?order_by=생성일` / `?order_by=총펀딩금액`
  (`달성률`: 1,000,000원 목표금액 일때,  총 펀딩금액이 5,000,000원 이면 500%, 소수점 무시)
- [ ] : 상품 상세 페이지 : `제목`, `게시자명`, `총펀딩금액`, `달성률`, `D-day(펀딩 종료일까지)`, `상품설명`, `목표금액`  및 `참여자 수` 가 포함되어야 합니다.
