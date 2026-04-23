from alife_biosphere.ant_sandbox import AntSandboxConfig


def test_ant_sandbox_config_round_trip_shape() -> None:
    config = AntSandboxConfig()
    payload = config.to_dict()
    assert payload["width"] == 128
    assert payload["height"] == 96
    assert len(payload["food_patches"]) == 3
    assert len(payload["colonies"]) == 3
    assert payload["ants"]["ant_count"] == 32
    assert payload["terrain"]["enabled"] is True
