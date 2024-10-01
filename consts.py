from pathlib import Path
from typing import Literal

input_folder = Path("data/input")


output_folder = Path("data/output")
process = Path("data/process")
missing_folder = Path("data/missing")

outputformat: Literal["csv","excel"] = "excel"