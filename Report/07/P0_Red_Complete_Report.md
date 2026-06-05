# Report/07 — P0 Red 단계 완료 보고서 (UnitConverter_04)

| 항목 | 내용 |
|------|------|
| 작성일 | 2025-06-05 |
| 단계 | **P0 RED 완료** — FR-01~05, NFR-01~02 (7/7) |
| 세션 ID | 936663ad-c3bd-4d88-91ab-c49999074976 |
| Git 브랜치 | `red` (origin/red 푸시 완료) |
| Phase | red \| Layer: entity + boundary \| Track: B + A |

---

## 1. 주제 (1문장)

Entity layer Red TDD를 착수하여 FR-02부터 시작했고, P0 전체 Red 테스트(FR-01~05, NFR-01~02) 7건을 작성·검증하여 Green 구현을 위한 실패 테스트 세트를 완성했다.

---

## 2. 단계 요약

| 단계 | 상태 | 산출물 |
|------|------|--------|
| spec 완료 (Report/04) | ✅ | `.cursorrules`, Skill, Command, Harness |
| FR-02 Red (Report/06) | ✅ | `tests/entity/test_fr02_convert_all_units.py` |
| **P0 Red 전체** | ✅ | entity 4 + boundary 3 테스트 파일 |
| Entity Green | ⬜ | `src/entity/` 미구현 |
| Control / Boundary Green | ⬜ | `src/control/`, `src/boundary/` 미구현 |
| P1 EXT Red | ⬜ | P0 Green 후 |

---

## 3. P0 Red 테스트 목록

### Entity layer (Track B)

| ID | 파일 | Given | Then |
|----|------|-------|------|
| FR-02 | `test_fr02_convert_all_units.py` | meter 2.5 | feet≈8.2021, yard≈2.7340 |
| FR-04 | `test_fr04_reject_negative.py` | meter:-1 | `NegativeValueError` |
| FR-03 | `test_fr03_unknown_unit.py` | cubit (미등록) | `UnknownUnitError` |
| NFR-01 | `test_nfr01_ocp_add_inch.py` | inch 등록 | 결과에 inch 포함 |

### Boundary layer (Track A)

| ID | 파일 | Given | Then |
|----|------|-------|------|
| FR-01 | `test_fr01_parse_input.py` | `meter:2.5`, 공백 trim | unit=meter, value=2.5 |
| FR-05 | `test_fr05_invalid_format.py` | 5종 형식 오류 | `InvalidFormatError` |
| NFR-02 | `test_nfr02_module_separation.py` | SRP 모듈 5개 | 파일 존재 검증 |

---

## 4. pytest 실행 결과 (Red 확인)

```powershell
python -m pytest tests/entity tests/boundary -v
```

| 결과 | 건수 | 원인 |
|------|------|------|
| ERROR (collection) | 6 | `ModuleNotFoundError` — `src/` 미구현 |
| FAILED | 1 | NFR-02 — SRP 모듈 파일 5개 없음 |

**수집된 테스트:** 10개 (entity 4 + boundary 6)

| 확인 항목 | 결과 |
|-----------|------|
| `tests/` 만 변경 | ✅ |
| `src/` 프로덕션 코드 없음 | ✅ (Green 미착수) |
| Domain mock 없음 | ✅ |
| assert 완화 없음 | ✅ |

### 대표 FAIL 메시지

```
ModuleNotFoundError: No module named 'entity.converter'
```

```
AssertionError: missing SRP modules: src\entity\length_unit.py, ...
```

---

## 5. FR/NFR 커버리지 (Report/02)

| ID | Red | Green | 테스트 파일 |
|----|-----|-------|-------------|
| FR-01 | ✅ | ❌ | `tests/boundary/test_fr01_parse_input.py` |
| FR-02 | ✅ | ❌ | `tests/entity/test_fr02_convert_all_units.py` |
| FR-03 | ✅ | ❌ | `tests/entity/test_fr03_unknown_unit.py` |
| FR-04 | ✅ | ❌ | `tests/entity/test_fr04_reject_negative.py` |
| FR-05 | ✅ | ❌ | `tests/boundary/test_fr05_invalid_format.py` |
| NFR-01 | ✅ | ❌ | `tests/entity/test_nfr01_ocp_add_inch.py` |
| NFR-02 | ✅ | ❌ | `tests/boundary/test_nfr02_module_separation.py` |
| EXT-01 ~ EXT-03 | ❌ | ❌ | P1 — P0 Green 후 |

---

## 6. 테스트 실행 가이드 (Windows)

| 목적 | 명령 |
|------|------|
| P0 Red 전체 | `python -m pytest tests/entity tests/boundary -v` |
| Track B (entity) | `python -m pytest tests/entity -v` |
| Track A (boundary) | `python -m pytest tests/boundary -v` |
| ID 필터 | `python -m pytest -v -k "fr02"` |

> Windows에서는 `pytest` 단독 실행 대신 `python -m pytest` 권장.

---

## 7. GitHub 업로드 (본 세션)

| 항목 | 내용 |
|------|------|
| 브랜치 | `red` |
| 커밋 | `17defab` — FR-02 Red + Report/06 + Transcript |
| 저장소 | https://github.com/kjkim4841-arch/UnitConverter_04 |

> P0 Red 전체(Report/07, 추가 테스트 6건)는 본 Export 이후 커밋·푸시 대기.

---

## 8. 세션 활동 로그

| # | 주제 | 모드 | 결과 |
|---|------|------|------|
| 1 | Entity layer Red 진행 방법 | Ask | FR-02~NFR-01 순서·규칙 |
| 2 | FR-02 Red 작성 | Agent | 테스트 + FAIL 확인 |
| 3 | pytest 결과 확인 방법 | Ask | Windows 실행 가이드 |
| 4 | Report/06 + Transcript Export | Agent | FR-02 Red 보고서 |
| 5 | GitHub 업로드 | Agent | `red` 브랜치 푸시 |
| 6 | P0 Red 테스트 전체 추가 | Agent | FR-04~NFR-02 6건 |
| 7 | Report/07 + Transcript Export | Agent | 본 보고서 |

---

## 9. 권장 다음 작업

P0 Green 순서 (`.cursorrules` / Skill 기준):

```
src/entity → src/control → src/boundary
```

1. **Entity Green** — `LengthUnit`, `UnitRegistry`, `Converter`, `errors.py`
2. **Boundary Green** — `InputParser`, `OutputFormatter`
3. **Control Green** — 유스케이스 조율
4. **회귀** — `python -m pytest tests/entity tests/boundary -v` 전체 PASS
5. **P1 EXT Red** — EXT-01~03 (P0 Green 후)

---

## 10. 참고

- 이전 Red 보고: `Report/06/FR02_Red_Report.md`
- Transcript: `Prompting/transcript_936663ad.md`
- 추적표: `Report/02/Traceability_Matrix.md`
- Red Command: `.cursor/commands/tdd-red.md`
- Skill: `.cursor/skills/dual-track-ecb/SKILL.md`
