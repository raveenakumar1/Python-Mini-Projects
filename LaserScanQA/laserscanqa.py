
"""
laserscanqa - a simple python framework for laser scan quality assessment
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
import json
import time
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ScanMetrics:
    """data class to store scan quality metrics"""
    point_count: int
    density: float
    noise_level: float
    completeness: float
    geometric_accuracy: float
    timestamp: float
    processing_time: float

class LaserScanQA:
    """
    a simple framework for laser scan quality assessment
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        initialize the laserscanqa framework
        
        Args:
            config: optional configuration dictionary
        """
        #use provided config or default config if none provided
        self.config = config or self._default_config()
        #initialize empty list to store metrics history
        self.metrics_history = []
        
    def _default_config(self) -> Dict:
        """return default configuration for quality assessment"""
        return {
            'density_threshold': 1000,  #minimum points per cubic meter required
            'noise_threshold': 0.05,    #maximum acceptable noise level
            'completeness_threshold': 0.9,  #minimum completeness ratio needed
            'max_processing_time': 30.0  #maximum processing time in seconds
        }
    
    def load_point_cloud(self, file_path: str) -> Optional[np.ndarray]:
        """
        load point cloud data from file
        
        Args:
            file_path: path to point cloud file
            
        Returns:
            numpy array of points (N, 3) or None if loading failed
        """
        try:
            #check if file is csv format
            if file_path.endswith('.csv'):
                #try to load without header first
                try:
                    points = np.loadtxt(file_path, delimiter=',')
                except ValueError:
                    #if header exists, skip the first row
                    points = np.loadtxt(file_path, delimiter=',', skiprows=1)
                return points
            else:
                #print error for unsupported file formats
                print(f"unsupported file format: {file_path}")
                return None
        except Exception as e:
            #catch any exceptions during file loading
            print(f"error loading point cloud: {e}")
            return None
    
    def calculate_density(self, points: np.ndarray) -> float:
        """
        calculate point density of the scan
        
        Args:
            points: point cloud data (N, 3)
            
        Returns:
            point density (points per cubic meter)
        """
        #check if points array is empty
        if len(points) == 0:
            return 0.0
            
        #calculate minimum coordinates of bounding box
        min_coords = np.min(points, axis=0)
        #calculate maximum coordinates of bounding box
        max_coords = np.max(points, axis=0)
        #calculate volume of bounding box
        volume = np.prod(max_coords - min_coords)
        
        #avoid division by zero for very small volumes
        if volume < 1e-10:
            return float('inf')
            
        #return density as points count divided by volume
        return len(points) / volume
    
    def estimate_noise_level(self, points: np.ndarray, k: int = 5) -> float:
        """
        estimate noise level in the point cloud using numpy only
        
        Args:
            points: point cloud data (N, 3)
            k: number of neighbors to consider (not used in this implementation)
            
        Returns:
            estimated noise level (0-1)
        """
        #check if there are enough points for noise estimation
        if len(points) < k + 1:
            return 0.0
            
        #calculate centroid of all points
        centroid = np.mean(points, axis=0)
        #calculate distances from each point to centroid
        distances = np.linalg.norm(points - centroid, axis=1)
        
        #normalize distances to 0-1 range
        max_distance = np.max(distances) if np.max(distances) > 0 else 1.0
        normalized_distances = distances / max_distance
        
        #noise level is the average normalized distance
        noise_level = np.mean(normalized_distances)
        
        #ensure noise level doesn't exceed 1.0
        return min(noise_level, 1.0)
    
    def check_completeness(self, points: np.ndarray, 
                          expected_density: Optional[float] = None) -> float:
        """
        check scan completeness based on expected density
        
        Args:
            points: point cloud data (N, 3)
            expected_density: expected point density (if None, use config)
            
        Returns:
            completeness ratio (0-1)
        """
        #use config density threshold if expected_density not provided
        if expected_density is None:
            expected_density = self.config['density_threshold']
            
        #calculate actual density of the point cloud
        actual_density = self.calculate_density(points)
        
        #avoid division by zero
        if expected_density == 0:
            return 0.0
            
        #calculate completeness ratio (capped at 1.0)
        completeness = min(actual_density / expected_density, 1.0)
        return completeness
    
    def assess_geometric_accuracy(self, points: np.ndarray, 
                                 reference_points: Optional[np.ndarray] = None) -> float:
        """
        assess geometric accuracy of the scan using numpy only
        
        Args:
            points: point cloud data to assess
            reference_points: reference point cloud (if available)
            
        Returns:
            geometric accuracy score (0-1)
        """
        #if no reference points provided, use distribution-based method
        if reference_points is None or len(reference_points) == 0:
            #calculate bounding box volume
            bbox_volume = np.prod(np.ptp(points, axis=0))
            #return default accuracy for very small volumes
            if bbox_volume < 1e-10:
                return 0.5
                
            #calculate standard deviation of points
            std_dev = np.std(points, axis=0)
            #calculate uniformity based on standard deviation
            uniformity = 1.0 / (1.0 + np.mean(std_dev))
            #return accuracy score (capped at 1.0)
            return min(uniformity * 1.5, 1.0)
        
        #with reference points, calculate distance-based accuracy
        min_distances = []
        #calculate minimum distance for each point to reference points
        for point in points:
            distances = np.linalg.norm(reference_points - point, axis=1)
            min_distances.append(np.min(distances))
        
        #calculate mean error distance
        mean_error = np.mean(min_distances)
        
        #convert error to accuracy score (0-1)
        accuracy = max(0, 1 - (mean_error / 0.1))  #assuming 0.1m is high error
        return accuracy
    
    def run_quality_assessment(self, points: np.ndarray, 
                              reference_points: Optional[np.ndarray] = None) -> ScanMetrics:
        """
        run comprehensive quality assessment on point cloud
        
        Args:
            points: point cloud data to assess
            reference_points: optional reference point cloud for comparison
            
        Returns:
            scanmetrics object with quality assessment results
        """
        #start timing the processing
        start_time = time.time()
        
        #check if points are valid
        if points is None or len(points) == 0:
            raise ValueError("empty or invalid point cloud data")
        
        #create scanmetrics object with all calculated metrics
        metrics = ScanMetrics(
            point_count=len(points),
            density=self.calculate_density(points),
            noise_level=self.estimate_noise_level(points),
            completeness=self.check_completeness(points),
            geometric_accuracy=self.assess_geometric_accuracy(points, reference_points),
            timestamp=time.time(),
            processing_time=0.0
        )
        
        #calculate actual processing time
        metrics.processing_time = time.time() - start_time
        #add metrics to history
        self.metrics_history.append(metrics)
        
        return metrics
    
    def generate_report(self, metrics: ScanMetrics) -> Dict:
        """
        generate a quality assessment report
        
        Args:
            metrics: scanmetrics object
            
        Returns:
            dictionary with detailed report
        """
        #create report dictionary structure
        report = {
            'summary': {
                'total_points': metrics.point_count,
                'overall_quality': self._calculate_overall_quality(metrics),
                'processing_time': metrics.processing_time
            },
            'detailed_metrics': {
                'density': {
                    'value': metrics.density,
                    'status': 'PASS' if metrics.density >= self.config['density_threshold'] else 'FAIL',
                    'threshold': self.config['density_threshold']
                },
                'noise_level': {
                    'value': metrics.noise_level,
                    'status': 'PASS' if metrics.noise_level <= self.config['noise_threshold'] else 'FAIL',
                    'threshold': self.config['noise_threshold']
                },
                'completeness': {
                    'value': metrics.completeness,
                    'status': 'PASS' if metrics.completeness >= self.config['completeness_threshold'] else 'FAIL',
                    'threshold': self.config['completeness_threshold']
                },
                'geometric_accuracy': {
                    'value': metrics.geometric_accuracy,
                    'status': 'PASS' if metrics.geometric_accuracy >= 0.7 else 'WARN'
                }
            },
            'timestamp': metrics.timestamp
        }
        
        return report
    
    def _calculate_overall_quality(self, metrics: ScanMetrics) -> float:
        """calculate overall quality score (0-1) based on weighted metrics"""
        #define weights for different quality factors
        weights = {
            'density': 0.25,
            'noise': 0.25,
            'completeness': 0.25,
            'accuracy': 0.25
        }
        
        #calculate individual scores for each metric
        density_score = min(metrics.density / self.config['density_threshold'], 1.0)
        noise_score = max(0, 1 - (metrics.noise_level / self.config['noise_threshold']))
        
        #calculate weighted overall quality score
        overall = (
            weights['density'] * density_score +
            weights['noise'] * noise_score +
            weights['completeness'] * metrics.completeness +
            weights['accuracy'] * metrics.geometric_accuracy
        )
        
        return overall
    
    def save_report(self, report: Dict, output_path: str):
        """
        save quality assessment report to file
        
        Args:
            report: report dictionary
            output_path: output file path
        """
        try:
            #write report to json file with indentation
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"report saved to {output_path}")
        except Exception as e:
            #catch any errors during file saving
            print(f"error saving report: {e}")
    
    def batch_process(self, file_paths: List[str], 
                     output_dir: str = "reports") -> List[Dict]:
        """
        process multiple point cloud files in batch
        
        Args:
            file_paths: list of file paths to process
            output_dir: output directory for reports
            
        Returns:
            list of reports
        """
        #create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        reports = []
        
        #process each file in the list
        for file_path in file_paths:
            print(f"processing: {file_path}")
            
            #load point cloud from file
            points = self.load_point_cloud(file_path)
            if points is None:
                continue
                
            #run quality assessment on loaded points
            metrics = self.run_quality_assessment(points)
            #generate report from metrics
            report = self.generate_report(metrics)
            
            #save individual report file
            filename = Path(file_path).stem + '_report.json'
            output_path = Path(output_dir) / filename
            self.save_report(report, str(output_path))
            
            #add report to results list
            reports.append(report)
        
        return reports
