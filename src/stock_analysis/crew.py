from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# import os
# from dotenv import load_dotenv
# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

@CrewBase
class StockAnalysisCrew:
    """StockAnalysis crew for analyzing AAPL stock"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def financial_reporter(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_reporter"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def investment_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["investment_strategist"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_market_trends_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_market_trends_task"],
            agent=self.market_researcher(),
        )

    @task
    def analyze_stock_data_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_stock_data_task"],
            agent=self.data_analyst(),
        )

    @task
    def get_quarterly_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["get_quarterly_report_task"],
            agent=self.financial_reporter(),
        )

    @task
    def summarize_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_analysis_task"],
            agent=self.investment_strategist(),
            output_file="aapl_stock_analysis.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockAnalysis crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )