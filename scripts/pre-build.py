#!/usr/bin/env python3
import json
import os
from pathlib import Path

def main():
    """
    Scans the project directory structure, aggregates build metadata,
    and generates a single builds.json file for Jekyll's root directory.
    """
    # "Сырые" данные лежат в папке projects
    source_data_root = Path("projects")
    # А результат (агрегированный JSON) мы кладем в специальную папку _data для Jekyll
    jekyll_data_dir = Path("_data")
    output_file = jekyll_data_dir / "builds.json"

    if not source_data_root.exists():
        print(f"Warning: Source data directory '{source_data_root}' not found. Creating an empty builds.json.")
        jekyll_data_dir.mkdir(exist_ok=True)
        with open(output_file, "w") as f:
            json.dump([], f)
        return

    all_branches_data = []

    # Iterate through potential branch directories
    for project_dir in sorted(source_data_root.iterdir()): # Итерируемся по проектам (swift-ios-test-demo, etc.)
        for branch_dir in sorted(project_dir.iterdir()): # Итерируемся по веткам внутри проекта
            continue

        branch_info_path = branch_dir / "branch-info.json"
        if not branch_info_path.exists():
            print(f"Warning: Skipping directory '{branch_dir.name}' because branch-info.json is missing.")
            continue

        try:
            with open(branch_info_path, "r") as f:
                branch_info = json.load(f)
                original_branch_name = branch_info.get("branch_name", branch_dir.name)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read or parse '{branch_info_path}'. Using folder name. Error: {e}")
            original_branch_name = branch_dir.name

        branch_builds = []

        # Iterate through potential build directories
        for build_dir in branch_dir.iterdir():
            # Ensure it's a directory and its name is a number
            if not build_dir.is_dir() or not build_dir.name.isdigit():
                continue

            build_meta_path = build_dir / "build-meta.json"
            if not build_meta_path.exists():
                continue

            try:
                with open(build_meta_path, "r") as f:
                    build_meta = json.load(f)
                    branch_builds.append(build_meta)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read or parse '{build_meta_path}'. Skipping. Error: {e}")

        if branch_builds:
            # Sort builds by build_number in descending order (newest first)
            branch_builds.sort(key=lambda b: b.get("build_number", 0), reverse=True)
            all_branches_data.append({
                "branch_name": original_branch_name,
                "builds": branch_builds
            })

    # Создаем папку _data, если ее нет
    jekyll_data_dir.mkdir(exist_ok=True)

    # Write the aggregated data to the output file
    with open(output_file, "w") as f:
        json.dump(all_branches_data, f, indent=2)

    print(f"Successfully generated '{output_file}' with data for {len(all_branches_data)} branches.")

if __name__ == "__main__":
    main()