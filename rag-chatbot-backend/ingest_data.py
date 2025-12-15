#!/usr/bin/env python3
"""
Main ingestion script to populate the Qdrant vector database from the book sitemap.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the path so we can import from data_ingestion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_ingestion.ingest import main as ingest_main

if __name__ == "__main__":
    print("Starting sitemap ingestion process...")
    print(f"Sitemap URL: {os.getenv('SITEMAP_URL', 'https://ai-native-book-seven.vercel.app/sitemap.xml')}")
    print(f"Qdrant Collection: ai-native-book")
    print("-" * 50)
    
    try:
        ingest_main()
        print("\nIngestion completed successfully!")
    except Exception as e:
        print(f"\nError during ingestion: {str(e)}")
        sys.exit(1)