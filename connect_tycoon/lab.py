"""학습 실험실 두뇌 (connect-lab-brain/1) · 웹 시뮬레이터에서 내가 파라미터를 정해 강화학습한 두뇌.

    b = LabBrain.from_file("jay-logistics-ppo.json")
    b.act(obs, key)        # 관측 16개(0~1) · 표 모델이면 상황 키 → 행동 번호
    labenv.evaluate(b.policy())   # 웹과 똑같은 시험 24일
"""
import json
import os

import numpy as np

FORMAT = "connect-lab-brain/1"
ALGO_NAME = {"q": "Q러닝 (표)", "dqn": "DQN (신경망 + 경험 재생 + 타깃망)", "ppo": "PPO (행동가-비평가 + 클리핑)"}


def is_lab(path_or_dict):
    d = path_or_dict
    if isinstance(d, str):
        try:
            with open(d, encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            return False
    return isinstance(d, dict) and d.get("format") == FORMAT


class LabBrain:
    def __init__(self, spec):
        if spec.get("format") != FORMAT:
            raise ValueError("학습 실험실 두뇌(connect-lab-brain/1)가 아닙니다")
        self.spec = spec
        m = spec["model"]
        self.kind = m["type"]
        if self.kind == "mlp":
            self.W = [np.array(w, dtype=np.float32).astype(np.float64).reshape(m["sizes"][i], m["sizes"][i + 1]) for i, w in enumerate(m["W"])]
            self.b = [np.array(b, dtype=np.float32).astype(np.float64) for b in m["b"]]

    @classmethod
    def from_file(cls, path):
        with open(path, encoding="utf-8") as f:
            return cls(json.load(f))

    name = property(lambda self: self.spec.get("name", "lab-brain"))
    algo = property(lambda self: self.spec.get("algo"))
    test = property(lambda self: self.spec.get("test", {}))

    def act(self, obs=None, key=None):
        if self.kind == "q-table":
            q = self.spec["model"]["table"].get(key or "")
            return int(np.argmax(q)) if q else 1
        # 웹과 똑같이 · 가중치는 float32 값, 계산은 float64, 층마다 float32로 반올림
        h = np.asarray(obs, dtype=np.float32).astype(np.float64)
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            h = h @ W + b
            if i < len(self.W) - 1:
                h = np.maximum(h, 0)
            h = h.astype(np.float32).astype(np.float64)
        return int(np.argmax(h))

    def policy(self):
        """labenv.run_day · evaluate에 그대로 넣는 함수"""
        return lambda obs, key, env=None: self.act(obs, key)


def example():
    """예시 두뇌 · 웹 실험실 기본값(PPO · 500일)으로 키운 두뇌 (시험 24일 하루 279점 · 규칙 사장 86점). 내 brain.json이 없을 때 써 봅니다."""
    return LabBrain.from_file(os.path.join(os.path.dirname(__file__), "data", "lab", "example-ppo.json"))
