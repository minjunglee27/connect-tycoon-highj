"""학습 실험실 두뇌 (connect-lab-brain/1) · 웹 시뮬레이터에서 내가 파라미터를 정해 강화학습한 두뇌.

    b = LabBrain.from_file("jay-logistics-ppo.json")
    b.act(obs, key)        # 관측 8개(0~1) · 표 모델이면 상황 키 → 행동 번호
"""
import json

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
            self.W = [np.array(w, dtype=np.float32).reshape(m["sizes"][i], m["sizes"][i + 1]) for i, w in enumerate(m["W"])]
            self.b = [np.array(b, dtype=np.float32) for b in m["b"]]

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
        h = np.asarray(obs, dtype=np.float32)
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            h = h @ W + b
            if i < len(self.W) - 1:
                h = np.maximum(h, 0)
        return int(np.argmax(h))
