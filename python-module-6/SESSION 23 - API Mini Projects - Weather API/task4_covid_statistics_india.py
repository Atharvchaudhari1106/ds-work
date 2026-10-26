"""
Task 4: COVID-19 Statistics for India (Tabular Display)
Create a Python program that fetches the latest COVID-19 case numbers for India
from a public COVID API and displays total cases, recovered, and deaths in a table format.
"""

import requests


def fetch_india_covid_stats():
    # Public COVID-19 API endpoint (NovelCOVID / disease.sh)
    url = "https://disease.sh/v3/covid-19/countries/India"

    print("=" * 65)
    print("Task 4: COVID-19 Case Numbers for India")
    print("=" * 65)
    print(f"API Endpoint : {url}")
    print("=" * 65)

    try:
        response = requests.get(url, timeout=10)
        print(f"\nResponse Status Code : {response.status_code}\n")

        if response.status_code == 200:
            data = response.json()

            country = data.get("country", "India")
            population = data.get("population", 0)
            total_cases = data.get("cases", 0)
            total_recovered = data.get("recovered", 0)
            total_deaths = data.get("deaths", 0)
            active_cases = data.get("active", 0)
            critical_cases = data.get("critical", 0)
            total_tests = data.get("tests", 0)
            cases_per_million = data.get("casesPerOneMillion", 0)
            deaths_per_million = data.get("deathsPerOneMillion", 0)

            # Table Output
            print("+" + "-" * 32 + "+" + "-" * 26 + "+")
            print(f"| {'METRIC / CATEGORY':<30} | {'STATISTIC (INDIA)':<24} |")
            print("+" + "=" * 32 + "+" + "=" * 26 + "+")
            print(f"| {'Country':<30} | {country:<24} |")
            print(f"| {'Total Population':<30} | {population:>24,} |")
            print("+" + "-" * 32 + "+" + "-" * 26 + "+")
            print(f"| {'Total Confirmed Cases':<30} | {total_cases:>24,} |")
            print(f"| {'Total Recovered Cases':<30} | {total_recovered:>24,} |")
            print(f"| {'Total Recorded Deaths':<30} | {total_deaths:>24,} |")
            print(f"| {'Active Cases':<30} | {active_cases:>24,} |")
            print(f"| {'Critical Cases':<30} | {critical_cases:>24,} |")
            print("+" + "-" * 32 + "+" + "-" * 26 + "+")
            print(f"| {'Total Tests Administered':<30} | {total_tests:>24,} |")
            print(f"| {'Cases Per 1 Million':<30} | {cases_per_million:>24,} |")
            print(f"| {'Deaths Per 1 Million':<30} | {deaths_per_million:>24,} |")
            print("+" + "-" * 32 + "+" + "-" * 26 + "+")
            print("\n[SUCCESS] COVID-19 dataset fetched and formatted in table.")

            return data
        else:
            print(f"[ERROR] Failed to fetch COVID data. HTTP status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection error: {e}")


if __name__ == "__main__":
    fetch_india_covid_stats()
