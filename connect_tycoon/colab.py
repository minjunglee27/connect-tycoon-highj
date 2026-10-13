"""Colab에서 brain.json 찾기 · 파일 선택 버튼(files.upload)은 브라우저 설정에 따라 안 보이거나 멈추는 경우가 있어,
왼쪽 📁 파일 창에 끌어다 놓은 파일을 먼저 찾습니다."""
import glob
import os


class BrainNotFound(Exception):
    pass


HOW = ("brain.json을 찾지 못했습니다.\n"
       "  1) Colab 왼쪽 세로 막대의 📁(파일) 아이콘을 누릅니다\n"
       "  2) 게임에서 저장한 brain.json(다운로드 폴더의 회사이름-v2.json 같은 파일)을 그 창에 끌어다 놓습니다\n"
       "  3) 이 셀을 다시 실행합니다 (▶)\n"
       "  * 런타임을 다시 시작하면 올린 파일이 지워지니, 그때는 다시 끌어다 놓으세요")


def find_brain(folder="/content", upload_button=False):
    """1) 📁 파일 창에 올린 brain.json (가장 최근 것)  2) upload_button=True면 파일 선택 버튼  3) 없으면 방법을 알려 주고 멈춤."""
    import connect_tycoon as ct
    found = []
    for p in sorted(glob.glob(os.path.join(folder, "*.json")), key=os.path.getmtime, reverse=True):
        try:
            ct.CompanyBrain.from_file(p)
            found.append(p)
        except Exception:
            continue
    if found:
        print("찾은 brain.json ·", os.path.basename(found[0]) + (f" (다른 후보 {len(found) - 1}개는 무시)" if len(found) > 1 else ""))
        return found[0]
    if upload_button:
        print("파일 선택 버튼을 띄웁니다. 버튼이 안 보이거나 멈추면, 이 셀을 멈추고(■) 📁 파일 창에 끌어다 놓는 방법을 쓰세요.")
        from google.colab import files
        up = files.upload()
        if up:
            return os.path.join(os.getcwd(), next(iter(up)))
    raise BrainNotFound(HOW)
