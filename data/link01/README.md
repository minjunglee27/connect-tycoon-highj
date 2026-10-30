# LINK-01 의사결정 모델 학습 원천 데이터 (Source Data)

이 폴더는 [CONNECT AI WORLD 로봇 웹 학습기](https://www.ezerai.xyz/robot-lab/world/)에서 생성되어 LINK-01 의사결정 언어 모델(LoRA)들을 훈련시키는 데 사용된 원천 코스 및 결정 두뇌 파일들을 보관하는 곳입니다.

---

## 📂 파일 구성

### 1. `link01-goto_target-057d7cd9.world.json` (코스 맵 데이터 · 목표로 가기)
- **과제 (Task)**: `goto_target` (목표로 가기 · 머그컵까지 자율 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `057d7cd9`
- **내용**:
  - 시작 좌표: `[-0.4044, -0.4581, 1.2993]`
  - 배치된 장애물 7개 (원통형/블록형 장애물 위치 및 크기)
  - 목표 지점: 머그컵 (`mug`)
- **연계 모델**: [`connectailab-rl-highj-goto-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01)

### 2. `link01-goto_target-mine-brain.json` (선생님 결정 두뇌 · 목표로 가기)
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

### 3. `link01-choose_object-9814f10c.world.json` (코스 맵 데이터 · 물건 중 고르기)
- **과제 (Task)**: `choose_object` (물건 중 고르기 · 단서가 가리키는 물건 선택)
- **코스 이름**: 내 코스 1
- **코스 해시**: `9814f10c`
- **내용**:
  - 시작 좌표: `[-1.3345, 0.1702, -1.6455]`
  - 배치된 타겟: `mug` ([-0.2443, 1.6174]), `plant` ([1.5, 0])
  - 제시 단서 (cue): `"mug"` (머그컵으로 가야 성공, 다른 물건으로 가면 실패)
- **연계 모델**: [`connectailab-rl-highj-choose-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01)

### 4. `link01-choose_object-mine-brain.json` (선생님 결정 두뇌 · 물건 중 고르기)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 코스**: `9814f10c` (단서 판단 및 물건 탐색 학습)
- **계약 규격 (Contract)**: `link01-decision/choose_object/obs26-act4/walker51-14/v1`
- **관측 차원 (26개)**:
  - 단서 원-핫 4차원: `[머그컵, 사과, 랜턴, 화분]`
  - 4개 물건별 상태(각 4차원): `[존재여부, 거리, sin, cos]` × 4종 = 16차원
  - 직전 선택 행동 4차원: `[직전 선택 1~4]`
  - 기체 속도 2차원: `[전진 속도, 회전 각속도]`
- **행동 공간 (4개 선택지)**:
  - `머그컵`, `사과`, `랜턴`, `화분` (단서에 일치하는 올바른 물건 타겟팅 결정)
- **신경망 구조**: MLP `[26, 64, 64, 4]` (tanh 활성화 함수, 로짓 출력)

### 5. `link01-avoid_obstacles-eceb627a.world.json` (코스 맵 데이터 · 장애물 피하기)
- **과제 (Task)**: `avoid_obstacles` (장애물 피하기 · 장애물에 부딪히지 않고 화분까지 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `eceb627a`
- **내용**:
  - 시작 좌표: `[-1.7, 0.3309, -0.2825]`
  - 배치된 장애물 6개 (위치, 회전각, 크기)
  - 목표 지점: 화분 (`plant`, 좌표: `[1.7, -0.5392]`)
- **연계 모델**: `connectailab-rl-highj-avoid-v1-link01`

### 6. `link01-avoid_obstacles-mine-brain.json` (선생님 결정 두뇌 · 장애물 피하기)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 코스**: `eceb627a` (장애물 회피 및 목표 도달 집중 훈련)
- **공식 시험 20판 점수**: **90.0% (`score: 0.90`)** (보상합: 20.57)
- **계약 규격 (Contract)**: `link01-decision/avoid_obstacles/obs21-act5/walker51-14/v1`
- **관측 차원 (21개)**:
  - 목표 거리, 목표 방향 sin/cos
  - 11방향 거리 센서 (-100° ~ +100°)
  - 전진 속도, 회전 속도
  - 직전 선택 행동 5개
- **행동 공간 (5개)**:
  - `직진`, `왼쪽으로`, `오른쪽으로`, `제자리 좌회전`, `제자리 우회전`
- **신경망 구조**: MLP `[21, 64, 64, 5]` (tanh 활성화 함수, 로짓 출력)

---

## 🔗 연계 모델 목록
- 목표로 가기: [minjunglee27/connectailab-rl-highj-goto-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01)
- 물건 고르기: [minjunglee27/connectailab-rl-highj-choose-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01)
- 장애물 피하기: `minjunglee27/connectailab-rl-highj-avoid-v1-link01` (코랩 학습 대기)
