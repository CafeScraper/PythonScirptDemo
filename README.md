[English](https://docs.cafescraper.com/python-actor) | [中文](https://docs.cafescraper.com/cn/actor/actor/python-actor)


### Required Files (Located in the Project Root Directory)

``` 
├── main.py
├── requirements.txt
├── input_schema.json
├── README.md
├── sdk.py
├── sdk_pb2.py
├── sdk_pb2_grpc.py

```
| File Name               | Description                        |
|-------------------------| ------------------------- |
| **`main.py`**           | Script entry file (execution entry point), uniformly named `main` |
| **`requirements.txt`**  | Python dependency management file            |
| **`input_schema.json`** | UI input form configuration file              |
| **`README.md`**         | Project documentation file                  |
| **`sdk.py`**            | SDK core functionality     |
| **`sdk_pb2.py`**        |Enhanced data processing module    |
| **`sdk_pb2_grpc.py`**   | Network communication module|


# ⭐ Core SDK Files for Scripts

### 📁 File Description

The following are three important SDK files that must be placed in the root directory of your script:

| **File Name**     | **Core Functionality** |
|-------------------| --- |
| `sdk.py`          | Basic functional modules |
| `sdk_pb2.py`      | Enhanced data processing module |
| `sdk_pb2_grpc.py` | Network communication module |

These three files form the "toolkit" for your script, providing all core functionalities required for interacting with the mid-platform system and running web crawlers.

## 🔧 Core Function Usage Guide

### 1. Environment Parameter Retrieval - Get Configuration at Script Startup

When a script starts, you can pass external configuration parameters (e.g., target website URL, search keywords). Use the following method to retrieve these parameters:

```python
# Retrieve all incoming parameters and return them as a dictionary.
parameters = SDK.Parameter.get_input_json_dict()

# Example: Assume a website URL and keywords are provided as input.
# return：{"website": "example.com", "keyword": "news"}
```

**Use Case**：For example, if you need to scrape data from different websites for different tasks, you can achieve this by passing different parameters without modifying the code.

---

### 2. Run log - record the script execution process

During script execution, you can log information at different levels. These logs will be displayed in the mid-platform interface, facilitating status monitoring and troubleshooting:

```python
SDK.Log.debug("Connecting to the target website...")

SDK.Log.info("Successfully retrieved 10 news items.")

SDK.Log.warn("The network connection is slow, which may affect the data collection speed.")

SDK.Log.error("Unable to access the target website. Please check your network connection.")
```
# Log Level Explanation:
- **debug**: Most detailed debugging information, suitable for development
- **info**: Normal process logging, recommended for key steps
- **warn**: Warning messages indicating potential issues that don't stop execution
- **error**: Error messages indicating critical issues requiring attention
---

### 3.Result Return - Send Scraped Data to Mid-Platform

After scraping data, return it to the mid-platform system by following these two steps:

#### Step 1: Set Table Headers (Mandatory First Step)

Before pushing actual data, define the table structure (similar to setting column headers in Excel):

```python
# Define the table column structure.
headers = [
    {
        "label": "News title",      # column name
        "key": "title",          # column key
        "format": "text",        # Data type：text
    },
    {
        "label": "Publish time",
        "key": "publish_time",  
        "format": "text",
    },
    {
        "label": "News category",
        "key": "category",
        "format": "text",
    },
]

# set header
res = CafeSDK.Result.set_table_header(headers)
```

**Field Explanation:**：

- **label**：Column header displayed in the table (user-visible, Chinese recommended)
- **key**：Unique identifier for data (used in code, lowercase English with underscores recommended)
- **format**：Data type supporting the following formats:
    - `"text"`：Text/string
    - `"integer"`：Integer
    - `"boolean"`：Yes/No (Boolean)
    - `"array"`：Array/list
    - `"object"`：Object/dictionary

#### Step 2: Push Data Entry by Entry

After setting headers, start pushing scraped data:

```python
# News date
news_data = [
    {"title": "New breakthroughs in artificial intelligence", "publish_time": "2023-10-01", "category": "Technology"},
    {"title": "Today's stock market trends", "publish_time": "2023-10-01", "category": "Finance"},
    # ... more
]

# push data
for i, news in enumerate(news_data):
    obj = {
        "title": news.get('title'),          
        "publish_time": news.get('publish_time'), 
        "category": news.get('category'),
    }

    res = CafeSDK.Result.push_data(obj)

    # Record the push results
    SDK.Log.info(f"Data item {i+1}：{news.get('title')}")
```

**Important Reminders:**：

1. The order of setting headers and pushing data can be reversed.
2. Keys in the pushed data dictionary must exactly match those defined in headers
3. Data must be pushed entry by entry (bulk push not supported)
4. It is recommended to log after each push to track execution progress

---

### 💡 Complete Code Example

The following is a full script example demonstrating the complete workflow from parameter retrieval to data return:

```python
# 1. Retrieve startup parameters
config = SDK.Parameter.get_input_json_dict()
website = config.get("website", "Default website")
SDK.Log.info(f"Start collecting data from the website：{website}")

# 2. Set the result table header
headers = [
    {"label": "Title", "key": "title", "format": "text"},
    {"label": "Time", "key": "publish_time", "format": "text"},
    {"label": "Category", "key": "category", "format": "text"},
    {"label": "View count", "key": "view_count", "format": "integer"},
]
CafeSDK.Result.set_table_header(headers)

# 3. Simulate data collection (in practice, this could be web scraping code)
collected_data = [
    {"title": "Sample News 1", "publish_time": "2023-10-01 10:00", "category": "Technology", "view_count": 1000},
    {"title": "Sample News 2", "publish_time": "2023-10-01 11:00", "category": "Finance", "view_count": 500},
]

# 4. Push data
for data in collected_data:
    obj = {
        "title": data.get("title"),
        "publish_time": data.get("publish_time"),
        "category": data.get("category"),
        "view_count": data.get("view_count", 0),  # Provide a default value of 0
    }
    res = CafeSDK.Result.push_data(obj)

# 5. Completed
SDK.Log.info("Data collection task completed！")
```

---

### ⚠️ Common Issues & Notes

1. **File Location**： Ensure the three `SDK` files are placed in the script's **root directory** (folder containing the main file)
2. **Import Method**：Directly use `SDK` or `CafeSDK` in code to call related functions
3. **键名一致**：Keys used for pushing data must exactly match (**including case**) those defined in headers
4. **错误处理**： It is recommended to check return results for each SDK call, especially when pushing data

With the above functionalities, your script can seamlessly integrate with the mid-platform system, enabling flexible parameter configuration, transparent execution monitoring, and standardized return of scraped data.

---

# ⭐ Script Entry File (main.py)

### 💡 Code Example

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os

from sdk import CafeSDK

async def run():
    try:
        # 1. Get params
        input_json_dict = CafeSDK.Parameter.get_input_json_dict()
        CafeSDK.Log.debug(f"params: {input_json_dict}")
        
        # 2. proxy configuration
        proxyDomain = "proxy-inner.cafescraper.com:6000"
        
        try:
            proxyAuth = os.environ.get("PROXY_AUTH")
            CafeSDK.Log.info(f"Proxy authentication information: {proxyAuth}")
        except Exception as e:
            CafeSDK.Log.error(f"Failed to retrieve proxy authentication information: {e}")
            proxyAuth = None
        
        # 3. Construct the proxy URL
        proxy_url = f"socks5://{proxyAuth}@{proxyDomain}" if proxyAuth else None
        CafeSDK.Log.info(f"Proxy address: {proxy_url}")
        
        # 4. TODO: Handle business logic
        url = input_json_dict.get('url')
        CafeSDK.Log.info(f"start deal URL: {url}")
        
        # Simulate business processing results
        result = {
            "url": url,
            "status": "success",
            "data": {
                "title": "Sample title",
                "content": "Sample content",
                # ... Other fields
            }
        }
        
        # 5. Push result data
        CafeSDK.Log.info(f"Processing result: {result}")
        CafeSDK.Result.push_data(result)
        
        # 6. Set the table headers (if table output is needed)
        headers = [
            {
                "label": "URL",
                "key": "url",
                "format": "text",
            },
            # ... Other table header configurations
        ]
        res = CafeSDK.Result.set_table_header(headers)
        
        CafeSDK.Log.info("Script execution completed")
        
    except Exception as e:
        CafeSDK.Log.error(f"Script execution error: {e}")
        error_result = {
            "error": str(e),
            "error_code": "500",
            "status": "failed"
        }
        CafeSDK.Result.push_data(error_result)
        raise

if __name__ == "__main__":
    asyncio.run(run())
```

# Automated Data Scraping Script: Operation & Principle Guide

### 1. Script Overview

This is a template for an automation tool that acts like a "digital employee". It automatically opens specified web pages (e.g., social media pages), extracts the information you need, and organizes it into structured tables.

### 2.  How It Works (4 Core Stages)

### Stage 1: Receive Instructions (Retrieve Input Parameters)

Before starting the script, you provide instructions (e.g., which webpage URL to scrape, how many data entries to collect).

### Stage 2: Anonymity Setup (Proxy Network Configuration)

To access overseas or restricted websites smoothly, the script automatically configures an "encrypted tunnel" (proxy server).

### Stage 3: Automated Work (Business Logic Processing)

This is the core part of the script. Based on the provided URL, it automatically navigates to the target page and extracts information such as titles, content, and image URLs.

### Stage 4: Report Results (Data Push & Table Generation)

After scraping, the script converts unstructured information into a standard format and saves it to the system. It also automatically designs table headers (e.g., Column 1: "URL", Column 2: "Content").

---

# ⭐Python Dependency Management File (requirements.txt)

This file lists all third-party Python packages and their version information required to run the script. The system will automatically read this file and install all specified dependencies to ensure the script runs correctly.

### Dependency List Explanation

Below are the Python packages and their corresponding versions required for this project:

Example：

```
attrs==25.4.0
beautifulsoup4==4.14.2
certifi==2025.10.5
cffi==2.0.0
charset-normalizer==3.4.4
click==8.3.0
colorama==0.4.6
cssselect==1.3.0
DataRecorder==3.6.2
DownloadKit==2.0.7
DrissionPage==4.1.1.2
et_xmlfile
filelock
```

### ❗Important Notes

### 1. Version Number Explanation

- **Packages with version numbers**（e.g. `beautifulsoup4==4.14.2`）：The system installs this exact version to ensure consistency with the development environment.
- **Packages without version numbers**（e.g. `et_xmlfile`）：The system automatically installs the latest available version of the package.

### 2. Installation Notes

- The system automatically handles installation of all dependencies – no manual operation required.
- Installation may take several minutes depending on network speed and package size.
- If installation fails, the system displays error messages – resolve issues as prompted.
### 3. Ensure Script Functionality

To ensure smooth execution of the Python script:

- List all used third-party packages in this file.
- Specify version numbers for critical core packages (e.g., package==version).
- Regularly update dependencies to get new features and security fixes.

## Frequently Asked Questions (FAQs)

**Q：Why specify version numbers?**

A：Specifying version numbers ensures the same package versions are used across different environments (development, testing, production), avoiding inconsistent program behavior or compatibility issues caused by version differences.

**Q：What happens if no version number is specified?**

A：Without a version number, the system installs the latest version of the package. This may cause incompatibility with the script, so it's recommended to fix versions for core dependencies.

**Q：How to add new dependencies?**

A：Simply add a new line in this file in the format "package==version" or "package", then re-upload the zip compressed file in the backend. The system will automatically install it on next run.

**Q：What to do if installation fails?**

A： Check network connectivity or try switching Python package mirrors. If issues persist, contact the system administrator.

---

*Last Updated: Ensure this dependency list is updated promptly after modifying script functionality to reflect all new package dependencies.*