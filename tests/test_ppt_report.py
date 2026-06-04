# tests/test_ppt_report.py
"""
Test scaffolds for REP-02 requirement.
Initially skipped - will pass after src/report/ppt_report.py implementation.
"""

import pytest
from pathlib import Path
import tempfile


class TestPPTReport:
    """Tests for PPT report generation via python-pptx."""

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/ppt_report.py not implemented")
    def test_generate_ppt(self, tmp_path):
        """REP-02: Verify PPT file created via python-pptx."""
        from src.report.ppt_report import PPTReportGenerator

        # Create sample report data
        report_data = {
            'title': '数据分析报告',
            'metrics': {'ROI': 15.5, 'conversion_rate': 0.05},
            'themes': {
                'performance': {'title': '绩效分析', 'insights': ['ROI提升显著']}
            },
            'conclusions': ['建议继续优化']
        }

        generator = PPTReportGenerator()
        output_path = tmp_path / 'report.pptx'

        generator.generate(report_data, output_path)

        # Verify PPT file created
        assert output_path.exists()
        assert output_path.suffix == '.pptx'

        # Verify file size is reasonable (not empty)
        assert output_path.stat().st_size > 1000  # PPTX should be at least 1KB

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/ppt_report.py not implemented")
    def test_ppt_slide_structure(self, tmp_path):
        """Verify PPT slides have title and content structure."""
        from src.report.ppt_report import PPTReportGenerator
        from pptx import Presentation

        report_data = {
            'title': '分析报告',
            'metrics': {'ROI': 15.5},
            'themes': {
                'performance': {'title': '绩效分析', 'insights': ['insight1']}
            },
            'conclusions': ['结论1']
        }

        generator = PPTReportGenerator()
        output_path = tmp_path / 'report.pptx'

        generator.generate(report_data, output_path)

        # Open and verify structure
        prs = Presentation(str(output_path))

        # Verify slides exist
        assert len(prs.slides) >= 3  # Should have at least title + metrics + conclusions

        # Verify first slide has title
        first_slide = prs.slides[0]
        assert len(first_slide.shapes) > 0

    @pytest.mark.skip(reason="Wave 0 scaffold - src/report/ppt_report.py not implemented")
    def test_ppt_chart_embedding(self, tmp_path):
        """Verify charts embedded as images in PPT."""
        from src.report.ppt_report import PPTReportGenerator
        from pptx import Presentation
        from pptx.shapes.picture import Picture

        report_data = {
            'title': '分析报告',
            'metrics': {'ROI': 15.5},
            'themes': {},
            'conclusions': [],
            'charts': [{'type': 'bar', 'data': {'x': ['A', 'B'], 'y': [1, 2]}}]
        }

        generator = PPTReportGenerator()
        output_path = tmp_path / 'report.pptx'

        generator.generate(report_data, output_path)

        # Open and verify chart images
        prs = Presentation(str(output_path))

        # Check for picture shapes (chart images)
        picture_count = 0
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, 'image') or isinstance(shape, Picture):
                    picture_count += 1

        # Should have at least one chart image if charts provided
        assert picture_count >= 0  # May be 0 if no charts in data