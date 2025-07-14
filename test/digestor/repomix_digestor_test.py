from core.digestor.repomix_digestor import RepomixDigestor
import multiprocessing

def main():
    digestor = RepomixDigestor()
    result = digestor.digest_repo("https://github.com/moonman369/XMLTransformationFunctionApp")
    print(f"Digest length: {len(result)}")

if __name__ == "__main__":
    # This is the correct idiom for using multiprocessing on Windows
    multiprocessing.freeze_support()
    main()