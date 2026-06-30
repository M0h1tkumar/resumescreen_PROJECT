# Multi-Agent Resume Screening System

This repository contains the completed Multi-Agent Resume Screening System, developed as part of the TCS Assessment Framework. The system leverages an AI agent graph (using LangGraph) to deterministically parse, score, and rank candidates based on their resumes and the provided job description.

## Features

*   **Robust Text Parsing**: Extracts string text accurately from diverse formats (PDF, DOCX) via `utils/parsers.py`.
*   **Pydantic Data Models**: Enforces strict `CandidateProfile` schema definitions, isolating relevant career details and eliminating systemic bias.
*   **LangGraph Orchestration**:
    *   `Parser Node`: Structures the raw text.
    *   `Scoring Node`: Compares candidate experience to the Job Description (0-100 score).
    *   `Ranking Node`: Flags employment gaps or temporal anomalies.
    *   `Interview Node`: Generates targeted interview questions dynamically.
*   **Langfuse Instrumentation**: Embedded callback tracking records LLM token utilization, processing latencies, and total execution costs.
*   **Streamlit Reviewer Interface**: A modern web dashboard allowing recruiters to drag-and-drop resumes, paste job descriptions, and instantly review structured insights.

## Operational Setup

1.  **Clone the Repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file in the root directory and add your keys based on `.env.example`:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    LANGFUSE_PUBLIC_KEY=your_langfuse_public_key_here
    LANGFUSE_SECRET_KEY=your_langfuse_secret_key_here
    LANGFUSE_HOST=https://cloud.langfuse.com
    ```

4.  **Run the Streamlit Interface**:
    ```bash
    streamlit run ui/app.py
    ```

## Evaluation and Metrics (Phase 4)

To validate the system against human reviewer baselines, execute the statistical calculation script:

```bash
python evaluation/calculate_metrics.py
```
This script computes the **Pearson Correlation Coefficient ($r$)** to ensure the automated agent matches the decisions of senior technical recruiters ($r \ge 0.75$).

## Walkthrough Video

*(Please provide the link to your 5-minute technical walkthrough video here)*
*   [Watch the system demonstration](https://youtube.com)
*   **What it covers**: Successful resume processing, triggered anomalies (e.g., severe career gaps), and the corresponding Langfuse execution traces.
