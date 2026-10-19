---
license: apache-2.0
language: [ko, en]
library_name: numpy
pipeline_tag: reinforcement-learning
tags: [connect-ai-lab, deep-reinforcement-learning, gymnasium, connect-company, connect-tycoon, jev, jev-style, reinforcement-learning, ppo, decision-making, prefrontal-cortex, korean, highj, teacher]
---

<p align="center"><img src="https://raw.githubusercontent.com/wonseokjung/connect-tycoon/main/docs/brand/banner.gif" alt="RL AI COMPANY DECISION MAKING MODEL" width="100%"></p>

<p align="center"><a href="https://colab.research.google.com/github/wonseokjung/connect-tycoon/blob/main/notebooks/rl_decision_model_qwen_colab.ipynb"><img src="https://img.shields.io/badge/Colab-%EC%A7%81%EC%A0%91%20%ED%95%99%EC%8A%B5%ED%95%98%EA%B8%B0-d0f991?style=for-the-badge&logo=googlecolab&logoColor=d0f991&labelColor=050807&color=d0f991" alt="Colab"></a> <a href="https://github.com/wonseokjung/connect-tycoon"><img src="https://img.shields.io/badge/GitHub-CONNECT%20TYCOON-d0f991?style=for-the-badge&logo=github&logoColor=d0f991&labelColor=050807&color=d0f991" alt="GitHub"></a> <a href="https://www.youtube.com/@CONNECT-AI-LAB"><img src="https://img.shields.io/badge/YouTube-CONNECT%20AI%20LAB-d0f991?style=for-the-badge&logo=youtube&logoColor=d0f991&labelColor=050807&color=d0f991" alt="YouTube"></a> <a href="https://www.aicitybuilders.com/robot"><img src="https://img.shields.io/badge/AI%20CITY%20BUILDERS-%EA%B0%95%ED%99%94%ED%95%99%EC%8A%B5%20AI-d0f991?style=for-the-badge&logo=bookstack&logoColor=d0f991&labelColor=050807&color=d0f991" alt="AI CITY BUILDERS"></a></p>




# connectailab-rl-highj-v2-teacher · AI 사장 (CONNECT TYCOON)

**connectailab-rl-highj-v2-teacher** is a high-performance reinforcement learning decision policy (Numpy-based `brain.json`) trained via PPO in the CONNECT TYCOON simulator. It serves as the core teacher model that distilled balanced business decision-making capabilities into `connectailab-rl-highj-v2`.

### Performance Highlights (40-Month Unseen Simulation)
- **Monthly Net Profit**: **11.76M KRW** (vs 3.24M KRW rule-based CEO, +263% increase)
- **Customer Satisfaction**: **95.0%** (vs 79.0%)
- **Risk Incidents**: **2.5 / month** (vs 7.8 / month, -68% risk reduction)
- **Stockout Days**: **0.6 days / month** (near-zero inventory stockouts across 40 months)
- **Balanced Values**: Profit 1.0, Customer Satisfaction 1.0, Risk Aversion 1.0

---

## 만든 사람 · Minjung Lee (Highj)

CONNECT AI LAB에서 로컬 AI와 강화학습 AI를 공부하고, 이를 실전에 적용해 서비스를 하나씩 만들어 보며 AI 1인 기업가의 꿈을 이뤄가고 있습니다.

CONNECT AI LAB의 **Jay 멘토님**이 설계한 [CONNECT TYCOON](https://github.com/wonseokjung/connect-tycoon) 환경에서, 회사의 3대 핵심 가치(이익 1.0, 고객 만족 1.0, 위험 회피 1.0)를 균형 있게 추구하도록 집중 훈련된 **고성능 교사 정책(Teacher Brain · v2)**입니다.

처음 보는 40개월 동안 회사를 직접 경영하는 시험에서 **월평균 순이익 1,176만원**과 **고객 만족도 95%**, **품절일 0.6일(결품 제로 수렴)**을 달성하여 기본 규칙 사장(324만원) 대비 압도적인 경영 성과를 입증했습니다.  
본 두뇌는 **[connectailab-rl-highj-v2](https://huggingface.co/minjunglee27/connectailab-rl-highj-v2)** 언어 모델에게 고품질 의사결정 데이터를 가르친 핵심 교사 모델입니다.

| 처음 보는 40개월 평균 | 한 달 이익 | 고객 만족 | 위험 사고 | 사람 확인 초과 | 품절일 |
|---|---|---|---|---|---|
| 규칙 사장 | 324만원 | 79% | 7.8건 | 37.8건 | 10.7일 |
| **connectailab-rl-highj-v2-teacher** | **1176만원** | **95%** | **2.5건** | **12.4건** | **0.6일** |

회사 규모(config): `{"warehouse": 250.0, "base_demand": 40.0, "unit_cost": 1.5, "order_scale": 1.0, "staff_bonus": 0, "wage": 0.0, "ad_power": 1.0, "fraud_tool": 0, "extra_cs": 0, "extra_refund": 0}`

<p align="center"><img src="https://raw.githubusercontent.com/wonseokjung/connect-tycoon/main/docs/images/hero.gif" alt="모델이 회사를 운영하는 하루" width="88%"></p>
<p align="center"><sub>시뮬레이터 속 회사 · 맨 위층의 모델이 판단하면 빛줄기가 그 층으로 내려가고, 결과가 돈 · 만족 · 사고로 돌아옵니다</sub></p>


## JEV로 묻고 답하기 (API Usage)

```python
import connect_tycoon as ct
brain = ct.CompanyBrain.from_hub("minjunglee27/connectailab-rl-highj-v2-teacher")
brain({"model": "typesafe/jev-1.13", "state": {"department": "refund", "reason": "미배송", "tier": "단골", "amount": 8.7, "fraud_score": 0.31461497442796826}, "questions": {"decision": {"type": "choice", "instructions": "환불 요청을 어떻게 처리할지 고르세요. 악용이면 돈을 잃고, 정상 고객을 거절하면 만족이 떨어집니다. 회사의 가치 — 이익 1 · 고객 만족 1 · 위험 회피 1.", "criteria": {"full": "전액 환불", "partial": "부분 환불 (절반)", "deny": "거절", "human": "사람 확인 · 악용이면 사람이 거절합니다 · 건당 0.8만원"}}}})
```

```json
{
 "model": "connect-company/connectailab-rl-highj-v2-teacher",
 "answers": {
  "decision": {
   "type": "choice",
   "choice": "full",
   "probabilities": {
    "full": 0.9883,
    "partial": 0.0003,
    "deny": 0.0018,
    "human": 0.0097
   },
   "confidence": 0.9883,
   "reason": "강화학습 정책"
  }
 }
}
```

## 게임에서 사장으로 앉히기 (Play in Game)

```bash
pip install "connect-tycoon[game]"
connect-tycoon play --brain hf:minjunglee27/connectailab-rl-highj-v2-teacher
```

## 만든 곳 · CONNECT AI LAB × AI CITY BUILDERS

AI 교육 브랜드 · Transforming Lives Through AI Education

- [CONNECT AI LAB 유튜브](https://www.youtube.com/@CONNECT-AI-LAB) · AI 1인 기업 · 로컬 AI · 강화학습 · JEV 무료 강의
- [AI CITY BUILDERS](https://www.aicitybuilders.com) · AI 비즈니스의 정석 · [강화학습 AI 과정](https://www.aicitybuilders.com/robot)
- [Connect AI](https://www.ezerai.xyz) · 기업 의사결정 모델 C1 공동 연구 · 모델 연결은 테스트 중

합성 회사 시뮬레이터 위의 교육용 모형입니다. 실제 경영 성과를 보장하거나 예측하지 않습니다.
