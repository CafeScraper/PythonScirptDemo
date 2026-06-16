#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

from sdk import CoreSDK


def main():
    try:
        # 1. Get input parameters
        input_json_dict = CoreSDK.Parameter.get_input_json_dict()
        CoreSDK.Log.debug(f"Input parameters: {input_json_dict}")

        # 2. Read and log all input fields (demonstrating 11 editor types)
        urls = input_json_dict.get("urls", [])
        sources = input_json_dict.get("sources", [])
        search_terms = input_json_dict.get("searchTerms", [])
        location = input_json_dict.get("location", "")
        notes = input_json_dict.get("notes", "")
        max_results = int(input_json_dict.get("max_results", 100))
        language = input_json_dict.get("language", "en")
        category = input_json_dict.get("category", 1)
        data_sections = input_json_dict.get("data_sections", [])
        skip_closed = bool(input_json_dict.get("skip_closed", False))
        since_date = input_json_dict.get("since_date", "")

        CoreSDK.Log.info(f"[requestList] urls: {urls}")
        CoreSDK.Log.info(f"[requestListSource] sources: {sources}")
        CoreSDK.Log.info(f"[stringList] searchTerms: {search_terms}")
        CoreSDK.Log.info(f"[input] location: {location}")
        CoreSDK.Log.info(f"[textarea] notes: {notes}")
        CoreSDK.Log.info(f"[number] max_results: {max_results}")
        CoreSDK.Log.info(f"[select] language: {language}")
        CoreSDK.Log.info(f"[radio] category: {category}")
        CoreSDK.Log.info(f"[checkbox] data_sections: {data_sections}")
        CoreSDK.Log.info(f"[switch] skip_closed: {skip_closed}")
        CoreSDK.Log.info(f"[datepicker] since_date: {since_date}")

        # 3. Proxy configuration (read from environment variables)
        proxy_domain = os.environ.get("PROXY_DOMAIN")
        try:
            proxy_auth = os.environ.get("PROXY_AUTH")
            CoreSDK.Log.info(f"Proxy authentication: {proxy_auth}")
        except Exception as e:
            CoreSDK.Log.error(f"Failed to retrieve proxy authentication: {e}")
            proxy_auth = None

        # 4. Construct proxy URL
        proxy_url = f"socks5://{proxy_auth}@{proxy_domain}" if proxy_auth else None
        CoreSDK.Log.info(f"Proxy URL: {proxy_url}")

        # 5. Set table headers
        headers = [
            {"label": "Primary Key", "key": "id", "format": "text"},
            {"label": "Title", "key": "title", "format": "text"},
            {"label": "Description", "key": "description", "format": "text"},
        ]
        CoreSDK.Result.set_table_header(headers)

        # 6. Push data in batches (limited by max_results)
        batch_size = 100
        sleep_seconds = 1

        for index in range(1, max_results + 1):
            data = {
                "id": f"test-{index}",
                "title": f"Test Title {index}",
                "description": f"This is test description number {index}",
            }
            CoreSDK.Result.upsert_data(data, "id")

            if index % batch_size == 0:
                CoreSDK.Log.info(f"Pushed {index} items")
                if index < max_results:
                    time.sleep(sleep_seconds)

        CoreSDK.Log.info("Starting second push for multiples of 3")
        for index in range(3, max_results + 1, 3):
            data = {
                "id": f"test-{index}",
                "title": f"Test Title {index}",
                "description": f"This is updated test description number {index} after second push",
            }
            CoreSDK.Result.upsert_data(data, "id")

        CoreSDK.Log.info("Second push for multiples of 3 completed")

    except Exception as e:
        CoreSDK.Log.error(f"Script execution error: {e}")
        error_headers = [
            {"label": "Error", "key": "error", "format": "text"},
            {"label": "Error Code", "key": "error_code", "format": "text"},
            {"label": "Status", "key": "status", "format": "text"},
        ]
        CoreSDK.Result.set_table_header(error_headers)
        error_result = {
            "error": str(e),
            "error_code": "500",
            "status": "failed"
        }
        CoreSDK.Result.push_data(error_result)
        raise


if __name__ == "__main__":
    main()
