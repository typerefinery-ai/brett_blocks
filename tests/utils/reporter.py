"""
Reporter Module - Generate comprehensive test reports
"""
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import json


class TestReporter:
    """Generate JSON and Markdown test reports"""
    
    def __init__(self, generated_dir: Path):
        """
        Initialize reporter
        
        Args:
            generated_dir: Path to tests/generated/ directory
        """
        self.generated_dir = Path(generated_dir)
        self.results = []
    
    def add_result(
        self, 
        object_id: str, 
        object_type: str,
        status: str,  # PASS, FAIL, ERROR, SKIPPED
        differences: Dict = None,
        execution_time_ms: float = 0,
        error_message: str = None
    ):
        """
        Add a test result
        
        Args:
            object_id: STIX object ID
            object_type: STIX object type
            status: Test status (PASS, FAIL, ERROR, SKIPPED)
            differences: DeepDiff differences (if status=FAIL)
            execution_time_ms: Execution time in milliseconds
            error_message: Error message (if status=ERROR)
        """
        self.results.append({
            'object_id': object_id,
            'object_type': object_type,
            'status': status,
            'differences': differences or {},
            'execution_time_ms': execution_time_ms,
            'error_message': error_message,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Returns:
            Dictionary with summary statistics:
            {
                'total_objects': int,
                'passed': int,
                'failed': int,
                'errors': int,
                'pass_rate': float,
                'by_type': {type: {total, passed, failed, errors}},
                'failures': [list of failed objects]
            }
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        errors = sum(1 for r in self.results if r['status'] == 'ERROR')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIPPED')
        
        # Aggregate by type
        by_type = {}
        for result in self.results:
            obj_type = result['object_type']
            if obj_type not in by_type:
                by_type[obj_type] = {
                    'total': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'skipped': 0
                }
            by_type[obj_type]['total'] += 1
            if result['status'] == 'PASS':
                by_type[obj_type]['passed'] += 1
            elif result['status'] == 'FAIL':
                by_type[obj_type]['failed'] += 1
            elif result['status'] == 'ERROR':
                by_type[obj_type]['errors'] += 1
            elif result['status'] == 'SKIPPED':
                by_type[obj_type]['skipped'] += 1
        
        return {
            'total_objects': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'skipped': skipped,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'by_type': by_type,
            'failures': [r for r in self.results if r['status'] in ['FAIL', 'ERROR']]
        }
    
    def save_reports(self):
        """Save JSON and Markdown reports"""
        # Ensure reports directory exists
        reports_dir = self.generated_dir / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Save detailed results
        with open(reports_dir / 'test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        
        # Save summary
        summary = self.generate_summary()
        with open(reports_dir / 'test_summary.json', 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2)
        
        # Generate markdown
        self._generate_markdown_report(summary, reports_dir)
    
    def _generate_markdown_report(self, summary: Dict, reports_dir: Path):
        """
        Generate human-readable Markdown report
        
        Args:
            summary: Summary statistics dictionary
            reports_dir: Directory to save markdown report
        """
        md_lines = [
            "# StixORM Block Testing Report",
            f"\n**Generated:** {datetime.utcnow().isoformat()}",
            "\n## Summary\n",
            f"- **Total Objects:** {summary['total_objects']}",
            f"- **Passed:** {summary['passed']} ✅",
            f"- **Failed:** {summary['failed']} ❌",
            f"- **Errors:** {summary['errors']} ⚠️",
            f"- **Skipped:** {summary.get('skipped', 0)} ⏭️",
            f"- **Pass Rate:** {summary['pass_rate']:.1f}%",
            "\n## Results by Type\n"
        ]
        
        for obj_type, stats in sorted(summary['by_type'].items()):
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            md_lines.append(
                f"- **{obj_type}**: {stats['passed']}/{stats['total']} passed ({pass_rate:.1f}%)"
            )
        
        if summary['failures']:
            md_lines.append("\n## Failures\n")
            for failure in summary['failures']:
                md_lines.append(f"### {failure['object_type']} - `{failure['object_id']}`")
                md_lines.append(f"- **Status:** {failure['status']}")
                if failure.get('error_message'):
                    md_lines.append(f"- **Error:** {failure['error_message']}")
                if failure.get('differences'):
                    md_lines.append(f"- **Differences:** See `test_results.json` for details")
                md_lines.append("")
        
        with open(reports_dir / 'test_summary.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_lines))
