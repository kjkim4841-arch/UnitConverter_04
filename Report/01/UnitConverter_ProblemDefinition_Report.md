# Report/01 — UnitConverter Problem Definition Report

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 프로젝트 | UnitConverter_04 |
| 방법 | Mom Test 3회 → 주제 선정 → R-G-I-O |
| 상세 PRD | `docs/PRD.md` |
| Mom Test 원본 | `Report/05/Mom_Test_Interviews.md` |

---

## 1. 문제 정의 (1문장)

> meter / feet / yard 길이 변환 로직이 **여러 곳에 흩어져 있고**, **수동·부분 검증**에 의존하여 "작은 수정"이 **40분~3시간**의 디버깅·CS·온콜 비용으로 커진다.

---

## 2. Mom Test 요약

Rob Fitzpatrick Mom Test 스타일 1:1 인터뷰 3회. 솔루션·가설 질문 없이 **과거 행동·시간·비용**만 수집.

| 회차 | 페르소나 | 대표 사건 | 비용 |
|------|----------|-----------|------|
| 1 | 백엔드 4년 (물류 대시보드) | yard 추가 후 feet↔yard **meter 미경유** 버그 | 금요일 **2시간 30분**, QA 왕복 30분 |
| 2 | 데이터 6년 (ETL) | `convert.py` + `legacy/fix_units.py` **비율 상이** | 새벽 온콜 55분, 월합계 추적 **3시간** |
| 3 | 주니어 1.5년 (CLI 유지보수) | `meter:2.5` 형식·자릿수 불일치, 인수인계 검증 빈약 | 형식 수정 50분, feet→yard **1시간 10분** |

### 2.1 공통 패턴 (사실)

| # | 패턴 | 근거 |
|---|------|------|
| P1 | "작은 수정"이 40분~3시간으로 확대 | 인터뷰 1·2·3 |
| P2 | 비율·로직이 여러 파일·분기에 분산 | elif 2곳, convert+legacy, print 여러 곳 |
| P3 | feet↔yard **meter 미경유** 시 0.01~0.02 어긋남 | QA·동료 제보 |
| P4 | 검증이 `meter:2.5` / `meter:1` 등 **일부만** 손으로 확인 | yard·음수·형식은 사후 발견 |
| P5 | 단위 추가(inch, cubit, yard)마다 2시간~1일 + 회귀 불안 | 무테스트 PR, feet 값 미세 변화 |
| P6 | 음수·형식 오류는 CS/온콜/재적재로 **뒤늦은 비용** | `meter:-1`, `feet:-0.5` |

### 2.2 인터뷰에서 나오지 않은 것

- JSON/YAML 설정, json/csv 출력 포맷 — 과거 필요 행동 없음 → P1(EXT)로 분리
- TDD·ECB·registry — 피인터뷰이 솔루션 제안 없음 → 구현 품질 요구로만 연결

---

## 3. 선정 주제

### 3.1 주제 (1문장)

> **meter / feet / yard 길이 변환을, 비율과 검증 규칙이 한곳에 고정된 테스트 가능한 모듈로 만든다.**

### 3.2 후보 비교

| ID | 후보 | 탈락/약점 |
|----|------|-----------|
| A | CLI 전체 재설계 | 핵심 아픔은 CLI가 아니라 **신뢰·검증** |
| B | feet↔yard만 수정 | 증상 1개, 음수·형식·단위 추가 비용 누락 |
| C | ETL 전용 모듈 | 인터뷰 1·3 맥락과 불일치 |
| **D** | **meter 기준 테스트 가능 모듈** | **1·2·3 공통** — **선정** |

### 3.3 성공 기준 (인터뷰 언어)

1. yard 한 줄 추가가 금요일 오후 **2시간+**로 커지지 않는다.
2. feet→yard가 QA/동료 **0.01 차이 제보 전에** meter 경유로 검증된다.
3. `meter:-1`, `meter`(콜론 없음) 등이 CS/온콜 **이후가 아니라** 모듈 계약에서 걸러진다.
4. cubit/inch 추가 시 **meter/feet/yard 회귀가 자동 확인**된다.

---

## 4. R-G-I-O 정의

슬라이드 Step 2 (Role-Goal-Input-Output) + Mom Test 사실 + PRD 정합.

### 4.1 Role (R)

**누가:** meter / feet / yard 길이 변환 코드를 **직접 손대는 개발자**

| 세부 | 맥락 (인터뷰) |
|------|---------------|
| 백엔드 | 화면·API 단위 표시, DB meter ↔ UI feet/yard |
| 데이터 | CSV/배치 feet→meter, 컬럼 단위 혼재 |
| 유지보수 | 레거시 CLI·스크립트 인수인계, 형식 티켓 |

**Role 1문장:** 길이 단위 변환 로직을 수정·추가·검증해야 하는 개발자.

### 4.2 Goal (G)

**무엇을:** `unit:value` 입력에 대해 **전 단위 변환 결과를 신뢰**할 수 있게 얻는다.

| Goal 요소 | 인터뷰 근거 |
|-----------|-------------|
| 신뢰 | "비율이 맞는지 나만 안다", 계산기·머리 검증 |
| 전 단위 | yard 추가·feet↔yard 불일치가 반복 원인 |
| 검증 가능 | `meter:2.5`만 확인 → yard·음수 사후 터짐 |

**C2C 추적:** Goal 달성 여부는 FR/NFR 테스트(Red→Green)와 `Report/02` 추적표로 확인.

**Goal 1문장:** 개발자가 변환 결과를 **동료·QA·CS 제보 전에** 스스로 확신할 수 있다.

### 4.3 Input (I)

**형식:** `unit:value` (콜론 구분, 앞뒤 공백 trim 허용)

| 분류 | 예시 | 인터뷰 출처 | 기대 (P0) |
|------|------|-------------|-----------|
| 정상 | `meter:2.5` | 1·3 | 파싱·전 단위 변환 |
| 정상 | `feet:3` | 3 | meter 경유 변환 |
| 음수 | `meter:-1` | 1 | 거부 (FR-04) |
| 형식 오류 | `meter` (콜론 없음) | 3 | 거부 (FR-05) |
| 형식 오류 | `abc:2` | 3 | 거부 (FR-05) |
| 미지 단위 | `cubit:1` (미등록) | 1·3 | 명확한 오류 (FR-03) |

### 4.4 Output (O)

**형식:** table (기본), 소수 **4자리**

**예시** — 입력 `meter:2.5`:

```
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

| 규칙 | 값 | 근거 |
|------|-----|------|
| 변환 | 1m = 3.28084ft, 1m = 1.09361yd | PRD·README |
| feet↔yard | **meter 경유** | 인터뷰 P3, 레거시 버그 |
| 정밀도 | 4자리 (8.2021, 2.7340) | 인터뷰 3 (6자리 vs 4자리 기대) |
| 범위 | 등록된 **전 단위** 출력 | 슬라이드 "전 단위", FR-02 |

**P1 제외 (Output):** `--format json|csv` — 인터뷰 미언급 → EXT-03.

### 4.5 R-G-I-O → 요구 ID 매핑

| R-G-I-O | 요구 ID |
|---------|---------|
| I: `meter:2.5` 파싱 | FR-01 |
| O: 전 단위 4자리 변환 | FR-02 |
| I: `cubit:1` 미등록 | FR-03 |
| I: `meter:-1` | FR-04 |
| I: `meter`, `abc:2` | FR-05 |
| G: 단위 추가 시 핵심 안정 | NFR-01 |
| G: Parser/Converter 분리 | NFR-02 |

---

## 5. 범위

### 포함 (P0)

- 입력 `unit:value`, 단위 meter/feet/yard
- meter 기준 변환, feet↔yard meter 경유
- 음수·형식·미지 단위 검증
- table 출력 4자리
- ECB + Dual-Track TDD (`src/`, `tests/`)

### 제외 (P1·별도)

| 항목 | ID | 제외 이유 |
|------|-----|-----------|
| units.json/YAML | EXT-01 | Mom Test 미언급 |
| 동적 cubit 등록 | EXT-02 | 불안만 확인, 외부화 요구 없음 |
| json/csv 출력 | EXT-03 | table 4자리만 언급 |

---

## 6. 레거시 시드와의 관계

`UnitConverter.py`(37줄)는 **문제의 축소판**:

| 레거시 문제 | Mom Test 대응 |
|-------------|---------------|
| if/elif 분기 | yard/cubit 추가 시 2시간+ 헤맴 |
| 하드코딩 비율 | convert.py + legacy 비율 상이 |
| 검증 부재 | meter:-1 CS, feet:-0.5 재적재 |
| SRP 위반 | print·파싱·변환 혼재 → 형식 50분 |

신규 구현은 `src/` only. `UnitConverter.py` 수정 금지.

---

## 7. 다음 단계

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 1 | P0 RED | `tests/entity/test_fr02_...` (FR-02 선행) |
| 2 | P0 GREEN | `src/entity` → `control` → `boundary` |
| 3 | 추적 갱신 | `Report/02` Red/Green 커버리지 |
| 4 | P1 EXT | EXT-01~03 (P0 Green 후) |

RED 순서: `FR-02 → FR-04 → FR-03 → FR-01 → FR-05 → NFR-01 → NFR-02`

---

## 8. 참고 문서

| 경로 | 내용 |
|------|------|
| `docs/PRD.md` | 제품 요구사항 명세 |
| `Report/05/Mom_Test_Interviews.md` | 인터뷰 전체 |
| `Report/05/Topic_Selection.md` | 주제 선정 상세 |
| `Report/02/Traceability_Matrix.md` | FR/NFR ↔ 테스트 |
| `Report/01/PRD_Summary.md` | PRD 요약 (spec 초기) |
