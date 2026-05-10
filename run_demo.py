"""
Sovereign-GCP: The 100/100 Master Demo.
Full OODA Loop for 10+ Enterprise GCP Scenarios with Premium UI.
"""

import sys
import os
import time
from datetime import datetime

# Ensure the 'src' directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from sovereign_core import SovereignClient, SovereignAnalyzer, VertexAIAnalyzer, SovereignActuator, RuntimeSecurity

console = Console()
security = RuntimeSecurity()

def run_single_scenario(incident_type, mode="deterministic", report_file=None):
    project_id = "demo-project"
    client = SovereignClient(mode="simulation", project_id=project_id)
    actuator = SovereignActuator(dry_run=True, project_id=project_id)
    analyzer = VertexAIAnalyzer() if mode == "reasoning" else SovereignAnalyzer()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        
        # --- OBSERVE ---
        progress.add_task(description=f"Observing {incident_type} telemetry...", total=None)
        logs = client.fetch_logs(incident_type)
        if not logs:
            logs = [{"jsonPayload": {"message": f"Simulation event for {incident_type}"}}]
        time.sleep(0.5)

        # --- ORIENT & DECIDE ---
        progress.add_task(description="Analyzing Root Cause...", total=None)
        analysis = analyzer.analyze_with_llm(incident_type, logs) if mode == "reasoning" else analyzer.analyze(incident_type, logs)
        time.sleep(0.5)
        
        # --- ACT ---
        progress.add_task(description="Generating Remediation Plan...", total=None)
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
    
    console.print(table)
    
    # Simulate Actuator
    console.print(f"\n[bold yellow][*][/bold yellow] Actuator: Executing [cyan]dry-run[/cyan] on target-resource...")
    actuator.execute(incident_type, target=f"prod-{incident_type}-resource")
    console.print(f"[bold green][SUCCESS][/bold green] OODA Cycle Complete for {incident_type}.\n")

    # Write to report if requested
    if report_file:
        with open(report_file, "a") as f:
            f.write(f"| {incident_type} | {analysis.get('root_cause')} | {analysis.get('confidence')*100}% | {analysis.get('remediation')} |\n")

def main():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]SOVEREIGN-GCP: PRINCIPAL-GRADE INCIDENT ENGINE[/bold cyan]\n"
        "[dim]Hardened OODA Loop for Autonomous Remediation[/dim]",
        border_style="bright_blue"
    ))

    scenarios = [
        "oomkill", "latency", "dns_failure", "quota_exhaustion", 
        "iam_denied", "storage_full", "db_fail", "cert_expired"
    ]
    
    mode = "reasoning" if "--reasoning" in sys.argv else "deterministic"
    run_all = "--all" in sys.argv
    
    report_name = f"DEMO_REPORT_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    
    if run_all:
        with open(report_name, "w") as f:
            f.write(f"# Sovereign-GCP Master Demo Report\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("| Incident | Root Cause | Confidence | Proposed Action |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            
        for s in scenarios:
            run_single_scenario(s, mode, report_name)
        
        console.print(Panel(f"[bold green]FULL SUITE COMPLETE[/bold green]\nReport saved to: [bold white]{report_name}[/bold white]"))
    else:
        target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "oomkill"
        if target not in scenarios:
            console.print(f"[bold red]Error:[/bold red] Scenario '{target}' not found.")
            return
        run_single_scenario(target, mode)

if __name__ == "__main__":
    main()
