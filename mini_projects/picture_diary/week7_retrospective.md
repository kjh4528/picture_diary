# 그림일기 프로젝트 — 5일 결과 회고

## Day별 핵심 산출물

| Day | 강의 트랙 | 셀프 트랙 | 실행 확인 |
|-----|-----------|-----------|:---------:|
| Day 1 | LLM 발전 계보, DALL-E 첫 호출 | `.env` 설정, `day1_self1.py` — 이미지 1장 생성 | ✅ |
| Day 2 | JSON 스키마 설계, fal.ai 첫 호출 | `scene_prompts.json`, `day2_self2.py` — FLUX 이미지 생성 | ✅ |
| Day 3 | Chat JSON 모드, 모듈화 | `agents/scene.py`, `agents/image.py` — 4장 자동 생성 | ✅ |
| Day 4 | 비동기 폴링, image-to-video | `agents/video.py` — Kling v2로 영상 생성 | ✅ |
| Day 5 | 파이프라인 조립, 도메인 응용 | `pipeline.py`, `day5_01_product_catalog.py`, `README.md` | ✅ |

---

## 잘 된 점

- **모듈화 구조**: `scene.py → image.py → video.py` 단계를 독립 파일로 분리해서, 모델을 교체할 때 해당 파일만 수정하면 됐다. DALL-E → gpt-image-1-mini 교체도 `image.py` 내부만 바꿔서 해결했다.
- **두 API의 차이를 직접 체험**: OpenAI(base64 응답)와 fal.ai(CDN URL 응답)의 구조가 다르다는 것을 코드로 직접 다루면서 이해했다. `.env`를 잠긴 서랍처럼 관리한 덕분에 5일 내내 API 키 노출 없이 진행했다.
- **비동기 폴링 이해**: 영상 생성이 이미지와 달리 `subscribe()`로 처리해야 한다는 것을 병원 대기표 비유로 이해했다. `run()`은 카운터 앞에서 바로 받는 것, `subscribe()`는 번호표 뽑고 호명 대기하는 것.

---

## 개선할 점

- **에러 핸들링 부족**: API 호출 실패 시 재시도 로직이 없다. 네트워크 오류나 일시적 API 오류에 대비한 retry 패턴을 추가하면 더 안정적일 것 같다.
- **영상 생성 비용**: Kling v2 master가 $1.40/영상으로 4장 전체 생성 시 $5.60이 된다. 테스트 단계에서는 standard 티어를 쓰는 게 낫겠다.
- **`generate_images()` 순차 처리**: 현재 이미지 4장을 순서대로 생성한다. 병렬 처리로 바꾸면 전체 소요 시간을 줄일 수 있다.


