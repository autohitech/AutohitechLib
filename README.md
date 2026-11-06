# AutohitechLib — 공용 KiCad 풋프린트 라이브러리

autohitech 하드웨어 repo들에 흩어진 `MyLib.pretty`를 하나로 모은 저장소.
보드 repo에서는 서브모듈로 pin해서 참조한다 (버전 고정).

## 소비 방법 (보드 repo 측)

```sh
git submodule add https://github.com/autohitech/AutohitechLib.git libs/AutohitechLib
```

`fp-lib-table`에 추가:

```
(lib (name "Autohitech") (type "KiCad") (uri "${KIPRJMOD}/libs/AutohitechLib/Autohitech.pretty") (options "") (descr ""))
```

보드 PCB/회로도의 `MyLib:XXX` 링크를 아래 이름표대로 `Autohitech:YYY`로 교체 후
ERC/DRC가 변경 전과 동일한지 확인. 동일하면 보드 로컬 `footprints/` 삭제.

## 명명 규칙

- 충돌 없는 풋프린트: 원래 이름 그대로 (`ESP12E`)
- 보드별 변형: `이름__범위` (`PA1A-12__DIO`, `R411A01__008A`)
- 베어 이름은 충돌 해소(정본 선정) 전까지 예약 — 변형이 생기면 기존 베어 이름은
  서픽스 부여 후 정본만 베어 이름 유지. 이력으로 나중에 정본 교체 가능.

범위 태그: `DIO`(SCM-AI/AO/DI/DO 공용) `RTD`(SCM-RTD) `008A` `4KEY` `AIW`
`ES01` `ES12` `STA`(STANDARD-A) `STB`(STANDARD-B Library/) `STBP`(STANDARD-B 중첩구조)
`PWR`(SCM-PWR)
