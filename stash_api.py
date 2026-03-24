"""
StashApp API client for direct data retrieval.
"""

import sys
from typing import Dict, Any, Optional, List
import stashapi.log as log
from stashapi.stashapp import StashInterface


class StashApiClient:
    """Client for connecting to and querying StashApp GraphQL API."""
    
    def __init__(self, host: str = "localhost", port: str = "9999", 
                 scheme: str = "http", api_key: Optional[str] = None,
                 username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the StashApp API client.
        
        Args:
            host: StashApp server hostname
            port: StashApp server port
            scheme: Connection scheme (http or https)
            api_key: API key for authentication
            username: Username for authentication (alternative to API key)
            password: Password for authentication (alternative to API key)
        """
        self.config = {
            "scheme": scheme,
            "host": host,
            "port": port,
            "logger": log
        }
        
        # Add authentication if provided
        if api_key:
            self.config["ApiKey"] = api_key
        elif username and password:
            self.config["username"] = username
            self.config["password"] = password
        
        try:
            self.stash = StashInterface(self.config)
            # Test connection
            self._test_connection()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to StashApp at {scheme}://{host}:{port} - {e}")
    
    def _test_connection(self):
        """Test connection to StashApp API."""
        try:
            # Try to get system status to verify connection
            self.stash.call_GQL("query { version { version } }")
        except Exception as e:
            raise ConnectionError(f"Cannot connect to StashApp API: {e}")
    
    def get_scene(self, scene_id: int) -> Dict[str, Any]:
        """
        Get scene data by ID.
        
        Args:
            scene_id: StashApp scene ID
            
        Returns:
            Scene data dictionary
        """
        try:
            scene_data = self.stash.find_scene(scene_id)
            if not scene_data:
                raise ValueError(f"Scene with ID {scene_id} not found")
            return scene_data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch scene {scene_id}: {e}")
    
    def get_performer(self, performer_id: int) -> Dict[str, Any]:
        """
        Get performer data by ID.
        
        Args:
            performer_id: StashApp performer ID
            
        Returns:
            Performer data dictionary
        """
        try:
            performer_data = self.stash.find_performer(performer_id)
            if not performer_data:
                raise ValueError(f"Performer with ID {performer_id} not found")
            return performer_data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch performer {performer_id}: {e}")
    
    def get_gallery(self, gallery_id: int) -> Dict[str, Any]:
        """
        Get gallery data by ID.
        
        Args:
            gallery_id: StashApp gallery ID
            
        Returns:
            Gallery data dictionary
        """
        try:
            # Use raw GraphQL for gallery since stashapp-tools might not have direct method
            query = """
            query FindGallery($id: ID!) {
                findGallery(id: $id) {
                    id
                    title
                    url
                    date
                    details
                    rating
                    organized
                    studio {
                        name
                    }
                    performers {
                        name
                    }
                    tags {
                        name
                    }
                    scenes {
                        id
                        title
                    }
                    folder {
                        path
                    }
                    images {
                        path
                    }
                    cover
                    created_at
                    updated_at
                }
            }
            """
            
            variables = {"id": str(gallery_id)}
            result = self.stash.call_GQL(query, variables)
            
            if not result or not result.get("findGallery"):
                raise ValueError(f"Gallery with ID {gallery_id} not found")
            
            return result["findGallery"]
        except Exception as e:
            raise RuntimeError(f"Failed to fetch gallery {gallery_id}: {e}")
    
    def find_scene_by_path(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Find scene by file path.
        
        Args:
            file_path: Full file path to search for
            
        Returns:
            Scene data dictionary or None if not found
        """
        try:
            query = """
            query FindScenes($filter: FindFilterType, $scene_filter: SceneFilterType) {
                findScenes(filter: $filter, scene_filter: $scene_filter) {
                    scenes {
                        id
                        title
                        files {
                            path
                        }
                    }
                }
            }
            """
            
            variables = {
                "filter": {"per_page": -1},
                "scene_filter": {"path": {"value": file_path, "modifier": "EQUALS"}}
            }
            
            result = self.stash.call_GQL(query, variables)
            scenes = result.get("findScenes", {}).get("scenes", [])
            
            if scenes:
                # Return the full scene data for the first match
                return self.get_scene(int(scenes[0]["id"]))
            
            return None
        except Exception as e:
            print(f"Warning: Could not search for scene by path: {e}", file=sys.stderr)
            return None
    
    def search_scenes(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search scenes by text query.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of scene data dictionaries
        """
        try:
            search_query = """
            query FindScenes($filter: FindFilterType, $scene_filter: SceneFilterType) {
                findScenes(filter: $filter, scene_filter: $scene_filter) {
                    scenes {
                        id
                        title
                        studio {
                            name
                        }
                        performers {
                            name
                        }
                        files {
                            path
                        }
                    }
                }
            }
            """
            
            variables = {
                "filter": {"per_page": limit, "q": query},
                "scene_filter": {}
            }
            
            result = self.stash.call_GQL(search_query, variables)
            return result.get("findScenes", {}).get("scenes", [])
        except Exception as e:
            raise RuntimeError(f"Failed to search scenes: {e}")
    
    def get_all_scenes(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        Get all scenes with file paths using pagination.

        Args:
            page_size: Number of scenes per page

        Returns:
            List of scene data dictionaries with file paths and metadata
        """
        # Query includes all fields needed for NFO generation
        query = """
        query FindScenes($filter: FindFilterType) {
            findScenes(filter: $filter) {
                count
                scenes {
                    id
                    title
                    details
                    date
                    rating100
                    studio {
                        name
                    }
                    performers {
                        name
                        gender
                    }
                    tags {
                        name
                    }
                    files {
                        path
                        duration
                        video_codec
                        audio_codec
                        width
                        height
                        frame_rate
                        bit_rate
                    }
                    created_at
                    updated_at
                }
            }
        }
        """

        all_scenes = []
        page = 1

        while True:
            variables = {
                "filter": {
                    "page": page,
                    "per_page": page_size,
                    "sort": "id",
                    "direction": "ASC"
                }
            }

            result = self.stash.call_GQL(query, variables)
            scenes = result.get("findScenes", {}).get("scenes", [])

            if not scenes:
                break

            all_scenes.extend(scenes)

            # Check if we got all scenes
            total_count = result.get("findScenes", {}).get("count", 0)
            if len(all_scenes) >= total_count:
                break

            page += 1

        return all_scenes

    def get_connection_info(self) -> Dict[str, Any]:
        """Get connection information for display."""
        return {
            "host": self.config["host"],
            "port": self.config["port"],
            "scheme": self.config["scheme"],
            "authenticated": "ApiKey" in self.config or ("username" in self.config and "password" in self.config)
        }