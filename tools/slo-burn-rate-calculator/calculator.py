import argparse
import sys

def calculate_burn_rate(slo_target_percent, time_window_hours, current_error_rate_percent):
    """
    Calculates the SLO burn rate.
    
    A burn rate of 1 means the error budget will be exactly consumed by the end of the window.
    A burn rate > 1 means the error budget is being consumed too fast.
    """
    # Allowed error rate (Error Budget)
    allowed_error_rate = 100.0 - slo_target_percent
    
    if allowed_error_rate <= 0:
        print("SLO target must be less than 100%.")
        return None

    # Burn rate is the ratio of current error rate to the allowed error rate
    burn_rate = current_error_rate_percent / allowed_error_rate
    
    return burn_rate

def main():
    parser = argparse.ArgumentParser(description="SLO Burn Rate Calculator for CI/CD Quality Gates.")
    parser.add_argument("--slo", type=float, required=True, help="Target SLO percentage (e.g., 99.9)")
    parser.add_argument("--window", type=int, default=720, help="Time window in hours (default 720 for 30 days)")
    parser.add_argument("--error-rate", type=float, required=True, help="Current error rate percentage over the window")
    parser.add_argument("--threshold", type=float, default=2.0, help="Alert threshold burn rate (default 2.0)")

    args = parser.parse_args()

    burn_rate = calculate_burn_rate(args.slo, args.window, args.error_rate)

    if burn_rate is None:
        sys.exit(1)

    print(f"Target SLO: {args.slo}%")
    print(f"Allowed Error Rate: {100.0 - args.slo:.3f}%")
    print(f"Current Error Rate: {args.error_rate:.3f}%")
    print(f"Calculated Burn Rate: {burn_rate:.2f}x")

    if burn_rate >= args.threshold:
        print(f"\n[VIOLATION] Burn rate ({burn_rate:.2f}x) exceeds threshold ({args.threshold}x).")
        print("ACTION: Halt feature deployments. Focus on reliability.")
        sys.exit(1) # Return non-zero exit code to fail the CI/CD pipeline
    else:
        print(f"\n[PASS] Burn rate ({burn_rate:.2f}x) is within acceptable limits.")
        sys.exit(0)

if __name__ == "__main__":
    main()
