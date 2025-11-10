"""
Phase 5: Reporting Tests
"""
import pytest
from pathlib import Path


@pytest.mark.reporting
def test_generate_final_reports(test_reporter, generated_dir):
    """Generate final JSON and Markdown reports"""
    test_reporter.save_reports()
    
    reports_dir = generated_dir / 'reports'
    
    # Verify reports exist
    assert (reports_dir / 'test_results.json').exists(), "test_results.json not created"
    assert (reports_dir / 'test_summary.json').exists(), "test_summary.json not created"
    assert (reports_dir / 'test_summary.md').exists(), "test_summary.md not created"


@pytest.mark.reporting
def test_summary_completeness(test_reporter):
    """Verify summary includes all metrics"""
    summary = test_reporter.generate_summary()
    
    assert 'total_objects' in summary
    assert 'passed' in summary
    assert 'failed' in summary
    assert 'pass_rate' in summary
    assert 'by_type' in summary


@pytest.mark.reporting
def test_display_summary(test_reporter, capsys):
    """Display summary to console"""
    summary = test_reporter.generate_summary()
    
    print("\n" + "="*60)
    print("STIXORM BLOCK TESTING SUMMARY")
    print("="*60)
    print(f"Total Objects:  {summary['total_objects']}")
    print(f"Passed:         {summary['passed']} ✅")
    print(f"Failed:         {summary['failed']} ❌")
    print(f"Errors:         {summary['errors']} ⚠️")
    print(f"Skipped:        {summary.get('skipped', 0)} ⏭️")
    print(f"Pass Rate:      {summary['pass_rate']:.1f}%")
    print("="*60)
    
    if summary['by_type']:
        print("\nResults by Type:")
        for obj_type, stats in sorted(summary['by_type'].items()):
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {obj_type}: {stats['passed']}/{stats['total']} ({pass_rate:.1f}%)")
    
    print("="*60)
    
    captured = capsys.readouterr()
    assert "STIXORM BLOCK TESTING SUMMARY" in captured.out


@pytest.mark.reporting
def test_report_includes_failures(test_reporter):
    """Verify report includes failure details"""
    summary = test_reporter.generate_summary()
    
    if summary['failed'] > 0 or summary['errors'] > 0:
        assert 'failures' in summary
        assert len(summary['failures']) > 0
