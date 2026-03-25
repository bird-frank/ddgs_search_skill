#!/usr/bin/env python3
"""
Tests for ddgs_search.py

Uses pytest with unittest.mock for mocking.
- Chicago School (State-Based): get_proxy, format_result
- London School (Mock-Based): search_web, search_news, main
"""

import json
import sys
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from scripts.ddgs_search import format_result, get_proxy


class TestGetProxy:
    """Tests for get_proxy() function - Chicago School (State-Based)"""

    def test_returns_cli_proxy_when_provided(self):
        cli_proxy = "http://cli-proxy.example.com:8080"

        result = get_proxy(cli_proxy)

        assert result == cli_proxy

    @patch.dict(
        "os.environ", {"HTTP_PROXY": "http://http-proxy.example.com:8080"}, clear=True
    )
    def test_returns_http_proxy_from_env(self):
        result = get_proxy(None)

        assert result == "http://http-proxy.example.com:8080"

    @patch.dict(
        "os.environ",
        {"http_proxy": "http://lowercase-proxy.example.com:8080"},
        clear=True,
    )
    def test_returns_lowercase_http_proxy_from_env(self):
        result = get_proxy(None)

        assert result == "http://lowercase-proxy.example.com:8080"

    @patch.dict(
        "os.environ", {"DDGS_PROXY": "http://ddgs-proxy.example.com:8080"}, clear=True
    )
    def test_returns_ddgs_proxy_from_env(self):
        result = get_proxy(None)

        assert result == "http://ddgs-proxy.example.com:8080"

    @patch.dict(
        "os.environ",
        {
            "HTTP_PROXY": "http://http-proxy.example.com:8080",
            "DDGS_PROXY": "http://ddgs-proxy.example.com:8080",
        },
        clear=True,
    )
    def test_cli_proxy_takes_priority_over_env(self):
        cli_proxy = "http://cli-proxy.example.com:8080"

        result = get_proxy(cli_proxy)

        assert result == cli_proxy

    @patch.dict(
        "os.environ",
        {
            "HTTP_PROXY": "http://http-proxy.example.com:8080",
            "DDGS_PROXY": "http://ddgs-proxy.example.com:8080",
        },
        clear=True,
    )
    def test_http_proxy_takes_priority_over_ddgs_proxy(self):
        result = get_proxy(None)

        assert result == "http://http-proxy.example.com:8080"

    @patch.dict("os.environ", {}, clear=True)
    def test_returns_none_when_no_proxy_set(self):
        result = get_proxy(None)

        assert result is None

    @patch.dict(
        "os.environ", {"HTTPS_PROXY": "http://https-proxy.example.com:8080"}, clear=True
    )
    def test_ignores_https_proxy(self):
        result = get_proxy(None)

        assert result is None


class TestFormatResult:
    """Tests for format_result() function - Chicago School (State-Based)"""

    def test_formats_basic_web_result(self):
        result = {
            "title": "Test Title",
            "href": "https://example.com",
            "body": "Test body content",
        }

        output = format_result(result, index=1)

        assert "[1] Test Title" in output
        assert "URL: https://example.com" in output
        assert "摘要: Test body content" in output

    def test_formats_first_result_without_separator(self):
        result = {"title": "First", "href": "https://first.com", "body": "First body"}

        output = format_result(result, index=0)

        assert not output.startswith("\n" + "=" * 60)
        assert "[0] First" in output

    def test_formats_subsequent_results_with_separator(self):
        result = {
            "title": "Second",
            "href": "https://second.com",
            "body": "Second body",
        }

        output = format_result(result, index=1)

        assert output.startswith("\n" + "=" * 60)

    def test_handles_missing_title(self):
        result = {"href": "https://example.com", "body": "Body content"}

        output = format_result(result, index=1)

        assert "[1] N/A" in output

    def test_handles_missing_href(self):
        result = {"title": "Title", "body": "Body content"}

        output = format_result(result, index=1)

        assert "URL: N/A" in output

    def test_handles_missing_body(self):
        result = {"title": "Title", "href": "https://example.com"}

        output = format_result(result, index=1)

        assert "摘要: N/A" in output

    def test_formats_news_result_with_date(self):
        result = {
            "title": "News Title",
            "href": "https://news.example.com",
            "body": "News body",
            "date": "2024-01-15",
        }

        output = format_result(result, index=1)

        assert "日期: 2024-01-15" in output

    def test_formats_news_result_with_source(self):
        result = {
            "title": "News Title",
            "href": "https://news.example.com",
            "body": "News body",
            "source": "Example News",
        }

        output = format_result(result, index=1)

        assert "来源: Example News" in output

    def test_formats_news_result_with_date_and_source(self):
        result = {
            "title": "News Title",
            "href": "https://news.example.com",
            "body": "News body",
            "date": "2024-01-15",
            "source": "Example News",
        }

        output = format_result(result, index=1)

        assert "日期: 2024-01-15" in output
        assert "来源: Example News" in output

    def test_handles_empty_result(self):
        result = {}

        output = format_result(result, index=1)

        assert "[1] N/A" in output
        assert "URL: N/A" in output
        assert "摘要: N/A" in output


class TestSearchWeb:
    """Tests for search_web() function - London School (Mock-Based)"""

    @patch("scripts.ddgs_search.DDGS")
    def test_calls_ddgs_with_correct_parameters(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.text.return_value = [{"title": "Test"}]

        from scripts.ddgs_search import search_web

        search_web(
            query="test query",
            max_results=5,
            region="us-en",
            safesearch="on",
            timelimit="d",
            backend="html",
            proxy="http://proxy.example.com:8080",
        )

        mock_ddgs_class.assert_called_once_with(proxy="http://proxy.example.com:8080")
        mock_ddgs.text.assert_called_once_with(
            "test query",
            region="us-en",
            safesearch="on",
            timelimit="d",
            max_results=5,
            backend="html",
        )

    @patch("scripts.ddgs_search.DDGS")
    def test_returns_list_of_results(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        expected_results = [
            {"title": "Result 1", "href": "https://example1.com", "body": "Body 1"},
            {"title": "Result 2", "href": "https://example2.com", "body": "Body 2"},
        ]
        mock_ddgs.text.return_value = iter(expected_results)

        from scripts.ddgs_search import search_web

        results = search_web(query="test")

        assert results == expected_results
        assert isinstance(results, list)

    @patch("scripts.ddgs_search.DDGS")
    def test_uses_default_parameters(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.text.return_value = []

        from scripts.ddgs_search import search_web

        search_web(query="test query")

        mock_ddgs.text.assert_called_once_with(
            "test query",
            region="wt-wt",
            safesearch="moderate",
            timelimit=None,
            max_results=10,
            backend="auto",
        )

    @patch("scripts.ddgs_search.DDGS")
    def test_handles_no_proxy(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.text.return_value = []

        from scripts.ddgs_search import search_web

        search_web(query="test", proxy=None)

        mock_ddgs_class.assert_called_once_with(proxy=None)

    @patch("scripts.ddgs_search.DDGS")
    def test_handles_empty_results(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.text.return_value = []

        from scripts.ddgs_search import search_web

        results = search_web(query="test")

        assert results == []


class TestSearchNews:
    """Tests for search_news() function - London School (Mock-Based)"""

    @patch("scripts.ddgs_search.DDGS")
    def test_calls_ddgs_news_with_correct_parameters(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.news.return_value = [{"title": "News"}]

        from scripts.ddgs_search import search_news

        search_news(
            query="test news",
            max_results=3,
            region="cn-zh",
            safesearch="off",
            timelimit="w",
            proxy="http://proxy.example.com:8080",
        )

        mock_ddgs_class.assert_called_once_with(proxy="http://proxy.example.com:8080")
        mock_ddgs.news.assert_called_once_with(
            "test news",
            region="cn-zh",
            safesearch="off",
            timelimit="w",
            max_results=3,
        )

    @patch("scripts.ddgs_search.DDGS")
    def test_returns_list_of_news_results(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        expected_results = [
            {
                "title": "News 1",
                "href": "https://news1.com",
                "body": "Body 1",
                "date": "2024-01-15",
                "source": "Source 1",
            },
        ]
        mock_ddgs.news.return_value = iter(expected_results)

        from scripts.ddgs_search import search_news

        results = search_news(query="test")

        assert results == expected_results

    @patch("scripts.ddgs_search.DDGS")
    def test_uses_default_parameters(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value = mock_ddgs
        mock_ddgs.news.return_value = []

        from scripts.ddgs_search import search_news

        search_news(query="test news")

        mock_ddgs.news.assert_called_once_with(
            "test news",
            region="wt-wt",
            safesearch="moderate",
            timelimit=None,
            max_results=10,
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
