from momapa import Logging


def test_logging_file():
    data = {
        'client': {
            'type': 'log4j2-xml',
            'argument': '-Dlog4j.configurationFile=${path}',
            'file': {
                'id': 'client-1.12.xml',
                'sha1': 'bd65e7d2e3c237be76cfbef4c2405033d7f91521',
                'size': 888,
                'url': 'https://url/client-1.12.xml',
            }
        }
    }

    l = Logging.parse(data)

    assert l is not None
    assert l.client is not None
    assert l.client.type == 'log4j2-xml'
    assert l.client.argument == '-Dlog4j.configurationFile=${path}'
    assert l.client.file is not None
    assert l.client.file.path == 'client-1.12.xml'
