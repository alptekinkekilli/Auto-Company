# scripts/ops/ledger-guard.py

- _env_int · function · L43-L48 — def _env_int(name: str, default: int) -> int
- _env_float · function · L51-L55 — def _env_float(name: str, default: float) -> float
- _app · function · L58-L59 — def _app(arg: str | None) -> Path
- _find_ledger · function · L62-L69 — def _find_ledger(app: Path) -> Path | None
- _metrics · function · L72-L84 — def _metrics(path: Path) -> dict | None
- _backup · function · L87-L101 — def _backup(app: Path, cycle: int, path: Path, keep: int) -> None
- _load_state · function · L104-L108 — def _load_state(path: Path) -> dict
- _save_state · function · L111-L118 — def _save_state(path: Path, state: dict) -> None
- _check · function · L121-L146 — def _check(name: str, cur: dict | None, prev: dict | None, drop_sections: int, drop_rows: int, drop_frac: float) -> str | None
- main · function · L149-L212 — def main() -> int
