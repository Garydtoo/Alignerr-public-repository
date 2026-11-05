Python
import csv
from typing import List, Dict, Any
from parser import PayloadParser, ParsingError

# Sample CSV data matching the 10-row test dataset
CSV_DATA = """id,status,owner,retry_count,notes
101,ACTIVE,admin,0,Standard valid payload
102,pending,user_dev,3,Lowercase status test
   103   , ACTIVE ,  sys_user  , 1 ,Whitespace padded values
104,UNKNOWN,qa_lead,5,Valid numeric ID with unknown status
,ACTIVE,dev_ops,2,Missing required ID (empty string)
106,,guest,0,Missing status string
107,INACTIVE,system,-1,Negative integer edge case for retries
108,ACTIVE,super_admin,abc,Non-numeric string for numeric retry count
109,null,null,0,Explicit null strings instead of actual values
110,ACTIVE,"admin, lead",2,Quoted string containing commas inside notes
"""


def process_csv_payloads(csv_text: str, strict: bool = False) -> List[Dict[str, Any]]:
    """
    Reads raw CSV text line-by-line and processes each row with PayloadParser.
    """
    parser = PayloadParser(strict_mode=strict)
    parsed_records = []
    
    # Split CSV string into lines to simulate reading a file
    csv_lines = csv_text.strip().splitlines()
    reader = csv.DictReader(csv_lines)

    for row_idx, row in enumerate(reader, start=2):  # Start at row 2 (row 1 is header)
        # Pre-process row: strip outer whitespace from string values
        cleaned_row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}
        
        # Convert literal "null" strings to empty strings/None representation
        for key, val in cleaned_row.items():
            if val.lower() == "null":
                cleaned_row[key] = ""

        try:
            # Map CSV fields into the payload structure expected by PayloadParser
            payload_input = {
                "id": cleaned_row.get("id"),
                "status": cleaned_row.get("status"),
                "meta": {
                    "owner": cleaned_row.get("owner"),
                    "retry_count": cleaned_row.get("retry_count"),
                    "notes": cleaned_row.get("notes"),
                }
            }

            result = parser.parse_payload(payload_input)
            parsed_records.append(result)
            print(f"Row {row_idx} [SUCCESS]: ID='{result['id']}', Status='{result['status']}'")

        except ParsingError as err:
            print(f"Row {row_idx} [FAILED]: {err}")

    return parsed_records


if __name__ == "__main__":
    print("--- Processing CSV in Non-Strict Mode ---")
    results = process_csv_payloads(CSV_DATA, strict=False)
    print(f"\nSuccessfully processed {len(results)} records.\n")

    print("--- Processing CSV in Strict Mode ---")
    results_strict = process_csv_payloads(CSV_DATA, strict=True)
    print(f"\nSuccessfully processed {len(results_strict)} records in strict mode.")