import os
import shutil
import sys
import time

def print_loading(message, folder_name, interval=0.1):
    """로딩바 출력"""
    symbols = ['|', '/', '-', '\\']
    for symbol in symbols:
        sys.stdout.write(f"\r{message} ({folder_name}) {symbol}")
        sys.stdout.flush()
        time.sleep(interval)

def reorganize_folders(base_path, keep_single_file_folder=True):
    try:
        print(f"작업을 시작합니다: {base_path}")
        
        # 작업 통계
        stats = {
            "processed_files": 0,
            "moved_files": 0,
            "deleted_folders": 0,
            "errors": 0,
        }
        error_logs = []

        for artist_folder in os.listdir(base_path):
            artist_path = os.path.join(base_path, artist_folder)
            if not os.path.isdir(artist_path):
                continue

            print(f"\n작가 폴더 처리 시작: {artist_folder}")

            for item_folder in os.listdir(artist_path):
                item_path = os.path.join(artist_path, item_folder)
                if not os.path.isdir(item_path):
                    continue

                print(f"  품번 폴더 처리 시작: {item_folder}")
                artworks = [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]

                if len(artworks) == 1 and not keep_single_file_folder:
                    single_file = artworks[0]
                    single_file_path = os.path.join(item_path, single_file)
                    new_file_name = f"{item_folder}-{single_file}"
                    new_file_path = os.path.join(artist_path, new_file_name)

                    try:
                        shutil.move(single_file_path, new_file_path)
                        stats["moved_files"] += 1
                    except Exception as e:
                        error_logs.append(f"파일 이동 실패: {single_file} - {e}")
                        stats["errors"] += 1

                    try:
                        os.rmdir(item_path)
                        stats["deleted_folders"] += 1
                    except Exception as e:
                        error_logs.append(f"폴더 삭제 실패: {item_folder} - {e}")
                        stats["errors"] += 1

                else:
                    for artwork in artworks:
                        artwork_path = os.path.join(item_path, artwork)
                        new_artwork_name = f"{item_folder}-{artwork}"
                        new_artwork_path = os.path.join(artist_path, new_artwork_name)

                        counter = 1
                        while os.path.exists(new_artwork_path):
                            new_artwork_name = f"{item_folder}-{os.path.splitext(artwork)[0]}_{counter}{os.path.splitext(artwork)[1]}"
                            new_artwork_path = os.path.join(artist_path, new_artwork_name)
                            counter += 1

                        try:
                            shutil.move(artwork_path, new_artwork_path)
                            stats["moved_files"] += 1
                        except Exception as e:
                            error_logs.append(f"파일 이동 실패: {artwork} - {e}")
                            stats["errors"] += 1

                    try:
                        if not os.listdir(item_path):
                            os.rmdir(item_path)
                            stats["deleted_folders"] += 1
                        else:
                            error_logs.append(f"폴더가 비어 있지 않아 삭제 불가: {item_folder}")
                    except Exception as e:
                        error_logs.append(f"빈 폴더 삭제 실패: {item_folder} - {e}")
                        stats["errors"] += 1
                
                # 로딩바 업데이트
                print_loading("  처리 중", item_folder, interval=0.05)
                sys.stdout.write(f"\r  품번 폴더 처리 완료: {item_folder}\n")

            print(f"작가 폴더 처리 완료: {artist_folder}")

        # 작업 통계 출력
        print("\n작업이 완료되었습니다:")
        print(f"  이동한 파일 수: {stats['moved_files']}")
        print(f"  삭제한 폴더 수: {stats['deleted_folders']}")
        print(f"  오류 발생 수: {stats['errors']}")

        if stats["errors"] > 0:
            print("\n발생한 오류:")
            for error in error_logs:
                print(f"  - {error}")

    except Exception as e:
        print(f"작업 중 예외 발생: {e}")


if __name__ == "__main__":
    base_directory = input("작업할 최상위 폴더 경로를 입력하세요: ").strip()
    if os.path.exists(base_directory) and os.path.isdir(base_directory):
        user_choice = input("파일이 하나인 폴더를 그대로 유지할까요? (Y/N): ").strip().lower()
        keep_single_file = user_choice == "y"
        reorganize_folders(base_directory, keep_single_file_folder=keep_single_file)
    else:
        print(f"유효하지 않은 경로입니다: {base_directory}")
