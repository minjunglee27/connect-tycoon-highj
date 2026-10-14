# Model Card Standard & Researcher Attribution Rules

## 1. Naming & Case Convention (명명 규칙)
* **저장소 ID / 코드 / URL**: 반드시 **소문자 (`highj`)** 유지
  - 예: `minjunglee27/connectailab-rl-highj-v1`
  - 이유: 리눅스/파이썬 라이브러리 및 웹 URL 호환성 보장
* **연구원 소속 및 본명 표기**:
  - 표준 포맷: `CONNECT AI LAB 소속 연구원 Minjung Lee (Highj)`
  - 본명: Minjung Lee (영문 본명)
  - 활동명: Highj

## 2. Standard Header & Intro Format (모델 카드 제목 및 서두 규격)
* **H1 제목 규격**:
  - 모델 고유 저장소 ID 사용 (예: `# connectailab-rl-highj-{version}`)
* **만든 사람 시그니처 블록 (고정 유지, 불릿 목록 규격)**:
## 만든 사람 · Minjung Lee (Highj)

- CONNECT AI LAB 소속 연구원 및 개발자
- 로컬 AI, 피지컬 AI, Micro SaaS를 탐구하고 직접 개발해보며, 기술을 실제 비즈니스로 연결해 나가는 **AI 1인 기업가**입니다.
* **모델 소개 표준 도입부 (시뮬레이터 학습 및 Jay 멘토 명시)**:
CONNECT AI LAB의 **Jay 멘토님**이 제작한 가상 비즈니스 시뮬레이터 환경을 바탕으로, 공개 데이터와 강화학습(RL)을 활용해 **에이전트 자율 의사결정 원리를 공부하고 구현해 본 {version} 모델**입니다.  
회사의 6대 핵심 영역(인력·재고·마케팅·CS·환불·FDS 보안)에서 상황을 읽고 스스로 판단하는 실험을 진행했습니다.  
(※ 가상 시뮬레이터 환경에서 학습된 모델로, 실제 사업 환경에 바로 적용하는 모델은 아닙니다.)

## 3. Evaluation Table Convention (성적표 모델명 규격)
* **성적표 표 안의 모델 행**: 소속 연구실(`connectailab`)과 본인 식별자(`highj`), 버전(`v{N}`)이 모두 포함된 **정식 모델 전체명**을 직접 명시 (방법 B 스타일 적용).
  - 예: `| **connectailab-rl-highj-{version}** | ... |`
  - 세부 분석 제목: `* **세부 검증 결과 (connectailab-rl-highj-{version})**:`

## 4. Colab Results Processing Workflow (코랩 결과 처리 및 부연설명 규칙)
사용자가 코랩 결과(딕셔너리 수치 등)를 가져오면 항상 아래 규격으로 자동 파싱하여 표와 상세 부연설명을 작성한다:
1. **성적표 비교 테이블 생성**:
   - `Qwen 학습 전 (Base)` vs `지도학습 (SFT)` vs `**connectailab-rl-highj-v{N}**`
   - 컬럼: 시험 문제 정답률 | 후회 (작을수록 좋음) | 시뮬레이터 한 달 이익 | 실제 카드 거래 · 손실 줄임
2. **상세 부연설명 (글머리 기호) 필수 포함**:
   - **🏢 시뮬레이터 경영 검증**: 운영 개월 수, 월평균 영업이익(흑자/수익률), 고객 만족도(`sat: XX%`), 월 리스크/보안 사고 건수(`incidents: XX건`)
   - **💳 실제 카드 이상 거래(FDS) 백테스트**: 총 검증 케이스, 실제 부정/사기 결제 건수, 적발 건수(`caught`) 및 적발률, 금전 손실 방어율(`saved: XX%`)
   - **👨‍🏫 선생님 정책 대비 성장 인사이트**: PPO 전용 기준 모델(`teacher_profit`) 대비 성장 폭 및 비즈니스적 시사점 해설
3. **로컬 파일 아카이빙**:
   - `model_cards/v{N}/metrics.json`: 원본 수치 JSON 영구 보존
   - `model_cards/v{N}/brain.json`: 훈련에 사용된 선생님 강화학습 정책 파일(brain.json) 영구 보관
   - `model_cards/v{N}/README.md`: 완성된 모델 카드 저장
   - `model_cards/README.md`: 전체 버전 히스토리 테이블 자동 업데이트
4. **허깅페이스 실시간 동기화**:
   - `minjunglee27/connectailab-rl-highj-v{N}`의 `README.md`로 즉시 커밋 & 푸시
5. **깃허브 자동 커밋 & 푸시 (Automatic Git Push)**:
   - 새로운 버전(v2, v3...), 브레인 백업, 문서 수정 등 유의미한 작업이 완료될 때마다 자동으로 커밋하고 `origin main` (`minjunglee27/connect-tycoon-highj`)으로 즉시 `git push`를 수행한다.

## 5. Template & Section Policy
* **기본 템플릿**: `connectailab-rl-highj-teacher`의 원본 구조 및 레이아웃을 엄격히 준수.
* **하단 출처 (`## 만든 곳`)**: 원본 템플릿의 링크, 텍스트, 디스클레이머(면책조항)를 **100% 원형 그대로 보존**.
* **용어 정책**: 임의의 "공동연구" 섹션이나 단어를 추가하지 않고, 공식 연구원 소속(`CONNECT AI LAB 소속 연구원`)으로 일관되게 표현.
* **사용법 (`## 쓰는 법`)**: `peft_model_id`에 해당 버전의 소문자 저장소 ID 지정.
