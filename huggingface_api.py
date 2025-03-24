import requests
from typing import Dict, Any, List
from datetime import datetime, timezone

def get_huggingface_trending() -> Dict[str, Any]:
    """
    Fetch trending data from the Hugging Face API.
    
    Returns:
        Dict[str, Any]: The parsed JSON response containing trending data
    """
    url = "https://huggingface.co/api/trending"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

def extract_model_info(raw_block: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract specific information from a single model's data.
    """
    model_data = raw_block['repoData']

    # Parse the lastModified timestamp
    last_modified = datetime.strptime(model_data.get('lastModified'), "%Y-%m-%dT%H:%M:%S.%fZ")
    last_modified = last_modified.replace(tzinfo=timezone.utc)

    # Calculate time difference from now
    now = datetime.now(timezone.utc)
    time_diff = now - last_modified

    # Format the time difference string
    if time_diff.days < 1:
        hours = int(time_diff.total_seconds() / 3600)
        time_str = f"Updated {hours} hours ago"
    else:
        days = time_diff.days
        time_str = f"Updated {days} day{'s' if days > 1 else ''} ago"

    extracted_info = {
        'id': model_data.get('id'),
        'lastModified': time_str,
        'likes': model_data.get('likes'),
        'downloads': model_data.get('downloads'),
        'avatarUrl': model_data.get('authorData', {}).get('avatarUrl'),
    }

    # Add pipeline_tag if it exists
    if 'pipeline_tag' in model_data:
        extracted_info['pipeline_tag'] = model_data['pipeline_tag']

    return extracted_info

def get_top_trending_models(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get top trending models with their information.
    
    Args:
        limit (int): Number of top models to return
        
    Returns:
        List[Dict[str, Any]]: List of trending model information
    """
    trending_data = get_huggingface_trending()
    if not trending_data:
        return []
        
    trending_models = []
    for model in trending_data['recentlyTrending'][:limit]:
        model_info = extract_model_info(model)
        trending_models.append(model_info)
        
    return trending_models 