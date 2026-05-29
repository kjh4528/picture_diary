# 글로 쓰는 그림일기 — Picture Diary

일기 텍스트를 4장면 이미지 + 영상으로 변환하는 멀티 LLM 파이프라인

```
diary.md (일기 텍스트)
    │
    ▼ GPT-4o-mini (장면 추출)
    │
    ▼ gpt-image-1-mini / fal-ai FLUX schnell (이미지 생성)
    │
    ▼ fal-ai Kling v2 Master (영상 생성)
    │
    ▼ outputs/ (이미지 4장 + 영상)
```

---

## 빠른 시작

```bash
# 1. 패키지 설치
uv venv && uv pip install -r requirements.txt

# 2. .env 파일 생성
echo "OPENAI_API_KEY=sk-..." > .env
echo "FAL_KEY=..."          >> .env

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

## 운영 지표

| Day | 모델 | 호출 수 | 비용 (예상) |
|-----|------|--------:|------------:|
| Day 1~3 | gpt-4o-mini (장면 추출) | 1회/실행 | ~$0.001 |
| Day 3 | gpt-image-1-mini low (이미지 4장) | 4회 | ~$0.020 |
| Day 3 | fal-ai/flux/schnell (이미지 4장) | 4회 | ~$0.012 |
| Day 4 | fal-ai/kling-video/v2/master (영상 1개) | 1회 | ~$1.400 |

---

## 파일 구조

```
picture_diary/
├── .env                          ← API 키 (⛔ 커밋 금지)
├── .gitignore
├── README.md
├── requirements.txt
├── pipeline.py                   ← 전체 파이프라인 진입점
├── day5_01_product_catalog.py    ← 도메인 응용 (product)
├── agents/
│   ├── __init__.py
│   ├── scene.py                  ← 일기 → 장면 JSON 추출
│   ├── image.py                  ← 장면 → 이미지 생성
│   └── video.py                  ← 이미지 → 영상 생성
├── domains/
│   └── product_prompts.json      ← 제품 카탈로그 프롬프트
├── week7_retrospective.md
└── outputs/                      ← 생성 결과물 (로컬 실행 시 생성됨)
```

---

## 도메인 응용

**선택 도메인:** Product (제품 카탈로그)

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

---

## 보안 체크리스트

- [x] `.env`가 `.gitignore`에 포함됨
- [x] 코드에 `sk-` 패턴 없음 (API 키 하드코딩 없음)
- [x] `outputs/`가 `.gitignore`에 포함됨

---

## 라이선스

MIT
