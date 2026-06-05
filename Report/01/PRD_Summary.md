# Report/01 — PRD Summary (UnitConverter_04)

> PRD에서 테스트·코드까지 추적 가능하도록 길이 단위 변환 CLI를 재구현한다.

## 목표

- 레거시 `UnitConverter.py`(37줄 procedural)를 ECB + Dual-Track TDD로 재구현
- PRD 요구사항과 테스트를 1:1 추적

## 핵심 기능 (P0)

| 항목 | 내용 |
|------|------|
| 입력 형식 | `unit:value` (예: `meter:2.5`) |
| 기본 단위 | meter, feet, yard |
| 변환 로직 | 1m = 3.28084ft = 1.09361yd; feet↔yard는 meter 경유 |
| CLI 예시 | `python -m unit_converter "meter:2.5"` |
| 출력 예시 | `2.5 meter = 8.2021 feet`, `2.5 meter = 2.7340 yard` … |

## 품질 요구 (P0)

- **OCP**: 새 단위 추가 시 기존 converter 코드 수정 최소화
- **SRP**: Parser / Registry / Converter / Formatter 분리
- **입력 검증**: 음수, 잘못된 형식, 미지 단위

## 추가 요구 (P1)

| ID | 내용 |
|----|------|
| EXT-01 | `units.json` 또는 YAML에서 변환 비율 로드 |
| EXT-02 | `1 cubit = 0.4572 meter` 동적 등록 후 즉시 변환 |
| EXT-03 | `--format json \| csv \| table` 출력 포맷 선택 |

## 레거시 시드 문제 (UnitConverter.py)

1. OCP 위반 — `if/elif` 단위 분기, 단위 추가 시 `main()` 수정 필요
2. 하드코딩 — `3.28084` 등 상수 내장
3. SRP 위반 — 파싱·변환·출력이 한 함수에 혼재
4. 검증 부재 — 음수·형식 오류·경계 케이스 미처리
5. 취약한 파싱 — `split(':', 1)`만 사용

## 타깃 아키텍처 (슬라이드 ↔ ECB 매핑)

| 슬라이드 모듈 | ECB 배치 (Harness) | SRP 역할 |
|--------------|---------------------|----------|
| `length_unit.py`, `unit_registry.py`, `converter.py` | `src/entity/` | Registry, Converter |
| 유스케이스 조율 | `src/control/` | Control |
| `input_parser.py`, `output_formatter.py`, `cli.py` | `src/boundary/` | Parser, Printer |
| `config_loader.py` | `src/boundary/` (spec 확정) | EXT-01 |

## 상태

- **spec 단계**: PRD·아키텍처 방향 확정
- **미확정**: 패키지명 `unit_converter` vs `unit-converter`, CLI 스캐폴드
