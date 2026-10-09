import filecmp
import shutil
import sys


def main(argv=None):
    sys.stdout.write(
        "Comparing model_prices_and_context_window and waypoint/model_prices_and_context_window_backup.json files... checking if they match."
        + "\n"
    )

    file1 = "model_prices_and_context_window.json"
    file2 = "waypoint/model_prices_and_context_window_backup.json"

    cmp_result = filecmp.cmp(file1, file2, shallow=False)

    if cmp_result:
        sys.stdout.write(f"Passed! Files {file1} and {file2} match." + "\n")
        return 0
    else:
        sys.stdout.write(
            f"Failed! Files {file1} and {file2} do not match. Copying content from {file1} to {file2}." + "\n"
        )
        copy_content(file1, file2)
        return 1


def copy_content(source, destination):
    shutil.copy2(source, destination)


if __name__ == "__main__":
    sys.exit(main())
