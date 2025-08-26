# agent_swarm
An automated, multi-agent system designed to generate daily business performance reports. This project was built to demonstrate a deep understanding of multi-agent architectures, microservices, and production-ready AI systems.
-----
### 🚀 Key Features
  * **Multi-Agent Architecture**: A "swarm" of three specialized agents (`Sales`, `Marketing`, and `Reporting`) collaborate to achieve a single, complex goal.
  * **Microservice Design**: The system is built on a microservice architecture using **FastAPI** and **Docker**, ensuring modularity, scalability, and independent deployment of components.
  * **Proactive, Scheduled Execution**: The entire workflow is triggered automatically every morning at 9 AM using a **Linux cron job** inside the Docker container, requiring no manual intervention.
  * **Dynamic Data Integration**: The agents retrieve real-time data from dynamic mock APIs that generate new sales and marketing figures on every call.
  * **Advanced AI Reasoning**:
      * **Chain of Thought (CoT)**: Agents are prompted to think step-by-step, providing detailed analysis of raw data.
      * **Tree of Thoughts (ToT)**: The Reporting Agent uses a structured prompting approach to explore multiple analytical paths before synthesizing the final report.
  * **Diverse Output Formats**: The final report is saved as a detailed **PDF file** and a structured **Excel file**, showcasing a versatile approach to data presentation.
  * **Robust Error Handling**: The system is designed to gracefully handle API failures. If an agent fails to retrieve data, the Reporting Agent detects this and still generates a report, noting the missing information.
-----
### 🧠 Architectural Overview
The system is composed of three interconnected services within a single Docker network.
1.  **`sales-api`**: A FastAPI microservice that generates and serves dynamic sales data.
2.  **`marketing-api`**: A FastAPI microservice that generates and serves dynamic marketing data.
3.  **`agent-app`**: The core application that houses the three agents. It orchestrates the workflow, fetches data from the two APIs, uses a local **Hugging Face** model for AI tasks, and generates the final output files and email.
The entire stack is orchestrated by `docker-compose.yml`, simplifying deployment to a single command.
-----
### ⚙️ Getting Started
Follow these simple steps to get the entire system up and running on your local machine.
#### Prerequisites

  * [**Docker**](https://docs.docker.com/get-docker/) installed and running.
  * `pip` and `python` installed.
#### 1\. Setup Environment
Clone the repository and create your `.env` file for credentials.
```bash
git clone https://github.com/your-username/agent_swarm.git
cd agent_swarm
```
Create a `.env` file with the following content (and remember not to commit it to git):
```env
SENDER_EMAIL="your_email@gmail.com"
SENDER_PASSWORD="your_app_password"
RECEIVER_EMAIL="recipient_email@example.com"
```
#### 2\. Launch the System
From the project's root directory, run the following command. This will build all three services and start them in the background.
```bash
docker compose up --build -d
```
#### 3\. View the Output
To see the system in action and verify that everything is working, check the logs of the `agent-app` container.
```bash
docker compose logs -f agent-app
```
You should see a detailed log of the agents' thought processes, API calls, and the final report generation.
-----
### 📋 Testing & Verification
  * **API Health Check**: Navigate to `http://localhost:8001/sales` and `http://localhost:8002/marketing` in your browser to confirm the APIs are serving dynamic data.
  * **File Output**: Check the root directory for `company_report.pdf` and `company_data.xlsx`.
  * **Email Report**: Check the `RECEIVER_EMAIL` inbox for the automated report.
-----
### 🤝 Contact
Created by Abhinav Sharma - ahvnav01@gmail.com