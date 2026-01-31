import csv
import re
from pathlib import Path


def normalize_data(input_file):
    """Normalize the CSV data by removing redundant patterns"""

    # Generate output filename
    path = Path(input_file)
    output_file = path.parent / f"{path.stem}_normalized{path.suffix}"

    # Read input data
    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        data = list(reader)

    print(f"Loaded {len(data)} rows with {len(headers)} columns")

    # Normalize each row
    for row in data:
        # Clean processor specification
        if row["spec_procesor"]:
            row["spec_procesor"] = re.sub(
                r"^Procesor\s*", "", row["spec_procesor"]
            ).strip()

        # Clean processor brand
        if row["spec_marka_procesora"]:
            row["spec_marka_procesora"] = re.sub(
                r"^Marka procesora\s*", "", row["spec_marka_procesora"]
            ).strip()
            # Standardize brand names
            brand = row["spec_marka_procesora"].lower()
            if "intel" in brand:
                row["spec_marka_procesora"] = "Intel"
            elif "amd" in brand:
                row["spec_marka_procesora"] = "AMD"
            elif "apple" in brand:
                row["spec_marka_procesora"] = "Apple"

        # Clean RAM specification
        if row["spec_pami_ram"]:
            row["spec_pami_ram"] = re.sub(
                r"^Pamięć RAM\s*", "", row["spec_pami_ram"]
            ).strip()

        # Clean graphics card specification
        if row["spec_karta_graficzna"]:
            row["spec_karta_graficzna"] = re.sub(
                r"^Karta graficzna\s*", "", row["spec_karta_graficzna"]
            ).strip()

        # Clean disk specification
        if row["spec_dysk"]:
            # Remove "Dysk " prefix and clean up formatting
            row["spec_dysk"] = re.sub(r"^Dysk\s*", "", row["spec_dysk"]).strip()
            # Clean up comma-separated values
            row["spec_dysk"] = re.sub(r"\s*,\s*", ", ", row["spec_dysk"])

        # Clean disk capacity specification
        if row["spec_pojemno_dysku_1"]:
            row["spec_pojemno_dysku_1"] = re.sub(
                r"^Pojemność dysku 1\s*", "", row["spec_pojemno_dysku_1"]
            ).strip()

        # Clean operating system specification
        if row["spec_system_operacyjny"]:
            row["spec_system_operacyjny"] = re.sub(
                r"^System operacyjny\s*", "", row["spec_system_operacyjny"]
            ).strip()
            # Standardize OS names
            os_text = row["spec_system_operacyjny"].lower()
            if "windows 11 pro" in os_text:
                row["spec_system_operacyjny"] = "Windows 11 Pro"
            elif "windows 11 home" in os_text:
                row["spec_system_operacyjny"] = "Windows 11 Home"
            elif "windows 10 pro" in os_text:
                row["spec_system_operacyjny"] = "Windows 10 Pro"
            elif "macos" in os_text or "mac os" in os_text:
                row["spec_system_operacyjny"] = "macOS"

        # Clean product type specification
        if row["spec_typ_produktu"]:
            row["spec_typ_produktu"] = re.sub(
                r"^Typ produktu\s*", "", row["spec_typ_produktu"]
            ).strip()

        # Clean core count specification
        if row["spec_liczba_rdzeni"]:
            row["spec_liczba_rdzeni"] = re.sub(
                r"^Liczba rdzeni\s*", "", row["spec_liczba_rdzeni"]
            ).strip()

        # Clean RAM configuration specification
        if row["spec_pami_ram_konfiguracja"]:
            row["spec_pami_ram_konfiguracja"] = re.sub(
                r"^Pamięć RAM \(konfiguracja\)\s*",
                "",
                row["spec_pami_ram_konfiguracja"],
            ).strip()

        # Clean all text fields from extra whitespace
        for key, value in row.items():
            if isinstance(value, str):
                # Remove extra spaces and normalize
                row[key] = re.sub(r"\s+", " ", value.strip()) if value else ""

    # Skip duplicate removal - preserve all rows
    unique_data = data
    print("Preserving all rows (duplicate removal disabled)")

    # Write normalized data
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(unique_data)

    print(f"Normalized data saved to: {output_file}")
    print(f"Final dataset: {len(unique_data)} rows")


def main():
    """Main function"""
    input_file = "mediamarkt_desktops.csv"

    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found!")
        return

    normalize_data(input_file)
    print("Normalization completed successfully!")


if __name__ == "__main__":
    main()
