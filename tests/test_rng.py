from alife_biosphere.rng import derive_seed


def test_same_seed_same_label_is_stable() -> None:
    assert derive_seed(7, "root") == derive_seed(7, "root")


def test_same_seed_different_labels_differ() -> None:
    assert derive_seed(7, "a") != derive_seed(7, "b")
