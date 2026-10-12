import os
import shutil
from pathlib import Path
import getpass

#-------------------------------------------------------------------------------

def get_temp_folders():
    username = getpass.getuser()
    windows_temp = Path(r"C:\Windows\Temp")
    user_temp = Path(rf"C:\Users\{username}\AppData\Local\Temp")
    folders = [windows_temp, user_temp]
    return [f for f in folders if f.exists()]

#-------------------------------------------------------------------------------

def clean_folder(folder):
    deleted = 0
    skipped = 0
    freed_bytes = 0

    for item in folder.iterdir():
        try:
            if item.is_file():
                size = item.stat().st_size
                item.unlink()
                deleted += 1
                freed_bytes += size
            elif item.is_dir():
                shutil.rmtree(item)
                deleted += 1
        except (PermissionError, OSError):
            skipped += 1
            continue

    return deleted, skipped, freed_bytes

#-------------------------------------------------------------------------------

def print_summary(deleted, skipped, freed_bytes):

    freed_mb = freed_bytes / (1024 * 1024)
    print("\n" + "=" * 55)
    print("📊 Cleanup Summary:")
    print(f"   ✅ Deleted files     : {deleted}")
    print(f"   ⏭️ Skipped files     : {skipped}")
    print(f"   💾 Freed size        : {freed_mb:.2f} MB")
    print("=" * 55)

#-------------------------------------------------------------------------------

def main():
    print("🧹 Welcome to Windows temp cleaner.")
    print("=" * 55)

    folders = get_temp_folders()

    if not folders:
        print("❌ The cleanup program cannot find the Temp folder.")
        return

    print("Target folders:")

    for f in folders:
        print(f"   • {f}")
    print(55 * "=")

    answer = input("Are you sure? (If yes, y) >>> ")
    print("=" * 55)
    if answer.strip().lower() != "y":
        print("Cancelled. No files were deleted.👋")
        print("=" * 55)
        return

    total_deleted = 0
    total_skipped = 0
    total_freed = 0

    for folder in folders:
        print(f"\n📂 Cleaning up : {folder}")
        d, s, b = clean_folder(folder)
        total_deleted += d
        total_skipped += s
        total_freed += b

    print_summary(total_deleted, total_skipped, total_freed)
