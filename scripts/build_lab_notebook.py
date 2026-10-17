"""notebooks/logistics_brain_qwen_colab.ipynb 만들기 · 웹 학습 실험실의 물류 두뇌(brain.json) → Qwen 지도학습 → 강화학습 → Hugging Face."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_notebook as B

REPO = B.REPO
LAB = "https://www.ezerai.xyz/models/rl"
CELLS = [
    ("md", """# 물류 두뇌 → Qwen 의사결정 모델 (Colab)

**CONNECT AI LAB × AI CITY BUILDERS** · [CONNECT TYCOON](https://github.com/wonseokjung/connect-tycoon)

웹 학습 실험실에서 내가 알고리즘(Q러닝 · DQN · PPO)과 파라미터(감마 · 보상 · 동전 · 목표 · 꿈 · 호기심)를 정해 키운 **물류 두뇌(brain.json)** 를,
언어 모델 **Qwen3.5-0.8B** 에 옮겨 담아 **물류센터 의사결정 AI 모델**로 만들고 Hugging Face에 올립니다.

1. **두뇌 불러오기** · 내 brain.json (없으면 예시 두뇌)
2. **문제집** · 두뇌가 하루를 운영하는 동안 10분마다 보기 7개를 하나씩 해 보고, 하루 끝까지 다시 돌려 점수를 매깁니다
3. **학습 전 Qwen** · 아무것도 배우지 않은 Qwen을 물류센터장 자리에 앉혀 봅니다
4. **지도학습** · Qwen이 내 두뇌의 답을 그대로 배웁니다 (LoRA)
5. **강화학습** · 두뇌의 답보다 확실히 나은 보기는 올리고, 확실히 나쁜 보기는 내립니다
6. **공개** · 시험 24일 점수가 더 높은 쪽을 Hugging Face에 `connectailab-rl-이름-버전-logistics-qwen`

> 메뉴 **런타임 → 런타임 유형 변경 → GPU (T4 이상)**. 왼쪽 🔑(보안 비밀)에 `HF_TOKEN`(Write 권한)을 넣어 두면 마지막 셀에서 바로 올라갑니다."""),
    ("code", f"""# 설치 (2~3분)
!pip -q install "connect-tycoon @ git+{REPO}" "transformers==5.18.0" peft accelerate huggingface_hub
!pip -q install flash-linear-attention || echo "(빠른 계산 모듈 없이 진행 · 조금 느릴 뿐 결과는 같습니다)"
!pip -q uninstall -y torchao   # Colab 기본 torchao(0.10)가 최신 peft와 맞지 않습니다 · 이 학습에는 필요 없습니다
import torch, connect_tycoon as ct
print("CONNECT TYCOON", ct.__version__, "· GPU", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "없음 (런타임을 GPU로 바꾸세요)")""", "install"),
    ("md", f"""## 1 · 내 물류 두뇌 불러오기

[학습 실험실]({LAB})에서 학습을 마치고 **brain.json 내려받기**를 누른 파일입니다.
- **끌어다 놓기** · Colab 왼쪽 **📁(파일)** 창에 brain.json을 끌어다 놓고 실행 (가장 확실)
- **파일 선택 버튼** · 파일 창에 없으면 이 셀 아래에 [파일 선택] 버튼이 뜹니다
- `USE_MY_BRAIN`을 끄면 예시 두뇌(PPO · 기본값)로 해 봅니다

**왜** · 파이썬 시뮬레이터가 웹과 걸음마다 똑같이 움직여서, 웹에서 본 점수가 여기서도 그대로 나와야 합니다.

✅ **정상이면** · 아래 '시험 24일 하루 점수'가 웹 실험실 결과 화면의 점수와 같습니다 (예시 두뇌 279 · 규칙 사장 86)"""),
    ("code", """USE_MY_BRAIN = True                                    #@param {type:"boolean"}
UPLOAD_BUTTON = True                                   #@param {type:"boolean"}
from connect_tycoon import labenv as E
from connect_tycoon.lab import LabBrain, example, is_lab, ALGO_NAME

if USE_MY_BRAIN:
    from connect_tycoon.colab import find_brain           # 📁에 있으면 그것, 없으면 [파일 선택] 버튼
    path = find_brain(upload_button=UPLOAD_BUTTON)
    assert is_lab(path), "회사 게임(CONNECT TYCOON)의 brain.json입니다 · 그 두뇌는 'Qwen 강화학습' Colab ①을 쓰세요"
    brain = LabBrain.from_file(path)
else:
    brain = example()
assert brain.spec.get("env") == E.ENV_ID, f"다른 버전 환경의 두뇌입니다 ({brain.spec.get('env')}) · 실험실에서 새로 학습해 내려받으세요"
mine = E.evaluate(brain.policy())
rule = E.evaluate(E.rule_policy)
print(f"두뇌 {brain.name} · {ALGO_NAME.get(brain.algo, brain.algo)}")
print(f"시험 24일 하루 점수 {mine['score']:.1f} (웹 {brain.test.get('score', 0):.1f}) · 제시간 출발 {mine['onTimeRate']:.0%} · 규칙 사장 {rule['score']:.1f}")""", None),
    ("md", """## 2 · 문제집 · 보기마다 하루 끝까지 다시 돌려 봅니다 (약 2~4분)

**무엇을** · 두뇌가 하루를 운영하는 동안, 10분마다 보기 7개(대기 · 먼저 온 트럭 도킹 · 급한 트럭 도킹 · 초과근무 · 지게차 집중 · 검수 강화 · 임시 인력)를 하나씩 해 보고, 남은 하루를 두뇌로 끝까지 돌립니다.
보기마다 '그렇게 했으면 남은 하루의 보상이 얼마였나'(서로 다른 미래 8개의 평균)가 점수입니다. 연습 때 보상을 어떻게 바꿨든, 점수는 **공식 보상**으로만 매깁니다.

**정답** · 지도학습의 정답은 **내 두뇌의 답**입니다. 언어 모델이 먼저 내 두뇌를 그대로 배웁니다.
**점수** · 강화학습에서 씁니다. 두뇌의 답보다 20점 넘게 낫거나 나쁜 보기만 반영합니다.

**왜 이렇게 (예시 두뇌로 해 본 실험)**
- 점수 1등을 정답으로 쓰면 → 운 좋게 높게 나온 보기만 골라 두뇌보다 나빠짐 (279 → 250)
- 점수를 그대로 강화학습에 쓰면 → 점수는 '나머지 하루는 두뇌가 운영한다'는 가정이라 임시 인력 호출이 늘 조금 좋아 보여, 모델이 그것만 고르고 트럭을 대지 않음 (−805점)

**모양** · 상황(사람이 읽는 화면 글) · 질문 · 보기 A~G → 답은 글자 하나

✅ **정상이면** · 30일이면 학습 약 1,800문제 · 검증 240 · 시험 240"""),
    ("code", """from connect_tycoon.llm import labdata as L, data as D
TRAIN_DAYS = 30                                        # 늘릴수록 문제가 많아집니다 (하루 ≈ 60문제 · 3~5초)
splits = {"train": range(30000, 30000 + TRAIN_DAYS), "valid": range(31000, 31004), "test": range(32000, 32004)}
print(L.build(brain, "lab_data", splits=splits, log=None))
rows = D.load("lab_data", "train")
adv = L.advantages(rows)
print(f"강화학습 신호가 있는 문제 {sum(any(a) for a in adv)}개 / {len(rows)}개 (두뇌의 답보다 20점 넘게 차이 나는 보기가 있는 문제)")
k = next(i for i, a in enumerate(adv) if any(a))
ex = rows[k]
print(); print(ex["task"]["state"]); print(ex["task"]["question"])
for o, s, a in zip(ex["task"]["options"], ex["scores"], adv[k]): print(f"  {o['label']} {o['description'][:34]:36s} 점수 {s:6.1f}  장점 {a:+.2f}")
print("정답(두뇌의 답)", ex["answer"])""", None),
    ("md", """## 3 · 학습 전 Qwen · 물류센터장 자리에 앉혀 보기 (약 2분)

**무엇을** · 아무것도 배우지 않은 Qwen에게 시험 문제를 풀게 하고, 웹 실험실과 똑같은 시험 24일 동안 물류센터를 맡깁니다.
**왜** · 학습 효과를 보려면 출발점을 먼저 재야 합니다.

✅ **정상이면** · 정답률 낮음 · 하루 점수가 규칙 사장 근처이거나 더 낮음"""),
    ("code", """from connect_tycoon.llm import train_torch as T
test = D.load("lab_data", "test")
base = T.Scorer()
results = {"Qwen 학습 전": D.agreement(test, base.pick)}
results["Qwen 학습 전"].update(L.day_report(base.pick, log=None))
print(results["Qwen 학습 전"])
del base; torch.cuda.empty_cache()""", None),
    ("md", """## 4 · 지도학습 · 내 두뇌의 답을 따라 배우기 (T4 약 40분)

**무엇을** · 두뇌가 고른 보기 글자를 맞히도록 LoRA를 학습합니다 (모델 전체가 아니라 작은 덧붙임 층만).
**왜** · 두뇌(작은 신경망)가 숫자로 하던 판단을, 언어 모델이 글을 읽고 하도록 옮깁니다.
**드문 답은 여러 번** · 두뇌가 82%는 '급한 트럭 도킹', 18%는 '초과근무'를 고르면, 그대로 배운 Qwen은 언제 초과근무를 할지 배우기 전에 늘 도킹만 고릅니다. 그래서 드문 답을 몇 번 반복해 보여 줍니다.

✅ **정상이면** · 정답률 85% 안팎 · 하루 점수가 두뇌 가까이 올라옵니다"""),
    ("code", """sft = T.sft("lab_data", "adapters/sft", epochs=2, lr=1e-4, batch=8)
results["지도학습"] = D.agreement(test, sft.pick)
results["지도학습"].update(L.day_report(sft.pick, log=None))
print(results["지도학습"])
del sft; torch.cuda.empty_cache()""", None),
    ("md", """## 5 · 강화학습 · 시뮬레이터 점수로 고치기 (T4 약 15분)

**무엇을** · 두뇌의 답보다 확실히(20점 넘게) 나은 보기의 확률은 올리고, 확실히 나쁜 보기는 내립니다. 지도학습 모델에서 너무 멀어지지 않게 붙잡아 둡니다(KL).
임시 인력이 이미 근무 중일 때 또 부르기는 좋아 보여도 올리지 않습니다.
**손실** · −Σ p(보기) · 장점(보기) + β · KL(p ‖ 지도학습 모델)

✅ **정상이면** · 하루 점수가 지도학습과 비슷하거나 오릅니다. 마지막 셀은 **시험 24일 점수가 더 높은 쪽**(지도학습 또는 강화학습)을 올립니다"""),
    ("code", """rlm, hist = T.rl("lab_data", "adapters/sft", "adapters/rl", steps=100, batch=8, lr=5e-6, beta=0.2, max_rows=1500)
results["강화학습"] = D.agreement(test, rlm.pick)
results["강화학습"].update(L.day_report(rlm.pick, log=None))
print(f"{'':12s} 정답률  후회   하루 점수  제시간")
for k, v in results.items(): print(f"{k:12s} {v['accuracy']:.1%}  {v['regret']:.2f}  {v['day_score']:7.1f}   {v['on_time']:.0%}")
print(f"{'두뇌':12s}   —      —    {mine['score']:7.1f}   {mine['onTimeRate']:.0%}")
print(f"{'규칙 사장':12s}   —      —    {rule['score']:7.1f}   {rule['onTimeRate']:.0%}")
BEST = "adapters/rl" if results["강화학습"]["day_score"] >= results["지도학습"]["day_score"] else "adapters/sft"
print("올릴 모델 ·", "강화학습" if BEST.endswith("rl") else "지도학습", "(시험 24일 점수가 더 높은 쪽)")""", None),
    ("md", """## 6 · Hugging Face에 올리기

1. https://huggingface.co/settings/tokens 에서 **Write** 토큰을 만듭니다.
2. Colab 왼쪽 🔑(보안 비밀)에 이름 `HF_TOKEN`, 값에 토큰을 넣고 **노트북 액세스**를 켭니다.
3. **이름**을 영문으로 적습니다. 업로드 이름은 `connectailab-rl-이름-버전-logistics-qwen` 입니다 (예: `connectailab-rl-jay-v1-logistics-qwen`).
4. **나를 알리는 글**을 자유롭게 적으면 모델 카드 맨 위 '만든 사람'에 들어갑니다.
5. `PUSH_BRAIN`을 켜면 두뇌(brain.json)도 `connectailab-rl-이름-버전-logistics`로 함께 올라갑니다.

토큰은 코드에 적지 않습니다."""),
    ("code", """from google.colab import userdata
from huggingface_hub import HfApi
from connect_tycoon.llm.hub import make_author, push, repo_name
import json

try:
    HF_TOKEN = userdata.get("HF_TOKEN")
except Exception:
    HF_TOKEN = None
assert HF_TOKEN, "왼쪽 🔑에 HF_TOKEN(Write 권한)을 넣고 노트북 액세스를 켜 주세요"
me = HfApi(token=HF_TOKEN).whoami()["name"]

NAME = "jay"                                         #@param {type:"string"}
VERSION = "v1"                                       #@param {type:"string"}
PRIVATE = False                                      #@param {type:"boolean"}
PUSH_BRAIN = True                                    #@param {type:"boolean"}
MODEL_NAME = repo_name(NAME, VERSION, "logistics-qwen")   # connectailab-rl-이름-버전-logistics-qwen

# 나를 알리는 글 · 형식 없이 자유롭게 (모델 카드 맨 위 '만든 사람'에 그대로 들어갑니다)
ABOUT_ME = '''
'''
author = make_author(ABOUT_ME)

meta = json.load(open("lab_data/meta.json"))
meta["chosen"] = "강화학습" if BEST.endswith("rl") else "지도학습"
url = push(BEST, repo=f"{me}/{MODEL_NAME}", results=results, meta=meta, backend="torch", token=HF_TOKEN, private=PRIVATE, author=author)
print("올라갔습니다 ·", url)
if PUSH_BRAIN:
    from connect_tycoon.hub import push_lab_brain
    json.dump(brain.spec, open("brain.json", "w"), ensure_ascii=False)
    print("두뇌 ·", push_lab_brain("brain.json", name=NAME, version=VERSION, author=author, token=HF_TOKEN))""", None),
]


if __name__ == "__main__":
    B.CELLS = CELLS
    path = B.build(os.path.join(os.path.dirname(__file__), "..", "notebooks", "logistics_brain_qwen_colab.ipynb"))
    import json
    nb = json.load(open(path, encoding="utf-8"))
    nb["metadata"]["accelerator"] = "GPU"; nb["metadata"]["colab"]["gpuType"] = "T4"
    json.dump(nb, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path)
