from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

RUNTIME_CONFIG_FILENAME = ".agents-sync.runtime.json"
RUNTIME_CONFIG_VERSION = 1


class RuntimeConfigError(RuntimeError):
    """Erro ao ler ou validar a configuracao de ambiente local."""


class RuntimeProbeError(RuntimeError):
    """Erro ao validar dependencias de runtime."""


@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    version: int
    github_enabled: bool
    playwright_enabled: bool
    chrome_devtools_enabled: bool
    install_playwright_browsers: bool
    chrome_channel: str
    chrome_executable_path: str | None


@dataclass(frozen=True, slots=True)
class RuntimeIssue:
    tool: str
    message: str
    detail: str


@dataclass(frozen=True, slots=True)
class RuntimeReport:
    config: RuntimeConfig
    issues: tuple[RuntimeIssue, ...]

    def has_errors(self) -> bool:
        return len(self.issues) > 0


def runtime_config_path_for(project_root: Path) -> Path:
    return project_root / RUNTIME_CONFIG_FILENAME


def default_runtime_config() -> RuntimeConfig:
    return RuntimeConfig(
        version=RUNTIME_CONFIG_VERSION,
        github_enabled=True,
        playwright_enabled=True,
        chrome_devtools_enabled=True,
        install_playwright_browsers=False,
        chrome_channel="stable",
        chrome_executable_path=None,
    )


def runtime_config_to_dict(config: RuntimeConfig) -> dict[str, Any]:
    return {
        "version": config.version,
        "github_enabled": config.github_enabled,
        "playwright_enabled": config.playwright_enabled,
        "chrome_devtools_enabled": config.chrome_devtools_enabled,
        "install_playwright_browsers": config.install_playwright_browsers,
        "chrome_channel": config.chrome_channel,
        "chrome_executable_path": config.chrome_executable_path,
    }


def runtime_config_from_dict(payload: dict[str, Any]) -> RuntimeConfig:
    version = payload.get("version")
    if version != RUNTIME_CONFIG_VERSION:
        raise RuntimeConfigError(f"Versao de runtime nao suportada: {version!r}")

    github_enabled = payload.get("github_enabled")
    playwright_enabled = payload.get("playwright_enabled")
    chrome_devtools_enabled = payload.get("chrome_devtools_enabled")
    install_playwright_browsers = payload.get("install_playwright_browsers")
    chrome_channel = payload.get("chrome_channel")
    chrome_executable_path = payload.get("chrome_executable_path")

    if not isinstance(github_enabled, bool):
        raise RuntimeConfigError("Runtime invalido: github_enabled ausente")
    if not isinstance(playwright_enabled, bool):
        raise RuntimeConfigError("Runtime invalido: playwright_enabled ausente")
    if not isinstance(chrome_devtools_enabled, bool):
        raise RuntimeConfigError("Runtime invalido: chrome_devtools_enabled ausente")
    if not isinstance(install_playwright_browsers, bool):
        raise RuntimeConfigError("Runtime invalido: install_playwright_browsers ausente")
    if not isinstance(chrome_channel, str) or not chrome_channel:
        raise RuntimeConfigError("Runtime invalido: chrome_channel ausente")
    if chrome_executable_path is not None and not isinstance(chrome_executable_path, str):
        raise RuntimeConfigError("Runtime invalido: chrome_executable_path invalido")

    return RuntimeConfig(
        version=RUNTIME_CONFIG_VERSION,
        github_enabled=github_enabled,
        playwright_enabled=playwright_enabled,
        chrome_devtools_enabled=chrome_devtools_enabled,
        install_playwright_browsers=install_playwright_browsers,
        chrome_channel=chrome_channel,
        chrome_executable_path=chrome_executable_path,
    )


def load_runtime_config(project_root: Path) -> RuntimeConfig:
    path = runtime_config_path_for(project_root)
    if not path.exists():
        return default_runtime_config()

    content = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeConfigError(f"JSON invalido em {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise RuntimeConfigError(f"Runtime invalido em {path}: esperava um objeto JSON")

    return runtime_config_from_dict(payload)


def write_runtime_config(project_root: Path, config: RuntimeConfig) -> None:
    path = runtime_config_path_for(project_root)
    payload = runtime_config_to_dict(config)
    rendered = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    path.write_text(rendered, encoding="utf-8")


def create_runtime_config(install_playwright_browsers: bool) -> RuntimeConfig:
    chrome_executable_path = detect_chrome_executable_path()
    if chrome_executable_path is None and install_playwright_browsers:
        install_playwright_chromium()
        chrome_executable_path = detect_chrome_executable_path()

    return replace(
        default_runtime_config(),
        install_playwright_browsers=install_playwright_browsers,
        chrome_executable_path=chrome_executable_path,
    )


def probe_runtime(config: RuntimeConfig) -> RuntimeReport:
    issues: list[RuntimeIssue] = []

    if config.github_enabled:
        probe_github(issues)
    if config.playwright_enabled:
        probe_playwright(issues)
    if config.chrome_devtools_enabled:
        probe_chrome_devtools(config, issues)

    return RuntimeReport(
        config=config,
        issues=tuple(issues),
    )


def ensure_runtime_ready(project_root: Path) -> RuntimeReport:
    config = load_runtime_config(project_root)
    report = probe_runtime(config)
    if report.has_errors():
        raise RuntimeProbeError(render_runtime_report(report))
    return report


def render_runtime_report(report: RuntimeReport) -> str:
    lines = [
        "Ambiente de runtime com pendencias:",
        f"- github_enabled={report.config.github_enabled}",
        f"- playwright_enabled={report.config.playwright_enabled}",
        f"- chrome_devtools_enabled={report.config.chrome_devtools_enabled}",
        f"- install_playwright_browsers={report.config.install_playwright_browsers}",
        f"- chrome_channel={report.config.chrome_channel}",
        f"- chrome_executable_path={report.config.chrome_executable_path or 'ausente'}",
    ]
    for issue in report.issues:
        lines.append(f"- [{issue.tool}] {issue.message}: {issue.detail}")
    lines.append(
        "Execute 'glpi-agents-sync setup' na raiz do plugin para gerar a configuracao local."
    )
    return "\n".join(lines)


def build_export_script(report: RuntimeReport) -> str:
    lines: list[str] = []
    if report.config.github_enabled:
        lines.append('export GITHUB_TOKEN="$(gh auth token)"')
        lines.append('export GH_TOKEN="$GITHUB_TOKEN"')
    if report.config.chrome_executable_path is not None:
        lines.append(
            f'export PLAYWRIGHT_CHROME_EXECUTABLE_PATH="{report.config.chrome_executable_path}"'
        )
        lines.append(
            f'export CHROME_DEVTOOLS_EXECUTABLE_PATH="{report.config.chrome_executable_path}"'
        )
    return "\n".join(lines)


def probe_github(issues: list[RuntimeIssue]) -> None:
    if shutil.which("gh") is None:
        issues.append(
            RuntimeIssue(
                tool="github",
                message="gh nao encontrado",
                detail="Instale o GitHub CLI para validar autenticacao e usar os fluxos do framework.",
            )
        )
        return

    has_token_env = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if has_token_env:
        return

    command = ["gh", "auth", "status"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        issues.append(
            RuntimeIssue(
                tool="github",
                message="gh sem autenticacao valida",
                detail=completed.stderr.strip() or completed.stdout.strip(),
            )
        )
        return


def probe_playwright(issues: list[RuntimeIssue]) -> None:
    if shutil.which("node") is None:
        issues.append(
            RuntimeIssue(
                tool="playwright",
                message="node nao encontrado",
                detail="Instale Node.js para executar '@playwright/mcp' e instalar browsers.",
            )
        )
        return

    if shutil.which("npx") is None:
        issues.append(
            RuntimeIssue(
                tool="playwright",
                message="npx nao encontrado",
                detail="Instale Node.js com npm para executar os MCPs via npx.",
            )
        )
        return

    completed = subprocess.run(
        ["npx", "--yes", "@playwright/mcp@latest", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        issues.append(
            RuntimeIssue(
                tool="playwright",
                message="Playwright MCP indisponivel",
                detail=completed.stderr.strip() or completed.stdout.strip(),
            )
        )


def probe_chrome_devtools(config: RuntimeConfig, issues: list[RuntimeIssue]) -> None:
    if shutil.which("npx") is None:
        issues.append(
            RuntimeIssue(
                tool="chrome-devtools",
                message="npx nao encontrado",
                detail="Instale Node.js com npm para executar chrome-devtools-mcp.",
            )
        )
        return

    completed = subprocess.run(
        ["npx", "--yes", "chrome-devtools-mcp@latest", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        issues.append(
            RuntimeIssue(
                tool="chrome-devtools",
                message="chrome-devtools-mcp indisponivel",
                detail=completed.stderr.strip() or completed.stdout.strip(),
            )
        )
        return

    chrome_executable_path = config.chrome_executable_path or detect_chrome_executable_path()
    if chrome_executable_path is None:
        issues.append(
            RuntimeIssue(
                tool="chrome-devtools",
                message="Chrome nao encontrado",
                detail=(
                    "Nenhum Chromium/Chrome local foi encontrado. Execute 'glpi-agents-sync "
                    "setup --install-playwright-browsers' ou configure chrome_executable_path."
                ),
            )
        )
        return


def detect_chrome_executable_path() -> str | None:
    system_candidates = (
        "chromium",
        "chromium-browser",
        "google-chrome",
        "google-chrome-stable",
        "chrome",
    )
    for candidate in system_candidates:
        resolved = shutil.which(candidate)
        if resolved is not None:
            return resolved

    cache_root = Path.home() / ".cache" / "ms-playwright"
    if cache_root.exists():
        browser_dirs = sorted(
            [path for path in cache_root.iterdir() if path.is_dir()],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        for browser_dir in browser_dirs:
            executable = _detect_cached_browser_executable(browser_dir)
            if executable is not None:
                return str(executable)

    return None


def _detect_cached_browser_executable(browser_dir: Path) -> Path | None:
    candidates = (
        browser_dir / "chrome-linux64" / "chrome",
        browser_dir / "chrome-linux" / "chrome",
        browser_dir / "chrome-mac" / "Chromium.app" / "Contents" / "MacOS" / "Chromium",
        browser_dir / "chrome-win" / "chrome.exe",
    )
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate
    return None


def install_playwright_chromium() -> None:
    command = ["npx", "--yes", "playwright@latest", "install", "chromium"]
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeProbeError(
            "Falha ao instalar Chromium via Playwright: "
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )
