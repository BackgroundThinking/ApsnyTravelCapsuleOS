#!/usr/bin/env python3
"""
Autoupdate Roadmap Integration Script

This script reads the ROADMAP.md file and executes the next task in the queue.
It handles iterative task execution, progress tracking, and status updates.

Usage:
    python3 autoupdate_roadmap.py [--status] [--next] [--execute] [--help]
    
Examples:
    python3 autoupdate_roadmap.py --status              # Show current status
    python3 autoupdate_roadmap.py --next                # Show next task
    python3 autoupdate_roadmap.py --execute             # Execute next iteration
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse

class RoadmapParser:
    """Parses and manages ROADMAP.md file."""
    
    def __init__(self, roadmap_path: str = "ROADMAP.md"):
        self.roadmap_path = Path(roadmap_path)
        self.content = None
        self.phases = {}
        self.current_phase = None
        self.load_roadmap()
    
    def load_roadmap(self) -> None:
        """Load and parse ROADMAP.md file."""
        if not self.roadmap_path.exists():
            raise FileNotFoundError(f"ROADMAP.md not found: {self.roadmap_path}")
        
        with open(self.roadmap_path, "r", encoding="utf-8") as f:
            self.content = f.read()
        
        self.parse_phases()
        print(f"✓ Loaded ROADMAP from {self.roadmap_path}")
    
    def parse_phases(self) -> None:
        """Parse phases from ROADMAP content."""
        # Find all phases
        phase_pattern = r"## Phase (\d+):[^(]*\(([^)]+)\)"
        matches = re.finditer(phase_pattern, self.content)
        
        for match in matches:
            phase_num = int(match.group(1))
            phase_name = match.group(2)
            
            self.phases[phase_num] = {
                "name": phase_name,
                "tasks": self.extract_phase_tasks(phase_num)
            }
    
    def extract_phase_tasks(self, phase_num: int) -> List[Dict]:
        """Extract tasks from a specific phase."""
        tasks = []
        
        # Find phase section
        phase_pattern = f"## Phase {phase_num}:"
        phase_start = self.content.find(phase_pattern)
        
        if phase_start == -1:
            return tasks
        
        # Find next phase or end of file
        next_phase_pattern = f"## Phase {phase_num + 1}:"
        phase_end = self.content.find(next_phase_pattern, phase_start)
        if phase_end == -1:
            phase_end = len(self.content)
        
        phase_content = self.content[phase_start:phase_end]
        
        # Find all milestones (M#.#)
        milestone_pattern = r"### (M\d+\.\d+):[^(]*\(([^)]+)\)"
        matches = re.finditer(milestone_pattern, phase_content)
        
        for match in matches:
            milestone_id = match.group(1)
            milestone_name = match.group(2)
            
            # Extract tasks for this milestone
            milestone_tasks = self.extract_milestone_tasks(
                phase_content, milestone_id
            )
            
            tasks.append({
                "id": milestone_id,
                "name": milestone_name,
                "tasks": milestone_tasks,
                "status": self.get_milestone_status(phase_content, milestone_id)
            })
        
        return tasks
    
    def extract_milestone_tasks(self, content: str, milestone_id: str) -> List[str]:
        """Extract individual tasks from a milestone."""
        tasks = []
        
        # Find milestone section
        milestone_pattern = f"### {milestone_id}:"
        milestone_start = content.find(milestone_pattern)
        
        if milestone_start == -1:
            return tasks
        
        # Find next milestone or end of content
        next_milestone_pattern = r"### M\d+\.\d+:"
        next_match = re.search(next_milestone_pattern, content[milestone_start + 10:])
        if next_match:
            milestone_end = milestone_start + 10 + next_match.start()
        else:
            milestone_end = len(content)
        
        milestone_content = content[milestone_start:milestone_end]
        
        # Find all task checkboxes
        task_pattern = r"- \[([ x~!?])\] (.+)"
        matches = re.finditer(task_pattern, milestone_content)
        
        for match in matches:
            status = match.group(1)
            task_text = match.group(2)
            tasks.append({
                "text": task_text,
                "status": status
            })
        
        return tasks
    
    def get_milestone_status(self, content: str, milestone_id: str) -> str:
        """Get status of a milestone."""
        # Find status line
        status_pattern = f"{milestone_id}:[^\\n]*\\*\\*Status:\\*\\* ([^\\n]+)"
        match = re.search(status_pattern, content)
        
        if match:
            return match.group(1).strip()
        return "Unknown"
    
    def get_current_task(self) -> Optional[Dict]:
        """Get the next incomplete task."""
        for phase_num in sorted(self.phases.keys()):
            phase = self.phases[phase_num]
            
            for milestone in phase["tasks"]:
                for task in milestone["tasks"]:
                    if task["status"] == " ":  # Not completed
                        return {
                            "phase": phase_num,
                            "phase_name": phase["name"],
                            "milestone": milestone["id"],
                            "milestone_name": milestone["name"],
                            "task": task["text"],
                            "status": task["status"]
                        }
        
        return None
    
    def print_status(self) -> None:
        """Print current roadmap status."""
        print("\n" + "=" * 80)
        print("ROADMAP STATUS")
        print("=" * 80)
        
        for phase_num in sorted(self.phases.keys()):
            phase = self.phases[phase_num]
            print(f"\nPhase {phase_num}: {phase['name']}")
            
            for milestone in phase["tasks"]:
                total = len(milestone["tasks"])
                completed = sum(1 for t in milestone["tasks"] if t["status"] == "x")
                progress = (completed / total * 100) if total > 0 else 0
                
                status_icon = "✓" if completed == total else "⏳" if completed > 0 else "○"
                print(f"  {status_icon} {milestone['id']}: {milestone['name']}")
                print(f"     Progress: {completed}/{total} ({progress:.0f}%)")
        
        print("\n" + "=" * 80)
    
    def print_next_task(self) -> None:
        """Print the next task to execute."""
        task = self.get_current_task()
        
        if not task:
            print("✓ All tasks completed!")
            return
        
        print("\n" + "=" * 80)
        print("NEXT TASK")
        print("=" * 80)
        print(f"\nPhase {task['phase']}: {task['phase_name']}")
        print(f"Milestone: {task['milestone']} - {task['milestone_name']}")
        print(f"Task: {task['task']}")
        print("\n" + "=" * 80)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Autoupdate Roadmap Integration"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current roadmap status"
    )
    parser.add_argument(
        "--next",
        action="store_true",
        help="Show next task to execute"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute next iteration"
    )
    
    args = parser.parse_args()
    
    try:
        roadmap = RoadmapParser()
        
        if args.status:
            roadmap.print_status()
        elif args.next:
            roadmap.print_next_task()
        elif args.execute:
            roadmap.print_next_task()
            print("\n✓ Ready to execute next iteration")
            print("Use `/autoupdate` command to execute")
        else:
            roadmap.print_status()
            roadmap.print_next_task()
        
        return 0
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
