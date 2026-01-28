"""
Test Case Generator Module
Generates test cases for ETL mappings in various test management tool formats
"""
import json
import csv
import io
from typing import List, Dict, Any
from datetime import datetime


class TestCaseGenerator:
    """Generate test cases for ETL mapping documents in multiple formats"""
    
    def __init__(self, mappings: List[Dict[str, Any]], summary: Dict[str, Any]):
        """
        Initialize the test case generator
        
        Args:
            mappings: List of mapping records from the ETL validator
            summary: Summary information about the mappings
        """
        self.mappings = mappings
        self.summary = summary
        self.source_table = summary.get('detected_source_tables', ['source_table'])[0]
        self.target_table = 'target_table'
        
    def generate_positive_test_cases(self) -> List[Dict[str, Any]]:
        """Generate positive test cases for valid data transformations"""
        test_cases = []
        
        # Test Case 1: All columns mapped correctly
        test_cases.append({
            'test_id': 'TC_POSITIVE_001',
            'name': f'Verify all columns are mapped from {self.source_table} to {self.target_table}',
            'description': f'Validate that all {len(self.mappings)} columns are correctly mapped with specified transformations',
            'preconditions': [
                f'Source table {self.source_table} contains valid data',
                'ETL process is configured and ready',
                'Target table structure is created'
            ],
            'test_steps': [
                f'Load sample data into {self.source_table}',
                'Execute ETL process',
                f'Query target table {self.target_table}',
                'Compare source and target data'
            ],
            'expected_result': 'All columns are mapped correctly with transformations applied',
            'test_data': 'Valid records with all required fields',
            'priority': 'High',
            'type': 'Functional',
            'category': 'Positive'
        })
        
        # Test Case 2: Individual column transformation validation
        for idx, mapping in enumerate(self.mappings, start=2):
            source_col = mapping.get('source_column', 'N/A')
            target_col = mapping.get('target_column', 'N/A')
            transformation = mapping.get('transformation', 'N/A')
            
            test_cases.append({
                'test_id': f'TC_POSITIVE_{idx:03d}',
                'name': f'Validate transformation for {source_col} to {target_col}',
                'description': f'Verify that {source_col} is correctly transformed to {target_col} using: {transformation}',
                'preconditions': [
                    f'Column {source_col} exists in source table',
                    f'Column {target_col} exists in target table'
                ],
                'test_steps': [
                    f'Insert test record with valid {source_col} value',
                    'Execute ETL transformation',
                    f'Verify {target_col} contains expected transformed value',
                    'Compare with transformation logic'
                ],
                'expected_result': f'{target_col} contains correctly transformed value from {source_col}',
                'test_data': f'Valid test data for {source_col}',
                'priority': 'Medium',
                'type': 'Functional',
                'category': 'Positive'
            })
        
        # Test Case: Data type validation
        test_cases.append({
            'test_id': f'TC_POSITIVE_{len(test_cases) + 1:03d}',
            'name': 'Verify data types are preserved/converted correctly',
            'description': 'Validate that all data types are handled correctly during transformation',
            'preconditions': [
                'Source and target tables have defined data types',
                'Test data includes various data types'
            ],
            'test_steps': [
                'Insert records with different data types',
                'Execute ETL process',
                'Query and validate data types in target',
                'Verify no data type conversion errors'
            ],
            'expected_result': 'All data types are correctly preserved or converted',
            'test_data': 'Records with string, numeric, date, and boolean values',
            'priority': 'High',
            'type': 'Functional',
            'category': 'Positive'
        })
        
        # Test Case: Large volume test
        test_cases.append({
            'test_id': f'TC_POSITIVE_{len(test_cases) + 1:03d}',
            'name': 'Validate ETL with large data volume',
            'description': 'Test ETL process with large number of records',
            'preconditions': [
                'Large test dataset is prepared',
                'System resources are available'
            ],
            'test_steps': [
                'Load 10,000+ records into source table',
                'Execute ETL process',
                'Verify record count matches',
                'Sample check data accuracy'
            ],
            'expected_result': 'All records are processed correctly without errors',
            'test_data': '10,000+ valid records',
            'priority': 'Medium',
            'type': 'Performance',
            'category': 'Positive'
        })
        
        return test_cases
    
    def generate_negative_test_cases(self) -> List[Dict[str, Any]]:
        """Generate negative test cases for error handling"""
        test_cases = []
        
        # Test Case 1: Null value handling
        test_cases.append({
            'test_id': 'TC_NEGATIVE_001',
            'name': 'Verify handling of NULL values in source columns',
            'description': 'Validate ETL behavior when source columns contain NULL values',
            'preconditions': [
                'Source table accepts NULL values',
                'NULL handling rules are defined'
            ],
            'test_steps': [
                'Insert records with NULL values in various columns',
                'Execute ETL process',
                'Verify error handling or default value assignment',
                'Check target table for NULL or default values'
            ],
            'expected_result': 'NULL values are handled according to business rules (rejected, defaulted, or passed through)',
            'test_data': 'Records with NULL values in each column',
            'priority': 'High',
            'type': 'Negative',
            'category': 'Negative'
        })
        
        # Test Case 2: Invalid data type
        test_cases.append({
            'test_id': 'TC_NEGATIVE_002',
            'name': 'Verify rejection of invalid data types',
            'description': 'Test ETL behavior with incompatible data types',
            'preconditions': [
                'Data type constraints are defined',
                'Error handling is configured'
            ],
            'test_steps': [
                'Insert records with invalid data types (e.g., text in numeric field)',
                'Execute ETL process',
                'Verify error is logged',
                'Confirm record is rejected or error is raised'
            ],
            'expected_result': 'Invalid data type records are rejected with appropriate error message',
            'test_data': 'Records with type mismatches',
            'priority': 'High',
            'type': 'Negative',
            'category': 'Negative'
        })
        
        # Test Case 3: Missing mandatory columns
        for idx, mapping in enumerate(self.mappings[:3], start=3):  # Test first 3 mappings
            source_col = mapping.get('source_column', 'N/A')
            
            test_cases.append({
                'test_id': f'TC_NEGATIVE_{idx:03d}',
                'name': f'Verify handling of missing {source_col} column',
                'description': f'Test ETL behavior when {source_col} is missing or empty',
                'preconditions': [
                    f'{source_col} is identified as required column',
                    'Validation rules are active'
                ],
                'test_steps': [
                    f'Insert record without {source_col} value',
                    'Execute ETL process',
                    'Check for validation error',
                    'Verify record is not loaded to target'
                ],
                'expected_result': f'Record is rejected with error indicating missing {source_col}',
                'test_data': f'Record with empty/missing {source_col}',
                'priority': 'High',
                'type': 'Negative',
                'category': 'Negative'
            })
        
        # Test Case: Duplicate records
        test_cases.append({
            'test_id': f'TC_NEGATIVE_{len(test_cases) + 1:03d}',
            'name': 'Verify handling of duplicate records',
            'description': 'Test ETL behavior with duplicate source records',
            'preconditions': [
                'Duplicate detection logic is implemented',
                'Primary key or unique constraints are defined'
            ],
            'test_steps': [
                'Insert duplicate records in source table',
                'Execute ETL process',
                'Verify duplicate handling (reject, merge, or last-wins)',
                'Check target table for duplicate prevention'
            ],
            'expected_result': 'Duplicates are handled according to business rules',
            'test_data': 'Identical records repeated',
            'priority': 'Medium',
            'type': 'Negative',
            'category': 'Negative'
        })
        
        # Test Case: Data length validation
        test_cases.append({
            'test_id': f'TC_NEGATIVE_{len(test_cases) + 1:03d}',
            'name': 'Verify data length/size constraints',
            'description': 'Test ETL with data exceeding column length limits',
            'preconditions': [
                'Column length constraints are defined',
                'Truncation or rejection rules exist'
            ],
            'test_steps': [
                'Insert records with oversized values',
                'Execute ETL process',
                'Check if data is truncated or rejected',
                'Verify error logging'
            ],
            'expected_result': 'Oversized data is handled per business rules (truncate with warning or reject)',
            'test_data': 'Records with values exceeding max length',
            'priority': 'Medium',
            'type': 'Negative',
            'category': 'Negative'
        })
        
        # Test Case: Special characters
        test_cases.append({
            'test_id': f'TC_NEGATIVE_{len(test_cases) + 1:03d}',
            'name': 'Verify handling of special characters',
            'description': 'Test ETL with special characters and encoding issues',
            'preconditions': [
                'Character encoding is specified',
                'Special character rules are defined'
            ],
            'test_steps': [
                'Insert records with special characters (quotes, commas, unicode)',
                'Execute ETL process',
                'Verify characters are preserved or handled correctly',
                'Check for encoding errors'
            ],
            'expected_result': 'Special characters are correctly handled without data corruption',
            'test_data': 'Records with special characters: \', ", \\, unicode, etc.',
            'priority': 'Medium',
            'type': 'Negative',
            'category': 'Negative'
        })
        
        return test_cases
    
    def format_for_qtest(self, test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases for qTest import (CSV format)"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # qTest CSV headers
        writer.writerow([
            'Test Case ID', 'Name', 'Description', 'Precondition',
            'Test Step Description', 'Expected Result', 'Priority',
            'Type', 'Status'
        ])
        
        for tc in test_cases:
            steps = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(tc.get('test_steps', []))])
            preconditions = '\n'.join(tc.get('preconditions', []))
            
            writer.writerow([
                tc.get('test_id', ''),
                tc.get('name', ''),
                tc.get('description', ''),
                preconditions,
                steps,
                tc.get('expected_result', ''),
                tc.get('priority', 'Medium'),
                tc.get('type', 'Functional'),
                'Draft'
            ])
        
        return output.getvalue()
    
    def format_for_zephyr(self, test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases for Zephyr import (CSV format)"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Zephyr CSV headers
        writer.writerow([
            'ID', 'Name', 'Objective', 'Precondition', 'Test Script',
            'Priority', 'Component', 'Labels', 'Status'
        ])
        
        for tc in test_cases:
            steps = '\n'.join([f"Step {i+1}: {step}\nExpected: Part of overall test validation" 
                             for i, step in enumerate(tc.get('test_steps', []))])
            preconditions = '\n'.join(tc.get('preconditions', []))
            
            writer.writerow([
                tc.get('test_id', ''),
                tc.get('name', ''),
                tc.get('description', ''),
                preconditions,
                steps,
                tc.get('priority', 'Medium'),
                'ETL Mapping',
                tc.get('category', 'Functional'),
                'Draft'
            ])
        
        return output.getvalue()
    
    def format_for_testrail(self, test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases for TestRail import (CSV format)"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # TestRail CSV headers
        writer.writerow([
            'ID', 'Title', 'Section', 'Template', 'Type', 'Priority',
            'Estimate', 'References', 'Automation Type', 'Preconditions',
            'Steps', 'Expected Result'
        ])
        
        for tc in test_cases:
            steps_formatted = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(tc.get('test_steps', []))])
            preconditions = '\n'.join(tc.get('preconditions', []))
            
            writer.writerow([
                tc.get('test_id', ''),
                tc.get('name', ''),
                'ETL Mapping Tests',
                'Test Case (Steps)',
                tc.get('type', 'Functional'),
                tc.get('priority', 'Medium'),
                '30m',
                '',
                'None',
                preconditions,
                steps_formatted,
                tc.get('expected_result', '')
            ])
        
        return output.getvalue()
    
    def format_for_ado(self, test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases for Azure DevOps (ADO) import (CSV format)"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Azure DevOps CSV headers
        writer.writerow([
            'Work Item Type', 'ID', 'Title', 'State', 'Priority',
            'Area Path', 'Iteration Path', 'Description', 'Steps',
            'Automation Status', 'Test Type'
        ])
        
        for tc in test_cases:
            # Format steps in ADO format
            steps_xml = '<steps>'
            for i, step in enumerate(tc.get('test_steps', []), 1):
                steps_xml += f'<step id="{i}"><parameterizedString isformatted="true">{step}</parameterizedString><parameterizedString isformatted="true">Verify step completes successfully</parameterizedString><description/></step>'
            steps_xml += '</steps>'
            
            preconditions = '\n'.join(tc.get('preconditions', []))
            description = f"{tc.get('description', '')}\n\nPreconditions:\n{preconditions}\n\nExpected Result:\n{tc.get('expected_result', '')}"
            
            writer.writerow([
                'Test Case',
                tc.get('test_id', ''),
                tc.get('name', ''),
                'Design',
                tc.get('priority', '2'),
                'ETL',
                'Sprint 1',
                description,
                steps_xml,
                'Not Automated',
                tc.get('type', 'Functional')
            ])
        
        return output.getvalue()
    
    def format_for_json(self, test_cases: List[Dict[str, Any]]) -> str:
        """Format test cases as JSON for general purpose use"""
        return json.dumps({
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'source_table': self.source_table,
                'target_table': self.target_table,
                'total_mappings': self.summary.get('total_mappings', 0),
                'total_test_cases': len(test_cases)
            },
            'test_cases': test_cases
        }, indent=2)
    
    def generate_all_test_cases(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate both positive and negative test cases"""
        positive_cases = self.generate_positive_test_cases()
        negative_cases = self.generate_negative_test_cases()
        
        return {
            'positive': positive_cases,
            'negative': negative_cases,
            'all': positive_cases + negative_cases
        }
    
    def export_test_cases(self, format_type: str = 'qtest', test_type: str = 'all') -> str:
        """
        Export test cases in specified format
        
        Args:
            format_type: One of 'qtest', 'zephyr', 'testrail', 'ado', 'json'
            test_type: One of 'positive', 'negative', 'all'
            
        Returns:
            Formatted test cases as string
        """
        test_cases = self.generate_all_test_cases()
        selected_cases = test_cases.get(test_type, test_cases['all'])
        
        format_map = {
            'qtest': self.format_for_qtest,
            'zephyr': self.format_for_zephyr,
            'testrail': self.format_for_testrail,
            'ado': self.format_for_ado,
            'json': self.format_for_json
        }
        
        formatter = format_map.get(format_type.lower())
        if not formatter:
            raise ValueError(f"Unsupported format: {format_type}. Supported formats: {', '.join(format_map.keys())}")
        
        return formatter(selected_cases)
