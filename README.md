# Picture Diary — 멀티 LLM 파이프라인
## 프로젝트 소개
일기 텍스트를 입력받아 LLM으로 장면을 자동 추출하고, 이미지 생성 및 영상 변환까지 처리하는 자동화 멀티 LLM 파이프라인입니다.

```
diary.md (일기 텍스트)
    │
    ▼ 장면 추출 (GPT-4o-mini)
    │
    ▼ 이미지 생성 (gpt-image-1-mini / fal-ai FLUX schnell)
    │
    ▼ 영상 변환 (fal-ai Kling v2 Master)
    │
    ▼ outputs/ (이미지, 영상)
```

---

## 빠른 시작

```bash
# 1. 패키지 설치 (권장)
uv sync

# 또는 가상환경 직접 설정 시
uv venv
uv pip install -r requirements.txt

# 2. .env 파일 생성 후 API 키 입력
OPENAI_API_KEY=your_openai_key
FAL_KEY=your_fal_key

# 3. 파이프라인 실행
python pipeline.py
```

---

## 결과 미리보기

> 실행 후 `outputs/` 폴더에 생성됩니다.

| 파일 | 내용 |
|------|------|
| `outputs/scene_1.png` | 장면 1 이미지 |
| `outputs/scene_2.png` | 장면 2 이미지 |
| `outputs/scene_3.png` | 장면 3 이미지 |
| `outputs/scene_4.png` | 장면 4 이미지 |
| `outputs/scene_1.mp4` | 장면 1 영상 (generate_videos=True 시) |

---

## 파일 구조

```
picture_diary/
├── .env                          ← API 키 (⛔ 커밋 금지)
├── .gitignore                    ← Git 제외 파일 설정
├── README.md                     ← 프로젝트 문서
├── requirements.txt              ← 의존성 목록
├── pipeline.py                   ← 전체 파이프라인 진입점
├── day5_01_product_catalog.py    ← 도메인 응용 (product)
├── day5_02_emoticons.py          ← 도메인 응용 (emoji)
├── agents/
│   ├── __init__.py               ← 패키지 초기화
│   ├── scene.py                  ← 일기 → 장면 JSON 추출
│   ├── image.py                  ← 장면 → 이미지 생성
│   └── video.py                  ← 이미지 → 영상 생성
├── domains/
│   ├── product_prompts.json      ← 제품 카탈로그 프롬프트
│   └── emoji_prompts.json        ← 이모티콘 캐릭터 프롬프트
├── week7_retrospective.md        ← 5일 학습 회고
└── outputs/                      ← 생성 결과물 (로컬 실행 시 생성됨)
```

---

## 도메인 응용

**선택 도메인:** Product (제품 카탈로그), Emoji (이모티콘 캐릭터)

### Product
`day5_01_product_catalog.py`에서 `build_product_prompt(desc, background)`로 제품 설명을 카탈로그 스타일 프롬프트로 변환합니다.

적용한 시각 어휘:

| 어휘 | 값 |
|------|----|
| Shot | close-up |
| Angle | eye-level |
| Lighting | studio lighting |
| Lens | 50mm macro lens |
| Mood | clean, professional |

`shot_map` / `angle_map`으로 제품 크기·형태에 따라 샷과 앵글을 자동 매핑합니다.

### Emoji
`day5_02_emoticons.py`에서 `APPEARANCE`(공통 외모 단서)와 `EMOTIONS`(감정별 표현 딕셔너리)를 사용해 이모티콘 캐릭터 이미지를 생성합니다.

적용한 시각 어휘:

| 어휘 | 값 |
|------|----|
| Style | flat illustration |
| Lighting | soft lighting |
| Mood | cute, expressive |
| Background | clean white background |

---

## 보안 체크리스트

- [x] `.env`가 `.gitignore`에 포함됨
- [x] 코드에 `sk-` 패턴 없음 (API 키 하드코딩 없음)
- [x] `outputs/`가 `.gitignore`에 포함됨