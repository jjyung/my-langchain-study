# Quick Start

## 環境需求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## 啟動方式

```bash
# 安裝依賴
uv sync

# 執行程式
uv run main.py
```

## 環境變數

複製 `.env.example` 為 `.env` 並填入必要的 API Key（程式啟動時會自動從 `.env` 載入）：

```bash
cp .env.example .env
```
