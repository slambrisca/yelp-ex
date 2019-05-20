import sys
import tarfile

def main():
    check_arguments()
    tarfile_path = get_filepath()

    tar_object = tarfile.open(tarfile_path)
    for file in tar_object.getmembers():
        print(file)

    print("Hello!")


def check_arguments():
    if len(sys.argv) < 2:
        print("ERROR: Expected tarfile path to be open")
        exit(1)


def get_filepath():
    return sys.argv[1]


if __name__ == "__main__":
    main()