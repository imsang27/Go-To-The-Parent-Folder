import os
import shutil

def reorganize_folders(base_path: str) -> None:
    """
    This function reorganizes the folder structure under the given base path.
    It moves artwork files from subfolders to the parent folder, appending the item folder name to the file name.
    It also deletes any empty folders after the reorganization.

    Parameters:
      base_path (str):
        The base path under which the folder structure needs to be reorganized.

    Returns:
      None
    """
    
    try:
        print(f"작업을 시작합니다: {base_path}")
        for artist_folder in os.listdir(base_path):
            artist_path = os.path.join(base_path, artist_folder)
            if not os.path.isdir(artist_path):
                continue

            print(f"작가 폴더 처리 중: {artist_path}")
            for item_folder in os.listdir(artist_path):
                item_path = os.path.join(artist_path, item_folder)
                if not os.path.isdir(item_path):
                    continue

                print(f"  품번 폴더 처리 중: {item_path}")
                for artwork in os.listdir(item_path):
                    artwork_path = os.path.join(item_path, artwork)
                    if not os.path.isfile(artwork_path):
                        print(f"    파일이 아님: {artwork_path}")
                        continue

                    # 파일 이동
                    new_artwork_name = f"{item_folder}-{artwork}"
                    new_artwork_path = os.path.join(artist_path, new_artwork_name)
                    
                    # 중복이 있다면
                    counter = 1
                    while os.path.exists(new_artwork_path):
                        new_artwork_name = f"{item_folder}-{os.path.splitext(artwork)[0]}_{counter}{os.path.splitext(artwork)[1]}"  # 뒤에 번호 추가
                        new_artwork_path = os.path.join(artist_path, new_artwork_name)
                        counter += 1

                    try:
                        shutil.move(artwork_path, new_artwork_path)
                        print(f"    이동 완료: {artwork_path} → {new_artwork_path}")
                    except Exception as e:
                        print(f"    파일 이동 실패: {artwork_path} - {e}")

                # 빈 폴더 삭제
                try:
                    if not os.listdir(item_path):
                        os.rmdir(item_path)
                        print(f"  빈 폴더 삭제 완료: {item_path}")
                    else:
                        print(f"  폴더가 비어 있지 않아 삭제 불가: {item_path}")
                except Exception as e:
                    print(f"  빈 폴더 삭제 실패: {item_path} - {e}")

        print(f"모든 작업이 완료되었습니다: {base_path}")

    except Exception as e:
        print(f"작업 중 예외 발생: {e}")



if __name__ == "__main__":
    base_directory = input("작업할 최상위 폴더 경로를 입력하세요: ").strip()
    if os.path.exists(base_directory) and os.path.isdir(base_directory):
        reorganize_folders(base_directory)
    else:
        print(f"유효하지 않은 경로입니다: {base_directory}")
