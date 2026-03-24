import json
import csv
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Użycie: python3 json_to_csv.py <input_json> <output_csv>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Błąd: Nie znaleziono pliku wejściowego '{input_file}'.")
        sys.exit(1)
        
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            # QUOTE_ALL zapewnia, że każde pole zostanie otoczone cudzysłowami ""
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            
            # Wpisanie nagłówków kolumn
            writer.writerow(['Link', 'Tytuł', 'Opis', 'Tagi', 'Czas'])
            
            for item in data:
                # Wypisanie rekordów, obsługa brakujących kluczy
                writer.writerow([
                    item.get('Link', ''),
                    item.get('Tytuł', ''),
                    item.get('Opis', ''),
                    item.get('Tagi', ''),
                    item.get('Czas', '')
                ])
                
        print(f"Sukces: Wygenerowano poprawny plik CSV pod ścieżką {output_file}")
    except Exception as e:
        print(f"Wystąpił błąd podczas przetwarzania pliku: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
