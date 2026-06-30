import numpy as np

def calculate_pearson_r(human_scores, agent_scores):
    """
    Calculates the Pearson Correlation Coefficient (r) between human reviewer scores
    and the automated agent scores to validate system accuracy.
    """
    if len(human_scores) != len(agent_scores):
        raise ValueError("The number of human scores and agent scores must match.")
        
    if len(human_scores) < 2:
        raise ValueError("At least two data points are required to calculate Pearson r.")
        
    r_matrix = np.corrcoef(human_scores, agent_scores)
    
    # corrcoef returns a 2x2 matrix, the correlation coefficient is at [0,1] or [1,0]
    return r_matrix[0, 1]

if __name__ == "__main__":
    # Example validation dataset of 50 distinct resumes (Simulated)
    # Replace these lists with the actual evaluation scores when conducting Week 4 testing.
    
    # 0-100 scores from manual human review
    sample_human_scores = [
        85, 90, 78, 92, 60, 45, 88, 76, 95, 82, 
        70, 65, 80, 85, 72, 55, 98, 89, 74, 68,
        81, 91, 77, 86, 62, 48, 87, 75, 94, 83,
        71, 66, 81, 84, 73, 56, 97, 90, 76, 69,
        82, 92, 79, 87, 63, 49, 88, 77, 96, 84
    ]
    
    # 0-100 scores from the Multi-Agent Screening System
    sample_agent_scores = [
        83, 88, 75, 94, 65, 42, 85, 80, 92, 80, 
        68, 62, 82, 86, 70, 52, 95, 87, 72, 65,
        80, 89, 75, 84, 60, 45, 86, 74, 91, 82,
        69, 64, 80, 82, 71, 54, 95, 88, 74, 67,
        80, 90, 78, 85, 61, 47, 86, 75, 94, 82
    ]
    
    try:
        r_value = calculate_pearson_r(sample_human_scores, sample_agent_scores)
        print("--- Metric Collection Tracker ---")
        print(f"Validation Dataset Size: {len(sample_human_scores)} resumes")
        print(f"Pearson Correlation (r): {r_value:.4f}")
        
        target_threshold = 0.75
        if r_value >= target_threshold:
            print(f"✅ PASSED: Target threshold of r >= {target_threshold} met.")
        else:
            print(f"❌ FAILED: Target threshold of r >= {target_threshold} not met.")
            
    except Exception as e:
        print(f"Error calculating metrics: {e}")
