import subprocess
import sys
from pathlib import Path

def run_script(script_path):
    result = subprocess.run([sys.executable, str(script_path)])
    if result.returncode != 0:
        sys.exit(1)

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    src_dir = base_dir / "src"
    
    run_script(src_dir / "generate_data.py")
    run_script(src_dir / "analysis.py")
    run_script(src_dir / "visualization.py")
    
    print("Data generation, analysis, and visualization completed successfully.")
