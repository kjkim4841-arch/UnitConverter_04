# Report/11 — FR-05 Green 단계 보고서 (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 단계 | **P0 GREEN 진행** — Boundary layer FR-05 완료 (6/7) |
| Git 브랜치 | `green` |
| Phase | green \| Layer: boundary \| Track: A \| ID: FR-05 |

---

## 1. 주제 (1문장)

P0 Boundary Green 순서(FR-01 다음)에 따라 **FR-05(잘못된 형식 오류)** 를 구현하고, 5종 형식 오류 Red 테스트를 Green(PASS)으로 전환했다.

---

## 2. 단계 요약

| 단계 | 상태 | 산출물 |
|------|------|--------|
| P0 Red (Report/07) | ✅ | FR-01~05, NFR-01~02 (7/7) |
| Entity Green (Report/08~10) | ✅ | FR-02~04, FR-03, NFR-01 |
| FR-01 Green (Report/10) | ✅ | `InputParser`, `ParsedInput` |
| **FR-05 Green** | ✅ | `InvalidFormatError` + 형식 검증 |
| NFR-02 Green | ⬜ | `output_formatter.py` 미생성 |
| Control Green | ⬜ | EXT-02 (P1) |

---

## 3. FR-05 Green 상세

### 테스트 (변경 없음)

`tests/boundary/test_fr05_invalid_format.py`

| 항목 | 내용 |
|------|------|
| Given | 5종 잘못된 입력 (parametrize) |
| Then | `InvalidFormatError` 발생 |
| 검증 | `pytest.raises(InvalidFormatError)` |

**거부 케이스:**

| 입력 | 거부 이유 |
|------|-----------|
| `meter` | 콜론 없음 |
| `meter:abc` | 비숫자 value |
| `meter:2.5:extra` | value 파싱 실패 |
| `:2.5` | 빈 unit |
| `meter:` | 빈 value |

### 구현 파일

| 파일 | 역할 |
|------|------|
| `src/entity/errors.py` | `InvalidFormatError` 도메인 예외 (`ValueError` 서브클래스) |
| `src/boundary/input_parser.py` | `parse()` — 콜론·빈 필드·float 변환 검증 |

### 검증 로직

- `:` 없음 → 즉시 `InvalidFormatError`
- unit 또는 value trim 후 빈 문자열 → `InvalidFormatError`
- `float()` 실패 → `InvalidFormatError` (chain from `ValueError`)
- FR-01 회귀: `meter:2.5`, 공백 trim 정상 파싱 유지

### pytest 실행 결과 (Green 확인)

```powershell
python -m pytest tests/boundary/test_fr05_invalid_format.py tests/boundary/test_fr01_parse_input.py tests/entity -v
```

```
test_invalid_format_rejected[meter] PASSED
test_invalid_format_rejected[meter:abc] PASSED
test_invalid_format_rejected[meter:2.5:extra] PASSED
test_invalid_format_rejected[:2.5] PASSED
test_invalid_format_rejected[meter:] PASSED
test_parse_meter_value PASSED
test_parse_trims_whitespace PASSED
(+ entity 4 tests PASSED)
11 passed in 0.08s
```

| 확인 항목 | 결과 |
|-----------|------|
| FR-05 Green (5 cases) | ✅ |
| FR-01 회귀 | ✅ |
| Entity 회귀 | ✅ |
| assert 완화 없음 | ✅ |
| `UnitConverter.py` 미수정 | ✅ |

---

## 4. FR/NFR 커버리지 (Report/02)

| ID | Red | Green | 비고 |
|----|-----|-------|------|
| FR-02~04, FR-03, NFR-01 | ✅ | ✅ | entity — Report/08~10 |
| FR-01 | ✅ | ✅ | boundary — Report/10 |
| **FR-05** | ✅ | ✅ | boundary — 본 세션 |
| NFR-02 | ✅ | ❌ | `output_formatter.py` 없음 |
| EXT-01 ~ EXT-03 | ❌ | ❌ | P1 |

---

## 5. Boundary Green 잔여 작업

```
NFR-02
```

| ID | 필요 구현 |
|----|----------|
| NFR-02 | `src/boundary/output_formatter.py` 생성 → SRP 모듈 5/5 |

---

## 6. 세션 활동 로그

| # | 주제 | 모드 | 결과 |
|---|------|------|------|
| 1 | FR-05 Green 요청 | Agent | `InvalidFormatError` + InputParser 검증 |
| 2 | FR-05 PASS + 회귀 | Agent | 11 passed 확인 |
| 3 | Report/02·03 갱신 | Agent | FR-05 Green ✅ 반영 |
| 4 | Report/11 + Transcript + GitHub | Agent | 본 보고서 |

---

## 7. 권장 다음 작업

1. **NFR-02 Green** — `output_formatter.py` stub → P0 Green 7/7 완료
2. **Refactor** — Green 누적 후 OCP/SRP 회귀 검사
3. **P1 EXT** — EXT-01~03 (P0 Green 후)

---

## 8. 참고

- P0 Green 진행 보고: `Report/10/P0_Green_Progress_Report.md`
- P0 Red 보고: `Report/07/P0_Red_Complete_Report.md`
- Transcript: `Prompting/transcript_fr05_green.md`
- 추적표: `Report/02/Traceability_Matrix.md`
- Skill: `.cursor/skills/dual-track-ecb/SKILL.md`
