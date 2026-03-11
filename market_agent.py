"""
Market Intelligence AI Agent
Searches, analyzes, and reports on company/competitor news automatically.
"""

import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

from tavily import TavilyClient
import chromadb
from chromadb.config import Settings
from groq import Groq
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class NewsArticle:
    """Represents a news article."""
    title: str
    url: str
    content: str
    source: str
    published_date: str


class TavilySearch:
    """Handles news and company search using Tavily API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        self.client = TavilyClient(api_key=self.api_key)
    
    def search_news(self, query: str, max_results: int = 10) -> List[NewsArticle]:
        """
        Search for news articles related to companies/competitors.
        
        Args:
            query: Search query (e.g., "Apple Inc news")
            max_results: Maximum number of results to return
            
        Returns:
            List of NewsArticle objects
        """
        print(f"🔍 Searching Tavily for: {query}")
        
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True
        )
        
        articles = []
        for result in response.get("results", []):
            article = NewsArticle(
                title=result.get("title", "No title"),
                url=result.get("url", ""),
                content=result.get("content", result.get("answer", "")),
                source=result.get("source", "Unknown"),
                published_date=datetime.now().strftime("%Y-%m-%d")
            )
            articles.append(article)
        
        print(f"✅ Found {len(articles)} articles")
        return articles
    
    def search_companies(self, companies: List[str]) -> Dict[str, List[NewsArticle]]:
        """
        Search news for multiple companies.
        
        Args:
            companies: List of company names
            
        Returns:
            Dictionary mapping company names to their news articles
        """
        results = {}
        for company in companies:
            query = f"{company} company news 2024 2025"
            articles = self.search_news(query)
            results[company] = articles
        return results


class ChromaDBStore:
    """Handles vector storage and retrieval using ChromaDB."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="market_intelligence",
            metadata={"description": "Company and competitor news articles"}
        )
    
    def store_articles(self, articles: List[NewsArticle], company: str) -> None:
        """
        Store news articles in the vector database.
        
        Args:
            articles: List of NewsArticle objects
            company: Company name for categorization
        """
        print(f"💾 Storing {len(articles)} articles for {company}")
        
        for i, article in enumerate(articles):
            doc_id = f"{company}_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create metadata
            metadata = {
                "company": company,
                "source": article.source,
                "url": article.url,
                "published_date": article.published_date,
                "title": article.title
            }
            
            # Store in ChromaDB
            self.collection.add(
                documents=[article.content],
                metadatas=[metadata],
                ids=[doc_id]
            )
        
        print(f"✅ Stored articles for {company}")
    
    def get_similar_news(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Retrieve similar news articles based on query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of similar articles with metadata
        """
        print(f"🔎 Retrieving similar news for: {query}")
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        articles = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                article = {
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                }
                articles.append(article)
        
        print(f"✅ Found {len(articles)} similar articles")
        return articles
    
    def get_all_companies(self) -> List[str]:
        """Get list of all companies in the database."""
        companies = set()
        
        # Get all metadata to extract company names
        collection_data = self.collection.get(include=["metadatas"])
        
        for metadata in collection_data.get("metadatas", []):
            if metadata and "company" in metadata:
                companies.add(metadata["company"])
        
        return list(companies)
    
    def get_company_articles(self, company: str) -> List[Dict]:
        """Get all articles for a specific company."""
        results = self.collection.get(
            where={"company": company},
            include=["documents", "metadatas"]
        )
        
        articles = []
        for i, doc in enumerate(results.get("documents", [])):
            article = {
                "content": doc,
                "metadata": results["metadatas"][i] if results["metadatas"] else {}
            }
            articles.append(article)
        
        return articles


class GroqAnalyzer:
    """Handles LLM analysis using Llama 3 via Groq API."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"
    
    def analyze_market_trends(self, articles: List[Dict], company: str) -> str:
        """
        Analyze market trends from news articles.
        
        Args:
            articles: List of article dictionaries
            company: Company name being analyzed
            
        Returns:
            Analysis summary as string
        """
        print(f"🤖 Analyzing trends for {company} using Llama 3")
        
        # Prepare context from articles
        context = "\n\n".join([
            f"Title: {art.get('metadata', {}).get('title', 'N/A')}\n"
            f"Content: {art.get('content', 'N/A')[:500]}"
            for art in articles[:10]  # Limit to 10 articles
        ])
        
        prompt = f"""
Analyze the following news articles about {company} and provide a concise executive summary.

Focus on:
1. Key business developments
2. Market positioning changes
3. Competitive threats or opportunities
4. Financial implications
5. Strategic recommendations

NEWS ARTICLES:
{context}

Provide your analysis in the following format:

📊 EXECUTIVE SUMMARY: {company}

🎯 Key Developments:
- [List 3-5 key points]

⚠️ Risks & Threats:
- [List 2-3 risks]

💡 Opportunities:
- [List 2-3 opportunities]

📈 Market Impact: [Brief assessment]

🔮 Recommendations: [2-3 strategic recommendations]
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert market intelligence analyst. Provide concise, actionable insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        analysis = response.choices[0].message.content
        print(f"✅ Analysis complete for {company}")
        return analysis
    
    def generate_competitive_report(
        self, 
        company_data: Dict[str, str],
        companies: List[str]
    ) -> str:
        """
        Generate a competitive analysis report comparing multiple companies.
        
        Args:
            company_data: Dictionary mapping company names to their analyses
            companies: List of company names
            
        Returns:
            Competitive analysis report
        """
        print("🤖 Generating competitive analysis report")
        
        # Prepare context
        context = "\n\n".join([
            f"=== {company} ===\n{analysis}"
            for company, analysis in company_data.items()
        ])
        
        prompt = f"""
Generate a comprehensive competitive analysis report comparing these companies: {', '.join(companies)}

INDIVIDUAL ANALYSES:
{context}

Provide a comparative report in this format:

🏆 COMPETITIVE LANDSCAPE REPORT

📋 Overview:
[Brief overview of the competitive landscape]

🥊 Head-to-Head Comparison:
[Compare companies across key dimensions]

🎯 Market Leaders:
[Identify leaders and why]

📊 Emerging Trends:
[Key trends affecting all companies]

⚡ Strategic Moves to Watch:
[Recommended actions for each company]

📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior competitive intelligence analyst. Provide strategic insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        report = response.choices[0].message.content
        print("✅ Competitive report generated")
        return report


class TwilioNotifier:
    """Handles WhatsApp notifications using Twilio API."""
    
    def __init__(
        self,
        account_sid: Optional[str] = None,
        auth_token: Optional[str] = None,
        from_number: Optional[str] = None,
        to_number: Optional[str] = None
    ):
        self.account_sid = account_sid or os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = auth_token or os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = from_number or os.getenv("TWILIO_WHATSAPP_NUMBER")
        self.to_number = to_number or os.getenv("RECIPIENT_WHATSAPP_NUMBER")
        
        if not all([self.account_sid, self.auth_token, self.from_number, self.to_number]):
            raise ValueError("Twilio credentials not found in environment")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_message(self, message: str) -> bool:
        """
        Send a WhatsApp message.
        
        Args:
            message: Message content to send
            
        Returns:
            True if sent successfully, False otherwise
        """
        print("📱 Sending WhatsApp message...")
        
        try:
            # Truncate message if too long (WhatsApp limit ~1600 chars)
            if len(message) > 1600:
                message = message[:1597] + "..."
            
            twilio_message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            print(f"✅ Message sent! SID: {twilio_message.sid}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def send_executive_summary(self, summary: str, companies: List[str]) -> bool:
        """
        Send an executive summary via WhatsApp.
        
        Args:
            summary: Executive summary content
            companies: List of companies analyzed
            
        Returns:
            True if sent successfully
        """
        header = f"""📊 MARKET INTELLIGENCE REPORT
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}
🏢 Companies: {', '.join(companies)}

"""
        message = header + summary
        
        return self.send_message(message)


class MarketIntelligenceAgent:
    """Main agent orchestrating all components."""
    
    def __init__(self):
        print("🚀 Initializing Market Intelligence Agent...")
        
        self.search_engine = TavilySearch()
        self.db = ChromaDBStore()
        self.analyzer = GroqAnalyzer()
        self.notifier = TwilioNotifier()
        
        print("✅ Agent initialized successfully\n")
    
    def run_analysis(
        self,
        companies: List[str],
        send_notification: bool = True
    ) -> Dict[str, str]:
        """
        Run complete market intelligence analysis.
        
        Args:
            companies: List of company names to analyze
            send_notification: Whether to send WhatsApp notification
            
        Returns:
            Dictionary of company analyses
        """
        print("=" * 60)
        print("🎯 Starting Market Intelligence Analysis")
        print("=" * 60)
        print(f"📌 Companies: {', '.join(companies)}\n")
        
        all_analyses = {}
        
        # Step 1: Search and store news for each company
        print("📰 STEP 1: Searching & Storing News")
        print("-" * 40)
        for company in companies:
            articles = self.search_engine.search_news(f"{company} company news 2024 2025")
            if articles:
                self.db.store_articles(articles, company)
            print()
        
        # Step 2: Analyze each company
        print("🧠 STEP 2: Analyzing Market Trends")
        print("-" * 40)
        for company in companies:
            articles = self.db.get_company_articles(company)
            if articles:
                analysis = self.analyzer.analyze_market_trends(articles, company)
                all_analyses[company] = analysis
                print()
        
        # Step 3: Generate competitive report
        print("📊 STEP 3: Generating Competitive Report")
        print("-" * 40)
        competitive_report = self.analyzer.generate_competitive_report(
            all_analyses, 
            companies
        )
        print()
        
        # Step 4: Send notification
        if send_notification:
            print("📱 STEP 4: Sending WhatsApp Notification")
            print("-" * 40)
            self.notifier.send_executive_summary(competitive_report, companies)
            print()
        
        print("=" * 60)
        print("✅ Analysis Complete!")
        print("=" * 60)
        
        # Save report to file
        report_filename = f"market_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(competitive_report)
        print(f"💾 Report saved to: {report_filename}")
        
        return {
            "individual_analyses": all_analyses,
            "competitive_report": competitive_report
        }


if __name__ == "__main__":
    # Example usage
    agent = MarketIntelligenceAgent()
    
    # Define companies to analyze
    companies_to_analyze = ["Apple", "Microsoft", "Google"]
    
    # Run analysis
    results = agent.run_analysis(
        companies=companies_to_analyze,
        send_notification=True
    )
