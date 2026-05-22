# 영상 프롬프트 기본 구조
# 이미지 프롬프트 = 촬영 지시서
# prompt = f'{캐릭터 외모}, {샷 사이즈}, {렌즈}, {앵글}, {조명}, {스타일 마무리}'

# 기본 프롬프트
APPEARANCE = (
    '젊은 여성 AI 비서 아리아, 짧은 검은 머리, 따뜻한 갈색 눈,'
    '파란색 포인트가 들어간 흰색 테크 의상, 친근한 미소, 상반신 샷,'
    '50mm 렌즈, 눈높이, 영화 같은 조명, 사실적인 표현'
)

# 6종 샷 사이즈 레퍼런스 
SHOT_SIZES = {
    'ECU': ('extreme close-up', '감정 미세 변화, 눈빛 강조'),
    'CU': ('close-up', '얼굴 중심, SNS 프로필'),
    'BS': ('bust shot', '표준 포트레이트, 캐릭터 가드 기준'),
    'MS': ('medium shot', '제스처, 옷차림 포함'),
    'FS': ('full shot', '전신, 의상 카탈로그'),
    'WS': ('wide shot', '환경, 세계관 등 강조')
}

# 앵글 3종
ANGLES = ['eye_level', 'low angle', 'high angle'] # 기본, 올려보기, 내려보기 

# 조명 3종
LIGHTING_SETUPS = ['key light','fill light', 'back light'] # 주광, 보조광, 후면광 

# 렌즈 
LENSES = ['24mm wide', '50mm portrait', '85mm tight', '200mm', '400mm'] # 광각, 표준, 망원 ...

# 심도
DEPTHS = ['shallow depth of field', 'bokeh background', 'deep focus, sharp background']

# 구도
COMPOSITIONS = ['rule of thirds','centered composition', 'negative space, minimalist']

# 최종 프롬프트 조합 
prompt = f'{APPEARANCE}, {SHOT_SIZES["BS"][0]}, {ANGLES[0]},{LIGHTING_SETUPS[0]}' 
print('최종 프롬프트: ', prompt) 

