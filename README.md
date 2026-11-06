# AutohitechLib — 공용 KiCad 풋프린트 라이브러리

autohitech 하드웨어 repo들에 흩어진 `MyLib.pretty`를 하나로 모으는 저장소.
보드 repo에서는 서브모듈로 pin해서 참조한다 (버전 고정).

## 소비 방법 (보드 repo 측)

```sh
git submodule add https://github.com/autohitech/AutohitechLib.git libs/AutohitechLib
```

`fp-lib-table`에 추가:

```
(lib (name "Autohitech") (type "KiCad") (uri "${KIPRJMOD}/libs/AutohitechLib/Autohitech.pretty") (options "") (descr ""))
```

보드 PCB의 풋프린트 링크 `MyLib:XXX` → `Autohitech:XXX`로 교체 후 ERC/DRC 재검증.
단, 아래 충돌 목록의 풋프린트는 교체 금지 (보드별 변형 존재).

## 수록 (충돌 없음 15종)

ESP12E, HC06_Bluetooth, LM2596, MP2307_5V, OLED130(+_PIN),
SL-105-X-XX_1x05, SLIDE_SW, SOP-4_4.4x2.8mm_P1.27mm, SW_4P_SMD,
TerminalBlock_Phoenix_PT-3.5mm_4pol/5pol,
TerminalBlock_bornier-4/5_P5.08mm, ZLSN3007S

## 충돌 목록 (29종 — 보드별 변형, 미해결)

같은 이름·다른 형상이라 합치지 못함. F.Cu/B.Cu 차이 포함.
해결 정책(정본 선정 vs 변형 분리) 확정 전까지 각 보드 로컬 유지.

| 풋프린트 | 변형별 사용 repo |
|---|---|
| ADS1105 | 008A / STDB |
| Arduino_nano | AIW / STDB |
| Arduino_nano_B | 008A / STDA / STDB |
| ATM_AV | 008A / STDB |
| ENC28J60 | 008A / STDB |
| ESP-02 | 008A / STDB |
| ESP-05 | STDA / STDB(×2) |
| ESP01 | ES01 / STDA / AIW |
| HC-06_bluetooth | STDA / STDB |
| MP1584EN_3V/5V | 008A / STDB |
| MP1584_SBX_12V | STDA / STDB(×2) |
| MP1584_SBX_3V | AIW / STDA / STDB(×2) |
| MP1584_SBX_5V | STDB(×2) |
| OLED096(+_PIN) | 008A / STDB(×2) |
| OLED_I2C | STDA / STDB |
| PA1A-12 | SCM-RTD / DIOAIO 4종 / STDB(×2) |
| Potentiometer_Trimmer-EVM3E | DIOAIO 4종 / SCM-RTD |
| Push_Mont_SW | STDA / STDB(×2) |
| R411A01 | STDA / AIW / 008A / STDB |
| SCM_V1.1 | STDA / STDB(×2) / AIW |
| SW_TACT_x1 | 008A / STDB |
| TACT_SW4(+_PIN) | STDA / STDB(×2) / 008A |
| TerminalBlock_bornier-9/12 | STDA / STDB |
| XY-017_RS485 | STDA / STDB(×2) |
| sw1208 | STDA / STDB(×2) |

STDB = SCB-STANDARD-B (내부 Library/와 중첩 구조에도 변형 존재).
DIOAIO 4종 = SCM-AI/AO/DI/DO (PA1A-12·트리머 변형 공유).
