import csv
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_reports import read_csv,summarize

class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.issues=read_csv('github_issues_snapshot.csv')
        self.prs=read_csv('github_prs_snapshot.csv')
    def test_snapshot_counts(self):
        s=summarize(self.issues,self.prs)
        self.assertEqual(s['issues_closed']+s['issues_open'],s['issues_total'])
        self.assertEqual(s['prs_merged']+s['prs_open']+s['prs_closed_without_merge'],s['prs_total'])
        if not (ROOT/'data'/'refresh_info.json').exists():
            self.assertEqual((s['issues_total'],s['issues_closed'],s['issues_open']),(137,118,19))
            self.assertEqual((s['prs_total'],s['prs_merged'],s['prs_open'],s['prs_closed_without_merge']),(95,88,5,2))
    def test_uniqueness_and_links(self):
        self.assertEqual(len(set(x['issue_number'] for x in self.issues)),len(self.issues))
        self.assertEqual(len(set(x['pr_number'] for x in self.prs)),len(self.prs))
        for x in self.issues:
            self.assertTrue(x['source_url'].endswith('/issues/'+x['issue_number']))
            self.assertEqual(x['state']=='closed',bool(x['closed_date']))
        for x in self.prs:
            self.assertEqual(x['outcome']=='merged',bool(x['merged_date']))
    def test_sources_are_separate(self):
        self.assertTrue((ROOT/'data'/'github_issues_snapshot.csv').is_file())
        self.assertFalse((ROOT/'data'/'github_issues_snapshot.csv').samefile(ROOT/'data'/'github_prs_snapshot.csv'))

if __name__=='__main__':unittest.main()
