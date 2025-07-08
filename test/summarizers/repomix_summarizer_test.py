from core.summarizer.repomix_summarizer import RepoMixSummarizer
import multiprocessing

def main():
    summarizer = RepoMixSummarizer()
    result = summarizer.summarize_repo("https://github.com/moonman369/Portfolio")
    print(f"Summary length: {len(result)}")

if __name__ == "__main__":
    # This is the correct idiom for using multiprocessing on Windows
    multiprocessing.freeze_support()
    main()