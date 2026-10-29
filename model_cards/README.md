# Highj Decision Models - Version History

CONNECT TYCOON & Qwen 강화학습 의사결정 모델 버전별 기록 저장소입니다.  
* Minjung Lee (Highj) · CONNECT AI LAB

| 버전 | 일자 | 월평균 이익 | 고객 만족도 | FDS 사기 손실 방어 | Hugging Face 저장소 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| [**Teacher Baseline**](./teacher/README.md) | 2026-10-13 | **1,221.2만원** | 96.8% | 72.0% (146/177건 방어) | [minjunglee27/connectailab-rl-highj-teacher](https://huggingface.co/minjunglee27/connectailab-rl-highj-teacher) |
| [**Highj v1**](./v1/README.md) | 2026-10-14 | **+362.2만원** (흑자) | 96.5% | 37.3% (91/177건 방어) | [minjunglee27/connectailab-rl-highj-v1](https://huggingface.co/minjunglee27/connectailab-rl-highj-v1) |
| [**Teacher v2**](./v2-teacher/README.md) | 2026-10-15 | **1,176.0만원** | 95.0% | 실전 40개월 고도화 두뇌 (품절일 0.6일) | [minjunglee27/connectailab-rl-highj-v2-teacher](https://huggingface.co/minjunglee27/connectailab-rl-highj-v2-teacher) |
| [**Highj v2**](./v2/README.md) | 2026-10-15 | **+679.0만원** (흑자) | 97.0% | 70.6% (145/177건 방어) | [minjunglee27/connectailab-rl-highj-v2](https://huggingface.co/minjunglee27/connectailab-rl-highj-v2) |
| [**LINK-01 goto v1**](./goto-v1-link01/README.md) | 2026-10-30 | **코스 완주 55%** | 68.3% (두뇌 일치율) | 4족 보행 로봇 장애물 회피 자율주행 (목표로 가기) | [minjunglee27/connectailab-rl-highj-goto-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-goto-v1-link01) |
| [**LINK-01 choose v1**](./choose-v1-link01/README.md) | 2026-10-30 | **20판 성공률 100%** | 100.0% (두뇌 일치율) | 4족 보행 로봇 단서 기반 사물 선택 의사결정 (오선택 0건) | [minjunglee27/connectailab-rl-highj-choose-v1-link01](https://huggingface.co/minjunglee27/connectailab-rl-highj-choose-v1-link01) |

---
*각 모델의 학습 파라미터와 평가 수치는 해당 버전 디렉터리 내 `metrics.json` 및 `README.md`에 아카이빙됩니다.*
