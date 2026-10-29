# LINK-01 의사결정 모델 학습 원천 데이터 (Source Data)

이 폴더는 [CONNECT AI WORLD 로봇 웹 학습기](https://www.ezerai.xyz/robot-lab/world/)에서 생성되어 **`connectailab-rl-highj-v1-link01`** 의사결정 언어 모델(LoRA)을 훈련시키는 데 사용된 원천 코스 및 결정 두뇌 파일들을 보관하는 곳입니다.

---

## 📂 파일 구성

### 1. `link01-goto_target-057d7cd9.world.json` (코스 맵 데이터)
- **과제 (Task)**: `goto_target` (목표로 가기 · 머그컵까지 자율 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `057d7cd9`
- **내용**:
  - 시작 좌표: `[-0.4044, -0.4581, 1.2993]`
  - 배치된 장애물 5개 (원통형/블록형 장애물 위치 및 크기)
  - 목표 지점 (머그컵) 위치 정의

### 2. `link01-goto_target-mine-brain.json` (선생님 결정 두뇌)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 코스**: `057d7cd9` (위 `world.json` 코스에서 집중 학습)
- **관측 차원 (21개)**:
  - 목표 상대 거리, 목표 방향 sin/cos
  - 전진 속도, 회전 각속도
  - 직전 선택 행동 5개
  - 11방향 레이저 거리 센서 (-100° ~ +100°)
- **행동 공간 (5개)**:
  - `직진`, `왼쪽으로`, `오른쪽으로`, `제자리 좌회전`, `제자리 우회전`
- **신경망 구조**: MLP `[21, 64, 64, 5]` (tanh 활성화 함수, 로짓 출력)

---

## 🔗 연계 모델
- Hugging Face 저장소: [minjunglee27/connectailab-rl-highj-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-v1-link01)
- 웹 학습기 두뇌의 주행 판단을 0.5초 단위 텍스트 문제집(586건)으로 변환하여 `Qwen/Qwen3.5-0.8B` LoRA 지도학습(SFT) 및 강화학습(RL)에 적용되었습니다.
