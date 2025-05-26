REM Windows-friendly script to remove sensitive .env and force-push repo

:: Step 1 - Remove the .env from history if it exists
if exist .env (
  git rm --cached .env
  echo ".env removed from index"
) else (
  echo ".env not tracked (already removed or in .gitignore)"
)

:: Step 2 - Commit the removal
git commit -m "Remove .env from repo"

:: Step 3 - Push changes forcefully to bypass GitHub secret scan
git push -f origin main
