
#!/usr/bin/env python3
"""
create sample csv files for testing the laserscanqa framework
"""

import numpy as np
from pathlib import Path

def create_sample_scans():
    """create sample scan csv files without headers"""
    
    #create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    #create 3 sample scans with different qualities
    print("creating sample scan files...")
    
    #scan 1: good quality (high density, low noise)
    #generate 8000 random points in 3d space with larger volume
    points1 = np.random.rand(8000, 3) * 2.0  #more points in larger volume
    #save points to csv file without any headers or comments
    np.savetxt(data_dir / "scan_good.csv", points1, delimiter=",", comments="")
    print("created scan_good.csv - high quality scan")
    
    #scan 2: medium quality (medium density, some noise)
    #generate 4000 random points in smaller volume
    points2 = np.random.rand(4000, 3) * 1.5
    #add some gaussian noise to simulate real-world imperfections
    noise = np.random.normal(0, 0.05, points2.shape)
    points2 += noise
    #save the noisy points to csv file
    np.savetxt(data_dir / "scan_medium.csv", points2, delimiter=",", comments="")
    print("created scan_medium.csv - medium quality scan")
    
    #scan 3: poor quality (low density, high noise)
    #generate only 1500 random points in small volume
    points3 = np.random.rand(1500, 3) * 1.0
    #add significant noise to simulate very poor quality scan
    noise = np.random.normal(0, 0.1, points3.shape)
    points3 += noise
    #save the very noisy points to csv file
    np.savetxt(data_dir / "scan_poor.csv", points3, delimiter=",", comments="")
    print("created scan_poor.csv - poor quality scan")
    
    #print summary of created files
    print(f"\nsample files created in '{data_dir}/' directory:")
    print("  - scan_good.csv (high quality)")
    print("  - scan_medium.csv (medium quality)") 
    print("  - scan_poor.csv (low quality)")

if __name__ == "__main__":
    #call the function to create sample scans when script is run
    create_sample_scans()
