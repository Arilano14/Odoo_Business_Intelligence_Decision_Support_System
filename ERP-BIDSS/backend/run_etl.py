import os
import sys

# Add app to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from etl.pipeline import run_pipeline

def main():
    run_pipeline()

if __name__ == "__main__":
    main()
