# Project Guidelines

## Overview

easytrader is a Chinese stock trading automation library. It supports:
- Windows desktop client brokers via pywinauto GUI automation (同花顺-based)
- Xueqiu (雪球) web portfolio trading via REST API
- MiniQMT (迅投) official quant SDK integration
- Strategy following from JoinQuant / RiceQuant / Xueqiu
- Remote client-server execution via Flask

## Architecture

**Entry points**: `easytrader.use(broker)` and `easytrader.follower(platform)` — factory functions in `easytrader/api.py`.

**Three parallel branches**:

| Branch | Base class | Purpose |
|--------|-----------|---------|
| Desktop GUI | `ClientTrader` → broker subclasses | pywinauto-driven Windows client automation |
| Web/API | `WebTrader` → `XueQiuTrader`, `MiniqmtTrader` | HTTP/SDK-based trading |
| Followers | `BaseFollower` → platform subclasses | Mirror strategies from quant platforms |

**Remote**: `server.py` (Flask) + `remoteclient.py` enables controlling a Windows trader remotely.

**Config**: `easytrader/config/client.py` holds broker-specific UI control IDs. JSON configs in `easytrader/config/` store API URLs.

## Code Style

- **Formatter**: `black -l 79` (79-char line limit)
- **Import sorting**: `isort`
- **Linter**: `pylint`
- **Type checking**: `mypy` (with `ignore_missing_imports = True`)
- **Language**: Comments, error messages, log messages, and docstrings are in **Chinese**. Follow this convention.
- Type hints are used sparingly (mainly in newer code like `miniqmt/`). Match the style of the surrounding code.

## Build and Test

```bash
# Install
pipenv install

# Run tests (only xq_follower and xqtrader tests are runnable without Windows + broker)
make test                  # or: pipenv run test → pytest -vx --cov=easytrader tests

# Lint & format
pipenv run lint            # pylint
pipenv run format          # black -l 79
pipenv run sort_imports    # isort
pipenv run type_check      # mypy
```

Tests use `unittest` (run via pytest). Desktop client tests require Windows + live broker sessions and are gated by `@unittest.skipUnless` with `EZ_TEST_CLIENTS` env var.

## Conventions

- **Factory dispatch** in `api.py` — broker modules are lazily imported inside `if` branches, not registered via a plugin system.
- **ABC + strategy pattern**: `IGridStrategy`, `IRefreshStrategy` abstract bases with swappable implementations for grid reading and data refresh.
- **Logging**: Single shared logger `logging.getLogger("easytrader")` — do not create module-level loggers.
- **Exceptions**: Use `TradeError` and `NotLoginError` from `easytrader/exceptions.py`.
- **Perf timing**: `@perf_clock` decorator from `easytrader/utils/perf.py` for performance-critical operations.
- **Session keepalive**: `WebTrader` uses a daemon heartbeat thread.

## Platform Pitfalls

- `ClientTrader`, `grid_strategies.py`, `refresh_strategies.py`, `pop_dialog_handler.py` require **pywinauto** and Win32 — non-functional on macOS/Linux. Guard platform-specific imports appropriately.
- `xtquant` (miniqmt dependency) is a proprietary SDK installed from the QMT terminal, not from PyPI.
- `pywinauto` is pinned to `==0.6.6` — do not upgrade without testing.
