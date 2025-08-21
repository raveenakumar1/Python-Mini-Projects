#!/usr/bin/env python3
"""
main script to analyze laser scans using laserscanqa framework
"""

from laserscanqa import LaserScanQA
from pathlib import Path
import json

def analyze_single_scan():
    """analyze a single scan file"""
    print("=== SINGLE SCAN ANALYSIS ===")
    
    #initialize the quality assessment framework
    qa = LaserScanQA()
    
    #scan file path here
    scan_file = "data/scan_good.csv"  #file path
    
    #load the point cloud
    print(f"loading scan: {scan_file}")
    points = qa.load_point_cloud(scan_file)
    
    #check if points loaded successfully
    if points is None:
        print("failed to load point cloud. please check the file path.")
        return
    
    #print number of points loaded
    print(f"loaded {len(points):,} points")
    
    #run quality assessment on the points
    print("running quality assessment...")
    metrics = qa.run_quality_assessment(points)
    
    #generate report from the metrics
    report = qa.generate_report(metrics)
    
    #display the results summary
    print("\n" + "="*50)
    print("QUALITY ASSESSMENT RESULTS")
    print("="*50)
    print(f"overall quality: {report['summary']['overall_quality']:.2%}")
    print(f"total points: {report['summary']['total_points']:,}")
    print(f"processing time: {report['summary']['processing_time']:.3f}s")
    
    #display detailed metrics with their status
    print("\ndetailed metrics:")
    for metric_name, metric_data in report['detailed_metrics'].items():
        print(f"  {metric_name.upper():<18}: {metric_data['value']:.3f} [{metric_data['status']}]")
    
    #save the report to json file
    output_file = "scan_quality_report.json"
    qa.save_report(report, output_file)
    print(f"\nfull report saved to: {output_file}")

def analyze_batch_scans():
    """analyze multiple scans in batch"""
    print("\n=== BATCH SCAN ANALYSIS ===")
    
    #initialize the quality assessment framework
    qa = LaserScanQA()
    
    #find all csv files in data directory
    data_dir = Path("data")
    csv_files = list(data_dir.glob("*.csv"))
    
    #check if any csv files found
    if not csv_files:
        print("no csv files found in data folder!")
        print("run 'create_sample_data.py' first to create sample files.")
        return
    
    #list all found csv files
    print(f"found {len(csv_files)} scan files:")
    for file in csv_files:
        print(f"  - {file.name}")
    
    #process all files in batch
    print("\nprocessing files...")
    reports = qa.batch_process([str(f) for f in csv_files], "reports")
    
    #confirm reports generated
    print(f"\ngenerated {len(reports)} quality reports!")
    print("reports saved in 'reports/' folder:")
    
    #list all generated report files
    report_dir = Path("reports")
    for report_file in report_dir.glob("*.json"):
        print(f"  - {report_file.name}")

def read_report_example():
    """example of how to read and use saved reports"""
    print("\n=== READING SAVED REPORTS ===")
    
    #specify report file to read
    report_file = "scan_quality_report.json"
    
    #check if report file exists
    if not Path(report_file).exists():
        print(f"no report file found at {report_file}")
        print("run single scan analysis first.")
        return
    
    #read the json report file
    with open(report_file, 'r') as f:
        report = json.load(f)
    
    #display report information
    print(f"report from: {report_file}")
    print(f"overall quality score: {report['summary']['overall_quality']:.3f}")
    
    #check if all quality standards are met
    all_pass = all(metric['status'] == 'PASS' 
                  for metric in report['detailed_metrics'].values() 
                  if 'threshold' in metric)
    
    #print quality standards status
    print(f"meets all quality standards: {'YES' if all_pass else 'NO'}")

if __name__ == "__main__":
    #run the single scan analysis function
    analyze_single_scan()
    #run the batch scan analysis function
    analyze_batch_scans()
    #run the report reading example function
    read_report_example()