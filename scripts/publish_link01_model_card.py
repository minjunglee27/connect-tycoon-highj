#!/usr/bin/env python3
"""
publish_link01_model_card.py
minjunglee27/connectailab-rl-highj-v1-link01 허깅페이스 모델 카드 업로드 스크립트
"""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi

REPO_ID = "minjunglee27/connectailab-rl-highj-v1-link01"
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_CARD_PATH = BASE_DIR / "model_cards" / "link01-v1" / "README.md"
TOKEN_PATH = Path.home() / ".cache" / "huggingface" / "token"

def main():
    token = os.environ.get("HF_TOKEN")
    if not token and TOKEN_PATH.exists():
        token = TOKEN_PATH.read_text().strip()
    
    if not token:
        print("❌ HF_TOKEN 환경변수나 ~/.cache/huggingface/token 파일이 필요합니다.")
        sys.exit(1)
        
    if not MODEL_CARD_PATH.exists():
        print(f"❌ 모델 카드 파일을 찾을 수 없습니다: {MODEL_CARD_PATH}")
        sys.exit(1)

    print(f"🚀 {REPO_ID} 로 모델 카드 업로드를 시작합니다...")
    api = HfApi(token=token)
    api.upload_file(
        path_or_fileobj=str(MODEL_CARD_PATH),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        commit_message="docs: update model card from connect-tycoon repo"
    )
    print(f"🎉 성공적으로 반영되었습니다: https://huggingface.co/{REPO_ID}")

if __name__ == "__main__":
    main()

