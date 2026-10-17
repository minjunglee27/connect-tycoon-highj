"""웹 학습 실험실의 "물류센터 하루" 환경 (logistics-day/2)을 파이썬으로 그대로 옮긴 것.
같은 씨앗 · 같은 두뇌면 웹(TypeScript)과 걸음마다 똑같이 움직입니다 (난수 · 정렬 · 반올림까지 맞춤).
Qwen 문제집을 만들 때 씁니다: 두뇌가 운영하는 하루에서, 걸음마다 보기 7개를 하나씩 해 보고 하루 끝까지 다시 돌려 점수를 매깁니다.
"""
import math

import numpy as np

ENV_ID = "logistics-day/2"
STEPS, DOCKS = 60, 4
WORLD = {"base": 0.16, "am": 0.9, "pm": 0.72, "slack": 7, "span": 7, "supply": 2, "lifts": 3, "trap": 0.09}
ACTIONS = ["대기", "먼저 온 트럭 도킹", "급한 트럭 먼저 도킹", "초과근무 (피킹 +3)", "지게차를 급한 트럭에 집중", "검수 강화", "임시 인력 호출"]
EVENTS = [("rain", "소나기", 8), ("breakdown", "지게차 고장", 8), ("absent", "결근 · 신입 실수", 10), ("vip", "VIP 긴급 주문", 1),
          ("jam", "도로 정체", 6), ("outage", "시스템 다운", 3), ("surge", "피크 폭주", 8)]
EVENT_NAME = {e[0]: e[1] for e in EVENTS}
DEFAULT_REWARD = {"onTime": 12, "latePerStep": 1, "waitCost": 0.25, "overtimeCost": 2.5, "leftover": 6}
TEST_SEEDS = list(range(90001, 90025))


# ── 자바스크립트와 같은 32비트 난수 ──
def _u32(x):
    return x & 0xFFFFFFFF


def _i32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x


def _imul(a, b):
    return _i32(_u32(a) * _u32(b))


class Rng:
    def __init__(self, seed):
        self.a = _u32(seed)

    def __call__(self):
        self.a = _u32(self.a + 0x6D2B79F5)
        t = self.a
        t = _imul(_i32(t) ^ (_u32(t) >> 15), _i32(t) | 1)
        t = _i32(_i32(t) ^ _i32(t + _imul(_i32(t) ^ (_u32(t) >> 7), _i32(t) | 61)))
        return _u32(_i32(t) ^ (_u32(t) >> 14)) / 4294967296


def _lam(t):
    return WORLD["base"] + WORLD["am"] * math.exp(-(((t - 12) / 5) ** 2)) + WORLD["pm"] * math.exp(-(((t - 40) / 6) ** 2))


class Truck:
    __slots__ = ("arr", "need", "cargo", "due", "vip")

    def __init__(self, arr, need, due, vip=False):
        self.arr, self.need, self.cargo, self.due, self.vip = arr, need, 0, due, vip


def _f32(v):
    return float(np.float32(v))


class DayEnv:
    def __init__(self, reward=None):
        self.reward = dict(DEFAULT_REWARD, **(reward or {}))

    def reset(self, seed):
        self.r = Rng(seed)
        self.t, self.waiting, self.docked, self.staged, self.active, self.held, self.temp = 0, [], [], 4, {}, 0, 0
        self.stats = dict(onTime=0, late=0, left=0, lateSteps=0, overtime=0, pallets=0, events=0, redo=0, temp=0, vipOnTime=0)
        self._arrive()
        self.last = self.observe()
        return self.last

    def on(self, e):
        return self.active.get(e, 0) > 0

    def _arrive(self):
        l = _lam(self.t) * (1.8 if self.on("surge") else 1)
        n = (1 if self.r() < l else 0) + (1 if self.r() < l * 0.35 else 0)
        if self.on("jam"):
            self.held += n
            return
        burst, self.held = self.held, 0
        for _ in range(n + burst):
            need = 2 + math.floor(self.r() * 5)
            due = self.t + WORLD["slack"] + math.floor(self.r() * WORLD["span"])
            self.waiting.append(Truck(self.t, need, due))

    def _trap(self):
        if self.r() > WORLD["trap"]:
            return None
        e, _, length = EVENTS[math.floor(self.r() * len(EVENTS))]
        if e == "vip":
            self.waiting.append(Truck(self.t, 3 + math.floor(self.r() * 3), self.t + 5, True))
        else:
            self.active[e] = length
        self.stats["events"] += 1
        return e

    def observe(self):
        w, d, noise = self.waiting, self.docked, self.on("outage")
        jitter = (lambda v: max(0.0, min(1.0, v + (self.r() - 0.5) * 0.6))) if noise else (lambda v: v)
        min_w = min(x.due - self.t for x in w) if w else 16
        min_d = min(x.due - self.t for x in d) if d else 16
        remain = sum(x.need - x.cargo for x in d)
        late_d = sum(1 for x in d if x.due < self.t)
        left = max([0] + [self.active.get(e[0], 0) for e in EVENTS]) / 10
        vip = any(x.vip for x in w) or any(x.vip for x in d)
        ev = [(1 if vip else 0) if e[0] == "vip" else (1 if self.on(e[0]) else 0) for e in EVENTS]
        obs = [self.t / STEPS, jitter(min(len(w), 6) / 6), jitter((DOCKS - len(d)) / DOCKS), jitter(min(self.staged, 10) / 10),
               jitter((max(-4, min(16, min_w)) + 4) / 20), jitter(min(remain, 16) / 16), jitter((max(-4, min(16, min_d)) + 4) / 20), late_d / DOCKS, *ev, min(1, left)]
        obs = [_f32(v) for v in obs]
        b = lambda v, cuts: sum(1 for c in cuts if v >= c)
        ev_key = "".join(EVENTS[i][0][0] for i, v in enumerate(ev) if v) or "-"
        key = "".join(str(x) for x in [min(5, self.t // 10), min(3, len(w)), min(2, DOCKS - len(d)), b(self.staged, [1, 3, 6]),
                                       b(min_w, [0, 5]) + 1 if w else 0, b(min_d, [0, 4]) + 1 if d else 0]) + ev_key
        return {"obs": obs, "key": key}

    def step(self, a):
        R = self.reward
        r, pallets, departed, redo = 0.0, 0, 0, 0
        prio = lambda x: x.due - 3 if x.vip else x.due

        def dock(pick):
            if self.waiting and len(self.docked) < DOCKS:
                self.docked.append(self.waiting.pop(pick(self.waiting)))
        if a == 1:
            dock(lambda q: min(range(len(q)), key=lambda i: (q[i].arr, i)))
        if a == 2:
            dock(lambda q: min(range(len(q)), key=lambda i: (prio(q[i]), i)))
        supply = WORLD["supply"] - (1 if self.on("rain") else 0)
        if a == 3:
            supply += 3; r -= R["overtimeCost"]; self.stats["overtime"] += 1
        if a == 6:
            self.temp = 6; r -= R["overtimeCost"] * 2; self.stats["temp"] += 1
        if self.temp > 0:
            supply += 1
        self.staged = min(14, self.staged + supply)
        lifts = WORLD["lifts"] - (1 if self.on("breakdown") else 0) + (1 if self.temp > 0 else 0)
        careful = a == 5
        if careful:
            lifts = max(1, lifts - 1)
        order = sorted(self.docked, key=prio if a == 4 else (lambda x: x.arr))
        k = 0
        while k < lifts and self.staged > 0:
            open_ = [x for x in order if x.cargo < x.need]
            if not open_:
                break
            tr = open_[0] if a == 4 else open_[k % max(1, len(open_))]
            tr.cargo += 1; self.staged -= 1; pallets += 1
            if self.on("absent") and not careful and self.r() < 0.35:
                tr.cargo -= 1; redo += 1
            k += 1
        for tr in list(self.docked):
            if tr.cargo >= tr.need:
                late = max(0, self.t - tr.due)
                bonus = R["onTime"] * (2 if tr.vip else 1)
                r += bonus if late == 0 else max(-10, bonus - R["latePerStep"] * late * 2)
                if late == 0:
                    self.stats["onTime"] += 1
                    self.stats["vipOnTime"] += 1 if tr.vip else 0
                else:
                    self.stats["late"] += 1; self.stats["lateSteps"] += late
                self.docked = [x for x in self.docked if x is not tr]
                departed += 1
        r -= R["waitCost"] * len(self.waiting)
        self.stats["redo"] += redo; self.stats["pallets"] += pallets
        for e in EVENTS:
            if self.active.get(e[0]):
                self.active[e[0]] -= 1
        if self.temp > 0:
            self.temp -= 1
        self.t += 1
        done = self.t >= STEPS
        event = None
        if done:
            left = len(self.waiting) + len(self.docked) + self.held
            r -= R["leftover"] * left; self.stats["left"] = left
        else:
            event = self._trap(); self._arrive()
        self.last = self.observe()
        return r, done, {"pallets": pallets, "departed": departed, "event": event, "redo": redo}


def run_day(policy, seed, reward=None):
    """policy(obs, key, env) → 행동 번호. 반환: (하루 보상 합, 걸음별 행동, 통계)"""
    env = DayEnv(reward); o = env.reset(seed); total, acts, done = 0.0, [], False
    while not done:
        a = policy(o["obs"], o["key"], env)
        r, done, _ = env.step(a); total += r; acts.append(a); o = env.last
    return total, acts, env.stats


def evaluate(policy, reward=None, seeds=None):
    seeds = seeds or TEST_SEEDS
    tot, agg = 0.0, {}
    for s in seeds:
        t, _, st = run_day(policy, s, reward)
        tot += t
        for k, v in st.items():
            agg[k] = agg.get(k, 0) + v
    n = len(seeds)
    return {"score": tot / n, "onTimeRate": agg["onTime"] / max(1, agg["onTime"] + agg["late"] + agg["left"]), "perDay": {k: v / n for k, v in agg.items()}}


rule_policy = lambda obs, key, env=None: 1 if obs[1] > 0 and obs[2] > 0 else 0


def _copy_truck(x):
    t = Truck.__new__(Truck)
    t.arr, t.need, t.cargo, t.due, t.vip = x.arr, x.need, x.cargo, x.due, x.vip
    return t


def clone(env):
    """지금 상황을 그대로 복사 (보기마다 다시 돌려 볼 때) · deepcopy보다 몇 배 빠릅니다."""
    c = DayEnv.__new__(DayEnv)
    c.reward, c.t, c.staged, c.held, c.temp = env.reward, env.t, env.staged, env.held, env.temp
    c.waiting = [_copy_truck(x) for x in env.waiting]
    c.docked = [_copy_truck(x) for x in env.docked]
    c.active, c.stats, c.last = dict(env.active), dict(env.stats), env.last
    c.r = Rng(0); c.r.a = env.r.a
    return c
