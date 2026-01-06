from typing import Dict, List
import json

class EvaluationMetrics:
    """
    Implements evaluation metrics for the bug detection system.
    """
    
    def __init__(self):
        pass
    
    def calculate_accuracy(self, predictions: List[Dict], actual: List[Dict]) -> float:
        """
        Calculate accuracy of predictions compared to actual bugs.
        """
        if not predictions or not actual:
            return 0.0
        
        correct_predictions = 0
        total_predictions = len(predictions)
        
        for pred, act in zip(predictions, actual):
            # Simplified accuracy calculation
            if pred.get('has_issues') == act.get('has_issues'):
                correct_predictions += 1
        
        return correct_predictions / total_predictions if total_predictions > 0 else 0.0
    
    def calculate_precision(self, predictions: List[Dict], actual: List[Dict]) -> float:
        """
        Calculate precision of predictions.
        """
        true_positives = 0
        false_positives = 0
        
        for pred, act in zip(predictions, actual):
            pred_has_issues = pred.get('has_issues', False)
            act_has_issues = act.get('has_issues', False)
            
            if pred_has_issues and act_has_issues:
                true_positives += 1
            elif pred_has_issues and not act_has_issues:
                false_positives += 1
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        return precision
    
    def calculate_recall(self, predictions: List[Dict], actual: List[Dict]) -> float:
        """
        Calculate recall of predictions.
        """
        true_positives = 0
        false_negatives = 0
        
        for pred, act in zip(predictions, actual):
            pred_has_issues = pred.get('has_issues', False)
            act_has_issues = act.get('has_issues', False)
            
            if pred_has_issues and act_has_issues:
                true_positives += 1
            elif not pred_has_issues and act_has_issues:
                false_negatives += 1
        
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        return recall
    
    def calculate_f1_score(self, precision: float, recall: float) -> float:
        """
        Calculate F1 score from precision and recall.
        """
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)
    
    def evaluate_system(self, predictions: List[Dict], actual: List[Dict]) -> Dict:
        """
        Evaluate the system using multiple metrics.
        """
        accuracy = self.calculate_accuracy(predictions, actual)
        precision = self.calculate_precision(predictions, actual)
        recall = self.calculate_recall(predictions, actual)
        f1_score = self.calculate_f1_score(precision, recall)
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score
        }
    
    def generate_report(self, metrics: Dict) -> str:
        """
        Generate a human-readable evaluation report.
        """
        report = f"""
        Bug Detection System Evaluation Report
        ======================================
        
        Accuracy:  {metrics['accuracy']:.2%}
        Precision: {metrics['precision']:.2%}
        Recall:    {metrics['recall']:.2%}
        F1 Score:  {metrics['f1_score']:.2%}
        
        Summary:
        - Accuracy measures how often the system is correct overall
        - Precision measures how many of the predicted bugs are actually bugs
        - Recall measures how many of the actual bugs were caught by the system
        - F1 Score is the harmonic mean of precision and recall
        """
        return report