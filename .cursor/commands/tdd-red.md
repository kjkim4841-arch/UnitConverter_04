# UnitConverter_04 Dual-Track TDD — RED 단계만

`.cursorrules`, `Report/02/Traceability_Matrix.md`를 따른다. **Red만** 수행한다. Green·src 구현 금지.

---

# TDD RED — 실패 테스트 먼저

## 필수 선언

작업 시작 시 **응답 첫 줄**에 반드시 선언한다:

```
Phase: red | Layer: {entity|control|boundary} | Track: {A|B} | ID: {FR-01|FR-02|…}
```

| Layer | Track | tests 폴더 |
|-------|-------|-----------|
| entity | B (Logic) | `tests/entity/` |
| control | B (Logic) | `tests/control/` |
| boundary | A (I/O) | `tests/boundary/` |

**FR → Layer/Track 매핑**

| ID | Layer | Track | 폴더 |
|----|-------|-------|------|
| FR-01 | boundary | A | `tests/boundary/` |
| FR-02 | entity | B | `tests/entity/` |
| FR-03 | entity | B | `tests/entity/` |
| FR-04 | entity | B | `tests/entity/` |
| FR-05 | boundary | A | `tests/boundary/` |
| NFR-01 | entity | B | `tests/entity/` |
| NFR-02 | boundary | A | `tests/boundary/` |
| EXT-02 | control | B | `tests/control/` |
| EXT-01, EXT-03 | boundary | A | `tests/boundary/` |

**P0 Red 순서:** FR-02 → FR-04 → FR-03 → FR-01 → FR-05 → NFR-01 → NFR-02

---

## 절차

1. **ID 확인** — 사용자 지정 FR/NFR/EXT ID, 없으면 P0 순서에서 다음 ID 선택
2. **Layer·Track·폴더** — 위 매핑표 적용
3. **AAA 테스트 작성**
   - **Arrange:** Given 조건 (입력값, Registry 등)
   - **Act:** 변환·파싱·호출 실행
   - **Assert:** Then 기대값 (`pytest.approx` rel=1e-4, `pytest.raises` 등)
   - 파일: `tests/{layer}/test_{id_lowercase}_{slug}.py`
   - docstring 첫 줄: `FR-02: 전 단위 출력` 형식
4. **pytest FAIL** — 해당 테스트 실행, **실패 확인** 후 종료

---

## pytest 예시 (bash)

```bash
# Track B — Logic (entity + control)
pytest tests/entity -v -k "fr02"
pytest tests/control -v -k "ext02"

# Track A — I/O (boundary)
pytest tests/boundary -v -k "fr01"

# 방금 작성한 파일만
pytest tests/entity/test_fr02_convert_all_units.py -v
```

실패 유형 예: `ImportError`, `ModuleNotFoundError`, `AssertionError`, `Failed: Red: not implemented`

---

## 보고

Red 완료 시 아래 형식으로 보고한다:

```
Phase: red | Layer: entity | Track: B | ID: FR-02

- 테스트 ID: FR-02
- FAIL 요약: ImportError — entity.converter not found (1 failed)
- 변경 파일: tests/entity/test_fr02_convert_all_units.py (tests/ 만)
- Green 미착수 확인: src/ 변경 없음
```

---

## 금지

- `src/` 수정 (import stub·주석 처리된 import 참조만 허용)
- `UnitConverter.py` 수정
- **Logic Track (B)에서 Domain Mock** — entity/control 테스트에 도메인 객체 mock·patch 금지
- **assert 완화** — `pytest.approx` 기준 낮추기, `raises` 제거, `pytest.fail` 삭제로 통과시키기 금지
- P0 미완료 시 P1 EXT Red
- 요청 ID 외 테스트 추가
- git commit
