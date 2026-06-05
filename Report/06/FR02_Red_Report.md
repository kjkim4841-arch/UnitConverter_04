# Report/06 — FR-02 Red 단계 보고서 (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 단계 | **P0 RED 착수** — Entity layer FR-02 완료 |
| 세션 ID | 936663ad-c3bd-4d88-91ab-c49999074976 |
| Phase | red \| Layer: entity \| Track: B \| ID: FR-02 |

---

## 1. 주제 (1문장)

Entity layer Dual-Track TDD **Red 단계**를 착수하고, P0 우선순위 첫 항목 **FR-02(전 단위 출력)** 실패 테스트를 작성·검증했다.

---

## 2. 단계 요약

| 단계 | 상태 | 산출물 |
|------|------|--------|
| spec 완료 (Report/04) | ✅ | `.cursorrules`, Skill, Command, Harness |
| Entity Red 가이드 | ✅ | Ask 세션 — FR-02~NFR-01 순서·AAA·규칙 정리 |
| **FR-02 Red** | ✅ | `tests/entity/test_fr02_convert_all_units.py` |
| FR-04 Red | ⬜ | 미착수 |
| FR-03 Red | ⬜ | 미착수 |
| NFR-01 Red | ⬜ | 미착수 |
| Entity Green | ⬜ | `src/entity/` 미구현 |

---

## 3. FR-02 Red 상세

### 테스트 파일

`tests/entity/test_fr02_convert_all_units.py`

| 항목 | 내용 |
|------|------|
| Given | `UnitRegistry()` + `Converter(registry)`, 입력 `"meter", 2.5` |
| Then | `results["feet"] ≈ 8.2021`, `results["yard"] ≈ 2.7340` |
| 검증 | `pytest.approx(..., rel=1e-4)` |
| docstring | `FR-02: 전 단위 출력` |

### pytest 실행 결과 (Red 확인)

```powershell
python -m pytest tests/entity/test_fr02_convert_all_units.py -v
```

```
ModuleNotFoundError: No module named 'entity.converter'
```

| 확인 항목 | 결과 |
|-----------|------|
| `tests/` 만 변경 | ✅ |
| `src/` 변경 없음 | ✅ (Green 미착수) |
| Domain mock 없음 | ✅ |
| assert 완화 없음 | ✅ |

---

## 4. FR/NFR 커버리지 (Report/02 갱신)

| ID | Red | Green | 비고 |
|----|-----|-------|------|
| **FR-02** | ✅ | ❌ | entity — 본 세션 |
| FR-01 | ❌ | ❌ | boundary |
| FR-03 | ❌ | ❌ | entity |
| FR-04 | ❌ | ❌ | entity |
| FR-05 | ❌ | ❌ | boundary |
| NFR-01 | ❌ | ❌ | entity |
| NFR-02 | ❌ | ❌ | boundary |
| EXT-01 ~ EXT-03 | ❌ | ❌ | P1 — P0 Green 후 |

---

## 5. Entity layer Red 잔여 작업

P0 Entity Red 순서 (남은 항목):

```
FR-04 → FR-03 → NFR-01
```

| ID | 테스트 파일 (예정) | Given | Then |
|----|-------------------|-------|------|
| FR-04 | `test_fr04_reject_negative.py` | meter:-1 | `NegativeValueError` |
| FR-03 | `test_fr03_unknown_unit.py` | cubit (미등록) | `UnknownUnitError` |
| NFR-01 | `test_nfr01_ocp_add_inch.py` | inch 등록 | converter 핵심 미수정 |

Entity Red 4건 완료 후 → **Green** (`src/entity/`: LengthUnit, UnitRegistry, Converter)

---

## 6. 테스트 실행 가이드 (Windows)

| 목적 | 명령 |
|------|------|
| FR-02만 | `python -m pytest tests/entity/test_fr02_convert_all_units.py -v` |
| entity 전체 | `python -m pytest tests/entity -v` |
| Track B | `python -m pytest tests/entity tests/control -v` |

> Windows에서는 `pytest` 단독 실행 대신 `python -m pytest` 권장.

---

## 7. 세션 활동 로그

| # | 주제 | 모드 | 결과 |
|---|------|------|------|
| 1 | Entity layer Red 진행 방법 | Ask | FR-02~NFR-01 순서·예시·규칙 |
| 2 | FR-02 Red 작성 | Agent | 테스트 파일 + FAIL 확인 |
| 3 | pytest 결과 확인 방법 | Ask | Windows 명령·결과 해석 |
| 4 | Report + Transcript Export | Agent | Report/06, Prompting/ |

---

## 8. 권장 다음 작업

1. **FR-04 Red** — `tests/entity/test_fr04_reject_negative.py`
2. **FR-03 Red** — `tests/entity/test_fr03_unknown_unit.py`
3. **NFR-01 Red** — `tests/entity/test_nfr01_ocp_add_inch.py`
4. **Entity Green** — `src/entity/` 구현 후 FR-02 pytest PASS 확인
5. `/review-ecb` — ECB·계약 검수

---

## 9. 참고

- Transcript: `Prompting/transcript_936663ad.md`
- 추적표: `Report/02/Traceability_Matrix.md`
- Red Command: `.cursor/commands/tdd-red.md`
- Skill: `.cursor/skills/dual-track-ecb/SKILL.md`
