# WebLM API Client

A Python client library for interacting with the WebLM API, providing HTML to Markdown conversion and web content extraction capabilities.

## Features

- Convert HTML content from URLs to Markdown
- Smart conversion with AI enhancement
- Extract links from webpages
- Transform web content into structured data using Pydantic models
- Synchronous and asynchronous API support
- Simple API key authentication

## Installation

```bash
pip install weblm-client
```

## Quick Start

### Basic Usage

```python
from weblm import WebLMClient

# Initialize with your API key
client = WebLMClient(api_key="your_api_key")

# Convert HTML to Markdown
result = client.convert(url="https://example.com")
print(result["markdown"])

# Smart convert with AI enhancement
smart_result = client.smart_convert(url="https://example.com")
print(smart_result["markdown"])

# Extract links from a webpage
links = client.scrape_links(url="https://example.com")
print(links["urls"])
```

### Asynchronous Usage

```python
import asyncio
from weblm import AsyncWebLMClient

async def main():
    # Initialize with your API key
    client = AsyncWebLMClient(api_key="your_api_key")

    try:
        # Convert HTML to Markdown
        result = await client.convert(url="https://example.com")
        print(result["markdown"][:100] + "...")

        # Run multiple operations concurrently
        smart_result, links = await asyncio.gather(
            client.smart_convert(url="https://example.com"),
            client.scrape_links(url="https://example.com")
        )

        print(f"Smart conversion: {smart_result['markdown'][:100]}...")
        print(f"Found {len(links['urls'])} links")

    finally:
        # Always close the client when done
        await client.close()

# Run the async function
asyncio.run(main())
```

### Transform Web Content with Pydantic Models

Define a Pydantic model and transform web content directly into structured data:

```python
from pydantic import BaseModel
from typing import List, Optional
from weblm import WebLMClient

# Define your data model
class Article(BaseModel):
    title: str
    author: Optional[str] = None
    content: str
    categories: List[str] = []

# Initialize client
client = WebLMClient(api_key="your_api_key")

# Transform web content into your model
article = client.transform(
    url="https://example.com/article",
    model_class=Article
)

# Work with structured data
print(f"Title: {article.title}")
print(f"Author: {article.author}")
print(f"Content preview: {article.content[:100]}...")
print(f"Categories: {', '.join(article.categories)}")
```

## API Reference

### WebLMClient

#### Initialization

```python
client = WebLMClient(api_key="your_api_key", base_url="http://localhost:8000")
```

- `api_key`: Your API key for authentication
- `base_url`: Optional API base URL (default: "http://localhost:8000")

#### Methods

- `convert(url, return_token_count=False, model_name="gemini-2.0-flash")`: Convert HTML to Markdown
- `smart_convert(url, return_token_count=False, model_name="gemini-2.0-flash")`: Convert HTML to refined Markdown using AI
- `scrape_links(url, include_media=False, domain_only=True)`: Extract links from a webpage
- `get_models()`: Get list of available language models
- `transform(url, model_class)`: Transform web content into a Pydantic model

### AsyncWebLMClient

Provides the same methods as `WebLMClient` but with asynchronous support. Additionally includes:

- `close()`: Close the underlying HTTP session (should be called when done)

### Error Handling

```python
from weblm import WebLMClient, WebLMAPIError

client = WebLMClient(api_key="your_api_key")

try:
    result = client.convert(url="https://example.com")
    print(result["markdown"])
except WebLMAPIError as e:
    print(f"API Error: {e}")
```

## Advanced Usage

### Concurrent Processing with AsyncWebLMClient

```python
import asyncio
from weblm import AsyncWebLMClient
from pydantic import BaseModel
from typing import List

class ArticlePreview(BaseModel):
    title: str
    summary: str

async def process_multiple_urls(urls):
    client = AsyncWebLMClient(api_key="your_api_key")

    try:
        # Create tasks for all URLs
        tasks = [
            client.transform(url=url, model_class=ArticlePreview)
            for url in urls
        ]

        # Process all URLs concurrently
        articles = await asyncio.gather(*tasks)

        # Return the processed articles
        return articles

    finally:
        await client.close()

# Example usage
urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
]

articles = asyncio.run(process_multiple_urls(urls))
for i, article in enumerate(articles):
    print(f"Article {i+1}: {article.title}")
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
