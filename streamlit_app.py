import streamlit as st
import os
import pandas as pd

# Define the logs folder path (adjust if needed)
LOGS_DIR = "logs"

st.title("Cybersecurity Agent Dashboard")
st.write("Real-time dashboard for task statuses, log outputs, and final audit report.")

# Section: Task Statuses
st.header("Task Statuses")
task_status_file = os.path.join(LOGS_DIR, "task_statuses.csv")
if os.path.exists(task_status_file):
    df = pd.read_csv(task_status_file)
    st.dataframe(df)
else:
    st.info("No task statuses available. Make sure your agent writes task statuses to logs/task_statuses.csv.")

# Section: Real-Time Log Outputs
st.header("Real-Time Log Outputs")
log_file = os.path.join(LOGS_DIR, "agent.log")
if os.path.exists(log_file):
    with open(log_file, "r") as f:
        log_content = f.read()
    st.text_area("Agent Logs", log_content, height=300)
else:
    st.info("No logs available. Ensure your agent writes logs to logs/agent.log.")

# Section: Final Audit Report
st.header("Final Audit Report")
audit_report_file = os.path.join(LOGS_DIR, "audit_report.txt")
if os.path.exists(audit_report_file):
    with open(audit_report_file, "r") as f:
        report_content = f.read()
    st.text_area("Audit Report", report_content, height=300)
else:
    st.info("No audit report available. Your agent should generate a final audit report at logs/audit_report.txt.")

# Refresh button: In Streamlit, the script re-runs automatically on user interaction.
if st.button("Refresh"):
    st.write("Refreshing dashboard...")
    # No explicit rerun is needed because clicking a button triggers a re-run.
