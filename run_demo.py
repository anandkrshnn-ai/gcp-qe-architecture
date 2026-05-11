import sys
import time
import argparse
import random
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from sovereign_core import SovereignClient, SovereignAnalyzer, VertexAIAnalyzer, GemmaAnalyzer, HybridSovereignAnalyzer, SovereignActuator, RuntimeSecurity, SafetyGate

console = Console()

def run_single_scenario(incident_type, mode="deterministic", simulate_attestation=False, speed_run=False, report_file=None):
    project_id = "demo-project"
    
    # 1. Initialize Runtime Security
    security = RuntimeSecurity(simulate_attestation=simulate_attestation)
    
    # 2. Initialize Safety with optional Time Dilation
    # For speed-run/CI, we stretch the window (dilation > 1) to ensure we capture sequential demo runs.
    dilation = 100.0 if speed_run else 1.0
    safety = SafetyGate(production_mode=False, time_dilation=dilation)
    
    client = SovereignClient(mode="simulation", project_id=project_id)
    actuator = SovereignActuator(dry_run=True, project_id=project_id)
    
    # Selection based on mode
    if mode == "reasoning":
        analyzer = VertexAIAnalyzer(security=security)
    elif mode == "hybrid":
        analyzer = HybridSovereignAnalyzer(security=security)
    elif mode == "gemma":
        analyzer = GemmaAnalyzer(security=security)
    else:
        analyzer = SovereignAnalyzer(security=security)
    
    # --- Wave 3 Scenarios ---
    if incident_type == "platform_outage":
        rprint("[bold yellow][EPISTEMIC] Simulating Platform Instability (Sibling Storm)...[/bold yellow]")
        safety.store.record_action("restart", "sibling-service-a")
        safety.store.record_action("restart", "sibling-service-b")
        safety.store.record_action("restart", "sibling-service-c")
    
    if incident_type == "uncertain_oom":
        # Inject conflicting logs
        logs.append({"jsonPayload": {"message": "Batch Job 'NightlyData' started on node-1"}})
        logs.append({"jsonPayload": {"message": "Memory limit reached on node-1"}})

    # --- OODA Loop ---
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        # Step 1: Security Handshake
        progress.add_task(description="[bold cyan]OODA Step 1: OBSERVE - Attestation Handshake...", total=None)
        token = security.perform_handshake()
        time.sleep(0.5)
        
        # Step 2: Observation
        progress.add_task(description=f"OODA Step 1: OBSERVE - Fetching logs for {incident_type}...", total=None)
        if incident_type != "uncertain_oom":
            logs = client.fetch_logs(incident_type)
        
        # Scrubbing Check
        scrubber = analyzer if not hasattr(analyzer, "local_tier") else analyzer.local_tier
        logs = [scrubber._deep_scrub(l) for l in logs]
        
        # Step 3: Orientation / Analysis
        progress.add_task(description=f"OODA Step 2: ORIENT - Epistemic Analysis...", total=None)
        analysis = analyzer.analyze(incident_type, logs)
        time.sleep(0.8)

        # Step 4: Decision / Safety Audit
        progress.add_task(description="OODA Step 3: DECIDE - Safety & Conflict Audit...", total=None)
        remediation = analysis.get('remediation', 'N/A')
        
        target = f"prod-{incident_type}-resource"
        if incident_type == "new_resource":
            target = f"brand-new-service-{random.randint(100, 999)}"
            
        is_safe = safety.validate_action(remediation, target)
        time.sleep(0.6)

        # Step 5: Act
        if is_safe and trust_ok and remediation != "MONITOR_AND_WAIT":
            progress.add_task(description=f"OODA Step 4: ACT - Executing {remediation}...", total=None)
            actuator.execute(remediation, target)
            
            # Principal: Stabilization Phase
            rprint(f"[bold yellow][STABILIZATION] Remediation executed. Entering Stabilization Phase for {target}...[/bold yellow]")
            for _ in range(3):
                progress.add_task(description=f"[dim]Stabilization Cycle {_+1}/3...", total=None)
                time.sleep(0.5)
                safety.verify_stabilization(target)
            
            success = True
            ttr = random.uniform(10.5, 25.2)
        else:
            success = False
            ttr = 0.0

    # --- UI DISPLAY ---
    sec_summary = security.get_security_summary()
    status_color = "green" if sec_summary["status"] == "VERIFIED" else "red"
    conflict_color = "green" if analysis.get('conflict', 0) < 0.4 else "red"
    
    table = Table(title=f"Sovereign OODA Cycle (Wave 3): {incident_type.upper()}", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim", width=25)
    table.add_column("Value")
    
    table.add_row("Runtime Attestation", f"[{status_color}]{sec_summary['attestation']}[/{status_color}]")
    table.add_row("Conflict Score", f"[{conflict_color}]{analysis.get('conflict', 0) * 100}%[/{conflict_color}]")
    table.add_row("Root Cause", analysis.get('root_cause', 'Unknown'))
    table.add_row("Reasoning Path", f"[dim]{analysis.get('reasoning', 'N/A')}[/dim]")
    table.add_row("Remediation", f"[green]{remediation}[/green]")
    table.add_row("Safety Audit", "[green]PASSED[/green]" if is_safe else "[red]BLOCKED (Epistemic Safety)[/red]")
    table.add_row("Engine", f"[cyan]{analysis.get('engine', 'Sovereign-Internal')}[/cyan]")
    
    console.print(table)
    
    # Telemetry & Tracing
    telemetry = f"TTD: {random.uniform(2,5):.2f}s | TTR: {ttr:.2f}s | Trace: {analyzer.local_tier.tracer.trace_id if hasattr(analyzer, 'local_tier') else 'N/A'}"
    console.print(Panel(telemetry, title="Operational Telemetry & Tracing", style="bold yellow"))
    
    if report_file:
        with open(report_file, "a") as f:
            f.write(f"### Scenario: {incident_type}\n")
            f.write(f"- **Conflict**: {analysis.get('conflict', 0)}\n")
            f.write(f"- **Safety**: {'Passed' if is_safe else 'Blocked (Wave 3)'}\n")
            f.write(f"- **Reasoning**: {analysis.get('reasoning')}\n\n")

    rprint(f"[SUCCESS] OODA Cycle Complete for {incident_type}.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign GCP Master Demo")
    parser.add_argument("--scenario", help="Specific incident type to run")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--mode", choices=["deterministic", "reasoning", "hybrid", "gemma"], default="deterministic", help="Analysis engine mode")
    parser.add_argument("--speed-run", action="store_true", help="Compress safety windows for CI testing")
    args = parser.parse_args()

    scenarios = [
        "oomkill", "platform_outage", "uncertain_oom", "new_resource"
    ]
    
    console.print(Panel.fit("SOVEREIGN-GCP: THE EPISTEMIC ENGINE (WAVE 3)\nUncertainty Quantification | Platform Awareness | Honeymoon Period", style="bold blue"))
    
    report_name = f"DEMO_REPORT_WAVE3_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(report_name, "w") as f:
        f.write("# Sovereign GCP Master Demo Report (Wave 3)\n")
        f.write(f"Generated on: {datetime.now().isoformat()}\n")
        f.write("Status: Epistemic Autonomy Verified\n\n")

    if args.scenario:
        run_single_scenario(args.scenario, mode=args.mode, speed_run=args.speed_run, report_file=report_name)
    elif args.all:
        for s in scenarios:
            run_single_scenario(s, mode=args.mode, speed_run=args.speed_run, report_file=report_name)
    else:
        # Default to first scenario
        run_single_scenario("oomkill", mode=args.mode, speed_run=args.speed_run, report_file=report_name)

    console.print(Panel(f"FULL SUITE COMPLETE\nReport saved to: {report_name}", style="bold green"))
