from lineup_info_collector.crawlers.devalue import unflatten


def test_unflatten_plain_object():
    flat = [{"data": 1}, {"page": 2}, {"acts": 3}, [4], {"url": 5, "title": 6}, "/acts/x", "X"]
    assert unflatten(flat) == {"data": {"page": {"acts": [{"url": "/acts/x", "title": "X"}]}}}


def test_unflatten_empty_array():
    flat = [{"genres": 1}, []]
    assert unflatten(flat) == {"genres": []}


def test_unflatten_primitives():
    flat = [{"a": 1, "b": 2, "c": 3}, 42, True, None]
    assert unflatten(flat) == {"a": 42, "b": True, "c": None}


def test_unflatten_unwraps_custom_reducer():
    # Vue's "ShallowReactive"/"Reactive"/"Ref" tags wrap a single payload reference.
    flat = [["ShallowReactive", 1], {"title": 2}, "hello"]
    assert unflatten(flat) == {"title": "hello"}
