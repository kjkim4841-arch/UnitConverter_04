# Report/02 — PRD → Test Traceability Matrix

> FR/NFR/EXT 요구사항을 Test ID와 1:1 매핑. Given/Then은 Red 테스트 docstring 기준.

## Functional Requirements (P0)

| ID | 요구 | Given | Then | Track | 테스트 폴더 (권장) |
|----|------|-------|------|-------|-------------------|
| FR-01 | meter:2.5 파싱 | 유효 문자열 | value=2.5, unit=meter | A | `tests/boundary/` |
| FR-02 | 전 단위 출력 | meter 2.5 | feet≈8.2021, yard≈2.7340 | B | `tests/entity/` 또는 `tests/control/` |
| FR-03 | 미지 단위 | cubit:1 (미등록) | 명확한 오류 | B | `tests/entity/` |
| FR-04 | 음수 | meter:-1 | 거부 또는 예외 | B | `tests/entity/` |
| FR-05 | 잘못된 형식 | meter / abc | 형식 오류 | A | `tests/boundary/` |

## Non-Functional Requirements (P0)

| ID | 요구 | Given | Then | Track | 테스트 폴더 (권장) |
|----|------|-------|------|-------|-------------------|
| NFR-01 | OCP | inch 등 신규 단위 추가 | converter 핵심 코드 미수정 | B | `tests/entity/` |
| NFR-02 | SRP | — | Parser/Registry/Converter/Formatter 분리 | A+B | `tests/boundary/` + import 검사 |

## Extension Requirements (P1)

| ID | 요구 | Given | Then | Track | 테스트 폴더 (권장) |
|----|------|-------|------|-------|-------------------|
| EXT-01 | 설정 파일 | units.json | 비율 로드 | A | `tests/boundary/` |
| EXT-02 | 동적 등록 | 1 cubit = 0.4572 m | 즉시 변환 가능 | B+A | `tests/control/` |
| EXT-03 | 출력 포맷 | --format 플래그 | json/csv/table 검증 | A | `tests/boundary/` |

## Dual-Track 실행 명령

```powershell
# Track B — 도메인·유스케이스 (빠름)
pytest tests/entity tests/control -v

# Track A — CLI·통합 (느림)
pytest tests/boundary -v
```

## 테스트 파일 네이밍 규칙 (spec)

- `test_fr01_parse_input.py`
- `test_fr02_convert_all_units.py`
- `test_nfr01_ocp_add_inch.py`
- docstring 첫 줄에 `FR-02:` 등 ID 명시

## 커버리지 현황 (2025-06-05)

| ID | Red | Green | 비고 |
|----|-----|-------|------|
| FR-01 | ✅ | ❌ | `tests/boundary/test_fr01_parse_input.py` |
| FR-02 | ✅ | ✅ | `tests/entity/test_fr02_convert_all_units.py` |
| FR-03 | ✅ | ❌ | `tests/entity/test_fr03_unknown_unit.py` |
| FR-04 | ✅ | ✅ | `tests/entity/test_fr04_reject_negative.py` |
| FR-05 | ✅ | ❌ | `tests/boundary/test_fr05_invalid_format.py` |
| NFR-01 | ✅ | ❌ | `tests/entity/test_nfr01_ocp_add_inch.py` |
| NFR-02 | ✅ | ❌ | `tests/boundary/test_nfr02_module_separation.py` |
| EXT-01 ~ EXT-03 | ❌ | ❌ | P1 — P0 Green 후 |
