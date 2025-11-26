"""Vehicle API service for fetching car makes and models"""
import requests
from typing import List
from functools import lru_cache
import time

VPIC_API_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"


@lru_cache(maxsize=1)
def get_all_makes() -> List[str]:
    """Fetch all car makes from NHTSA VPIC API (cached)"""
    for attempt in range(3):
        try:
            response = requests.get(
                f"{VPIC_API_URL}/GetAllMakes?format=json",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if 'Results' in data and len(data['Results']) > 0:
                makes = sorted(list(set([
                    make['Make_Name'] 
                    for make in data['Results'] 
                    if make.get('Make_Name')
                ])))
                return makes
            return []
        except requests.exceptions.Timeout:
            if attempt < 2:
                print(f"Timeout on attempt {attempt + 1}, retrying...")
                time.sleep(1)
            else:
                print(f"Error fetching car makes: Request timed out after 3 attempts")
                return []
        except Exception as e:
            print(f"Error fetching car makes: {e}")
            return []
    return []


@lru_cache(maxsize=100)
def get_models_for_make(make: str) -> List[str]:
    """Fetch car models for a specific make from NHTSA VPIC API (cached)"""
    for attempt in range(3):
        try:
            response = requests.get(
                f"{VPIC_API_URL}/GetModelsForMake/{make}?format=json",
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if 'Results' in data and len(data['Results']) > 0:
                models = sorted(list(set([
                    model['Model_Name'] 
                    for model in data['Results'] 
                    if model.get('Model_Name')
                ])))
                return models
            return []
        except requests.exceptions.Timeout:
            if attempt < 2:
                print(f"Timeout fetching models for {make}, attempt {attempt + 1}, retrying...")
                time.sleep(1)
            else:
                print(f"Error fetching models for {make}: Request timed out after 3 attempts")
                return []
        except Exception as e:
            print(f"Error fetching models for {make}: {e}")
            return []
    return []


def search_makes(query: str) -> List[str]:
    """Search car makes by query string"""
    all_makes = get_all_makes()
    if not query:
        return all_makes
    
    query_lower = query.lower()
    return [make for make in all_makes if query_lower in make.lower()]


def search_models(make: str, query: str) -> List[str]:
    """Search car models for a specific make by query string"""
    all_models = get_models_for_make(make)
    if not query:
        return all_models
    
    query_lower = query.lower()
    return [model for model in all_models if query_lower in model.lower()]
