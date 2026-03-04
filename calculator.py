import numpy as np

class PTRRFramework:
    """
    PTRR: Prompts, Time, Results, Rubric.
    A framework to measure and mitigate Automation Bias in AI-assisted 
    vulnerability research.
    """
    def __init__(self):
        # Weights derived from the PTRR Preregistration V5
        self.weights = {
            'FH': 0.4,   # Failed Hypotheses
            'TFA': 0.3,  # Time to First AI Assistance
            'HR': 0.3    # Hypothesis Refinement
        }

    def calculate_abi(self, prompt_score, copy_paste_ratio, verification_rate):
        """
        Automation Bias Index (ABI): Measures uncritical reliance on AI.
        Range: 0.0 (Expert/Independent) to 1.0 (Dependent/Biased).
        """
        # Prompt Score is inverted because high quality prompts reduce bias
        ats_norm = (5 - prompt_score) / 4 
        abi = (ats_norm + copy_paste_ratio + (1 - verification_rate)) / 3
        return round(abi, 4)

    def calculate_csi(self, failed_hypotheses, tfa_minutes, refinements):
        """
        Cognitive Struggle Index (CSI): Measures productive independent effort.
        High CSI indicates 'System 2' engagement (Analytical thinking).
        """
        # Normalize TFA (Time to First AI) - 30 mins is the study benchmark
        tfa_norm = min(tfa_minutes / 30, 1.0)
        # Normalize FH and HR based on max observed in study
        fh_norm = min(failed_hypotheses / 10, 1.0)
        hr_norm = min(refinements / 10, 1.0)
        
        csi = (self.weights['FH'] * fh_norm) + \
              (self.weights['TFA'] * tfa_norm) + \
              (self.weights['HR'] * hr_norm)
        return round(csi, 4)

    def calculate_tiis(self, invocations, data_prompts, tool_sequence_gap):
        """
        Tool Integration Intensity Score (TIIS): Measures multi-tool synthesis.
        Captures the 'Augmented' workflow efficiency.
        """
        # Sinv: Inverse of the gap between AI usage and Tool usage
        s_inv = 1 / max(tool_sequence_gap, 0.1)
        tiis = (invocations * data_prompts) * s_inv
        return round(tiis, 4)

# ==========================================
# FULL CASE STUDY DATA (60-Hour Self-Study)
# ==========================================

case_study_data = {
    "Pre-PTRR_Phase": {
        "description": "Initial 10 hours without structured metacognition",
        "sessions": [
            {"name": "General Recon", "prompt_score": 2, "cp_ratio": 0.8, "mvr": 0.2, "fh": 1, "tfa": 2, "hr": 1, "tools": 2},
            {"name": "Simple Injection", "prompt_score": 3, "cp_ratio": 0.6, "mvr": 0.4, "fh": 2, "tfa": 5, "hr": 2, "tools": 3}
        ],
        "vulnerabilities": 2  # Low severity (Informational/Low)
    },
    "Post-PTRR_Phase": {
        "description": "50 hours using PTRR Framework (Cognitive Augmentation)",
        "sessions": [
            {
                "name": "3DES Crypto Bypass", 
                "prompt_score": 5, "cp_ratio": 0.1, "mvr": 1.0, 
                "fh": 8, "tfa": 25, "hr": 9, "tools": 12
            },
            {
                "name": "1-Click ATO (PostMessage)", 
                "prompt_score": 5, "cp_ratio": 0.05, "mvr": 1.0, 
                "fh": 12, "tfa": 20, "hr": 15, "tools": 15
            },
            {
                "name": "HTTP Request Smuggling", 
                "prompt_score": 4, "cp_ratio": 0.2, "mvr": 0.9, 
                "fh": 6, "tfa": 18, "hr": 7, "tools": 8
            }
        ],
        "vulnerabilities": 9  # High/Critical severity
    }
}

# ==========================================
# ANALYSIS EXECUTION
# ==========================================

ptrr = PTRRFramework()

def analyze_phase(phase_name):
    data = case_study_data[phase_name]
    print(f"\n{'='*20} {phase_name} {'='*20}")
    print(f"Description: {data['description']}")
    
    avg_abi, avg_csi, avg_tiis = [], [], []
    
    for s in data['sessions']:
        abi = ptrr.calculate_abi(s['prompt_score'], s['cp_ratio'], s['mvr'])
        csi = ptrr.calculate_csi(s['fh'], s['tfa'], s['hr'])
        tiis = ptrr.calculate_tiis(s['tools'], 0.8, 0.5) # Constants for simplified example
        
        avg_abi.append(abi)
        avg_csi.append(csi)
        avg_tiis.append(tiis)
        
        print(f"[*] Session: {s['name']} | ABI: {abi} | CSI: {csi} | TIIS: {tiis}")

    return np.mean(avg_abi), np.mean(avg_csi), data['vulnerabilities']

# Run Comparison
pre_abi, pre_csi, pre_vulns = analyze_phase("Pre-PTRR_Phase")
post_abi, post_csi, post_vulns = analyze_phase("Post-PTRR_Phase")

# Calculate Performance Leap
performance_increase = (post_vulns / pre_vulns) * (post_csi / pre_csi)

print("\n" + "#"*40)
print(f"FINAL RESULT: PERFORMANCE MULTIPLIER = {round(performance_increase, 2)}x")
print(f"ABI Reduction (Bias Mitigation): {round((pre_abi - post_abi)/pre_abi * 100, 2)}%")
print("#"*40)
