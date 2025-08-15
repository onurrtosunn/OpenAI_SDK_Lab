# Job Application Evaluation Agents

## 📌 Overview
This project demonstrates an **AI-powered job application evaluation workflow** using the **OpenAI Agents SDK**.  
It simulates three job applicants (junior, mid-level, senior), each generating their own job application email.  
An **HR Manager agent** evaluates all applications, selects the best one, formats it into HTML, and sends it via email.

The system is designed to showcase:
- Multi-agent collaboration
- Tool-based communication between agents
- Agent handoffs for sequential task execution
- Automated email subject generation & HTML formatting

---

## 🚀 Features
- **Three Candidate Agents**  
  - `Junior Candidate` → Beginner-level application email  
  - `Mid-level Candidate` → Professional mid-career application email  
  - `Senior Candidate` → Expert-level persuasive application email
- **HR Manager Agent**  
  - Evaluates all candidate outputs  
  - Selects the most effective application email  
  - Handoffs to the Email Manager Agent
- **Email Manager Agent**  
  - Generates an attention-catching subject line  
  - Converts plain text email into HTML format  
  - Sends the email via a sending tool (SendGrid or similar)
- **Agent Workflow Visualization** with `graphviz`
