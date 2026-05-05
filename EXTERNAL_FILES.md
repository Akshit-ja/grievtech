# External Large Files

This repository had large files removed from git history and stored externally.

Please upload the folder `removed_large_files` (located one level above the repository root) to your cloud storage (Google Drive, S3, etc.) and paste the shareable link below.

- External files link:

  https://drive.google.com/drive/folders/1hNqnpVP-JGB7FHBDEhlus8NEffLqJ8M1?usp=sharing

Notes

```
git lfs install
git lfs track "models/*"
git add .gitattributes
git add path/to/large_file
git commit -m "Add large files via Git LFS"
git push origin main
```

**Using the fetch script**

- Paste your Google Drive folder or file URL(s) into the top of this file under "- External files link:". The script will detect folder links and file links.
- Run the fetch script to download files into `removed_large_files/` (one level above the repo root) or into the path set by the environment variable `EXTERNAL_FILES_DIR`:

```powershell
pip install gdown
python scripts\fetch_external.py
```

- To run your project with the downloaded files, set the environment variable if needed:

```powershell
# optional: change download target
setx EXTERNAL_FILES_DIR "C:\\path\\to\\removed_large_files"
# then run your app
python run_pipeline.py
```

If you prefer not to set the env var, the script and code default to `../removed_large_files`.
