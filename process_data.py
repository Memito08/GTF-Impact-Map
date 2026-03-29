#!/usr/bin/env python3
"""
Data Processing Script for Global Talent Map

This script automatically processes the CSV and Excel files in the data folder
and generates the necessary JavaScript data for the index.html file.

Usage: python process_data.py
"""

import pandas as pd
import json
import os
from pathlib import Path

def normalize_country_name(country):
    """Normalize country names to match the standard format"""
    name_mapping = {
        # Will add more mappings if needed
    }
    return name_mapping.get(country, country)

def load_bigscholars_data():
    """Load and process BIG scholars data from Excel (clean dataset)."""
    df = pd.read_excel(Path("data") / "GTF BIG Talent Scholars.xlsx")

    big_scholars = {}
    for _, row in df.iterrows():
        country = normalize_country_name(row["Country"])
        year = str(row["Year"])
        name = row["Name"]

        if country not in big_scholars:
            big_scholars[country] = {}
        if year not in big_scholars[country]:
            big_scholars[country][year] = []

        big_scholars[country][year].append(name)

    return big_scholars

def load_program_data():
    """
    Load the program data file, containing the countries and the respective programs they are enrolled in.
    """
    df = pd.read_excel(Path("data") / "Program Data.xlsx")

    gtf_programs = {}

    for _, row in df.iterrows():
        country = normalize_country_name(row["Country"])
        country_programs = []
        if row["NATIONS"] == 1:
            country_programs.append("NATIONS")
        if row["EXCL"] == 1:
            country_programs.append("EXCL")

        if country_programs:
            gtf_programs[country] = country_programs

    return gtf_programs

def generate_program_data():
    """Generate the program data structure"""
    big_scholars = load_bigscholars_data()
    gtf_programs = load_program_data()

    program_data = {}
    
    # Get all countries that have data
    all_countries = set()
    all_countries.update(big_scholars.keys())
    all_countries.update(gtf_programs.keys())

    print(f"There are {len(all_countries)} countries in total!")
    
    for country in all_countries:
        country_data = {"programs":[]}
        
        # Add programs

        if country in big_scholars:
            country_data["programs"].append("BIG")
        if country in gtf_programs:
            country_data["programs"].extend(gtf_programs[country])
        
        # Add BIG scholars if available
        if country in big_scholars:
            country_data["bigScholars"] = big_scholars[country]
        
        program_data[country] = country_data
    
    return program_data

def write_program_data_json(output_path=Path("data") / "programData.json"):
    """Write programData.json into /data/programData.json"""
    program_data = generate_program_data()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(program_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote {output_path.as_posix()}")
    print(f"📊 Generated data for {len(program_data)} countries")

def validate_mappings():
    """
    Cross-check programData.json country names against country_codes.json labels.
    Reports any names that won't render on the map due to a mismatch.
    """
    import difflib

    program_data_path = Path("data") / "programData.json"
    country_codes_path = Path("data") / "country_codes.json"

    if not program_data_path.exists() or not country_codes_path.exists():
        print("❌ Required files not found. Run from the project root after generating programData.json.")
        return

    with open(program_data_path, encoding="utf-8") as f:
        program_data = json.load(f)
    with open(country_codes_path, encoding="utf-8") as f:
        country_codes = json.load(f)

    valid_labels = {
        entry["label"]
        for entry in country_codes.get("countries", {}).values()
        if isinstance(entry, dict) and isinstance(entry.get("label"), str) and entry["label"].strip()
    }

    unmatched = [name for name in program_data if name not in valid_labels]

    if not unmatched:
        print(f"✅ All {len(program_data)} countries in programData.json match country_codes.json.")
        return

    print(f"\n⚠️  {len(unmatched)} country name(s) in programData.json have NO match in country_codes.json")
    print("   These countries exist in the data but will NOT appear on the map:\n")
    for name in sorted(unmatched):
        suggestions = difflib.get_close_matches(name, list(valid_labels), n=3, cutoff=0.6)
        hint = f"  → Did you mean: {', '.join(suggestions)}" if suggestions else "  → No close match found"
        print(f"   • \"{name}\"{hint}")
    print()


def main():
    """Main function"""
    print("🚀 Starting data processing...")

    if not Path("data").exists():
        print("Error: 'data' directory not found. Please run this script from the project root.")
        return

    try:
        write_program_data_json()
        validate_mappings()
        print("✨ Data processing completed successfully!")
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()
