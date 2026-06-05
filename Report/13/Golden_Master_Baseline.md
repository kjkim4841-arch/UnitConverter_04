# Report/13 — Golden Master Baseline (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 목적 | Refactor 전 회귀 기준선 (Golden Master) |
| Git 커밋 | `067ca8e` (green 브랜치, P0 Green 7/7) |
| Phase | refactor 준비 \| pre-refactor baseline |

---

## 1. 검증 명령

```powershell
python -m pytest tests/entity tests/control tests/boundary -v
```

또는 (pyproject `testpaths` 기준):

```powershell
python -m pytest -v
```

---

## 2. Golden Master 결과

| 항목 | 값 |
|------|-----|
| 수집 | **12 tests** |
| 통과 | **12 passed** |
| 실패 | 0 |
| 스킵/xfail | 0 |
| Exit code | **0** |
| 소요 | ~0.07s |

**판정: ✅ Refactor 착수 가능**

---

## 3. 테스트 목록 (12/12 PASS)

### Track B — Entity (4)

| # | 파일 | 테스트 | ID |
|---|------|--------|-----|
| 1 | `test_fr02_convert_all_units.py` | `test_meter_converts_to_all_registered_units` | FR-02 |
| 2 | `test_fr03_unknown_unit.py` | `test_unknown_unit_rejected` | FR-03 |
| 3 | `test_fr04_reject_negative.py` | `test_negative_value_rejected` | FR-04 |
| 4 | `test_nfr01_ocp_add_inch.py` | `test_register_inch_without_modifying_converter` | NFR-01 |

### Track A — Boundary (8)

| # | 파일 | 테스트 | ID |
|---|------|--------|-----|
| 5 | `test_fr01_parse_input.py` | `test_parse_meter_value` | FR-01 |
| 6 | `test_fr01_parse_input.py` | `test_parse_trims_whitespace` | FR-01 |
| 7 | `test_fr05_invalid_format.py` | `test_invalid_format_rejected[meter]` | FR-05 |
| 8 | `test_fr05_invalid_format.py` | `test_invalid_format_rejected[meter:abc]` | FR-05 |
| 9 | `test_fr05_invalid_format.py` | `test_invalid_format_rejected[meter:2.5:extra]` | FR-05 |
| 10 | `test_fr05_invalid_format.py` | `test_invalid_format_rejected[:2.5]` | FR-05 |
| 11 | `test_fr05_invalid_format.py` | `test_invalid_format_rejected[meter:]` | FR-05 |
| 12 | `test_nfr02_module_separation.py` | `test_srp_module_files_exist` | NFR-02 |

### Track B — Control (0)

`tests/control/` — 테스트 없음 (EXT-02 P1 예정)

---

## 4. Refactor 회귀 규칙

Refactor 후 **동일 명령** 실행 시:

- **12 passed, exit 0** → Golden Master 유지, Refactor 계속
- **1건이라도 FAIL** → 중단, diff 조사 후 baseline 대비 복구

---

## 5. 범위 밖 (본 baseline 미포함)

| 항목 | 상태 |
|------|------|
| EXT-01 ~ EXT-03 | Red/Green 미착수 |
| CLI 통합 (`python -m unit_converter`) | 미구현 |
| `UnitConverter.py` 레거시 | 시드 유지, 테스트 대상 아님 |

---

## 6. 참고

- P0 Green 완료: `Report/12/P0_Green_Complete_Report.md`
- 추적표: `Report/02/Traceability_Matrix.md`
- Refactor 절차: `.cursor/skills/dual-track-ecb/SKILL.md` §5
