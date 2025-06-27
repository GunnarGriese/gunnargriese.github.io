---
title: MCP Servers in Digital Analytics: Levelling Up Your LLM Game
author: gunnar
date: 2026-06-27 00:00:01 +0200
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

## Some Personal Reflections on the Recent AI Hype

While the above probably sounds like I have given in to the ever-present AI hype, I also want to be honest with you: Up until recently I've been struggling to think of groundbreaking applications for AI within my line of work - Digital Analytics.

I mean, of course, I have used tools like ChatGPT, Perplexity, and Claude Desktop to enhance my productivity. I have personally experienced how all of a sudden I was able to supercharge my JavaScript, Python, and SQL skills. I was able to finally wrap up (some) of my side projects that remained dormant for years, because now it didn't require me to sift through endless Stackoverflow conversations, documentations, and blog posts anymore. I turned my problem statements into prompts, iterated incredibly fast, and eventually solved (what previously seemed like) unsolvable problems.

While I embraced the enhanced productivity and overnight skills "enhancements", I could not see how this would fundamentally change the way I work. The processes and steps involved seemed to remain the same, I was simply able to achieve the desired end goal in a fraction of the time compared to pre-Large Language Model (LLM) days. At the end of the day, it was still me inspecting a website and its code, checking if dataLayer and GA4 events occur at the right time, and configuring GA4 and GTM via the interface or the API.

The final step of any good implementation, turning the collected data into actionable recommendations (or ideally simply actions) seemed far-fetched to me. The believe that dumping data into ChatGPT and hoping for some business-critical insights always made me wince and to this day sounds illusory (I can recommend Juliana's [blog post](https://julianajackson.substack.com/p/language-models-cant-do-data-analysis) on this topic. I share many of her thoughts expressed in her text). 

## What are MCP Servers?

So, Gunnar, what has changed now, you might (or should) ask? 

Well, in November 2024, Anthropic released the Model Context Protocol (MCP), enabling AI applications to interact with external services, access real-time information, manipulate data, and take actions on behalf of their users - namely, you. Finally, conversations could be turned into actions frictionlessly! 

When you use any AI application of your choice, e.g., Claude Desktop, Gemini, etc., your prompts are sent to an LLM that then attempts to generate relevant responses. These responses are based on patterns learned from vast amounts of text data during the initial model training phase. The training data eventually determines the model's "knowledge", and without further help its capabilities are limited to generating text answers to your questions/prompts.

Accordingly, I compare these models to kids who have been lucky enough to acquire some knowledge (the entirety of the internet, to be fair), can communicate their thoughts in a way that they have been taught to (=text), and have a set of capabilities (that definitely has the potential to grow). Other tools that we use in our profession, such as GA4, HubSpot, and GitHub, can be seen as persons with capabilities and knowledge/context of their own (often more relevant because they have awareness of business-specific information). These pieces of information or capabilities would be beneficial for the LLMs to learn or tap into, either to expand their knowledge (for a more up-to-date context) or to teach them new skills for the task at hand (to show them a way to actually **solve** a problem).

The challenge is that LLMs and these tools "speak" a completely different language, isolating the LLMs from the outside world and making it difficult for them to expand their knowledge and master new skills. So far, we've been lacking a standardized interface to overcome this hurdle.

Now, with the introduction of MCP servers, we have been provided with the necessary translators that enable an AI application or LLM to connect with and understand other online services. MCP servers bridge the gap between AI reasoning and real-world execution. Instead of copying and pasting code snippets or manually implementing AI-generated recommendations, you can now have AI applications that "understand" your current setup and implement changes directly.

The MCP architecture follows a classic client-server architecture and is relatively straightforward:

* Hosts (like Claude Desktop) can be configured to connect to various MCP Servers
* MCP Clients sit within the host application and maintain a connection the MCP server
* MCP Servers act as intermediaries between MCP clients and external services and provide the context and tools needed
* External Services (like Google Analytics, GTM, or BigQuery) provide the actual data and functionality

![MCP Servers - High-level Architecture](/assets/img/mcp-digital-analytics/mcp-high-level.png)
_MCP Servers - High-level Architecture (Source: [Deeplearning.ai](https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/))_

The architecture allows the host application to connect to multiple MCP servers - each of them designed for specific use cases and bringing additional capabilities to the AI application. Moreover, what makes MCP servers particularly powerful is their reusability factor. A single MCP Server developed once can be used across multiple AI applications, and once connected, it requires little additional integration work to enhance MCP-compatible tools.

Developers of an MCP server can decide whether they make the server available locally or remotely. A remote MCP server hosts one or more MCP-compatible tools over the internet. Unlike local MCP servers that users need to download and run on their own machine, remote servers are deployed to accessible URLs. This setup allows the same MCP server and its tools to be shared across multiple users and applications. Remote MCP servers are usually a tad more complex, because developers need to account for multi-tenant support, parallelization, and user authentication. Because the protocol is still fairly new and under active development, I expect it soon to become easier to develop remote servers. 

In a nutshell, the adoption of a standard protocol like MCP within the industry comes with several advantages for the entire ecosystem:

**For AI Application Developers**: Connect your app to any MCP Server with zero additional integration work. This means new tools and platforms become immediately available to AI applications without custom development.
**For Tool and API Developers**: Build an MCP server once, and it can be adopted across the entire ecosystem of MCP-compatible applications. This dramatically reduces the barrier to AI integration.
**For End Users**: AI applications gain extensive new capabilities, enabling workflows that were previously impossible or extremely time-consuming.

## How do MCP Servers work under the hood?

MCP servers can be built in various languages, such as Python, TypeScript, Rust, etc., as long as they can use the supported transports. In practice, I've seen most available MCP servers use either TypeScript or Python (e.g., via the [FastMCP framework](https://gofastmcp.com/getting-started/welcome)).

MCP Servers expose three key types of capabilities to AI applications:
1. Tools
2. Resources
3. Prompt Templates

Let's have a look what each of these components are and how they can be implemented for a Google Analytics (GA) MCP server using Python and the FastMCP framework.

### 1. Tools

Tools are functions that AI models can call to perform specific actions or access data. These are similar to POST endpoints in a REST API, but specifically designed for LLM interactions. Using the FastMCP framework, all it takes to turn a function into a tool is using the `@mcp.tool()` decorator. The below tool `get_realtime_data` would allow the client to fetch data from the [GA realtime API](https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics). As you can see, the tool takes three inputs a list of `metrics` and `dimensions` as well as the GA property ID. The LLM will derive these inputs from your prompt in the host application and then the client will call the tool with those. Eventually, the report response, a JSON string, will be passed back to the client and can be further processed by the host application and the LLM.
   
```python
@mcp.tool()
def get_realtime_data(
    metrics: Union[List[str], str], 
    dimensions: Union[List[str], str, None] = None,
    property_id: Optional[str] = None
) -> str:
    """
    Get real-time Google Analytics data.
    
    Args:
        metrics: List of metric names (e.g., ["activeUsers"]) or JSON string
        dimensions: Optional list of dimension names (e.g., ["deviceCategory"]) or JSON string
        property_id: Optional GA4 property ID (uses default if not provided)
    
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

Resources are read-only data sources that AI models can access to retrieve information, similar to GET endpoints in a REST API. They provide data access without performing computations or causing side effects.

To expose a resource, we can add the `@mcp.resource()` decorator. For example, the code example below connects to the GA Data API's [`getMetadata`](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getMetadata) method to return metadata (apiName, uiName, description, etc.) for all dimensions and metrics in a GA property, including custom dimensions and metrics.

This exemplary resource allows the client to access GA metadata as context for LLM interactions, such as requesting specific reports. This ensures the client has accurate, up-to-date information about available metrics and dimensions when generating queries or analyzing data.

```python
@mcp.resource("ga4://default/metadata")
async def get_default_metadata() -> str:
    """Get metadata for the default Google Analytics property."""
    if not default_property_id:
        return json.dumps({"error": "No default property ID configured"})
    
    return await get_property_metadata(default_property_id)
```

### 3. Prompt Templates

Prompt templates are reusable, pre-defined templates that standardize common AI interactions. These are particularly valuable for sharing your expertise and ensuring consistent, high-quality outputs. These are particularly valuable for sharing domain expertise and ensuring consistent, high-quality outputs across different users or use cases.

To create a prompt template, use the `@mcp.prompt()` decorator. The example above defines a template that guides the LLM through analyzing GA property metadata systematically. It provides structured instructions for retrieving data (use `get_metadata_tool(property_id='{property_id}')`), organizing information, and delivering comprehensive insights.

This template ensures that anyone analyzing GA4 metadata gets consistent, thorough results without needing to write and test prompts themselves. From my perspective, prompt templates are likely what will differentiate "great" MCP servers from "okay" ones, since this is the place were MCP server developers can persist and share their expertise and make it easily accessible to their users. In this example, all the user has to do is to insert the desired property, submit the prompt template, and wait for the client to call retrieve the metadata.

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

Now, let's come back to the original premise of this blog post: How does this have the potential to change the way you work, Gunnar?

After familiarizing myself with this technology, I was curious if I could apply it to a typical project of mine: Implementing GA via GTM for an ecommerce website. The typical (simplified) process for such an implementation project is as follows:

1. Collecting business requirements
2. Website analysis and data layer discovery
3. Identifying relevant tracking events
4. Implementing GA4 tags in GTM
5. Testing and verification

The skills and tools involved to successfully complete such a project usually require 
* Business understanding and domain expertise 
* Ability to navigate the website via a web browser
* Knowledge within the browser developer tools to inspect the DOM, the dataLayer available, and network requests
* Configuration skills for both GA & GTM

None of the tasks and skills involved are necessarily rocket science, but require a deep understanding of the underlying technical components and can be time-consuming when you want to get it right. So, I've been trying to reimagine the process with MCP servers handling the technical execution while I focus on the strategic decisions and arrived at the following:

![Digital Analytics Implementation Process](/assets/img/mcp-digital-analytics/mcp-implementation-process.png)
_Own visualization_

With MCP Servers, the process has the potential to become:

1. Collecting requirements (Human provides input)
2. Website analysis and data layer discovery (AI Agent using Playwright MCP Server)
3. Identifying relevant tracking events (AI Agent)
4. Implementing GA4 tags in GTM (AI Agent using GTM MCP Server)
5. Testing and verification (AI Agent using browser automation)
6. Review and final approval (Human oversight)

"Outsourcing" some of the laborious, time-consuming tasks to the AI application while maintaining human oversight for the strategic decisions fundamentally changes the nature of the work. Instead of spending hours manually configuring tags and debugging implementation issues, I might be able to focus on understanding the business context, defining the right measurement strategy, and ensuring the data will actually drive meaningful insights.

## The Digital Analytics MCP Server Toolkit

After I had mapped out the process, I've been looking into what MCP servers would be needed to make this vision a reality. The good news for me was that most of the foundational components already existed or building them from scratch was relatively straightforward. Here's the toolkit I assembled for my proof of concept:

![Digital Analytics MCP Server Toolkit](/assets/img/mcp-digital-analytics/mcp-server-overview.png)
_Own visualization_

### Customized Playwright MCP Server
Playwright is an open-source automation library, initially developed by Microsoft, for end-to-end testing and web scraping. I've been using it in the past already to automate certain tasks and, therefore, was familiar with the library. What always hindered me in the past to use it more broadly was the fact that I had to "hardcode" the logic making it impractical for more ad-hoc tasks like quickly inspecting a website's dataLayer events.

Microsoft developed a [Playwright MCP server](https://github.com/microsoft/playwright-mcp) that provides browser automation capabilities that essentially give an AI agent the same tools a digital analyst would use when inspecting a website. It includes core browser management for navigation and page interactions, content analysis through page snapshots and element detection, and monitoring capabilities for console messages and network requests. Since the code is open-sourced it was surprisingly easy to extend the base Playwright functionality to automatically detect and record dataLayer events as they occur during user interactions.

This means the AI agent can navigate through a website's user flow - from product browsing to checkout completion - while simultaneously capturing all the dataLayer events that fire along the way. This automated discovery eliminates the manual process of clicking through pages while keeping developer tools open to monitor the dataLayer array.

### Google Tag Manager MCP Server
Stape developed a [Google Tag Manager (GTM) MCP server](https://github.com/stape-io/google-tag-manager-mcp-server) that offers complete integration with the GTM API, providing capabilities that match what an analyst would typically do in the GTM interface. It handles account and container management, comprehensive asset management for tags, triggers, and variables, user permission management, and complete version control and publishing workflows.

This essentially gives the AI agent full access to a GTM container with the same capabilities as a human implementation egineer. The main limitation is that the GTM API is highly rate-limited, so bulk operations require careful orchestration and sometimes creative workarounds to avoid hitting API quotas during complex implementations.

### Google Analytics MCP Server
Last but not least, to give myself some hands-on practice with MCP servers I decided to build my own GA MCP server. The server connects to both the GA4 Data and Admin APIs, enabling property and data stream creation, metadata retrieval and comprehensive reporting capabilities, and real-time data access for immediate validation.

This provides the AI agent with both the administrative capabilities to configure GA4 properties and the analytical capabilities to verify that data is flowing correctly and to generate reports for validation purposes.

## Putting the Setup to the Test

Now, that I had all the tools in place the question really was: Does this actually work?

To answer this question I put the setup to the test by tasking it with implementing GA via GTM for my test ecommerce website. I've documented the process of this POC in videos to demonstrate how Claude Desktop enhanced with the MCP servers described above and guided by my prompts navigates through each step of the implementation workflow, from initial website analysis through final verification of the tracking setup. The videos run at 4x speed, because the entire process took around 30 minutes in total. Feel free to follow along!

1. Analyze the website structure using the Playwright MCP Server to identify key pages, forms, and user interaction points.

2. Discover existing dataLayer events by monitoring browser console output and network requests
Create a new GA4 property using the Google Analytics MCP Server with appropriate settings for the Danish market.

{% include embed/youtube.html id='XQzmI7QZkZM' %}

3. Create a new GA4 property and a respective data stream using the Google Analytics MCP Server.

{% include embed/youtube.html id='XCNb8t-mino' %}

4. Set up the complete GTM configuration including tags for pageviews, enhanced ecommerce events, and custom conversions.

{% include embed/youtube.html id='dZWt6ETAIOk' %}

5. Implement automated testing to verify that all tracking was working correctly and generate comprehensive documentation of the entire implementation.

{% include embed/youtube.html id='dJZeUA03EAI' %}

## Conclusion

While my POC shows the potential of MCP servers in digital analytics workflows, I totally realize that this is still very much an experimental approach with limitations and applied to a very basic example. Throughout the process, the AI also occasionally made decisions that required correction, sometimes struggled with complex dataLayer structures, and needed multiple iterations to achieve the desired GTM configuration. What you see in the compressed videos is the successful outcome after several attempts and refinements.

Still, I believe that this allows us to take a glimpse at how we might work in the future with digital analytics implementations. For me, the most important take away from this is that human expertise and oversight will likely remain essential in the future. The AI agent can execute technical tasks efficiently, but I don't believe that it will replace the strategic thinking, business context understanding, and quality assurance that experienced analysts bring to implementations anytime soon.

Despite the well-defined scope of the task and the limitations I experienced, the POC demonstrates that we're moving toward a future where AI hopefully will be able to handle more of the mechanical aspects of analytics implementation, freeing up human analysts to focus on strategy, analysis, and insight generation. The key will be to find the right balance between automation and human oversight.