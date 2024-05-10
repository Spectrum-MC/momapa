from momapa import File, PathFile

def test_parse_file_valid():
    file_dict = {
        'url': 'https://url/client.jar',
        'size': 18631012,
        'sha1': '3a008c012bd6bba29054701c7797493523660c57',
    }

    file = File.parse(file_dict)

    assert file is not None
    assert 'https://url/client.jar' == file.url
    assert 18631012 == file.size
    assert '3a008c012bd6bba29054701c7797493523660c57' == file.hash

# Missing a file should just return None, not crash
# E.g. trying to parse downloads.server_mappings on old versions
# that do not have it
def test_parse_file_notfound():
    file = File.parse(None)
    assert file is None

def test_parse_pathfile_valid():
    file_dict = {
        'path': 'com/mojang/patchy/1.3.9/patchy-1.3.9.jar',
        'url': 'https://url/patchy-1.3.9.jar',
        'size': 23581,
        'sha1': 'eb8bb7b66fa0e2152b1b40b3856e82f7619439ee',
    }

    file = PathFile.parse(file_dict)

    assert file is not None
    assert 'https://url/patchy-1.3.9.jar' == file.url
    assert 23581 == file.size
    assert 'eb8bb7b66fa0e2152b1b40b3856e82f7619439ee' == file.hash
    assert 'com/mojang/patchy/1.3.9/patchy-1.3.9.jar' == file.path

# Missing a pathfile should just return None, not crash
# E.g. trying to parse downloads.artifact on a lib that
# only has natives
def test_parse_pathfile_notfound():
    file = PathFile.parse(None)
    assert file is None