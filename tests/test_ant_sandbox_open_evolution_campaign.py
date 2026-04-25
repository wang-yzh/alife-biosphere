import json
from pathlib import Path

from alife_biosphere.ant_sandbox.campaign import run_multi_niche_open_evolution_campaign


def test_multi_niche_campaign_generates_branch_family_outputs(tmp_path: Path) -> None:
    manifest = run_multi_niche_open_evolution_campaign(
        tmp_path / "campaign",
        campaign_id="campaign_test",
        root_tick=20,
        fork_additional_ticks=10,
        fork_seeds=(11, 13),
    )
    assert manifest["campaign_id"] == "campaign_test"
    assert manifest["root_branch"]["branch_id"] == "campaign_test_root"
    assert len(manifest["fork_branches"]) == 2
    assert Path(manifest["root_branch"]["checkpoint_final"]).exists()
    assert Path(manifest["root_branch"]["observer_html"]).exists()
    assert Path(manifest["comparison_json"]).exists()
    assert Path(manifest["open_endedness_json"]).exists()
    assert Path(tmp_path / "campaign" / "campaign_manifest.json").exists()
    assert Path(tmp_path / "campaign" / "campaign_summary.md").exists()


def test_multi_niche_campaign_manifest_references_metrics_and_comparison(tmp_path: Path) -> None:
    manifest = run_multi_niche_open_evolution_campaign(
        tmp_path / "campaign",
        campaign_id="campaign_manifest",
        root_tick=18,
        fork_additional_ticks=8,
        fork_seeds=(17, 19),
    )
    comparison = json.loads(Path(manifest["comparison_json"]).read_text(encoding="utf-8"))
    open_metrics = json.loads(Path(manifest["open_endedness_json"]).read_text(encoding="utf-8"))
    assert comparison["checkpoint_count"] == 3
    assert comparison["family_count"] >= 1
    assert open_metrics["comparison_id"] == comparison["comparison_id"]
    assert "metric_families" in open_metrics
    assert "ecological_dependency" in open_metrics["metric_families"]
