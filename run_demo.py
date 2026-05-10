import sys
import time
import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from sovereign_core import SovereignClient, SovereignAnalyzer, VertexAIAnalyzer, GemmaAnalyzer, HybridSovereignAnalyzer, SovereignActuator, RuntimeSecurity

console = Console()
security = RuntimeSecurity()

def run_single_scenario(incident_type, mode="deterministic", report_file=None):
    project_id = "demo-project"
    client = SovereignClient(mode="simulation", project_id=project_id)
    actuator = SovereignActuator(dry_run=True, project_id=project_id)
    
    # Selection based on mode
    if mode == "reasoning":
        analyzer = VertexAIAnalyzer()
    elif mode == "hybrid":
        analyzer = HybridSovereignAnalyzer()
    elif mode == "gemma":
        analyzer = GemmaAnalyzer()
    else:
        analyzer = SovereignAnalyzer()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Fetching logs for {incident_type}...", total=None)
        logs = client.fetch_logs(incident_type)
        time.sleep(0.5)

        progress.add_task(description=f"Analyzing with {mode} engine...", total=None)
        analysis = analyzer.analyze(incident_type, logs)
        time.sleep(0.8)

        progress.add_task(description="Generating remediation plan...", total=None)
        success = actuator.execute(analysis.get('remediation', 'N/A'), f"prod-{incident_type}-resource")
        time.sleep(0.3)

    # --- UI DISPLAY ---
    sec_status = "[bold green]VERIFIED[/bold green]" if security.verify_trust_boundary() else "[bold yellow]INSECURE (Reference Only)[/bold yellow]"
    
    table = Table(title=f"Incident Analysis: {incident_type.upper()}", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim", width=15)
    table.add_column("Value")
    
    table.add_row("Runtime Trust", sec_status)
    table.add_row("Root Cause", analysis.get('root_cause', 'Unknown'))
    table.add_row("Confidence", f"{analysis.get('confidence', 0) * 100}%")
    table.add_row("Remediation", f"[green]{analysis.get('remediation', 'N/A')}[/green]")
    table.add_row("Engine", f"[cyan]{analysis.get('engine', 'Sovereign-Internal')}[/cyan]")
    
    console.print(table)
    
    if report_file:
        with open(report_file, "a") as f:
            f.write(f"## Scenario: {incident_type}\n")
            f.write(f"- **Trust**: {'Verified' if security.verify_trust_boundary() else 'Insecure'}\n")
            f.write(f"- **Analysis**: {analysis.get('root_cause')}\n")
            f.write(f"- **Action**: {analysis.get('remediation')}\n")
            f.write(f"- **Engine**: {analysis.get('engine')}\n\n")

    rprint(f"[SUCCESS] OODA Cycle Complete for {incident_type}.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign GCP Master Demo")
    parser.add_argument("--scenario", help="Specific incident type to run")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--mode", choices=["deterministic", "reasoning", "hybrid", "gemma"], default="deterministic", help="Analysis engine mode")
    args = parser.parse_args()

    scenarios = [
        "oomkill", "latency", "dns_fail", "quota_exceeded", 
        "iam_denied", "storage_full", "db_fail", "cert_expired"
    ]
    
    console.print(Panel.fit("SOVEREIGN-GCP: PRINCIPAL-GRADE INCIDENT ENGINE\nHardened OODA Loop for Autonomous Remediation", style="bold blue"))
    
    report_name = f"DEMO_REPORT_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(report_name, "w") as f:
        f.write("# Sovereign GCP Master Demo Report\n")
        f.write(f"Generated on: {datetime.now().isoformat()}\n\n")

    if args.scenario:
        run_single_scenario(args.scenario, mode=args.mode, report_file=report_name)
    elif args.all:
        for s in scenarios:
            run_single_scenario(s, mode=args.mode, report_file=report_name)
    else:
        # Default to first scenario
        run_single_scenario("oomkill", mode=args.mode, report_file=report_name)

    console.print(Panel(f"FULL SUITE COMPLETE\nReport saved to: {report_name}", style="bold green"))
