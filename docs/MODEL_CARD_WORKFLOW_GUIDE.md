# 📋 CONNECT AI LAB 모델 카드 작성 및 배포 워크플로우 가이드

이 문서는 **`minjunglee27/connectailab-rl-highj-v1`** 및 **`connectailab-rl-highj-v1-link01`**에서 확립된 **CONNECT AI LAB × AI CITY BUILDERS 표준 고품질 모델 카드(README.md) 작성 규칙과 배포 방법**을 정리한 가이드입니다.

---

## 1. 모델 카드의 핵심 8단 구조

### ① YAML Frontmatter (메타데이터)
허깅페이스 검색 및 라이브러리 연동 태그를 선언합니다:
```yaml
---
license: apache-2.0
base_model: Qwen/Qwen3.5-0.8B
library_name: peft
language: [ko, en]
pipeline_tag: reinforcement-learning
tags: [reinforcement-learning, deep-reinforcement-learning, ppo, robotics, decision-making, link01, connect-ai-world, connect-ai-lab, connectailab, lora, highj]
---
```

### ② 상단 비주얼 & 공식 실드 배지 바
상단에 프로젝트 애니메이션 GIF 배너와 함께 공식 채널 배지를 중앙 정렬로 배치합니다:
- **Banner**: `https://raw.githubusercontent.com/wonseokjung/connect-tycoon/main/docs/brand/banner.gif`
- **Badges**: Colab 실습 링크, GitHub 레포, YouTube 공식 채널, AI CITY BUILDERS

### ③ 영문 Executive Summary & Key Highlights
해외 및 글로벌 커뮤니티 접근성을 위해 맨 처음에는 영문 요약문과 핵심 성과 불릿을 배치합니다:
- **Base Model**: 베이스 언어 모델 (`Qwen/Qwen3.5-0.8B`)
- **Selected Policy**: 최종 채택된 정책 (예: `Supervised Fine-Tuning (SFT)`)
- **Benchmark Highlights**: 20판 주행 성공률 (55%), 정답률 (68.3%)
- **Author**: Minjung Lee (Highj) · AI Solopreneur

### ④ 한글 모델 개요 (Korean Overview)
로봇(또는 비즈니스) 환경에서 모델이 수행하는 역할(0.5초 주기 21차원 센서 입력 해석 ➔ 5개 보행 방향 결정)을 친절하게 설명합니다.

### ⑤ 만든 사람 (Author Profile) & 시뮬레이션 Hero GIF
- **Author Bio**: 루나랜더 v2 (267.9점 고득점 달성), Connect Tycoon, LINK-01 참여 이력 및 1인 기업가 비전 소개
- **Hero Visual**: `hero.gif` 시뮬레이션 동작 화면 삽입 (`width="88%"`)

### ⑥ 만든 방법 (5단계 학습 파이프라인)
1. 웹 학습기 PPO 두뇌 키우기 (`brain.json`, 코스 `world.json`)
2. 0.5초 관측 수치 ➔ 텍스트 문제집 변환 (train / valid / test)
3. 언어 모델 LoRA 지도학습 (SFT)
4. 보상 기반 강화학습 (RL with KL Divergence)
5. 동일 코스 20판 주행 채점 및 최우수 모델 채택

### ⑦ 실측 성적 벤치마크 표 (Evaluation Results)
| 모델 | 시험 문제 정답률 (두뇌 일치율) | 같은 코스 20판 성공률 | 부딪힌 판 (충돌률) | 성공한 판 평균 시간 |
|---|:---:|:---:|:---:|:---:|
| **두뇌 (선생님 PPO)** | 100.0% | 100% | 10% | 10.4초 |
| **학습 전 (Base Qwen)** | 52.5% | 0% | 75% | — |
| **지도학습 (SFT)** | 68.3% | **55%** | 80% | 15.3초 |
| **강화학습 (RL)** | 74.2% | 30% | 90% | 14.2초 |

### ⑧ Quickstart (추론 코드) 및 공식 출처 링크
`transformers`와 `peft`를 이용해 허깅페이스에서 가중치를 즉시 로드해 테스트할 수 있는 파이썬 코드 및 시스템 프롬프트 명시.

---

## 2. 안전한 모델 카드 배포 방법 (Colab 문자열 잘림 방지)

코랩(Colab) 셀에 긴 문자열을 직접 넣으면 클립보드 잘림(`IncompleteInputError`)이 발생할 수 있습니다.  
따라서 아래의 두 가지 방법 중 하나를 사용하는 것이 가장 안전합니다:

### 방법 A: 독립 배포 스크립트 실행 (로컬 환경)
```bash
python scripts/publish_link01_model_card.py
```

### 방법 B: `huggingface_hub.HfApi`로 로컬 파일 직접 업로드
```python
from huggingface_hub import HfApi

api = HfApi(token=HF_TOKEN)
api.upload_file(
    path_or_fileobj="model_cards/link01-v1/README.md",
    path_in_repo="README.md",
    repo_id="minjunglee27/connectailab-rl-highj-v1-link01",
    commit_message="docs: upgrade model card"
)
```

