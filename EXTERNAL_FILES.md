# External Large Files

This repository had large files removed from git history and stored externally.

Please upload the folder `removed_large_files` (located one level above the repository root) to your cloud storage (Google Drive, S3, etc.) and paste the shareable link below.

- External files link:

  (paste your shareable link here)

Notes
- Do not commit the large files back into the repo without using Git LFS.
- To track and commit large files with Git LFS, run:

```
git lfs install
git lfs track "models/*"
git add .gitattributes
git add path/to/large_file
git commit -m "Add large files via Git LFS"
git push origin main
```
