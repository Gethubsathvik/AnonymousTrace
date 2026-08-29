"""CLI entry point for AnonymousTrace."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import tempfile
import webbrowser
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table

from anonymoustrace.features.scanning.http_client import HTTPClient
from anonymoustrace.features.scanning.registry_loader import RegistryLoader
from anonymoustrace.models import ConfidenceLevel, ScanResult
from anonymoustrace.services.export_service import ExportService
from anonymoustrace.services.proxy_service import ProxyService, TorService
from anonymoustrace.services.scan_service import ScanService

console = Console(legacy_windows=(sys.platform == "win32"))

__version__ = "0.1.0"

FLAKY_SITES = {
    "AskFM",
    "labpentestit",
    "TikTok",
    "Rumble",
    "Imgur",
    "TryHackMe",
    "HackerNews",
    "Lemmy",
}

BANNER = """[bold green]
 █████╗ ███╗   ██╗ ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ██╗   ██╗████╗   ████╗███████╗
██╔══██║████╗  ██║██╔═══██╗████╗  ██║╚██╗ ██╔╝████╗ ████║██╔═══██╗██║   ██║██╔████╔╝██╔════╝
███████║██╔██╗ ██║██║   ██║██╔██╗ ██║ ╚████╔╝ ██╔████╔██║██║   ██║██║   ██║██║╚██╔╝ ███████╗
██╔══██║██║╚██╗██║██║   ██║██║╚██╗██║  ╚██╔╝  ██║╚██╔╝██║██║   ██║██║   ██║██║ ╚═╝  ╚════██║
██║  ██║██║ ╚████║╚██████╔╝██║ ╚████║   ██║   ██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║     ███████║
╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝

                  👻  A N O N Y M O U S   T R A C E  👻
               ───────────────────────────────────────────
                     OSINT • RECON • IDENTITY SEARCH

========================================
          AnonymousTrace
========================================
    AUTHORIZED USE ONLY
    Do not use for stalking,
    harassment, or doxxing.
========================================
[/bold green]"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="AnonymousTrace",
        description="AnonymousTrace: Find Usernames Across Social Networks (Version 0.1.0)",
    )
    parser.add_argument(
        "usernames",
        nargs="*",
        help="One or more usernames to check with social networks",
    )
    parser.add_argument(
        "--site",
        action="append",
        dest="sites",
        help="Limit analysis to just the listed sites (repeatable)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Time (in seconds) to wait for response to requests (Default: 60)",
    )
    parser.add_argument(
        "--proxy",
        "-p",
        help="Make requests over a proxy. e.g. socks5://127.0.0.1:1080",
    )
    parser.add_argument(
        "--tor",
        action="store_true",
        help="Route through Tor SOCKS proxy",
    )
    parser.add_argument(
        "--unique-tor",
        action="store_true",
        help="Route through Tor, requesting a new circuit per request",
    )
    parser.add_argument(
        "--dump-response",
        action="store_true",
        help="Dump the HTTP response to stdout for targeted debugging",
    )
    parser.add_argument(
        "--json",
        metavar="JSON_FILE",
        help="JSON output file",
    )
    parser.add_argument(
        "--print-all",
        action="store_true",
        help="Output sites where the username was not found",
    )
    parser.add_argument(
        "--print-found",
        action="store_true",
        help="Output sites where the username was found (also if exported as file)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Don't color terminal output",
    )
    parser.add_argument(
        "--browse",
        "-b",
        action="store_true",
        help="Browse to all results on default browser",
    )
    parser.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Force the use of the local data.json file",
    )
    parser.add_argument(
        "--nsfw",
        action="store_true",
        help="Include checking of NSFW sites from default list",
    )
    parser.add_argument(
        "--txt",
        action="store_true",
        help="Enable creation of a txt file",
    )
    parser.add_argument(
        "--ignore-exclusions",
        action="store_true",
        help="Ignore upstream exclusions (may return more false positives)",
    )
    parser.add_argument(
        "--skip-flaky",
        action="store_true",
        help="Skip known problematic sites with DNS/timeout issues",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=20,
        help="Concurrent worker threads (default: 20)",
    )
    parser.add_argument(
        "--min-confidence",
        choices=["found", "likely", "unknown"],
        default="unknown",
        help="Minimum confidence level to report (default: unknown)",
    )
    parser.add_argument(
        "--rate-limit",
        type=float,
        help="Polite throttle in seconds between requests to the same host",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Display extra debugging information and metrics",
    )
    parser.add_argument(
        "--folderoutput",
        "-fo",
        help="If using multiple usernames, the output of the results will be saved to this folder",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="If using single username, the output of the result will be saved to this file",
    )
    parser.add_argument(
        "--input-file",
        help="Batch usernames from a text file (one per line)",
    )
    parser.add_argument(
        "--data-file",
        help="Load data from a JSON file or an online, valid, JSON file",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Create Comma-Separated Values (CSV) File",
    )
    parser.add_argument(
        "--xlsx",
        action="store_true",
        help="Create the standard file for the modern Microsoft Excel spreadsheet",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Superpowers flags (original extensions)
    parser.add_argument(
        "-s",
        "--scan",
        action="store_true",
        help="Quick scan mode - fast scan with default settings",
    )
    parser.add_argument(
        "--super",
        action="store_true",
        help="Super mode - enables verbose output, print-all, and JSON export",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Fast mode - high speed scan with reduced timeout",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Deep mode - thorough scan with extended timeout and all sites",
    )
    parser.add_argument(
        "--stealth",
        action="store_true",
        help="Stealth mode - slow scan with low profile (rate limiting + Tor)",
    )
    parser.add_argument(
        "--list-sites",
        action="store_true",
        help="List all available platforms and exit",
    )
    parser.add_argument(
        "--plain",
        action="store_true",
        help="Plain text output - simple list format without tables",
    )
    return parser


def run_cli(args: argparse.Namespace) -> int:
    console = Console(no_color=args.no_color, legacy_windows=(sys.platform == "win32"))

    console.print(Panel(BANNER, border_style="red", expand=False))

    # Handle version flag
    if getattr(args, "version", False):
        console.print(f"[bold]AnonymousTrace[/bold] version [cyan]{__version__}[/cyan]")
        return 0

    # Handle list-sites flag
    if args.list_sites:
        loader = RegistryLoader()
        try:
            sites = loader.list_sites()
            console.print(f"\n[bold cyan]Available Platforms ({len(sites)} total):[/bold cyan]\n")
            for i, site in enumerate(sites, 1):
                console.print(f"  {i:3d}. {site}")
            return 0
        except FileNotFoundError as exc:
            console.print(f"[red]{exc}[/red]")
            return 1

    # Super mode enables multiple flags
    if args.super:
        args.verbose = max(args.verbose, 2)
        args.print_all = True
        if not args.json:
            args.json = "results.json"

    if args.print_all:
        args.min_confidence = "not_found"

    # Quick scan mode
    if args.scan:
        args.timeout = min(args.timeout, 15)
        args.workers = max(args.workers, 30)

    # Fast mode adjustments
    if args.fast:
        args.timeout = min(args.timeout, 10)
        args.workers = max(args.workers, 50)

    # Deep mode adjustments
    if args.deep:
        args.timeout = max(args.timeout, 60)
        args.print_all = True

    # Stealth mode adjustments
    if args.stealth:
        args.workers = min(args.workers, 5)
        args.timeout = max(args.timeout, 30)
        if not args.tor:
            args.tor = True

    # Warnings for flags that don't change behavior yet
    if args.local:
        console.print("[yellow]Using local registry (default behavior)[/yellow]")
    if args.nsfw:
        console.print("[yellow]NSFW sites are not included in the default registry[/yellow]")
    if args.ignore_exclusions:
        console.print("[yellow]No upstream exclusions to ignore[/yellow]")

    log_level = logging.WARNING
    if args.verbose >= 2:
        log_level = logging.DEBUG
    elif args.verbose == 1:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

    if not args.verbose:
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)

    usernames = list(args.usernames)
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.exists():
            console.print(f"[red]Input file not found: {input_path}[/red]")
            return 1
        with open(input_path, encoding="utf-8") as f:
            file_users = [line.strip() for line in f if line.strip()]
        usernames.extend(file_users)

    if not usernames:
        console.print("[red]No usernames provided.[/red]")
        return 1

    loader = RegistryLoader(registry_path=args.data_file)
    try:
        registry = loader.load()
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        return 1

    if args.skip_flaky:
        skipped = [s for s in registry if s in FLAKY_SITES]
        registry = {k: v for k, v in registry.items() if k not in FLAKY_SITES}
        if skipped:
            console.print(f"[yellow]Skipping {len(skipped)} flaky sites: {', '.join(skipped)}[/yellow]")

    ProxyService(args.proxy)  # Validate proxy
    tor_service = TorService() if (args.tor or args.unique_tor) else None

    if args.tor or args.unique_tor:
        if tor_service is not None and not tor_service.is_running():
            console.print("[yellow]Warning: Tor SOCKS proxy not detected on 127.0.0.1:9050[/yellow]")

    http_client = HTTPClient(
        timeout=args.timeout,
        proxy=args.proxy,
        tor=args.tor,
        unique_tor=args.unique_tor,
        dump_response=args.dump_response,
    )

    export_service = ExportService(
        output_path=args.json or args.output,
        folder_output=args.folderoutput,
    )

    scan_service = ScanService(
        registry=registry,
        http_client=http_client,
        workers=args.workers,
        rate_limit=args.rate_limit,
        min_confidence=args.min_confidence,
        export_service=export_service,
    )

    try:
        export_format = None
        if args.csv:
            export_format = "csv"
        elif args.xlsx:
            export_format = "xlsx"
        elif args.txt:
            export_format = "txt"
        elif args.json:
            export_format = "json"

        all_results: list[ScanResult] = []
        for username in usernames:
            if args.plain:
                console.print(f"\n[*] Checking username {username} on:")
            else:
                console.print(f"\n[bold cyan]Scanning:[/bold cyan] {username}")

            target_sites = list(scan_service.scanner.registry.values())
            if args.sites:
                registry_lower = {k.lower(): v for k, v in scan_service.scanner.registry.items()}
                target_sites = [registry_lower[s.lower()] for s in args.sites if s.lower() in registry_lower]

            total_sites = len(target_sites) if target_sites else 1

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console,
                transient=True,
            ) as progress:
                task = progress.add_task(f"Scanning {username}...", total=100)

                class ProgressCallback:
                    def __init__(self, total: int):
                        self.total = max(total, 1)
                        self.completed = 0

                    def update(self, result: ScanResult) -> None:
                        self.completed += 1
                        progress.update(task, completed=int(self.completed / self.total * 100))

                callback = ProgressCallback(total_sites)

                original_scan_site = scan_service.scanner.scan_site
                def wrapped_scan_site(site, username):
                    result = original_scan_site(site, username)
                    callback.update(result)
                    return result

                scan_service.scanner.scan_site = wrapped_scan_site
                results = scan_service.execute(
                    usernames=[username],
                    sites=args.sites,
                    export_format=export_format,
                    username_for_export=username,
                )
                scan_service.scanner.scan_site = original_scan_site

                progress.update(task, completed=100)

            all_results.extend(results)
            display_results(console, results, args)

        if len(usernames) > 1:
            if args.plain:
                console.print(f"\n[*] Search completed with {len(all_results)} results.")
            else:
                console.print("\n[bold yellow]=== Aggregate Summary ===[/bold yellow]")
                display_results(console, all_results, args)

        # Browse results if requested
        if args.browse:
            browse_results(all_results)

        return 0
    finally:
        scan_service.close()


def display_results(
    console: Console,
    results: list[ScanResult],
    args: argparse.Namespace,
) -> None:
    found = [r for r in results if r.detected]
    not_found = [r for r in results if not r.detected]

    if args.plain:
        for r in found:
            url = r.response_url or r.metadata.get("url", "N/A")
            console.print(f"[+] {r.site_name}: {url}")
        console.print(f"\n[*] Search completed with {len(found)} results.")
        return

    total = len(results)
    found_count = len(found)
    not_found_count = len(not_found)
    found_pct = (found_count / total * 100) if total else 0
    not_found_pct = (not_found_count / total * 100) if total else 0

    console.print(
        f"\n[bold]Total checked:[/bold] {total} | [green]Found: {found_count} "
        f"({found_pct:.0f}%)[/green] | [red]Not Found: {not_found_count} "
        f"({not_found_pct:.0f}%)[/red]"
    )

    if not results:
        console.print("[yellow]No results to display.[/yellow]")
        return

    if args.print_all:
        display_set = results
    elif args.print_found:
        display_set = found
    else:
        display_set = found if found else not_found

    table = Table(box=box.SIMPLE_HEAVY, expand=True, show_lines=False)
    table.add_column("Site", style="bold cyan", no_wrap=True)
    table.add_column("Detected", justify="center", style="bold")
    table.add_column("Confidence", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Error", style="dim")

    for r in display_set:
        if r.detected:
            detected_str = "[bold green]YES[/bold green]"
            site_style = "bold green"
        else:
            detected_str = "[bold red]NO[/bold red]"
            site_style = "bold red"

        conf_color = {
            "found": "bold green",
            "likely": "bold yellow",
            "unknown": "bold white",
            "not_found": "bold red",
        }.get(r.confidence.value, "bold white")

        table.add_row(
            f"[{site_style}]{r.site_name}[/{site_style}]",
            detected_str,
            f"[{conf_color}]{r.confidence.value.upper()}[/{conf_color}]",
            str(r.status_code or "-"),
            r.error or "[dim]-[/dim]",
        )

    console.print(table)

    if found:
        console.print("\n[bold green]Found profiles:[/bold green]")
        for r in found:
            url = r.response_url or r.metadata.get("url", "N/A")
            console.print(f"  [green]*[/green] [bold cyan]{r.site_name}:[/bold cyan] {url}")

    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"\n[dim]Scan completed at {scan_time}[/dim]")


def browse_results(results: list[ScanResult]) -> None:
    """Open found results in the default browser."""
    found = [r for r in results if r.detected]
    if not found:
        console.print("[yellow]No results to browse.[/yellow]")
        return

    console.print(f"[cyan]Opening {len(found)} results in browser...[/cyan]")
    for r in found:
        url = r.response_url or r.metadata.get("url")
        if url:
            webbrowser.open(url)


def cli() -> None:
    parser = build_parser()
    args = parser.parse_args()
    sys.exit(run_cli(args))


if __name__ == "__main__":
    cli()
