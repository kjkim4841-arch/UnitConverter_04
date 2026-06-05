# UnitConverter_04 — ECB·계약 리뷰 (Test/Review Loop)

`.cursorrules`, `Report/01`, `Report/02`를 기준으로 **읽기 전용 리뷰**만 수행한다.
**코드·테스트·설정 파일 수정 금지.** 위반 항목만 표로 보고한다.

---

# ECB Review — 코드 수정 없이 검수

## 필수 선언

응답 **첫 줄**:

```
Phase: review | Scope: {src|tests|all} | Layer: {entity|control|boundary|cross}
```

---

## 절차

1. **범위 확인** — 사용자 지정 경로, 없으면 `src/` + `tests/` 전체
2. **읽기 전용 분석** — Read/Grep만 사용, Write/Edit/Shell(파일 변경) 금지
3. **pytest 실행 허용** — 통과/실패 현황 파악용 (수정 없음)
4. **위반만 표로 정리** — 해당 없으면 "위반 없음" 명시
5. **수정 제안은 텍스트로만** — 코드 패치·자동 수정 금지

---

## 검사 항목

### A. ECB 계층

| 검사 ID | 계약 | 위반 예시 |
|---------|------|----------|
| ECB-01 | `length_unit`, `unit_registry`, `converter` → `src/entity/` | boundary에 Converter 배치 |
| ECB-02 | `input_parser`, `output_formatter`, `cli`, `config_loader` → `src/boundary/` | entity에 Parser 배치 |
| ECB-03 | 유스케이스 조율 → `src/control/` | boundary에서 변환 로직 직접 수행 |
| ECB-04 | entity → 외부 계층 import 금지 | `entity`가 `boundary` import |
| ECB-05 | control → entity만 import | control이 boundary import |
| ECB-06 | boundary → control, entity import 가능 | — |

### B. SRP / OCP (NFR-02, NFR-01)

| 검사 ID | 계약 | 위반 예시 |
|---------|------|----------|
| SRP-01 | Parser — 파싱·검증만 | Parser에서 변환 수행 |
| SRP-02 | Registry — 등록·조회만 | Registry에서 출력 포맷 |
| SRP-03 | Converter — meter 기준 변환만 | Converter에서 CLI 인자 처리 |
| SRP-04 | Formatter — 출력만 | Formatter에서 비율 하드코딩 |
| OCP-01 | 단위 추가 시 converter 핵심 미수정 | `if/elif` 단위 분기 |
| OCP-02 | 신규 단위 = LengthUnit + register | converter에 단위별 메서드 추가 |
| OCP-03 | 비율 하드코딩 금지 | `3.28084`가 converter에 직접 상수 |

### C. FR/NFR 계약 (Report/02)

| 검사 ID | 계약 | 위반 예시 |
|---------|------|----------|
| FR-01 | `meter:2.5` → value=2.5, unit=meter | 파싱 결과 타입·필드 불일치 |
| FR-02 | meter 2.5 → feet≈8.2021, yard≈2.7340 | 정밀도·meter 경유 미준수 |
| FR-03 | 미등록 단위 → 명확한 오류 | UnknownUnitError 없음 |
| FR-04 | 음수 → 거부/예외 | NegativeValueError 없음 |
| FR-05 | 잘못된 형식 → 형식 오류 | `meter:2.5:extra` 미처리 |
| NFR-01 | inch 추가 시 converter 미수정 | converter diff 발생 |
| NFR-02 | 4모듈 파일·import 분리 | Parser↔Converter 직접 결합 |

### D. Dual-Track 테스트 배치

| 검사 ID | 계약 | 위반 예시 |
|---------|------|----------|
| TRK-01 | FR-01, FR-05 → `tests/boundary/` | entity에 파싱 테스트 |
| TRK-02 | FR-02~04, NFR-01 → `tests/entity/` | boundary에 변환 단위 테스트 |
| TRK-03 | EXT-02 → `tests/control/` | entity에 동적 등록 유스케이스 |
| TRK-04 | docstring 첫 줄에 FR ID | ID 누락 |
| TRK-05 | Logic Track(B) Domain Mock 금지 | entity 테스트에 mock 남용 |

### E. 오류 처리 계약

| 검사 ID | 계약 | 위반 예시 |
|---------|------|----------|
| ERR-01 | Entity — 도메인 예외 | print 후 return |
| ERR-02 | Boundary — 예외 → stderr 메시지 | 예외 삼킴 |
| ERR-03 | FR-02 approx rel=1e-4 | assert 완화·정밀도 불일치 |

---

## pytest (현황 파악용, bash)

```bash
pytest tests/entity tests/control -v
pytest tests/boundary -v
```

실행 결과는 **리뷰 표의 "테스트 현황" 행**에만 반영. 실패 수정 금지.

---

## 보고 형식 (표 필수)

### 1. 요약

| 항목 | 값 |
|------|-----|
| Phase | review |
| Scope | src + tests |
| ECB 위반 | {N}건 |
| 계약 위반 | {N}건 |
| 테스트 | passed {P} / failed {F} |

### 2. ECB·계약 위반 목록

| # | 검사 ID | 심각도 | 파일 | 위반 내용 | 계약 근거 |
|---|---------|--------|------|----------|----------|
| 1 | ECB-04 | HIGH | `src/entity/foo.py` | boundary import | .cursorrules §2 의존 방향 |
| 2 | OCP-01 | HIGH | `src/entity/converter.py` | if/elif unit | NFR-01 |

- **심각도:** HIGH (아키텍처·OCP/SRP) / MED (FR·테스트 배치) / LOW (네이밍·docstring)
- 위반 0건이면: `| — | — | — | 위반 없음 | — |`

### 3. 테스트 현황 (FR별)

| FR ID | Red | Green | 테스트 파일 | 비고 |
|-------|-----|-------|------------|------|
| FR-02 | ✅ | ❌ | `tests/entity/test_fr02_…` | Report/02 대조 |

### 4. 권고 (수정 없이 텍스트만)

- 우선 수정 대상 1~3건 (사용자가 Green/Refactor 요청 시 참고)

---

## 금지

- `src/`, `tests/`, `pyproject.toml`, `.cursorrules` **수정**
- 위반 항목 **자동 수정·리팩터**
- git commit
- Skill 파일 생성
- 리뷰 범위 밖 기능 제안 (위반 관련만)
