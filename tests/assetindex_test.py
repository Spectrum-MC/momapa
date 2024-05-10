from momapa import AssetIndex


def test_asset_valid():
    ai_dict = {
        'id': '1.17',
        'sha1': 'f425401a00adf0112fde624ee80c66333530f8a1',
        'size': 346398,
        'totalSize': 348383264,
        'url': 'https://url/1.17.json',
    }

    ai = AssetIndex.parse(ai_dict)

    assert ai is not None
    assert ai.id == '1.17'
    assert ai.hash == 'f425401a00adf0112fde624ee80c66333530f8a1'
    assert ai.size == 346398
    assert ai.total_size == 348383264
    assert ai.url == 'https://url/1.17.json'


def test_asset_notfound():
    ai = AssetIndex.parse(None)
    assert ai is None