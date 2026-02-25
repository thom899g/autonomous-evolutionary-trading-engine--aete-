"""
Firebase integration manager for AETE state persistence and real-time updates.
Handles all Firestore operations with error handling and retry logic.
"""
import logging
from typing import Dict, Any, Optional, List
import time
from datetime import datetime
import json
from google.cloud import firestore
from google.cloud.exceptions import GoogleCloudError
from aete_config import logger

class FirebaseManager:
    """Manages Firebase Firestore connections and operations"""
    
    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize Firebase connection.
        
        Args:
            project_id: Firebase project ID. If None, uses default credentials.
        
        Raises:
            GoogleCloudError: If Firebase connection fails
        """
        self.logger = logging.getLogger("AETE.Firebase")
        
        try:
            # Initialize Firebase
            self.db = firestore.Client(project=project_id)
            self.logger.info(f"Firebase Firestore initialized for project: {project_id or 'default'}")
            
            # Test connection
            test_doc = self.db.collection("_health_check").document("connection_test")
            test_doc.set({"timestamp": datetime.utcnow().isoformat(), "status": "active"})
            test_doc.delete()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Firebase: {str(e)}")
            raise GoogleCloudError(f"Firebase initialization failed: {str(e)}")
    
    def save_strategy(self, 
                     strategy_id: str, 
                     strategy_data: Dict[str, Any], 
                     collection: str = "aete_strategies") -> bool:
        """
        Save strategy to Firestore with retry logic.