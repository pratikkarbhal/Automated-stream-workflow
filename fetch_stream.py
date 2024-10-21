name: Fetch Stream URL

on:
  push:
    branches:
      - main

jobs:
  fetch-url:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9' # Adjust the version as needed

      - name: Install dependencies
        run: |
          pip install pyppeteer

      - name: Run fetch_stream.py
        env:
          NODE_OPTIONS: --no-sandbox
        run: |
          python fetch_stream.py
