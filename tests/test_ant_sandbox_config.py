from alife_biosphere.ant_sandbox import AntSandboxConfig


def test_ant_sandbox_config_round_trip_shape() -> None:
    config = AntSandboxConfig()
    payload = config.to_dict()
    assert payload["width"] == 64
    assert payload["height"] == 48
    assert len(payload["food_patches"]) == 2
    assert payload["ants"]["ant_count"] == 32
