#!/usr/bin/env python3
"""
Tests for main() function in ddgs_search.py - London School (Mock-Based)

This file is separate because main() function captures references to
search_web/search_news at module load time, requiring special handling.
"""

import json
import sys
from io import StringIO
from unittest.mock import patch

import pytest


class TestMain:
    """Tests for main() function"""

    def test_basic_web_search(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = [
                {"title": "Test", "href": "https://test.com", "body": "Test body"}
            ]
            with patch("sys.argv", ["ddgs_search.py", "test query"]):
                from scripts.ddgs_search import main

                with patch("sys.stdout", new=StringIO()) as fake_stdout:
                    main()

        output = fake_stdout.getvalue()
        assert "🔍 DuckDuckGo 网页搜索" in output
        assert "test query" in output
        assert "找到 1 条结果" in output

    def test_news_search(self):
        with patch("scripts.ddgs_search.search_news") as mock_search_news:
            mock_search_news.return_value = [
                {"title": "News", "href": "https://news.com", "body": "News body"}
            ]
            with patch("sys.argv", ["ddgs_search.py", "test query", "--news"]):
                from scripts.ddgs_search import main

                with patch("sys.stdout", new=StringIO()) as fake_stdout:
                    main()

        output = fake_stdout.getvalue()
        assert "🔍 DuckDuckGo 新闻搜索" in output

    def test_json_output(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = [
                {"title": "Test", "href": "https://test.com", "body": "Body"}
            ]
            with patch("sys.argv", ["ddgs_search.py", "test", "--json"]):
                from scripts.ddgs_search import main

                with patch("sys.stdout", new=StringIO()) as fake_stdout:
                    main()

        output = fake_stdout.getvalue()
        data = json.loads(output)
        assert len(data) == 1
        assert data[0]["title"] == "Test"

    def test_max_results_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "--max-results", "5"]):
                from scripts.ddgs_search import main

                main()

        mock_search_web.assert_called_once()
        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["max_results"] == 5

    def test_region_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "--region", "us-en"]):
                from scripts.ddgs_search import main

                main()

        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["region"] == "us-en"

    def test_safesearch_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "--safesearch", "off"]):
                from scripts.ddgs_search import main

                main()

        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["safesearch"] == "off"

    def test_timelimit_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "--timelimit", "d"]):
                from scripts.ddgs_search import main

                main()

        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["timelimit"] == "d"

    def test_backend_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "--backend", "html"]):
                from scripts.ddgs_search import main

                main()

        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["backend"] == "html"

    def test_proxy_option(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch(
                "sys.argv",
                ["ddgs_search.py", "test", "--proxy", "http://proxy.com:8080"],
            ):
                from scripts.ddgs_search import main

                main()

        call_kwargs = mock_search_web.call_args[1]
        assert call_kwargs["proxy"] == "http://proxy.com:8080"

    def test_verbose_output(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.return_value = []
            with patch("sys.argv", ["ddgs_search.py", "test", "-v"]):
                from scripts.ddgs_search import main

                with patch("sys.stdout", new=StringIO()) as fake_stdout:
                    main()

        output = fake_stdout.getvalue()
        assert "搜索参数:" in output

    def test_handles_keyboard_interrupt(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.side_effect = KeyboardInterrupt()
            with patch("sys.argv", ["ddgs_search.py", "test"]):
                from scripts.ddgs_search import main

                with patch("sys.stderr", new=StringIO()) as fake_stderr:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 130

        assert "搜索已取消" in fake_stderr.getvalue()

    def test_handles_general_exception(self):
        with patch("scripts.ddgs_search.search_web") as mock_search_web:
            mock_search_web.side_effect = Exception("Network error")
            with patch("sys.argv", ["ddgs_search.py", "test"]):
                from scripts.ddgs_search import main

                with patch("sys.stderr", new=StringIO()) as fake_stderr:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    assert exc_info.value.code == 1

        assert "错误: Network error" in fake_stderr.getvalue()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
