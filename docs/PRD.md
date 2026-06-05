# PRD — Unit Converter (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 버전 | 0.1 (초안) |
| 작성일 | 2025-06-05 |
| 문제 정의 | `Report/01/UnitConverter_ProblemDefinition_Report.md` |
| 추적표 | `Report/02/Traceability_Matrix.md` |

---

## 1. 개요

### 1.1 배경

사용자·시스템은 길이를 `meter`, `feet`, `yard` 등 서로 다른 단위로 입력·표시한다. Mom Test 3회에서 확인된 공통 문제:

- 변환 비율·로직이 **여러 파일·분기**에 분산
- **meter 경유 없이** feet↔yard를 계산하면 0.01~0.02 오차
- `meter:2.5` 등 **일부 케이스만** 수동 검증 → 음수·형식 오류는 CS/온콜로 비용 발생
- 단위 추가 시 **2시간~1일** + 회귀 불안

### 1.2 목표

레거시 `UnitConverter.py`(37줄)를 **ECB + Dual-Track TDD**로 재구현하여:

1. meter 기준 변환과 검증 규칙을 **한곳에 고정**
2. FR/NFR 요구와 테스트를 **1:1 추적** (C2C)
3. "작은 수정"이 QA·CS·온콜로 커지지 않게 **테스트 가능한 모듈** 제공

### 1.3 비목표 (P1)

- `units.json`/YAML 외부 설정 (EXT-01)
- 런타임 동적 단위 등록 (EXT-02)
- json/csv 출력 포맷 (EXT-03)

> Mom Test에서 위 3항목은 **과거 필요 행동으로 확인되지 않음**. P0 Green 완료 후 착수.

---

## 2. R-G-I-O

| 항목 | 정의 |
|------|------|
| **Role** | meter/feet/yard 변환 코드를 수정·추가·검증하는 개발자 (백엔드 / 데이터 / CLI 유지보수) |
| **Goal** | `unit:value` 입력에 대해 **전 단위** 변환 결과를 QA·CS 제보 **전에** 신뢰할 수 있게 얻는다 |
| **Input** | `unit:value` 문자열 (예: `meter:2.5`) |
| **Output** | 등록된 전 단위 변환 결과, table 형식, 소수 4자리 |

### 2.1 입력 (Input)

| ID | 케이스 | 예시 | 기대 |
|----|--------|------|------|
| — | 정상 | `meter:2.5` | 파싱 후 변환 |
| FR-04 | 음수 | `meter:-1` | 거부 또는 예외 |
| FR-05 | 콜론 없음 | `meter` | 형식 오류 |
| FR-05 | 비숫자 값 | `abc:2` | 형식 오류 |
| FR-03 | 미지 단위 | `cubit:1` (미등록) | 명확한 오류 |

- 앞뒤 공백 trim 허용: `" meter : 2.5 "` → FR-01 통과

### 2.2 출력 (Output)

**CLI 예시:**

```bash
python -m unit_converter "meter:2.5"
```

```
2.5 meter = 8.2021 feet
2.5 meter = 2.7340 yard
```

| 규칙 | 값 |
|------|-----|
| 기본 포맷 | table (`{value} {unit} = {result} {target_unit}`) |
| 정밀도 | 소수 4자리 |
| 검증 | `pytest.approx(..., rel=1e-4)` |

---

## 3. 기능 요구사항 (P0)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| FR-01 | `unit:value` 파싱 | `meter:2.5` | value=2.5, unit=meter |
| FR-02 | 전 단위 출력 | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-03 | 미지 단위 | cubit:1 (미등록) | 명확한 오류 |
| FR-04 | 음수 거부 | meter:-1 | 거부 또는 예외 |
| FR-05 | 잘못된 형식 | `meter`, `abc:2` | 형식 오류 |

### 3.1 변환 로직

| 규칙 | 값 |
|------|-----|
| 1 meter | 3.28084 feet |
| 1 meter | 1.09361 yard |
| feet ↔ yard | **반드시 meter 경유** |
| 기본 등록 단위 | meter, feet, yard |

### 3.2 Mom Test → FR 연결

| Mom Test 관찰 | FR |
|---------------|-----|
| feet↔yard 0.01~0.02 어긋남 | FR-02 (meter 경유) |
| `meter:-1` CS 티켓 | FR-04 |
| `meter`만 입력 이상 동작 | FR-05 |
| cubit 추가 2시간+ | FR-03, NFR-01 |
| `meter:2.5` 파싱·출력 | FR-01, FR-02 |

---

## 4. 비기능 요구사항 (P0)

| ID | 요구 | Then |
|----|------|------|
| NFR-01 | OCP | inch 등 신규 단위 추가 시 converter **핵심 코드 미수정** |
| NFR-02 | SRP | Parser / Registry / Converter / Formatter **파일·역할 분리** |

### 4.1 OCP (NFR-01)

- `LengthUnit` Protocol: `name`, `to_meter(value) -> float`
- 신규 단위: 구현 + `registry.register()` — `if/elif` 분기 금지
- 변환 비율 하드코딩 금지 → Registry 또는 설정 (P1: EXT-01)

### 4.2 SRP (NFR-02)

| 모듈 | 책임 |
|------|------|
| Parser | `unit:value` 파싱·검증 |
| Registry | 단위 등록·조회 |
| Converter | meter 기준 변환 |
| Formatter | table/json/csv 출력 (P0: table) |

---

## 5. 확장 요구사항 (P1)

| ID | 요구 | Given | Then |
|----|------|-------|------|
| EXT-01 | 설정 외부화 | units.json | Registry에 비율 로드 |
| EXT-02 | 동적 등록 | 1 cubit = 0.4572 m | cubit:1 즉시 변환 |
| EXT-03 | 출력 포맷 | `--format json\|csv\|table` | 포맷별 검증 |

**착수 조건:** P0 Green 완료.

---

## 6. 아키텍처

### 6.1 ECB 계층

| 계층 | 경로 | 책임 |
|------|------|------|
| Entity | `src/entity/` | LengthUnit, UnitRegistry, Converter |
| Control | `src/control/` | 유스케이스 조율 |
| Boundary | `src/boundary/` | InputParser, OutputFormatter, ConfigLoader, CLI |

**의존 방향:** `entity` ← `control` ← `boundary`

### 6.2 Dual-Track TDD

| Track | tests | FR/NFR |
|-------|-------|--------|
| B (Logic) | `tests/entity/`, `tests/control/` | FR-02~04, NFR-01, EXT-02 |
| A (I/O) | `tests/boundary/` | FR-01, FR-05, NFR-02, EXT-01, EXT-03 |

**P0 RED 순서:** FR-02 → FR-04 → FR-03 → FR-01 → FR-05 → NFR-01 → NFR-02

**P0 GREEN 순서:** `src/entity` → `src/control` → `src/boundary`

---

## 7. 오류 처리

| 계층 | 예외 (예) | Boundary 처리 |
|------|-----------|---------------|
| Entity | UnknownUnitError, NegativeValueError, InvalidFormatError | stderr 사용자 메시지 |

---

## 8. Harness·CLI

| 항목 | 값 |
|------|-----|
| Python | >= 3.10 |
| 테스트 | pytest only |
| pythonpath | `["src"]` |
| 패키지명 | `unit-converter` (pyproject.toml) |
| CLI | `python -m unit_converter "meter:2.5"` |
| 레거시 | `UnitConverter.py` — 참고용, **수정 금지** |

---

## 9. 성공 기준

Mom Test 언어 (`Report/01` §3.3):

1. yard 추가가 **2시간+** 디버깅으로 커지지 않음
2. feet→yard **0.01 차이**가 QA 제보 전에 테스트로 잡힘
3. `meter:-1`, 형식 오류가 **CS/온콜 이후가 아닌** 모듈 계약에서 거부됨
4. 단위 추가 시 **meter/feet/yard 회귀** 자동 확인

---

## 10. 참고

| 문서 | 용도 |
|------|------|
| `README.md` | 실습·실행 가이드 |
| `Report/01/UnitConverter_ProblemDefinition_Report.md` | Mom Test·주제·R-G-I-O |
| `Report/02/Traceability_Matrix.md` | FR/NFR ↔ 테스트 ID |
| `.cursorrules` | Agent 구현 규칙 |
