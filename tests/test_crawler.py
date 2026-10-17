import os
import pytest
from crawler.crawler_state import CrawlerState

def test_crawler_state(tmp_path):
    output_dir = str(tmp_path)
    state = CrawlerState(output_dir)
    
    state.add_discovered_case("WPCRL/100/2026")
    assert "WPCRL/100/2026" in state.state["discovered_cases"]
    
    state.mark_processed("WPCRL/100/2026")
    assert "WPCRL/100/2026" in state.state["processed_cases"]
    
    state.mark_failed("WPCRL/101/2026", "NETWORK_ERROR", "Connection timed out")
    assert "WPCRL/101/2026" in state.state["failed_cases"]
    
    # Reload from file
    reloaded = CrawlerState(output_dir)
    assert "WPCRL/100/2026" in reloaded.state["processed_cases"]
    assert "WPCRL/101/2026" in reloaded.state["failed_cases"]
