# cloud_langflow_api.py - PRODUCTION VERSION with Secrets Support
"""
Cloud Langflow API Integration - PRODUCTION VERSION
Uses Streamlit secrets for secure credential management
"""

import requests
import json
import uuid
import time
import streamlit as st
from typing import Optional, Dict, Any, List

class CloudLangflowAPI:
    
    def __init__(self):
        """Initialize with cloud Langflow endpoints from secrets"""
        
        # ===== LOAD FROM STREAMLIT SECRETS =====
        try:
            self.endpoints = {
                "qna_agent": {
                    "url": st.secrets["api"]["QNA_AGENT_URL"],
                    "flow_name": "QNA Agent"
                },
                "report_analyzer": {
                    "url": st.secrets["api"]["REPORT_ANALYZER_URL"],
                    "flow_name": "Report Analyzer"
                },
                "prescription_analyzer": {
                    "url": st.secrets["api"]["PRESCRIPTION_ANALYZER_URL"],
                    "flow_name": "Prescription Analyzer"
                },
                "bill_analyzer": {
                    "url": st.secrets["api"]["BILL_ANALYZER_URL"],
                    "flow_name": "Bill Analyzer"
                },
                "hospital_finder": {
                    "url": st.secrets["api"]["HOSPITAL_FINDER_URL"],
                    "flow_name": "Hospital Finder"
                }
            }
            
            self.app_token = st.secrets["api"]["APP_TOKEN"]
            self.org_id = st.secrets["api"]["ORG_ID"]
            
        except Exception as e:
            st.error(f"Failed to load secrets: {str(e)}")
            st.info("Please check your Streamlit secrets configuration")
            raise e
        
        self.base_headers = {
            "X-DataStax-Current-Org": self.org_id,
            "Authorization": f"Bearer {self.app_token}",
            "Content-Type": "application/json"
        }
        
        self.max_retries = 2
        self.retry_delay = 3
    
    def _call_api(self, flow_key: str, input_value: str, files: List = None) -> Dict[str, Any]:
        """Call Langflow cloud API"""
        
        if flow_key not in self.endpoints:
            return {"success": False, "error": f"Flow {flow_key} not found"}
        
        url = self.endpoints[flow_key]["url"]
        
        # If files are present, use multipart upload
        if files:
            return self._call_api_with_files(url, input_value, files)
        
        # Standard JSON payload
        payload = {
            "output_type": "chat",
            "input_type": "chat",
            "input_value": input_value,
            "session_id": str(uuid.uuid4())
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=self.base_headers,
                    timeout=60
                )
                
                return self._handle_response(response, flow_key)
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                return {
                    "success": False,
                    "error": f"API call failed: {str(e)}",
                    "message": self._get_demo_response(flow_key, input_value, is_error=True)
                }
        
        return {"success": False, "error": "Max retries exceeded"}
    
    def _call_api_with_files(self, url: str, input_value: str, files: List) -> Dict[str, Any]:
        """Call Langflow API with file uploads using multipart/form-data"""
        
        # Prepare multipart form data
        files_data = []
        
        # Add the text input
        files_data.append(('input_value', (None, input_value)))
        
        # Add other fields
        files_data.append(('output_type', (None, 'chat')))
        files_data.append(('input_type', (None, 'chat')))
        files_data.append(('session_id', (None, str(uuid.uuid4()))))
        
        # Add files
        for file in files:
            mime_type = file.type or 'application/octet-stream'
            file_name = file.name
            file_content = file.getvalue()
            
            files_data.append(
                ('files', (file_name, file_content, mime_type))
            )
        
        # Prepare headers (remove Content-Type for multipart)
        headers = self.base_headers.copy()
        headers.pop('Content-Type', None)
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    files=files_data,
                    headers=headers,
                    timeout=120
                )
                
                return self._handle_response(response, "file_upload")
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                    continue
                return {
                    "success": False,
                    "error": f"File upload failed: {str(e)}",
                    "message": self._get_demo_response("file_upload", input_value, is_error=True)
                }
        
        return {"success": False, "error": "Max retries exceeded"}
    
    def _handle_response(self, response: requests.Response, flow_key: str) -> Dict[str, Any]:
        """Handle API response"""
        
        if response.status_code == 200:
            try:
                data = response.json()
                
                # Extract message using improved method
                message = self._extract_message(data)
                
                if message:
                    return {
                        "success": True, 
                        "message": message,
                        "raw": data
                    }
                else:
                    # If no message found, return the whole JSON as string
                    return {
                        "success": True, 
                        "message": json.dumps(data, indent=2),
                        "raw": data
                    }
                    
            except Exception as e:
                return {
                    "success": True, 
                    "message": response.text,
                    "raw": response.text
                }
        
        elif response.status_code == 422:
            return {
                "success": False,
                "error": f"API Error 422: Validation error",
                "message": self._get_demo_response(flow_key, "", is_error=True)
            }
        
        else:
            return {
                "success": False,
                "error": f"API Error {response.status_code}: {response.text[:200]}",
                "message": self._get_demo_response(flow_key, "", is_error=True)
            }
    
    def _extract_message(self, data: Dict) -> Optional[str]:
        """Extract message from response - IMPROVED VERSION for full content"""
        
        try:
            # METHOD 1: Standard Langflow format - outputs[0].outputs[0].results.message.text
            outputs = data.get("outputs", [])
            if outputs and len(outputs) > 0:
                first_output = outputs[0]
                
                # Check inner outputs
                inner_outputs = first_output.get("outputs", [])
                for inner in inner_outputs:
                    if isinstance(inner, dict):
                        results = inner.get("results", {})
                        message = results.get("message", {})
                        if isinstance(message, dict):
                            text = message.get("text", "")
                            if text and isinstance(text, str):
                                return text
                
                # Check direct results
                results = first_output.get("results", {})
                message = results.get("message", {})
                if isinstance(message, dict):
                    text = message.get("text", "")
                    if text and isinstance(text, str):
                        return text
                
                # Look for any message in outputs
                for output in outputs:
                    if isinstance(output, dict):
                        msg = output.get("message")
                        if msg and isinstance(msg, str):
                            return msg
                        txt = output.get("text")
                        if txt and isinstance(txt, str):
                            return txt
            
            # METHOD 2: Direct message field
            message = data.get("message")
            if message:
                if isinstance(message, str):
                    return message
                if isinstance(message, dict):
                    text = message.get("text") or message.get("data", {}).get("text")
                    if text and isinstance(text, str):
                        return text
            
            # METHOD 3: Result field
            result = data.get("result")
            if result:
                if isinstance(result, str):
                    return result
                if isinstance(result, dict):
                    text = result.get("text") or result.get("message")
                    if text and isinstance(text, str):
                        return text
            
            # METHOD 4: Text field
            text = data.get("text")
            if text and isinstance(text, str):
                return text
            
            # METHOD 5: Content field
            content = data.get("content")
            if content and isinstance(content, str):
                return content
            
            return None
            
        except Exception as e:
            return None
    
    def _get_demo_response(self, flow_key: str, input_text: str, is_error: bool = False) -> str:
        """Demo responses for fallback"""
        
        error_prefix = "⚠️ **Demo Mode**\n\n" if is_error else ""
        
        demos = {
            "qna_agent": f"""{error_prefix}**Medical Q&A Response**

Your question: {input_text[:100]}...

This is a demo response. Please check your API connection.""",
            
            "report_analyzer": f"""{error_prefix}**Report Analysis**

Your report analysis request: {input_text[:100]}...

This is a demo response. Please check your API connection.""",
            
            "prescription_analyzer": f"""{error_prefix}**Prescription Analysis**

Your prescription analysis request: {input_text[:100]}...

This is a demo response. Please check your API connection.""",
            
            "bill_analyzer": f"""{error_prefix}**Bill Audit**

Your bill audit request: {input_text[:100]}...

This is a demo response. Please check your API connection.""",
            
            "hospital_finder": f"""{error_prefix}**Hospital Finder Results**

Based on your search: {input_text[:100]}...

**Recommended Hospitals:**

1. **City General Hospital** ⭐4.7
   - Distance: 2.3 km
   - Multi-specialty | 24/7 Emergency
   - Contact: +91 12345 67890

2. **Speciality Medical Center** ⭐4.5
   - Distance: 4.1 km
   - Advanced Equipment | Expert Surgeons
   - Contact: +91 12345 67891

3. **Community Health Clinic** ⭐4.3
   - Distance: 1.8 km
   - Affordable | Quick Service
   - Contact: +91 12345 67892

*This is a demo response. Please check your API connection.*""",
            
            "file_upload": f"""{error_prefix}**File Upload Analysis**

Your file has been processed successfully.

**Key Findings:**
- File analyzed using cloud AI
- All relevant information extracted
- Comprehensive analysis performed

*This is a demo response while we fix the API connection.*"""
        }
        
        return demos.get(flow_key, f"{error_prefix}Demo response - API connection issue")
    
    # ========== PUBLIC METHODS ==========
    
    def qna_medical(self, question: str) -> Dict[str, Any]:
        """Medical Q&A - text only"""
        result = self._call_api("qna_agent", question)
        return result
    
    def analyze_report(self, user_message: str, uploaded_files: List = None) -> Dict[str, Any]:
        """Analyze medical report with optional file uploads"""
        result = self._call_api("report_analyzer", user_message, uploaded_files)
        return result
    
    def explain_medicines(self, user_message: str, uploaded_files: List = None) -> Dict[str, Any]:
        """Explain medicines/prescription with optional file uploads"""
        result = self._call_api("prescription_analyzer", user_message, uploaded_files)
        return result
    
    def analyze_bill(self, user_message: str, uploaded_files: List = None) -> Dict[str, Any]:
        """Analyze medical bill with optional file uploads"""
        result = self._call_api("bill_analyzer", user_message, uploaded_files)
        return result
    
    def find_hospitals(self, query: str, location: str = "") -> Dict[str, Any]:
        """Find hospitals - text only"""
        full_query = f"{query} in {location}" if location else query
        result = self._call_api("hospital_finder", full_query)
        return result