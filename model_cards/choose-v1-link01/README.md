---
license: apache-2.0
base_model: Qwen/Qwen3.5-0.8B
library_name: peft
language: [ko, en]
pipeline_tag: reinforcement-learning
tags: [reinforcement-learning, deep-reinforcement-learning, ppo, robotics, decision-making, link01, choose-object, connect-ai-world, connect-ai-lab, connectailab, lora, highj]
---

<p align="center"><img src="https://raw.githubusercontent.com/wonseokjung/connect-tycoon/main/docs/brand/banner.gif" alt="RL AI DECISION MAKING MODEL" width="100%"></p>

<p align="center">
  <a href="https://github.com/wonseokjung/connect-tycoon"><img src="https://img.shields.io/badge/GitHub-CONNECT%20TYCOON-d0f991?style=for-the-badge&logo=github&logoColor=d0f991&labelColor=050807&color=d0f991" alt="GitHub"></a>
  <a href="https://www.youtube.com/@CONNECT-AI-LAB"><img src="https://img.shields.io/badge/YouTube-CONNECT%20AI%20LAB-d0f991?style=for-the-badge&logo=youtube&logoColor=d0f991&labelColor=050807&color=d0f991" alt="YouTube"></a>
  <a href="https://www.aicitybuilders.com/robot"><img src="https://img.shields.io/badge/AI%20CITY%20BUILDERS-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5%20AI-d0f991?style=for-the-badge&logo=bookstack&logoColor=d0f991&labelColor=050807&color=d0f991" alt="AI CITY BUILDERS"></a>
</p>

# connectailab-rl-highj-choose-v1-link01

**connectailab-rl-highj-choose-v1-link01** is an embodied cognitive decision-making language model for the LINK-01 quadruped robot based on `Qwen/Qwen3.5-0.8B`. It is designed for the `choose_object` task, where the robot reads environmental cues and multi-object spatial observations to select and navigate towards the correct target object among multiple choices.

### Key Highlights
- **Base Model**: `Qwen/Qwen3.5-0.8B` (PEFT / LoRA)
- **Task & Course**: `choose_object` on Custom Course (`9814f10c`)
- **Mission**: Read target cue (`cue: "mug"`) and discriminate the correct item while ignoring decoys/distractors
- **Observation Space**: 26 dimensions (cue one-hot [4], 4 object states [16], previous actions [4], velocities [2])
- **Action Space**: 4 discrete object choices (`머그컵`, `사과`, `랜턴`, `화분`)
- **Teacher Brain**: PPO Decision Brain (`brain.json`, contract `link01-decision/choose_object/obs26-act4/walker51-14/v1`)
- **Author**: Minjung Lee (Highj) · AI Solopreneur

---

## 모델 개요 (Overview)

**connectailab-rl-highj-choose-v1-link01**은 LINK-01 4족 보행 로봇이 주변 환경의 여러 물건 중 **주어진 단서(Cue)에 해당하는 올바른 물건을 인지하고 선택(Object Selection)**하도록 훈련된 AI 의사결정 모델입니다.

[CONNECT AI WORLD 로봇 웹 학습기](https://www.ezerai.xyz/robot-lab/world/)에서 PPO로 집중 훈련된 26차원 인지 결정 두뇌(`brain.json`)의 판단 지식을 증류(Distillation)하여, 텍스트로 표현된 시각/공간 센서 데이터를 언어 모델이 읽고 올바른 목표 대상을 스스로 판단합니다.

---

## 만든 사람 · Minjung Lee (Highj)

CONNECT AI LAB에서 로컬 AI와 강화학습 AI를 공부하고, 이를 실전에 적용해 서비스를 하나씩 만들어 보며 AI 1인 기업가의 꿈을 이뤄가고 있습니다.

- **LunarLander** 환경에서 267.9점 고득점 안정 착륙([`connectailab-rl-highj-v1-lunarlander`](https://huggingface.co/minjunglee27/connectailab-rl-highj-v1-lunarlander)) 및 우측 쏠림을 잡은 정중앙 정밀 착륙 달성([`connectailab-rl-highj-v2-lunarlander`](https://huggingface.co/minjunglee27/connectailab-rl-highj-v2-lunarlander))
- **CartPole** 환경에서 DQN 파라미터를 93% 축소한 초경량 의사결정 모델 구축 ([`connectailab-rl-highj-v1-cartpole-lite`](https://huggingface.co/minjunglee27/connectailab-rl-highj-v1-cartpole-lite))
- **Connect Tycoon** 비즈니스 의사결정 모델 구축 ([`connectailab-rl-highj-v1`](https://huggingface.co/minjunglee27/connectailab-rl-highj-v1) · 고도화 버전: [`connectailab-rl-highj-v2`](https://huggingface.co/minjunglee27/connectailab-rl-highj-v2))
- **LINK-01 (자율 주행)** 4족 보행 로봇 목표 지점 주행 모델 ([`connectailab-rl-highj-goto-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01))
- **LINK-01 (사물 선택)** 4족 보행 로봇 단서 기반 물건 고르기 모델 ([`connectailab-rl-highj-choose-v1-link01`](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01))
- [CONNECT AI LAB](https://www.youtube.com/@CONNECT-AI-LAB) × [AI CITY BUILDERS](https://www.aicitybuilders.com/robot) 공동 연구 참여

---

## 두뇌 및 코스 사양 (Specifications)

- **코스 파일**: `world.json` (해시: `9814f10c`, 시작점 `[-1.3345, 0.1702, -1.6455]`, 타겟: 머그컵, 화분)
- **선생님 두뇌**: `brain.json` (PPO 알고리즘, MLP `[26, 64, 64, 4]`)
- **입력 관측 (26개)**:
  1. 단서 원-핫 4개 (`단서=머그컵`, `단서=사과`, `단서=랜턴`, `단서=화분`)
  2. 4개 사물별 상태 16개 (`머그컵 있음/거리/sin/cos`, `사과 있음/거리/sin/cos`, `랜턴 있음/거리/sin/cos`, `화분 있음/거리/sin/cos`)
  3. 직전 선택 4개 (`직전 선택 1~4`)
  4. 로봇 속도 2개 (`앞 속도`, `회전 속도`)
- **출력 행동 (4개)**:
  - `머그컵`, `사과`, `랜턴`, `화분`

---

## 만든 곳 · CONNECT AI LAB × AI CITY BUILDERS

CONNECT AI LAB과 AI CITY BUILDERS가 함께 연구하고 개발합니다.

- 공식 웹사이트: [AI CITY BUILDERS](https://www.aicitybuilders.com/robot)
- 유튜브 채널: [CONNECT AI LAB](https://www.youtube.com/@CONNECT-AI-LAB)
- 깃허브 저장소: [CONNECT TYCOON](https://github.com/wonseokjung/connect-tycoon)
