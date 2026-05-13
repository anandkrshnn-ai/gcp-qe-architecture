# The Authenticity Scorer: Style-CPC Pattern

The **Authenticity Scorer** provides a probabilistic signal to detect stylistic traces of machine-revision in agent remediation proposals. This pattern hardens the OODA loop by adding a layer of **Quality Intelligence** over the raw AI output.

## 1. Architectural Thesis

As autonomous agents scale, the risk of "subtle hallucinations"—remediation plans that are grammatically perfect but stylistically uncharacteristic of the domain or the human-in-the-loop intent—increases. 

Instead of a binary "truth detector," we use **Style-CPC (Style-Conditional Probability Curvature)** to quantify the statistical risk that a proposal has been heavily machine-revised.

## 2. How it Works: Style-CPC

Ref: *Jiaqi Chen et al., 'Imitate Before Detect: A Stylistic Preference Optimization Framework for Machine-Revised Text Detection' (AAAI 2025).*

The scorer calculates a **Sampling Discrepancy** by measuring the deviation of the proposal's log-likelihood from the expected stylistic mean of the model distribution:

$$Discrepancy = \frac{\sum log P(x_i) - \sum \mu_{ref}(x_i)}{\sqrt{\sum \sigma^2_{ref}(x_i)}}$$

### Key Mechanisms:
- **Style Preference Optimization (SPO)**: The underlying model is aligned to become sensitive to machine-revised stylistic signatures.
- **Discrepancy Mapping**: Raw scores are mapped to **Threshold Bands** (Low, Medium, High) based on domain-specific calibration.

## 3. Implementation: Advisory Signaling

In this architecture (v8.3.0), the Authenticity Scorer operates in **Advisory Mode**. It does not block actuation but enriches the proposal metadata for human-in-the-loop review.

### Scoring Evidence Bundle
Every proposal includes:
- `authenticity_score`: Raw Style-CPC discrepancy.
- `authenticity_risk_flag`: [LOW, MEDIUM, HIGH] risk assessment.
- `evidence`: Sample variants count and threshold calibration version.

## 4. Operational Guardrails

- **Low Risk**: Actuation proceeds according to standard consensus rules.
- **Medium Risk**: Flagged in the audit trail for post-incident review.
- **High Risk**: Triggers **Mandatory SRE Approval** in the operational model (Phase 3), requiring a human to verify the proposal's authenticity before actuation.

## 5. Verification & Calibration

- **False Positive Measurement**: We measure FP rates on a labeled corpus of legitimate human remediation text to ensure the LOW risk band remains a high-confidence zone.
- **Model Drift**: Quarterly benchmarks evaluate if new Gemini versions shift the stylistic baseline, requiring threshold recalibration.
