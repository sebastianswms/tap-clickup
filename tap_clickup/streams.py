"""Stream type classes for tap-clickup."""
from pathlib import Path
from typing import Optional
from tap_clickup.client import ClickUpStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TeamsStream(ClickUpStream):
    """Teams"""

    name = "team"
    path = "/team"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "team.json"
    records_jsonpath = "$.teams[*]"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "team_id": record["id"],
        }


class SpacesStream(ClickUpStream):
    """Spaces"""

    name = "space"
    path = "/team/{team_id}/space"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    schema_filepath = SCHEMAS_DIR / "space.json"
    records_jsonpath = "$.spaces[*]"
    parent_stream_type = TeamsStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "space_id": record["id"],
        }


class FoldersStream(ClickUpStream):
    """Folders"""

    name = "folder"
    path = "/space/{space_id}/folder"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "folder.json"
    records_jsonpath = "$.folders[*]"
    parent_stream_type = SpacesStream

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "folder_id": record["id"],
        }


class FolderlessListsStream(ClickUpStream):
    """Folderless Lists"""

    name = "folderless_list"
    path = "/space/{space_id}/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "list.json"
    records_jsonpath = "$.lists[*]"
    parent_stream_type = SpacesStream
    
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class ListsStream(ClickUpStream):
    """Lists"""

    name = "list"
    path = "/folder/{folder_id}/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "list.json"
    records_jsonpath = "$.lists[*]"
    parent_stream_type = FoldersStream 
    
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "list_id": record["id"],
        }


class SharedHierarchyStream(ClickUpStream):
    """SharedHierarchy"""

    name = "shared_hierarchy"
    path = "/team/{team_id}/shared"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "shared.json"
    records_jsonpath = "$.shared"
    parent_stream_type = TeamsStream


class CustomFieldsStream(ClickUpStream):
    """CustomField"""

    name = "custom_field"
    path = "/list/{list_id}/field"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "custom_field.json"
    records_jsonpath = "$.fields[*]"
    parent_stream_type = FolderlessListsStream 
