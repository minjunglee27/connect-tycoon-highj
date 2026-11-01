# LINK-01 의사결정 모델 학습 원천 데이터 (Source Data)

이 폴더는 [CONNECT AI WORLD 로봇 웹 학습기](https://www.ezerai.xyz/robot-lab/world/)에서 생성되어 LINK-01 의사결정 언어 모델(LoRA)들을 훈련시키는 데 사용된 원천 코스 및 결정 두뇌 파일들을 보관하는 곳입니다.

---

## 📂 파일 구성

### 1. `link01-goto_target-057d7cd9.world-v1.json` (코스 맵 데이터 · 목표로 가기 v1)
- **과제 (Task)**: `goto_target` (목표로 가기 · 머그컵까지 자율 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `057d7cd9`
- **내용**:
  - 시작 좌표: `[-0.4044, -0.4581, 1.2993]`
  - 배치된 장애물 7개 (원통형/블록형 장애물 위치 및 크기 직접 배치)
  - 목표 지점: 머그컵 (`mug`)
- **연계 모델**: [`connectailab-rl-highj-goto-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01)

### 2. `link01-goto_target-mine-brain-v1.json` (선생님 결정 두뇌 · 목표로 가기 v1)
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

### 3. `link01-choose_object-9814f10c.world-v1.json` (코스 맵 데이터 · 물건 고르기 v1)
- **과제 (Task)**: `choose_object` (물건 고르기 · 단서가 가리키는 물건 선택)
- **코스 이름**: 내 코스 1
- **코스 해시**: `9814f10c`
- **내용**:
  - 시작 좌표: `[-1.3345, 0.1702, -1.6455]`
  - 배치된 타겟: `mug` ([-0.2443, 1.6174]), `plant` ([1.5, 0]) 직접 배치
  - 제시 단서 (cue): `"mug"` (머그컵으로 가야 성공, 다른 물건으로 가면 실패)
- **연계 모델**: [`connectailab-rl-highj-choose-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01)

### 4. `link01-choose_object-mine-brain-v1.json` (선생님 결정 두뇌 · 물건 고르기 v1)
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

### 5. `link01-avoid_obstacles-eceb627a.world-v1.json` (코스 맵 데이터 · 장애물 피하기 v1)
- **과제 (Task)**: `avoid_obstacles` (장애물 피하기 · 장애물에 부딪히지 않고 화분까지 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `eceb627a`
- **내용**:
  - 시작 좌표: `[-1.7, 0.3309, -0.2825]`
  - 배치된 장애물 6개 (직접 배치)
  - 목표 지점: 화분 (`plant`, 좌표: `[1.7, -0.5392]`)
- **연계 모델**: [`connectailab-rl-highj-avoid-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-avoid-v1-link01)

### 6. `link01-avoid_obstacles-mine-brain-v1.json` (선생님 결정 두뇌 · 장애물 피하기 v1)
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

### 7. `link01-avoid_obstacles-2ee8e71b.world-v2.json` (코스 맵 데이터 · 장애물 피하기 v2)
- **과제 (Task)**: `avoid_obstacles` (장애물 피하기 · 장애물에 부딪히지 않고 화분까지 주행)
- **코스 이름**: 내 코스 3
- **코스 해시**: `2ee8e71b`
- **내용**:
  - 시작 좌표: `[-1.7, 0.3309, -0.2825]`
  - 배치된 장애물 7개 (위치, 회전각, 크기 - v1과 다른 신규 복합 맵 배치)
  - 목표 지점: 화분 (`plant`, 좌표: `[1.1903, -0.7339]`)

### 8. `link01-avoid_obstacles-mine-brain-v2.json` (선생님 결정 두뇌 · 장애물 피하기 v2)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 코스**: `2ee8e71b` ("내 코스 3" 환경 확장 집중 훈련)
- **공식 시험 20판 점수**: **85.0% (`score: 0.85`)** (보상합: 20.86, 61,440회 판단)
- **계약 규격 (Contract)**: `link01-decision/avoid_obstacles/obs21-act5/walker51-14/v1`
- **관측 차원 (21개)**:
  - 목표 거리, 목표 방향 sin/cos
  - 11방향 거리 센서 (-100° ~ +100°)
  - 전진 속도, 회전 속도
  - 직전 선택 행동 5개
- **행동 공간 (5개)**:
  - `직진`, `왼쪽으로`, `오른쪽으로`, `제자리 좌회전`, `제자리 우회전`
- **신경망 구조**: MLP `[21, 64, 64, 5]` (tanh 활성화 함수, 로짓 출력)

### 9. `link01-follow_route-4837c8d8.world-v1.json` (코스 맵 데이터 · 경로 따라가기 v1)
- **과제 (Task)**: `follow_route` (경로 따라가기 · 경유점을 순서대로 통과하여 목표까지 주행)
- **코스 이름**: 코스 92001
- **코스 해시**: `4837c8d8`
- **내용**:
  - 시작 좌표: `[1.6, -0.3927, 2.1582]`
  - 목표 지점: 랜턴 (`lantern`, 좌표: `[-1.6, 0.5147]`)
  - 경로 형태: 완만한 기본 곡선 경로 (3번째 경유점: `[0.32, 0.5991]`)

### 10. `link01-follow_route-mine-brain-v1.json` (선생님 결정 두뇌 · 경로 따라가기 v1)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 방식**: 모든 판이 무작위 코스 (`random`)
- **공식 시험 20판 점수**: **100.0% (`score: 1.00`)** (보상합: 23.47, 30,720회 학습)
- **기본 보상 가중치**: 전진(`progress: 5.0`), 관문 통과(`gate: 3.5`), 도달(`reach: 10.0`), 전도 감점(`fall: -12.5`)
- **계약 규격 (Contract)**: `link01-decision/follow_route/obs16-act5/walker51-14/v1`

### 11. `link01-follow_route-f6fe2b3f.world-v2.json` (코스 맵 데이터 · 경로 따라가기 v2)
- **과제 (Task)**: `follow_route` (경로 따라가기 · 경유점을 순서대로 통과하여 목표까지 주행)
- **코스 이름**: 내 코스 1
- **코스 해시**: `f6fe2b3f`
- **내용**:
  - 시작 좌표: `[1.6, -0.3927, 2.3731]`
  - 목표 지점: 랜턴 (`lantern`, 좌표: `[-1.6, 0.5147]`)
  - 경로 형태: **S자 급커브 커스텀 코스** (3번째 경유점을 아래 `[-0.3463, -0.3366]`로 깊게 꺾어 난이도 상향)

### 12. `link01-follow_route-mine-brain-v2.json` (선생님 결정 두뇌 · 경로 따라가기 v2)
- **두뇌 이름**: 내 AI
- **학습 알고리즘**: PPO (Proximal Policy Optimization)
- **학습 코스**: `f6fe2b3f` ("내 코스 1" 커스텀 급커브 맵 맞춤형 집중 훈련)
- **공식 시험 20판 점수**: **95.0% (`score: 0.95`)** (보상합: 21.46, 81,920회 집중 훈련)
- **보상 가중치 튜닝**: 전진(`progress: 6.5`), 관문 통과(`gate: 7.0` - 2배 강화!), 도달(`reach: 15.5` - 1.55배 강화!), 전도 감점 완화(`fall: -9.5`)
- **계약 규격 (Contract)**: `link01-decision/follow_route/obs16-act5/walker51-14/v1`

---

## 🔗 연계 모델 목록 (Live Models)
- 목표로 가기: [minjunglee27/connectailab-rl-highj-goto-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01)
- 물건 고르기: [minjunglee27/connectailab-rl-highj-choose-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01)
- 장애물 피하기 (v1): [minjunglee27/connectailab-rl-highj-avoid-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-avoid-v1-link01)
*(이후 배포되는 모델은 배포 완료 순서대로 누적 추가됩니다)*
