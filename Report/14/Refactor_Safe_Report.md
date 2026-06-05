# Report/14 — Safe Refactor 보고서 (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 단계 | **Refactor** — Golden Master 확보 + Safe Refactoring |
| Git 브랜치 | `refactoring` |
| Phase | refactor \| Golden Master baseline → safe refactor |
| 기준선 | `Report/13/Golden_Master_Baseline.md` (커밋 `067ca8e`) |

---

## 1. 주제 (1문장)

P0 Green 7/7 완료 후 **Golden Master baseline(12 tests)** 을 확보하고, 동작 변경 없이 OCP/SRP 관점의 **safe refactoring**을 수행한 뒤 회귀 **12/12 PASS**를 확인했다.

---

## 2. 단계 요약

| 단계 | 상태 | 산출물 |
|------|------|--------|
| P0 Green (Report/12) | ✅ | FR-01~05, NFR-01~02 |
| **Golden Master 확보** | ✅ | `Report/13`, 12 passed baseline |
| **Safe Refactor** | ✅ | `length_unit`, `input_parser`, `output_formatter` |
| 회귀 검증 | ✅ | 12 passed, exit 0 |
| EXT P1 | ⬜ | 미착수 |

---

## 3. Golden Master (Refactor 전)

### 검증 명령

```powershell
python -m pytest tests/entity tests/control tests/boundary -v
```

### 결과

| 항목 | 값 |
|------|-----|
| 수집 | 12 tests |
| 통과 | **12 passed** |
| Exit code | 0 |

상세 baseline: `Report/13/Golden_Master_Baseline.md`

---

## 4. Safe Refactor 상세

### 변경 원칙

- **동작 변경 금지** — 테스트 assert·API 시그니처 유지
- **converter.py 미수정** — NFR-01 OCP (inch 등록 회귀)
- **UnitConverter.py 미수정** — 레거시 시드 유지
- **control/ EXT 미착수** — 테스트 없는 범위 제외

### 변경 파일 (3)

| 파일 | Refactor 내용 | 목적 |
|------|---------------|------|
| `src/entity/length_unit.py` | `METERS_PER_FOOT`, `METERS_PER_YARD` 상수 + `_RatioBasedUnit` | 비율 한곳 정의, Feet/Yard 중복 제거 (OCP-03) |
| `src/boundary/input_parser.py` | `_reject_invalid_format()` 추출 | 형식 오류 메시지 DRY (SRP) |
| `src/boundary/output_formatter.py` | `OUTPUT_DECIMAL_PLACES = 4` | PRD 4자리 정밀도 명명 |

### 미변경 (의도적)

| 파일 | 이유 |
|------|------|
| `converter.py` | NFR-01 — 변환 핵심 OCP |
| `unit_registry.py` | 변경 불필요 |
| `errors.py` | 변경 불필요 |
| `UnitConverter.py` | 레거시 금지 |

---

## 5. 회귀 결과 (Refactor 후)

```powershell
python -m pytest tests/entity tests/control tests/boundary -v
```

```
12 passed in 0.07s
Exit code: 0
```

| 확인 항목 | Baseline | Refactor 후 |
|-----------|----------|---------------|
| 테스트 수 | 12 | 12 |
| 통과 | 12 | 12 |
| 실패 | 0 | 0 |
| Golden Master 유지 | — | ✅ |

---

## 6. SRP / OCP 검사 요약

| 검사 | 결과 |
|------|------|
| `if/elif` 단위 분기 | 없음 ✅ |
| 비율 하드코딩 in converter | 없음 ✅ |
| ECB 의존 방향 (entity ← boundary) | 유지 ✅ |
| Parser — 파싱만 | ✅ |
| Formatter — 출력만 | ✅ |
| Registry / Converter | 미변경 ✅ |

---

## 7. diff 통계

```
src/boundary/input_parser.py     |  8 ++++++--
src/boundary/output_formatter.py |  5 ++++-
src/entity/length_unit.py        | 28 ++++++++++++++++++----------
3 files changed, 28 insertions(+), 13 deletions(-)
```

---

## 8. 권장 다음 작업

1. **control layer** — Parser + Converter + Formatter 유스케이스 조율 (CLI 전)
2. **EXT-01 Red** — `units.json` + ConfigLoader
3. **Git commit** — `refactoring` 브랜치에 본 Refactor + Report/13~14

---

## 9. 참고

- Golden Master: `Report/13/Golden_Master_Baseline.md`
- P0 Green 완료: `Report/12/P0_Green_Complete_Report.md`
- Transcript: `Prompting/transcript_refactor_safe.md`
- Skill Refactor: `.cursor/skills/dual-track-ecb/SKILL.md` §5
