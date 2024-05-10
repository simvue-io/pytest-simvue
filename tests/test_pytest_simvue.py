def test_simvue_fixture(pytester):
    """Make sure that pytest accepts our fixture."""

    # create a temporary pytest test module
    pytester.makepyfile("""
        def test_sth(simvue):
            assert simvue
    """)

    pytester.makepyfile("""
        import time
        def test_sth(simvue):
            time.sleep(1)
            assert simvue
    """)

    # run pytest with the following cmd args
    result = pytester.runpytest(
        '-v'
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*::test_sth PASSED*',
    ])

    # make sure that we get a '0' exit code for the testsuite
    assert result.ret == 0

