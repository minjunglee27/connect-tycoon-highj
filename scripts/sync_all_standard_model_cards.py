import os
from huggingface_hub import HfApi

MODELS_MAP = {
    "minjunglee27/connectailab-rl-highj-goto-v1-link01": "model_cards/goto-v1-link01/README.md",
    "minjunglee27/connectailab-rl-highj-choose-v1-link01": "model_cards/choose-v1-link01/README.md",
    "minjunglee27/connectailab-rl-highj-avoid-v1-link01": "model_cards/avoid-v1-link01/README.md",
    "minjunglee27/connectailab-rl-highj-v1": "model_cards/v1/README.md",
    "minjunglee27/connectailab-rl-highj-v2": "model_cards/v2/README.md",
    "minjunglee27/connectailab-rl-highj-teacher": "model_cards/teacher/README.md",
    "minjunglee27/connectailab-rl-highj-v2-teacher": "model_cards/v2-teacher/README.md",
}

def main():
    api = HfApi()
    print("Starting Hugging Face sync for all 7 standard model cards...")
    for repo_id, path in MODELS_MAP.items():
        if not os.path.exists(path):
            print(f"Skipping {repo_id}: {path} not found.")
            continue
        print(f"Uploading {path} to {repo_id}...")
        api.upload_file(
            path_or_fileobj=path,
            path_in_repo="README.md",
            repo_id=repo_id,
            commit_message="docs: standardize author bio and research collection links with full repo names",
        )
        print(f"Successfully uploaded {repo_id}!")
    print("All 7 models synced successfully to Hugging Face!")

if __name__ == "__main__":
    main()
