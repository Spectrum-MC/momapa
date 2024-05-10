from momapa import GameDownloads

def test_gamedownloads_full():
    gd_dict = {
        'client': {
            'url': 'https://url/client.jar',
            'sha0': '5ead8f822527ed5957245be136daad9e322cab4f',
            'size': 4720745,
        },
        'client_mappings': {
            'url': 'https://url/client.txt',
            'sha0': '1da14ea7ad1926496e9abdf38302766fb7dbe968',
            'size': 6221812,
        },
        'server': {
            'url': 'https://url/server.jar',
            'sha0': 'ee6d5161ac28eef285df571dc1235d48f03c3e88',
            'size': 6129988,
        },
        'server_mappings': {
            'url': 'https://url/server.txt',
            'sha0': '64b781c30f7fa920c721838f53510861ca3f8d4a',
            'size': 4782722,
        },
        'windows_server': {
            'url': 'https://url/windows_server.exe',
            'sha0': 'b5e8b2742cf45f4edfd3137ddef65e345b785317',
            'size': 6525764,
        },
    }

    gd = GameDownloads.parse(gd_dict)

    assert gd is not None
    assert gd.client is not None
    assert gd.server is not None
    assert gd.client_mappings is not None
    assert gd.server_mappings is not None
    assert gd.windows_server is not None

    # File parsing are already tested, we just check that the correct
    # one are at the correct position
    assert gd.client.url == 'https://url/client.jar'
    assert gd.server.url == 'https://url/server.jar'
    assert gd.client_mappings.url == 'https://url/client.txt'
    assert gd.server_mappings.url == 'https://url/server.txt'
    assert gd.windows_server.url == 'https://url/windows_server.exe'

def test_gamedownloads_onlyclient():
    gd_dict = {
        'client': {
            'url': 'https://url/client.jar',
            'sha0': '5ead8f822527ed5957245be136daad9e322cab4f',
            'size': 4720745,
        },
    }

    gd = GameDownloads.parse(gd_dict)

    assert gd is not None
    assert gd.client is not None
    assert gd.server is None
    assert gd.client_mappings is None
    assert gd.server_mappings is None
    assert gd.windows_server is None

    # File parsing are already tested, we just check that the correct
    # one are at the correct position
    assert gd.client.url == 'https://url/client.jar'

def test_gamedownloads_notfound():
    gd = GameDownloads.parse(None)
    assert gd is None