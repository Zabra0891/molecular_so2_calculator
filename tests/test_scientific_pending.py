"""Explicit blocked validation; no fabricated scientific expected values."""
import pytest

@pytest.mark.scientific
@pytest.mark.parametrize('topic', [
    'Sample-specific applicability of assumed ionic strength 0.056 M',
    'Measured molecular SO2 reference values across declared domain',
    'Scientific domain and acceptable absolute/relative errors',
])
def test_external_reference_pending(topic):
    pytest.skip(f'Source and reference dataset required: {topic}')
