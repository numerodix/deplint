from deplint.data_sources.site_packages.scripts.query_installed import main


def test_query_packages():
    results_dict = main(['packaging', 'six', 'not-installed-package'])
    
    # Some high level smoke testing - the script is tested more thoroughly in
    # the analyzer/integration tests
    assert 'errors' in results_dict
    assert results_dict['errors'] == []

    assert 'packages' in results_dict
    assert len(results_dict['packages']) >= 2

    # happy flow
    assert results_dict['packages']['packaging']['errors'] == []
    assert results_dict['packages']['packaging']['top_levels'] == ['packaging']

    assert results_dict['packages']['six']['errors'] == []
    assert results_dict['packages']['six']['top_levels'] == ['six']

    # package not installed
    assert 'not-installed-package' in results_dict['packages']
    assert results_dict['packages']['not-installed-package']['errors'] == [
        'error-not-installed'
    ]
