"""Upgrade manager for Magic Skills."""

import os
import json
import httpx
from typing import Dict, List, Optional
from pathlib import Path
from packaging import version


class UpgradeManager:
    """Manages skill upgrades and versioning."""

    VERSION_CHECK_URL = "https://api.github.com/repos/magic-skills/magic-skills/releases/latest"

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.version_file = Path(".magic_skills_version")
        self.current_version = self._get_current_version()

    def _get_current_version(self) -> str:
        """Get current installed version."""
        if self.version_file.exists():
            with open(self.version_file, "r") as f:
                data = json.load(f)
                return data.get("version", "1.0.0")
        return "1.0.0"

    async def check_for_updates(self) -> Dict:
        """Check for available updates."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.VERSION_CHECK_URL, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                latest_version = data.get("tag_name", "v1.0.0").lstrip("v")

                return {
                    "current_version": self.current_version,
                    "latest_version": latest_version,
                    "update_available": version.parse(latest_version) > version.parse(self.current_version),
                    "release_notes": data.get("body", ""),
                    "download_url": data.get("html_url", "")
                }
        except Exception as e:
            return {
                "current_version": self.current_version,
                "latest_version": self.current_version,
                "update_available": False,
                "error": str(e)
            }

    def upgrade_skill(
        self,
        skill_name: str,
        new_version: str,
        backup: bool = True
    ) -> Dict:
        """Upgrade a specific skill."""
        skill_path = self.skills_dir / skill_name

        if not skill_path.exists():
            return {
                "success": False,
                "error": f"Skill {skill_name} not found"
            }

        # Backup if requested
        if backup:
            backup_path = skill_path.with_suffix(f".backup_{self.current_version}")
            self._backup_skill(skill_path, backup_path)

        # Update version in skill.yaml
        skill_yaml_path = skill_path / "skill.yaml"
        if skill_yaml_path.exists():
            import yaml
            with open(skill_yaml_path, "r") as f:
                skill_config = yaml.safe_load(f)

            skill_config["version"] = new_version

            with open(skill_yaml_path, "w") as f:
                yaml.dump(skill_config, f, default_flow_style=False)

        return {
            "success": True,
            "skill": skill_name,
            "old_version": self.current_version,
            "new_version": new_version
        }

    def rollback_skill(self, skill_name: str) -> Dict:
        """Rollback a skill to previous version."""
        skill_path = self.skills_dir / skill_name

        # Find backup
        backups = list(self.skills_dir.glob(f"{skill_name}.backup_*"))
        if not backups:
            return {
                "success": False,
                "error": f"No backup found for {skill_name}"
            }

        # Use most recent backup
        backup_path = sorted(backups)[-1]

        # Remove current version
        if skill_path.exists():
            import shutil
            shutil.rmtree(skill_path)

        # Restore backup
        backup_path.rename(skill_path)

        return {
            "success": True,
            "skill": skill_name,
            "restored_from": backup_path.name
        }

    def _backup_skill(self, skill_path: Path, backup_path: Path):
        """Create a backup of a skill."""
        import shutil
        if backup_path.exists():
            shutil.rmtree(backup_path)
        shutil.copytree(skill_path, backup_path)

    def list_skill_versions(self, skill_name: str) -> List[Dict]:
        """List available versions for a skill."""
        skill_path = self.skills_dir / skill_name

        if not skill_path.exists():
            return []

        versions = []

        # Current version
        skill_yaml_path = skill_path / "skill.yaml"
        if skill_yaml_path.exists():
            import yaml
            with open(skill_yaml_path, "r") as f:
                config = yaml.safe_load(f)
                versions.append({
                    "version": config.get("version", "unknown"),
                    "type": "current",
                    "path": str(skill_path)
                })

        # Backups
        for backup in self.skills_dir.glob(f"{skill_name}.backup_*"):
            version_str = backup.suffix.replace(".backup_", "")
            versions.append({
                "version": version_str,
                "type": "backup",
                "path": str(backup)
            })

        return versions

    def update_system_version(self, new_version: str):
        """Update the system version file."""
        with open(self.version_file, "w") as f:
            json.dump({
                "version": new_version,
                "updated_at": str(Path(".").stat().st_mtime)
            }, f, indent=2)

        self.current_version = new_version
