from momapa import JavaVersion

def test_parse_valid():
    jv_dict = {
        'component': 'java-runtime-gamma',
        'majorVersion': 17,
    }

    jv = JavaVersion.parse(jv_dict)

    assert jv is not None
    assert 'java-runtime-gamma' == jv.component
    assert 17 == jv.major_version

# Not having a JVM should just return None, not crash
def test_parse_notfound():
    jv = JavaVersion.parse(None)
    assert jv is None