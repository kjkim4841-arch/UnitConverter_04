---
name: dual-track-ecb
description: UnitConverter_04 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차
---

# Dual-Track ECB 개발 절차

## When to use
- Red / Green / Refactor 단계 요청
- FR·NFR·EXT 구현 또는 테스트 작성
- ECB 계층(`entity`, `control`, `boundary`) 코드 추가
- 신규 단위 추가 (OCP / NFR-01)

## Prerequisites
- `.cursorrules`, `Report/01`, `Report/02` 준수
- Harness: `pyproject.toml`, `src/`, `tests/`
- `UnitConverter.py` 수정 금지; 신규 코드는 `src/`만

---

## 1. ECB 계층 — 어디에 무엇을

| 계층 | 경로 | 책임 |
|------|------|------|
| Entity | `src/entity/` | LengthUnit, UnitRegistry, Converter |
| Control | `src/control/` | 유스케이스 조율 |
| Boundary | `src/boundary/` | InputParser, OutputFormatter, ConfigLoader, CLI |

**의존 방향:** `entity` ← `control` ← `boundary` (역방향 import 금지)

**SRP:** Parser / Registry / Converter / Formatter — 한 파일 = 한 역할

**OCP:** 신규 단위 = `LengthUnit` 구현 + `registry.register()` — `converter.py` 핵심 수정 금지, `if/elif` 분기 금지

---

## 2. Dual-Track — 테스트 배치

| Track | 폴더 | 실행 |
|-------|------|------|
| B (빠름) | `tests/entity/`, `tests/control/` | `pytest tests/entity tests/control -v` |
| A (느림) | `tests/boundary/` | `pytest tests/boundary -v` |

| FR/NFR | 테스트 폴더 |
|--------|------------|
| FR-01, FR-05 | `tests/boundary/` |
| FR-02, FR-03, FR-04, NFR-01 | `tests/entity/` |
| NFR-02 | `tests/boundary/` (+ import 검사) |
| EXT-02 | `tests/control/` |
| EXT-01, EXT-03 | `tests/boundary/` |

- 파일명: `test_fr02_convert_all_units.py`
- docstring 첫 줄: `FR-02: 전 단위 출력`

---

## 3. Red 절차

### P0 순서 (건너뛰지 않음)
`FR-02 → FR-04 → FR-03 → FR-01 → FR-05 → NFR-01 → NFR-02`

### 단계
1. FR ID·폴더 결정 (§2 표)
2. `tests/{entity|control|boundary}/test_{id}_{slug}.py` 생성
3. Given/Then을 assert / `pytest.raises`로 표현
4. FR-02: `pytest.approx(..., rel=1e-4)` (8.2021, 2.7340)
5. `pytest` 실행 → **실패(Red) 확인** 후 종료
6. `src/` 프로덕션 코드 작성하지 않음 (import stub 허용)

### Given/Then 요약
| ID | Given | Then |
|----|-------|------|
| FR-01 | `meter:2.5` | value=2.5, unit=meter |
| FR-02 | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-03 | cubit:1 (미등록) | UnknownUnitError 등 |
| FR-04 | meter:-1 | NegativeValueError 등 |
| FR-05 | `meter / abc` | InvalidFormatError 등 |

---

## 4. Green 절차

### P0 Green 순서
`src/entity` → `src/control` → `src/boundary`

### 단계
1. **한 계층만** 수정 (요청 범위 준수)
2. Entity 먼저:
   - `LengthUnit` Protocol: `name`, `to_meter(value) -> float`
   - `UnitRegistry`: meter/feet/yard 초기 등록
   - `Converter`: meter 기준 변환, feet↔yard는 meter 경유
3. `pytest` 해당 Track 실행 → 통과 확인
4. Green 완료 시 `Report/02` 커버리지 갱신 제안

### 오류 처리
- Entity: `UnknownUnitError`, `NegativeValueError`, `InvalidFormatError`
- Boundary: 예외 → stderr 사용자 메시지

---

## 5. Refactor 절차

1. OCP/SRP 위반 제거 (`if/elif`, 하드코딩 비율, main() 혼합)
2. 중복 제거, 의존 방향 재확인
3. `pytest tests/entity tests/control tests/boundary -v` 회귀

---

## 6. 신규 단위 추가 (NFR-01 / OCP)

1. `src/entity/`에 `LengthUnit` 구현 (비율은 클래스 또는 `units.json`)
2. `registry.register(NewUnit())` — converter 핵심 미수정
3. `tests/entity/test_nfr01_ocp_add_{unit}.py` Red → Green
4. FR-02 회귀: `pytest tests/entity -v`

**체크:** converter.py diff 없음, if/elif 없음

---

## 7. P1 EXT (P0 Green 후만)

| ID | 작업 |
|----|------|
| EXT-01 | `units.json` / YAML → ConfigLoader → Registry |
| EXT-02 | 동적 등록 유스케이스 → `tests/control/` |
| EXT-03 | `--format json\|csv\|table` → `tests/boundary/` |

---

## Do NOT
- `UnitConverter.py` 수정
- P0 미완료 시 P1 EXT 착수
- Red 단계에서 Green 코드 선작성
- 요청 FR·계층 외 변경
- git commit (사용자 요청 시만)
- pytest 외 dev 의존성 추가
