name: Update Servers & Clash Config

on:
  schedule:
    - cron: "0 */3 * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-servers:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install Dependencies
        run: pip install requests

      - name: Run Python Script
        run: python script.py

      - name: Commit and Push Changes
        run: |
          git config --local user.name "GitHub Actions"
          git config --local user.email "actions@github.com"
          
          git add servers.txt
          
          # فقط اگر config.yaml وجود داشته باشد اضافه کن
          if [ -f "config.yaml" ]; then
            git add config.yaml
          fi
          
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "Update servers & Clash config - $(date '+%Y-%m-%d %H:%M:%S')"
            git push origin HEAD:main
          fi
