#!/usr/bin/env python3
"""
Market Intelligence AI Agent - Main Entry Point

This script provides a command-line interface for running market intelligence
analysis on companies and their competitors.

Usage:
    python main.py --companies "Apple,Microsoft,Google" --no-notification
    python main.py -c "Tesla,NVIDIA,AMD" -n
"""

import argparse
import sys
from typing import List

from market_agent import MarketIntelligenceAgent


def parse_companies(companies_str: str) -> List[str]:
    """Parse comma-separated company names."""
    return [c.strip() for c in companies_str.split(",") if c.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="📊 Market Intelligence AI Agent - Automated company analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --companies "Apple,Microsoft,Google"
  python main.py -c "Tesla,NVIDIA" --no-notification
  python main.py -c "Amazon" -n

Required Environment Variables:
  - GROQ_API_KEY         : Groq API key for Llama 3
  - TAVILY_API_KEY       : Tavily API key for news search
  - TWILIO_ACCOUNT_SID   : Twilio account SID
  - TWILIO_AUTH_TOKEN    : Twilio auth token
  - TWILIO_WHATSAPP_NUMBER: Twilio WhatsApp number
  - RECIPIENT_WHATSAPP_NUMBER: Your WhatsApp number
        """
    )
    
    parser.add_argument(
        "-c", "--companies",
        type=str,
        required=True,
        help="Comma-separated list of companies to analyze (e.g., 'Apple,Microsoft,Google')"
    )
    
    parser.add_argument(
        "-n", "--no-notification",
        action="store_true",
        help="Disable WhatsApp notification"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Parse companies
    companies = parse_companies(args.companies)
    
    if not companies:
        print("❌ Error: No companies provided")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🚀 Market Intelligence AI Agent")
    print("=" * 60)
    print(f"📌 Analyzing: {', '.join(companies)}")
    print(f"📱 Notifications: {'Disabled' if args.no_notification else 'Enabled'}")
    print("=" * 60 + "\n")
    
    try:
        # Initialize and run agent
        agent = MarketIntelligenceAgent()
        
        results = agent.run_analysis(
            companies=companies,
            send_notification=not args.no_notification
        )
        
        print("\n✅ Analysis completed successfully!")
        
        if args.verbose:
            print("\n" + "=" * 60)
            print("📄 INDIVIDUAL ANALYSES:")
            print("=" * 60)
            for company, analysis in results["individual_analyses"].items():
                print(f"\n{analysis}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
