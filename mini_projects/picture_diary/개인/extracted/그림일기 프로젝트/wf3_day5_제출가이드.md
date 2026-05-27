# Day 5 최종 산출물 제출 가이드

> **과정**: 7주차 MCP 활용 서비스 개발 — 멀티 LLM 파이프라인
> **대상**: 수강생 전원
> **목적**: LLM 자동 채점에 대응할 수 있도록 프로젝트 구조, 파일명, 함수명, 변수명 규칙을 통일합니다.
> **제출 기한**: Day 5 수업 종료 시점

---

## 1. 프로젝트 스케폴딩 구조

아래 폴더·파일 구조를 **반드시** 유지해야 합니다.

자동 채점기는 이 경로를 기준으로 파일 존재 여부를 판정합니다.

```text
picture_diary/                    ← 프로젝트 루트 (GitHub 저장소 루트)
├── .env                          ← API 키 (⛔ 절대 커밋 금지)
├── .gitignore                    ← .env, .venv/, outputs/, *.png, *.mp4, __pycache__/ 포함
├── README.md                     ← 포트폴리오 첫 화면 문서
├── requirements.txt              ← 의존성 목록 (uv pip freeze > requirements.txt)
├── pipeline.py                   ← 전체 파이프라인 실행 진입점
├── agents/                       ← 단계별 모듈
│   ├── __init__.py               ← 패키지 초기화 (빈 파일이어도 존재 필수)
│   ├── scene.py                  ← 일기 텍스트 → 장면 JSON 추출
│   ├── image.py                  ← 장면 → 이미지 생성
│   └── video.py                  ← 이미지 → 영상 생성 (비동기 폴링 포함)
├── domains/                      ← 도메인 응용 프롬프트
│   └── {chosen}_prompts.json     ← product / emoji / travel 중 1개
├── week7_retrospective.md        ← 5일 학습 회고
└── outputs/                      ← 생성 결과물 (이미지·영상)
    ├── product_earbuds.png       ← 제품 카탈로그 예시
    ├── emoji_happy.png           ← 이모티콘 예시
    ├── travel_1.png              ← 여행 블로그 예시
    └── ...
```

### 구조 규칙

| 규칙 | 설명 |
|------|------|
| 루트 폴더명 | `picture_diary` (하이픈 아님, 밑줄 사용) |
| `agents/` 위치 | 프로젝트 루트 바로 아래 |
| `__init__.py` | `agents/` 안에 반드시 존재 (빈 파일 허용) |
| `outputs/` | 프로젝트 루트 바로 아래, `Path("outputs").mkdir(exist_ok=True)`로 자동 생성 |
| `domains/` | 프로젝트 루트 바로 아래, 도메인 프롬프트 JSON 보관 |

---

## 2. 파일명 규칙

| 파일 유형 | 명명 규칙 | 예시 | 비고 |
|-----------|-----------|------|------|
| 파이프라인 진입점 | `pipeline.py` (고정) | `pipeline.py` | 이름 변경 금지 |
| 에이전트 모듈 | `agents/{역할}.py` | `agents/scene.py` | 소문자, 밑줄 구분 |
| 일별 실습 스크립트 | `day{N}_{번호}_{주제}.py` | `day5_01_product_catalog.py` | 강의 세션 코드용 |
| 셀프 실습 스크립트 | `day{N}_self{M}.py` | `day5_self1.py` | 셀프 트랙 실행 파일 |
| 도메인 프롬프트 | `domains/{domain}_prompts.json` | `domains/product_prompts.json` | `product`, `emoji`, `travel` 중 택 1 |
| 출력 이미지 | `outputs/{도메인}_{식별자}.png` | `outputs/product_earbuds.png` | 영문 ASCII, 밑줄 구분 |
| 출력 영상 | `outputs/{식별자}.mp4` | `outputs/aria_card.mp4` | 영문 ASCII |
| 회고 문서 | `week7_retrospective.md` (고정) | — | 루트에 위치 |
| README | `README.md` (고정) | — | 루트에 위치 |

### 파일명 금지 사항

- ❌ 한글 파일명 (`제품_이어폰.png`)
- ❌ 공백 포함 (`product earbuds.png`)
- ❌ 대문자 시작 (`Product_Earbuds.py`)
- ❌ 하이픈 사용 (`ab-test.py`) — 밑줄(`_`)만 허용

---

## 3. 필수 구현 함수 이름 규칙

아래 함수들은 채점 시 LLM이 코드를 읽고 구현 여부와 동작 품질을 판단하는 핵심 대상입니다. 함수 이름, 매개변수, 반환 타입을 아래 규칙에 맞춰 작성하세요.

### 3.1 `agents/scene.py` — 장면 추출

`extract_scenes`라는 이름의 함수를 정의합니다. 이 함수는 일기 텍스트 문자열을 `diary_text` 매개변수로 받아, LLM API를 호출하여 장면을 추출한 뒤, 장면 딕셔너리의 리스트를 반환합니다. 반환되는 각 딕셔너리에는 한국어 장면 설명을 담는 `scene_kr` 키와 영문 이미지 생성 프롬프트를 담는 `prompt_en` 키가 반드시 포함되어야 합니다.

### 3.2 `agents/image.py` — 이미지 생성

`generate_image`라는 이름의 함수를 정의합니다. 이 함수는 영문 이미지 생성 프롬프트를 `prompt` 매개변수로, 저장할 파일 경로를 `output_path` 매개변수로 받습니다. 사용할 모델을 지정하는 `model` 매개변수도 받으며, 기본값은 `"dalle"`이고 `"flux"`도 사용할 수 있습니다. DALL-E 또는 fal.ai API를 호출하여 이미지를 생성하고 파일로 저장한 뒤, 저장된 파일의 경로 문자열을 반환합니다.

### 3.3 `agents/video.py` — 영상 생성

`generate_video`라는 이름의 함수를 정의합니다. 이 함수는 입력 이미지 파일 경로를 `image_path` 매개변수로, 저장할 영상 파일 경로를 `output_path` 매개변수로 받습니다. 영상 생성 API를 호출하고 비동기 폴링 등으로 결과를 대기한 뒤, 저장된 영상 파일의 경로 문자열을 반환합니다.

### 3.4 `pipeline.py` — 전체 파이프라인

`picture_diary_pipeline`이라는 이름의 함수를 정의합니다. 이 함수는 일기 텍스트 문자열을 `diary_text` 매개변수로 받아, 장면 추출 → 이미지 생성 → (선택) 영상 생성 순서로 전체 파이프라인을 실행합니다. 반환값은 딕셔너리이며, `scenes` 키에 추출된 장면 리스트, `images` 키에 생성된 이미지 경로 리스트가 필수로 포함되어야 합니다. `videos` 키에 영상 경로 리스트를 포함하는 것은 선택 사항입니다.

### 3.5 도메인 응용 함수 (day5 세션)

제품 도메인을 선택한 경우 `build_product_prompt`라는 이름의 함수를 정의합니다. 이 함수는 제품 설명 문자열을 `desc` 매개변수로 받아, 카탈로그 스타일의 이미지 생성 프롬프트 문자열을 반환합니다.

---

## 4. 변수 이름 규칙

### 4.1 공통 규칙

| 규칙 | 예시 (올바름) | 예시 (금지) |
|------|:---:|:---:|
| snake_case 사용 | `diary_text` | `diaryText`, `DiaryText` |
| 상수는 UPPER_SNAKE_CASE | `MAX_SCENES = 4` | `maxScenes`, `MaxScenes` |
| 약어는 소문자 통일 | `api_key` | `API_Key` |
| 타입 힌트 필수 | `def func(x: str) -> int:` | `def func(x):` |

### 4.2 필수 변수·상수명

| 변수/상수 | 위치 | 타입 | 설명 |
|-----------|------|------|------|
| `APPEARANCE` | `day5_02_emoticons.py` | `str` | 캐릭터 외모 공통 단서 문자열 |
| `EMOTIONS` | `day5_02_emoticons.py` | `dict[str, str]` | 감정별 표현 딕셔너리 |
| `products` | `day5_01_product_catalog.py` | `list[dict]` | 제품 목록 |
| `shot_map` | `day5_01_product_catalog.py` (선택) | `dict[str, str]` | 제품 크기 → 샷 매핑 |
| `angle_map` | `day5_01_product_catalog.py` (선택) | `dict[str, str]` | 제품 형태 → 앵글 매핑 |

### 4.3 출력 파일 경로 변수

| 변수 패턴 | 값 패턴 | 예시 |
|-----------|---------|------|
| `output_path` | `f"outputs/{도메인}_{식별자}.png"` | `"outputs/product_earbuds.png"` |
| `save_path` | `f"outputs/emoji_{emotion}.png"` | `"outputs/emoji_happy.png"` |

---

## 5. `domains/{chosen}_prompts.json` 스키마

```json
{
  "domain": "product",
  "version": "day5",
  "prompt_style": {
    "shot": "close-up",
    "angle": "eye-level",
    "lighting": "studio lighting",
    "lens_or_style": "50mm macro lens",
    "mood": "clean, professional"
  },
  "scenes": [
    {
      "id": "scene_01",
      "diary_sentence": "오늘 새 이어폰을 샀다.",
      "visual_focus": "wireless earbuds",
      "prompt_addons": ["product photography", "clean white background", "soft shadows"],
      "negative_prompt": "text, watermark, blurry"
    }
  ]
}
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|:----:|------|
| `domain` | string | ✅ | `"product"`, `"emoji"`, `"travel"` 중 하나 |
| `version` | string | ✅ | 작성 세션 |
| `prompt_style` | object | ✅ | 도메인별 시각 어휘 설정 |
| `scenes` | list[object] | ✅ | 장면 목록 (1개 이상) |
| `scenes[].id` | string | ✅ | 장면 식별자 |
| `scenes[].diary_sentence` | string | ✅ | 한국어 일기 문장 |
| `scenes[].visual_focus` | string | ✅ | 시각적 초점 대상 |
| `scenes[].prompt_addons` | list[string] | ✅ | 추가 프롬프트 키워드 |
| `scenes[].negative_prompt` | string | ✅ | 제외할 요소 |

---

## 6. `README.md` 필수 섹션

| 섹션 | 내용 | 필수 |
|------|------|:----:|
| 프로젝트 소개 | 한 줄 소개 + 파이프라인 설명 | ✅ |
| 빠른 시작 | `uv sync` → `.env` 설정 → `python pipeline.py` | ✅ |
| 결과 미리보기 | 대표 이미지 1장 이상 링크 또는 경로 | ✅ |
| 파일 구조 | 프로젝트 트리 구조 | ✅ |
| 도메인 응용 | 선택한 도메인 + 적용한 프롬프트 어휘 | ✅ |
| 보안 체크리스트 | `.env` 관련 체크 항목 | ✅ |

---

## 7. `.gitignore` 필수 항목

```gitignore
.env
.venv/
outputs/
*.png
*.mp4
__pycache__/
*.pyc
```

---

## 8. 채점 루브릭

### 8.1 기본 점수 (코드 존재: 40점)

코드가 존재하면 기본 점수를 부여합니다.

| 항목 | 배점 | 판정 기준 |
|------|:----:|-----------|
| `pipeline.py` 파일 존재 | 8점 | 파일이 프로젝트 루트에 존재 |
| `agents/scene.py` 파일 존재 | 7점 | `agents/` 폴더 안에 존재 |
| `agents/image.py` 파일 존재 | 7점 | `agents/` 폴더 안에 존재 |
| `agents/video.py` 파일 존재 | 5점 | `agents/` 폴더 안에 존재 |
| `agents/__init__.py` 파일 존재 | 3점 | 빈 파일이어도 존재하면 부여 |
| `README.md` 파일 존재 | 4점 | 프로젝트 루트에 존재 |
| `.gitignore` 파일 존재 + `.env` 포함 | 3점 | `.gitignore`에 `.env` 줄 포함 |
| `week7_retrospective.md` 파일 존재 | 3점 | 프로젝트 루트에 존재 |
| **소계** | **40점** | |

### 8.2 에러 없음 점수 (정상 실행: 20점)

코드가 에러 없이 import되거나 실행되면 추가 점수를 부여합니다.

| 항목 | 배점 | 판정 기준 |
|------|:----:|-----------|
| `agents/scene.py` import 성공 | 5점 | `from agents.scene import extract_scenes` 에러 없음 |
| `agents/image.py` import 성공 | 5점 | `from agents.image import generate_image` 에러 없음 |
| `agents/video.py` import 성공 | 4점 | `from agents.video import generate_video` 에러 없음 |
| `pipeline.py` import 성공 | 4점 | `from pipeline import picture_diary_pipeline` 에러 없음 |
| `README.md` Markdown 유효 | 2점 | 필수 섹션 헤딩 5개 이상 존재 |
| **소계** | **20점** | |

### 8.3 핵심 기능 구현 점수 (기능별: 25점)

함수가 올바르게 구현되어 기대 동작을 수행하면 추가 점수를 부여합니다.

| 항목 | 배점 | 판정 기준 |
|------|:----:|-----------|
| `extract_scenes()` 반환값이 `list[dict]`이고 각 dict에 `scene_kr`, `prompt_en` 존재 | 7점 | 테스트 입력으로 호출 후 반환값 검증 |
| `generate_image()` 반환값이 문자열이고 `outputs/` 경로 형식 | 6점 | 함수 시그니처 + 반환 타입 검증 |
| `generate_video()` 반환값이 문자열이고 `.mp4` 경로 형식 | 4점 | 함수 시그니처 + 반환 타입 검증 |
| `picture_diary_pipeline()` 반환 dict에 `scenes`, `images` 키 존재 | 8점 | 반환값 구조 검증 |
| **소계** | **25점** | |

### 8.4 보너스 점수 (추가 기능: 최대 15점)

기본 요구사항 이외에 추가 기능을 구현하면 기능별로 보너스 점수를 부여합니다.

| 항목 | 배점 | 판정 기준 |
|------|:----:|-----------|
| `build_product_prompt()`에 `background` 파라미터 추가 | +2점 | 함수 시그니처에 `background: str` 존재 |
| `EMOTIONS` dict에 6개 초과 감정 추가 (예: `wink`, `embarrassed`) | +2점 | dict 키 개수 > 6 |
| `shot_map` 또는 `angle_map` 딕셔너리 구현 | +2점 | 3개 이상 매핑 항목 존재 |
| 여행 블로그 시간대 변형 비교 (`golden_hour` vs `blue_hour`) | +2점 | 관련 코드 또는 출력 파일 존재 |
| `.gitignore`에 `__pycache__/`, `*.pyc`, `outputs/*.mp4` 포함 | +1점 | 3개 항목 모두 포함 |
| `domains/` 폴더에 2개 이상 도메인 JSON 존재 | +2점 | 파일 2개 이상 |
| GitHub push 완료 (공개 URL 접근 가능) | +2점 | URL 존재 + README 렌더링 확인 |
| `week7_retrospective.md`에 13종 비유 카드 10개 이상 연결 | +2점 | 표에 10행 이상 + 연결 파일 기재 |
| **소계** | **최대 15점** | |

### 8.5 총점 구조

| 영역 | 배점 | 비고 |
|------|:----:|------|
| 기본 점수 (코드 존재) | 40점 | 파일이 있으면 획득 |
| 에러 없음 (정상 실행) | 20점 | import 성공 시 획득 |
| 핵심 기능 (동작 검증) | 25점 | 함수 반환값·구조 검증 |
| 보너스 (추가 기능) | 최대 15점 | 선택 구현 |
| **총점** | **100점** (보너스 포함 시 최대 115점) | |

### 등급 기준

| 등급 | 점수 범위 | 의미 |
|:----:|:---------:|------|
| S | 90점 이상 | 핵심 기능 완성 + 보너스 다수 구현 |
| A | 75~89점 | 핵심 기능 대부분 완성 |
| B | 60~74점 | 기본 구조 + 일부 기능 구현 |
| C | 40~59점 | 파일 구조 존재 + 에러 다수 |
| D | 40점 미만 | 파일 누락 또는 구조 미준수 |

---

## 9. 제출 전 자기 점검 체크리스트

아래 항목을 모두 확인한 뒤 제출합니다.

### 파일 구조

- [ ] `pipeline.py`가 프로젝트 루트에 있다
- [ ] `agents/scene.py`, `agents/image.py`, `agents/video.py`가 있다
- [ ] `agents/__init__.py`가 있다
- [ ] `README.md`가 프로젝트 루트에 있다
- [ ] `.gitignore`에 `.env`가 포함되어 있다
- [ ] `week7_retrospective.md`가 있다
- [ ] `domains/` 폴더에 도메인 프롬프트 JSON이 있다

### 함수 이름

- [ ] `extract_scenes(diary_text: str) -> list[dict]` 존재
- [ ] `generate_image(prompt: str, output_path: str, model: str = "dalle") -> str` 존재
- [ ] `generate_video(image_path: str, output_path: str) -> str` 존재
- [ ] `picture_diary_pipeline(diary_text: str) -> dict` 존재

### 데이터 파일

- [ ] `domains/{chosen}_prompts.json`이 `json.load()`로 파싱 가능하다
- [ ] `README.md`에 빠른 시작, 결과 미리보기, 파일 구조 섹션이 있다

### 안전

- [ ] `.env` 파일이 Git에 커밋되지 않았다
- [ ] README에 API 키 값이 없다 (`sk-` 패턴 없음)
- [ ] 코드에 API 키가 하드코딩되지 않았다

---

## 🛡️ 안전 수칙

- API 키는 **`.env` 파일에만** 저장하고 `load_dotenv()`로 로드합니다.
- `os.environ` 직접 할당, 코드에 키 하드코딩, AI 도우미에 키 입력을 **절대 금지**합니다.
- `.gitignore`에 `.env`가 포함되어 있는지 **제출 전 반드시 확인**합니다.

---

> 이 가이드의 모든 파일명, 함수명, 변수명, JSON 스키마는 LLM 자동 채점 시스템과 정확히 일치하도록 설계되었습니다.
> 임의 변경 시 자동 채점에서 감점될 수 있으니 반드시 이 규격을 준수하세요.
