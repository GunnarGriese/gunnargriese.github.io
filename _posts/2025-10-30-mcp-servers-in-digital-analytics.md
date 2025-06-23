---
title: MCP Servers in Digital Analytics: Levelling Up Your LLM Game
author: gunnar
date: 2025-10-30 00:00:01 +0200
categories: [GTM, GA4]
tags: [gtm-server-side, ga4]
comments: true
toc: true
lang: en
---

> This article is a write-up of my talk at MeasureCamp Copenhagen 2025 - thanks to everyone who attended the session and provided feedback. It's been a pleasure presenting in front of a room full of interested people in the applications of AI within the field of digital analytics.

Currently, we are experiencing a significant shift in how our AI applications and agents can interact with external services and data sources. While conversational AI (e.g., ChatGPT) has made remarkable improvements over the last few years, the real potential lies in creating AI "systems" that can go beyond a text input/output interaction to actually perform meaningful actions in our digital analytics workflows. 

Model Context Protocol (MCP) Servers might be just what we needed to make the move from conversations to actions, because with the introduction of MCP we now have a standardized way to close the previously existing gap between AI applications and the digital analytics tools that we do our actual work in (e.g., Google Analytics, Google Tag Manager, BigQuery, etc.).

In this post, I'll break down what MCP Servers are, how they work, and most importantly, how they can be used in your digital analytics workflows. I'll share the outcome of a thought experiment with you. In particular, a POC of how analytics implementations could like in the future and how it will change the role of implementation specialists.

## The Current State of AI Integration

While the above probably sounds like I have given in to the ever-present AI hype, I also want to be honest with you: Up until recently I've been struggling to think of groundbreaking applications for AI within my line of work - Digital Analytics.

I mean, of course, I have used tools like ChatGPT, Perplexity, and Claude Desktop to enhance my productivity. I have personally experienced how all of a sudden I was able to supercharge my JavaScript, Python, and SQL skills. I was able to finally wrap up (some) of my side projects that remained dormant for years, because now it didn't require me to sift through endless Stackoverflow conversations, documentations, and blog posts anymore. I turned my problem statements into prompts, iterated incredibly fast, and eventually solved (what previously seemed like) unsolvable problems.

While I embraced the enhanced productivity and overnight skills "enhancements", I could not see how this would fundamentally change the way I work. The processes and steps involved seemed to remain the same, I was simply able to achieve the desired end goal in a fraction of the time compared to pre-LLM days. At the end of the day, it was still me inspecting a website and its code, checking if dataLayer and GA4 events occur at the right time, and configuring GA4 and GTM via the interface or the API.

The final step of any good implementation, turning the collected data into actionable recommendations (or ideally simply actions) seemed far-fetched to me. The believe that dumping data into ChatGPT and hoping for some business-critical insights always made me wince and to this day sounds illusory (I can recommend Juliana's [blog post](https://julianajackson.substack.com/p/language-models-cant-do-data-analysis) on this topic. I share many of her thoughts expressed in her text). 

## What Are MCP Servers?

So, Gunnar, what has changed now, you might (or should) ask?

Model Context Protocol (MCP) Servers represent a standardized approach to connecting AI applications with external services and data sources. Think of them as universal translators that enable any MCP-compatible AI application to seamlessly interact with various tools and platforms.

The architecture is elegantly simple:

* MCP Clients (like Claude Desktop) connect to multiple MCP Servers
* MCP Servers act as intermediaries between AI applications and external services
* External Services (like Google Analytics, GTM, or BigQuery) provide the actual data and functionality

What makes this particularly powerful is the reusability factor. A single MCP Server can be used across multiple AI applications, and once connected, it requires zero additional integration work for new MCP-compatible tools.

Add picture from slides + analogy

## How do MCP Servers work under the hood?

ADD: You usually write them in Node or Python (e.g., FastMCP framework)
MCP Servers expose three key types of capabilities to AI applications:

### 1. Tools

Tools are functions that AI models can call to perform specific actions - similar to POST endpoints in a REST API, but specifically designed for LLM interactions. In our analytics context, this might include:

* Creating a new GA4 property via the GA4 Admin API
* Setting up conversion events in Google Analytics
* Creating tags, triggers, and variables in Google Tag Manager
* Publishing GTM container versions

```python
@mcp.tool()
def get_realtime_data(
    metrics: Union[List[str], str],  # Allow both types
    dimensions: Union[List[str], str, None] = None,  # Allow both types
    property_id: Optional[str] = None,
    limit: Optional[int] = None
) -> str:
    """
    Get real-time Google Analytics data.
    
    Args:
        metrics: List of metric names (e.g., ["activeUsers"]) or JSON string
        dimensions: Optional list of dimension names (e.g., ["deviceCategory"]) or JSON string
        property_id: Optional GA4 property ID (uses default if not provided)
        limit: Optional limit on number of rows returned
    
    Returns:
        JSON string containing the real-time data
    """
    if not analytics_client:
        return json.dumps({"error": "Google Analytics client not initialized"})
    
    try:
        # Preprocess list parameters
        processed_metrics = preprocess_list_param(metrics)
        processed_dimensions = preprocess_list_param(dimensions)
        
        if not processed_metrics:
            return json.dumps({"error": "Metrics parameter is required and must be a valid list"})
        
        # Use default property ID if not provided
        prop_id = property_id or default_property_id
        if not prop_id:
            return json.dumps({"error": "No property ID provided"})
        
        # Build metrics
        metric_objs = [Metric(name=metric) for metric in processed_metrics]
        
        # Build dimensions
        dimension_objs = []
        if processed_dimensions:
            dimension_objs = [Dimension(name=dim) for dim in processed_dimensions]
        
        # Create request
        request = RunRealtimeReportRequest(
            property=format_property_id(prop_id),
            metrics=metric_objs,
            dimensions=dimension_objs,
            limit=limit
        )
        
        # Run realtime report
        response = analytics_client.run_realtime_report(request=request)
        
        # Format response
        result = {
            "metrics_headers": [{"name": metric.name} for metric in response.metric_headers],
            "dimension_headers": [{"name": dim.name} for dim in response.dimension_headers],
            "rows": [],
            "row_count": response.row_count
        }
        
        # Process rows
        for row in response.rows:
            row_data = {
                "dimensions": [dim_value.value for dim_value in row.dimension_values],
                "metrics": [metric_value.value for metric_value in row.metric_values]
            }
            result["rows"].append(row_data)
        
        return json.dumps(result, indent=2)
        
    except GoogleAPIError as e:
        logger.error(f"Google API error: {e}")
        return json.dumps({"error": f"Google API error: {str(e)}"})
    except Exception as e:
        logger.error(f"Error getting realtime data: {e}")
        return json.dumps({"error": f"Error getting realtime data: {str(e)}"})
```

### 2. Resources

ADD: Screenshot of what it looks like in Claude.

Resources are data sources that AI models can access to retrieve information - similar to GET endpoints in a REST API. These provide read-only access to data without performing computations or having side effects. Examples include:

* Getting available dimensions and metrics from a GA4 property
* Retrieving GTM container configurations
* Accessing BigQuery dataset schemas
* Reading existing tag setups and configurations

```python
@mcp.resource("ga4://default/metadata")
async def get_default_metadata() -> str:
    """Get metadata for the default Google Analytics property."""
    if not default_property_id:
        return json.dumps({"error": "No default property ID configured"})
    
    return await get_property_metadata(default_property_id)
```

### 3. Prompt Templates

ADD: Screenshot of what it looks like in Claude.

Prompt templates are reusable, pre-defined templates that standardize common AI interactions. These are particularly valuable for sharing your expertise and ensuring consistent, high-quality outputs. For analytics work, this might include:

* Standardized prompts for GA4 property analysis
* Best practice templates for GTM implementation reviews
* Data quality assessment frameworks
* Conversion tracking setup guidelines

```python
@mcp.prompt()
async def analyze_ga4_metadata(property_id: str) -> str:
    """
    Generates a comprehensive analysis prompt for Claude to explore the metadata
    of a specific Google Analytics 4 property. This prompt guides Claude to
    utilize the `get_metadata_tool(property_id='{property_id}')` and then synthesize insights about the
    available dimensions and metrics.

    Args:
        property_id: The Google Analytics 4 property ID (e.g., "123456789") for which
                     to analyze metadata.

    Returns:
        A detailed prompt string for Claude, instructing it to fetch, parse, and
        analyze the GA4 property metadata.
    """
    return f"""Analyze the Google Analytics 4 property metadata for property ID '{property_id}'.

1.  First, use the `get_metadata_tool(property_id='{property_id}')` to retrieve the metadata.

2.  For the metadata found, extract and organize the following information for both dimensions and metrics:
    -   API Name
    -   UI Name (if available)
    -   Description
    -   Category (for both dimensions and metrics)
    -   Type (for metrics, e.g., INTEGER, FLOAT)

3.  Provide a comprehensive summary that includes:
    -   An overview of the total number of dimensions and metrics available.
    -   A breakdown of dimensions by category, highlighting the most common categories.
    -   A breakdown of metrics by category, highlighting the most common categories.
    -   Identify any potentially useful or commonly used dimensions (e.g., 'date', 'country', 'deviceCategory').
    -   Identify any potentially useful or commonly used metrics (e.g., 'activeUsers', 'screenPageViews', 'sessions').
    -   Suggest potential combinations of dimensions and metrics that could be used for common GA4 reports.
    -   Discuss any interesting or unusual dimensions/metrics.

4.  Organize your findings in a clear, structured format with headings and bullet points for easy readability.

Please present both detailed information about each dimension and metric and a high-level synthesis of the data capabilities of the '{property_id}' property.
"""
```

## Why Use MCP Servers in Digital Analytics?

The benefits of adopting MCP Servers in your analytics workflow extend far beyond simple automation. Here's why this technology represents a significant leap forward:

### Ecosystem Benefits

**For AI Application Developers**: Connect your app to any MCP Server with zero additional integration work. This means new analytics tools and platforms become immediately available to AI applications without custom development.
**For Tool and API Developers**: Build an MCP Server once, and it can be adopted across the entire ecosystem of MCP-compatible applications. This dramatically reduces the barrier to AI integration.
**For Analytics Professionals**: AI applications gain extensive new capabilities, enabling workflows that were previously impossible or extremely time-consuming.

### Practical Applications in Analytics

The real power becomes apparent when you consider end-to-end analytics implementations. Traditional workflows typically require:

ADD: Piccture

1. Collecting business requirements (Human)
2. Website analysis and data layer discovery (Human)
3. Identifying relevant tracking events (Human)
4. Implementing GA4 tags in GTM (Human)
5. Testing and verification (Human)

ADD: Piccture

With MCP Servers, this becomes:

1. Collecting requirements (Human provides input)
2. Website analysis and data layer discovery (AI Agent using Playwright MCP Server)
3. Identifying relevant tracking events (AI Agent)
4. Implementing GA4 tags in GTM (AI Agent using GTM MCP Server)
5. Testing and verification (AI Agent using browser automation)
6. Review and final approval (Human oversight)

"Outsourcing" some of the laborous, time-consuming tasks to the AI application 

## The Digital Analytics MCP Server Toolkit

To demonstrate the potential, I've been working with several MCP Servers specifically designed for digital analytics workflows.

ADD: Picture

### Customized Playwright MCP Server

Provides comprehensive browser automation capabilities including:

1. Core browser management (navigation, page interactions)
2. Content analysis (page snapshots, element detection)
3. Monitoring capabilities (console messages, network requests)
4. Custom analytics features (dataLayer event tracking)

Essentially, a digital analyst with access to a web browser and the browser development tools.

ADD: Describe how you added the capability to record the dataLayer.

### Google Tag Manager MCP Server

Offers complete GTM API integration:

1. Account and container management
2. Asset management (tags, triggers, variables)
3. User permission management
4. Version control and publishing workflows

An analyst with access to a GTM container. Limitations: GTM API is highly rate limited, bulk operations might need some more workarounds.

### Google Analytics MCP Server

Connects to both GA4 Data and Admin APIs:

1. Property and data stream creation
2. Metadata retrieval and reporting
3. Real-time data access
4. Conversion tracking setup

## Real-World Implementation Example

Let me walk you through a practical example that demonstrates the power of this approach. Recently, I used this MCP Server toolkit to automate the complete analytics setup for an e-commerce website.

### The Challenge

The task was to implement comprehensive GA4 tracking for a Danish e-commerce site, including:

* Enhanced ecommerce tracking
* Custom conversion events
* User engagement metrics
* Automated testing and validation

### The Solution

Using the MCP Server toolkit, the AI agent was able to:

1. Analyze the website structure using the Playwright MCP Server to identify key pages, forms, and user interaction points.

2. Discover existing dataLayer events by monitoring browser console output and network requests
Create a new GA4 property using the Google Analytics MCP Server with appropriate settings for the Danish market.

ADD: VIDEO
{% include embed/youtube.html id='XQzmI7QZkZM' %}

3. Set up the complete GTM configuration including tags for pageviews, enhanced ecommerce events, and custom conversions.

{% include embed/youtube.html id='dZWt6ETAIOk' %}

4. Create a new GA4 property and a respective data stream using the Google Analytics MCP Server.

{% include embed/youtube.html id='XCNb8t-mino' %}

5. Implement automated testing to verify that all tracking was working correctly
Generate comprehensive documentation of the entire implementation

{% include embed/youtube.html id='dJZeUA03EAI' %}

TONE THIS DOWN: The entire process, which would typically take several days of manual work, was completed in under an hour with minimal human intervention required only for business logic decisions and final approval.

## Challenges and Considerations

While MCP Servers represent a significant advancement, there are important considerations for implementation:

### Data Security and Access Control
Since MCP Servers provide direct access to your analytics tools and data, proper authentication and authorization are crucial. Always ensure:

* Secure credential management
* Principle of least privilege for API access
* Proper audit logging of all actions
* Review processes for automated changes

### Quality Assurance
While AI agents can perform many tasks automatically, human oversight remains critical for:

* Business logic validation
* Data quality assessment
* Privacy compliance verification
* Strategic decision-making

### Integration Complexity
Setting up MCP Servers requires some technical expertise, particularly for:

* API authentication and configuration
* Custom business logic implementation
* Error handling and fallback procedures
* Performance monitoring and optimization

## Conclusion

MCP Servers represent a fundamental shift in how AI applications interact with external services, offering unprecedented opportunities for automation and integration in digital analytics. By providing standardized access to tools, resources, and expert knowledge, they enable AI agents to perform complex, multi-step analytics implementations that were previously impossible.

The key insight is that MCP Servers don't replace human expertise - they amplify it. They handle the routine, time-consuming tasks while freeing analytics professionals to focus on strategy, innovation, and complex problem-solving.

As we've seen in the examples above, the combination of AI agents with proper MCP Server integration can dramatically reduce implementation time, improve consistency, and enable new types of analytics workflows that simply weren't feasible before.

The ecosystem is still in its early stages, but the potential is enormous. As more platforms adopt MCP support and more servers become available, we'll see increasingly sophisticated automation possibilities.
For those of us working in digital analytics, now is the time to start experimenting with this technology. The organizations that learn to effectively combine AI agents with their analytics workflows will have a significant competitive advantage in the years to come.

If you're interested in exploring MCP Servers for your analytics workflows or want to discuss specific implementation challenges, feel free to reach out. I'm always happy to help fellow analytics professionals navigate this exciting new frontier.