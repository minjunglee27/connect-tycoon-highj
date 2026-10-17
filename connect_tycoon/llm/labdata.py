"""① 문제집 (물류) · 웹 학습 실험실에서 키운 두뇌(brain.json) → Qwen이 배울 문제집.

두뇌가 물류센터 하루를 운영하는 동안, 10분(한 걸음)마다 보기 7개를 하나씩 해 보고 그 하루를 끝까지 두뇌로 다시 돌립니다.
보기마다 '그렇게 했으면 남은 하루의 보상이 얼마였나'(서로 다른 미래 8개의 평균)가 점수입니다.

정답(지도학습) · 두뇌의 답. 언어 모델은 먼저 내 두뇌를 그대로 배웁니다.
장점(강화학습) · 두뇌의 답보다 확실히(dead점 넘게) 낫거나 나쁜 보기만 · 그 사이는 0.

실험으로 정한 이유 (예시 두뇌 · 시험 24일)
- 점수 1등을 정답으로 · 운 좋게 높게 나온 보기만 골라 두뇌보다 나빠짐 (279 → 250)
- 점수를 그대로 장점으로 강화학습 · 점수는 '나머지 하루는 두뇌가 운영한다'는 가정이라, 임시 인력 호출이 늘 조금씩 좋아 보여
  모델이 그것만 고르고 트럭을 대지 않게 됨 (−805점). 그래서 두뇌의 답을 기준으로 확실한 차이만 씁니다.
- 두뇌의 답 + 10점 넘게 나은 보기로 고친 정답은 계획(미리 돌려 보기)으로는 336점이지만, 화면 글로는 72%만 맞힐 수 있어 따라 배우기 어려움
점수는 공식 보상(시험 세상)으로만 매깁니다. 연습할 때 보상을 어떻게 바꿨든, 모두가 같은 기준으로 비교됩니다.

    sft/train.jsonl   {"messages": [system, user(문제), assistant(정답 글자)]}     ← train_torch.sft · train_mlx.sft 그대로
    rl/train.jsonl    {"task": 문제, "scores": [보기별 점수], "answer", "teacher": 두뇌가 고른 글자, "dept": "logistics", ...}

문제(state)는 두뇌가 보던 화면(관측 16개)을 사람이 읽는 글로 바꾼 것입니다. 그래서 Qwen을 같은 시뮬레이터에 앉혀 바로 채점할 수 있습니다.
"""
import json
import os

from .. import labenv as E
from .format import LETTERS, messages

SPLITS = {"train": range(30000, 30030), "valid": range(31000, 31004), "test": range(32000, 32004)}
QUESTION = "지금부터 10분 동안 물류센터에서 무엇을 할까요?"
R = E.DEFAULT_REWARD
OPTIONS = [("wait", "대기 · 지금 하던 대로 둔다 (비용 0)"),
           ("dock_first", "먼저 온 트럭 도킹 · 빈 도크에 가장 오래 기다린 트럭을 댄다"),
           ("dock_urgent", "급한 트럭 먼저 도킹 · 출발 시각이 가장 급한 트럭(VIP 우선)을 댄다"),
           ("overtime", f"초과근무 · 이번 10분 피킹 팔레트 +3 (비용 {R['overtimeCost']:g})"),
           ("focus", "지게차 집중 · 모든 지게차가 가장 급한 도킹 트럭부터 싣는다"),
           ("inspect", "검수 강화 · 지게차 1대가 검수를 맡아 느려지지만 신입 실수(다시 싣기)를 막는다"),
           ("temp", f"임시 인력 호출 · 1시간 동안 지게차 +1 · 피킹 +1 (비용 {R['overtimeCost'] * 2:g})")]
TRAP = {"rain": "🌧 소나기 · 피킹 −1", "breakdown": "🔧 지게차 고장 · 지게차 1대 멈춤", "absent": "🤒 결근 · 신입 실수 · 실은 팔레트를 가끔 다시 실어야 함",
        "jam": "🚧 도로 정체 · 트럭이 묶였다가 한꺼번에 도착", "outage": "💻 시스템 다운 · 위 숫자가 틀릴 수 있음", "surge": "🔥 피크 폭주 · 주문 1.8배"}
EV = [e[0] for e in E.EVENTS]


def _clock(step):
    m = 10 * 60 + step * 10                               # 웹 실험실 다시보기와 같은 시각 · 오전 10시 → 오후 8시
    h = m // 60
    return f"{'오전' if h < 12 else '오후'} {h if h <= 12 else h - 12}:{m % 60:02d}"


def _slack(v):
    s = round(v * 20 - 4)
    return "이미 늦음" if s < 0 else "지금 출발 시각" if s == 0 else "160분 이상" if s >= 16 else f"{s * 10}분"


def state_text(obs, temp=0):
    """관측 16개(0~1) → 물류센터장이 보는 화면 글. 숫자는 두뇌가 본 값 그대로입니다 (시스템 다운이면 흔들린 값).
    temp · 임시 인력이 남은 걸음 (두뇌의 관측에는 없지만 센터장은 알고 있는 사실)."""
    o = [float(x) for x in obs]
    t = round(o[0] * E.STEPS)
    wait, free, staged, remain, late = round(o[1] * 6), round(o[2] * E.DOCKS), round(o[3] * 10), round(o[5] * 16), round(o[7] * E.DOCKS)
    docked = E.DOCKS - free
    lines = [f"물류센터 하루 · {_clock(t)} (하루 {E.STEPS}걸음 중 {t + 1}번째 · 한 걸음 10분 · 오후 8시 마감)"]
    lines.append(f"대기 트럭 {'6대 이상' if wait >= 6 else f'{wait}대'} · 가장 급한 대기 트럭 출발까지 {_slack(o[4])}" if wait else "대기 트럭 없음")
    lines.append(f"빈 도크 {free}/{E.DOCKS} · 상차 대기 팔레트 {'10개 이상' if staged >= 10 else f'{staged}개'}")
    if docked:
        lines.append(f"도킹한 트럭 {docked}대 · 남은 팔레트 {'16개 이상' if remain >= 16 else f'{remain}개'} · 가장 급한 도킹 트럭 출발까지 {_slack(o[6])}"
                     + (f" · 이미 늦은 트럭 {late}대" if late else ""))
    else:
        lines.append("도킹한 트럭 없음")
    if temp > 0:
        lines.append(f"임시 인력 근무 중 · {temp * 10}분 남음 (지게차 +1 · 피킹 +1)")
    ev = dict(zip(EV, o[8:15]))
    traps = [TRAP[e] for e in EV if e != "vip" and ev[e] > 0.5]
    if ev["vip"] > 0.5:
        traps.insert(0, "🚨 VIP 긴급 트럭 · 보너스 2배 · 여유가 짧음")
    lines.append("함정 · " + " | ".join(traps) + (f" · 남은 시간 약 {round(o[15] * 10) * 10}분" if o[15] > 0 else "") if traps else "함정 없음")
    lines.append(f"보상 · 제시간 출발 +{R['onTime']:g} (VIP +{R['onTime'] * 2:g}) · 늦으면 감점 · 대기 트럭 1대당 10분마다 −{R['waitCost']:g} · "
                 f"마감 때 남은 트럭 1대당 −{R['leftover']:g}")
    return "\n".join(lines)


def task(obs, temp=0):
    return {"state": state_text(obs, temp), "question": QUESTION,
            "options": [{"label": LETTERS[i], "key": k, "description": d} for i, (k, d) in enumerate(OPTIONS)]}


def _rest(env, policy):
    total, done = 0.0, False
    while not done:
        o = env.last
        r, done, _ = env.step(policy(o["obs"], o["key"], env)); total += r
    return total


def scores_now(env, policy, seed, futures=4):
    """지금 상황에서 보기 7개의 점수 · 보기마다 하루 끝까지 두뇌로 다시 돌린 보상, 서로 다른 미래 futures개의 평균.
    미래(트럭 · 함정)는 보기끼리 같게 맞추고(공정한 비교), 실제로 올 미래와는 다르게 뽑습니다(미래를 엿보지 않게)."""
    scores = [0.0] * len(E.ACTIONS)
    for k in range(futures):
        for a in range(len(E.ACTIONS)):
            c = E.clone(env)
            c.r = E.Rng(seed * 7919 + env.t * 101 + k + 1)
            r, d, _ = c.step(a)
            scores[a] += (r + (0.0 if d else _rest(c, policy))) / futures
    return scores


def label(scores, chosen, temp=0, margin=None):
    """정답 글자 번호 · 두뇌의 답 (margin을 주면 다른 보기가 margin점 넘게 나을 때 그 보기 · 임시 인력이 이미 있으면 다시 부르기는 빼고)."""
    if margin is None:
        return chosen
    ok = [i for i in range(len(scores)) if not (temp > 0 and i == 6)]
    best = max(ok, key=lambda i: scores[i])
    return best if scores[best] - scores[chosen] > margin else chosen


def rows_for_day(policy, seed, stride=1, futures=8, margin=None, min_gap=1e-6):
    """두뇌(policy)가 운영하는 하루 · 걸음마다 보기 7개를 하나씩 해 보고 하루 끝까지 다시 돌린 점수 (공식 보상)."""
    env, out, done = E.DayEnv(), [], False
    env.reset(seed)
    while not done:
        o = env.last
        chosen = policy(o["obs"], o["key"], env)
        if env.t % stride == 0:
            scores = scores_now(env, policy, seed, futures)
            if max(scores) - min(scores) >= min_gap:              # 무엇을 해도 결과가 같은 순간은 배울 것이 없습니다
                best = label(scores, chosen, env.temp, margin)
                out.append({"task": task(o["obs"], env.temp), "scores": [round(s, 4) for s in scores], "answer": LETTERS[best], "label": "lab",
                            "teacher": LETTERS[chosen], "temp": env.temp, "dept": "logistics", "seed": seed, "index": env.t})
        _, done, _ = env.step(chosen)
    return out


def build(brain, out_dir, splits=None, stride=1, futures=8, margin=None, log=print):
    """문제집을 만듭니다. brain은 lab.LabBrain. 반환: {split: 문제 수}. 하루 ≈ 60문제 · CPU 3~5초."""
    splits = splits or SPLITS
    policy = brain.policy()
    os.makedirs(os.path.join(out_dir, "sft"), exist_ok=True); os.makedirs(os.path.join(out_dir, "rl"), exist_ok=True)
    counts = {}
    for name, seeds in splits.items():
        rows = []
        for i, s in enumerate(seeds):
            rows += rows_for_day(policy, s, stride=stride, futures=futures, margin=margin)
            if log and (i + 1) % 10 == 0 or log and i + 1 == len(seeds): log(f"{name} {i + 1}/{len(seeds)}일 · 문제 {len(rows)}개")
        with open(os.path.join(out_dir, "sft", f"{name}.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps({"messages": messages(r["task"], r["answer"])}, ensure_ascii=False) + "\n")
        with open(os.path.join(out_dir, "rl", f"{name}.jsonl"), "w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        counts[name] = len(rows)
    spec = brain.spec
    meta = {"kind": "lab", "industry": "logistics", "env": E.ENV_ID, "counts": counts, "margin": margin,
            "futures": futures, "teacher": spec.get("name"), "algo": spec.get("algo"), "teacher_test": spec.get("test", {}).get("score"),
            "baselines": spec.get("baselines"), "config": spec.get("config"), "splits": {k: [v.start, v.stop] for k, v in splits.items()}}
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    return counts


def advantages(rows, dead=20.0, clip=3.0):
    """강화학습 장점 · 두뇌의 답과 비교해 dead점 넘게 나으면 +, 나쁘면 − (그 사이와 두뇌의 답은 0).
    임시 인력이 이미 근무 중일 때 다시 부르기는 더 낫게 보여도 0 (계속 부르기만 하는 버릇을 막습니다)."""
    out = []
    for r in rows:
        s, k = r["scores"], LETTERS.index(r["teacher"])
        temp = r.get("temp", 1 if "임시 인력 근무 중" in r["task"]["state"] else 0)
        adv = []
        for i, x in enumerate(s):
            d = x - s[k]
            if abs(d) <= dead or (d > 0 and temp > 0 and i == 6):
                d = 0.0
            adv.append(max(-clip, min(clip, d / (2 * dead))))
        out.append(adv)
    return out


def as_policy(pick):
    """pick(task) → 글자 (Scorer.pick) · Qwen을 물류센터장 자리에 앉히는 정책."""
    return lambda obs, key, env=None: LETTERS.index(pick(task(obs, env.temp if env is not None else 0)))


def day_report(pick, seeds=None, log=print):
    """Qwen이 시험 날(웹과 같은 24일)을 운영한 점수 · 웹 실험실의 점수와 바로 비교됩니다."""
    seeds = list(seeds or E.TEST_SEEDS)
    policy, tot, agg = as_policy(pick), 0.0, {}
    for i, s in enumerate(seeds):
        t, _, st = E.run_day(policy, s)
        tot += t
        for k, v in st.items():
            agg[k] = agg.get(k, 0) + v
        if log and (i + 1) % 6 == 0: log(f"  시험 {i + 1}/{len(seeds)}일 · 평균 {tot / (i + 1):.1f}")
    n = len(seeds)
    return {"day_score": tot / n, "on_time": agg["onTime"] / max(1, agg["onTime"] + agg["late"] + agg["left"]), "days": n}
