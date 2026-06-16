import subprocess

scripts = [
    "src/web_scraper.py",
    "src/clean_nasa.py",
    "src/refine_noaa.py",
    "src/merge_datasets.py",
    "src/clean_master_dataset.py",
    "src/build_documents.py",
    "src/vector_store.py",
    "src/ask_llama.py"

]

for script in scripts:
    print(f"\n🚀 Running {script}")
    subprocess.run(["python", script])
