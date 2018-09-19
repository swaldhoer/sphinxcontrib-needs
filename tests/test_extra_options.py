import re

from sphinx_testing import with_app


@with_app(buildername='html', srcdir='doc_test/extra_options')
def test_custom_attributes_appear(app, status, warning):
    app.build()

    html = (app.outdir / 'index.html').read_text()

    # Custom options should appear
    # assert 'introduced: <cite>1.0.0</cite>' in html
    assert '<div class="extra_option line">updated: <span class="needs-extra-option updated">1.5.1</span></div>' \
           in html
    assert '<div class="extra_option line">introduced: <span class="needs-extra-option introduced">1.0.0</span></div>' \
           in html
    assert '<div class="extra_option line">impacts: <span class="needs-extra-option impacts">component_a</span></div>' \
           in html

    tables = re.findall("(<table .*?</table>)", html, re.DOTALL)
    assert len(tables) == 2

    # First table should have all requirements
    assert 'R_12345' in tables[0]
    assert 'R_12346' in tables[0]
    assert all(column in tables[0] for column in ('Introduced', 'Updated',
                                                  'Impacts'))

    # Second table should only have component A requirements
    assert 'R_12345' in tables[1]
    assert 'R_12346' not in tables[1]

    # Need list should only have component B requirements
    items = re.findall('(<div class="line" id="needlist-index-.*?</div>)',
                       html, re.DOTALL)
    assert len(items) == 1
    assert 'R_12346' in items[0]