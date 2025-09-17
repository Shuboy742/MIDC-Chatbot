import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
from urllib.parse import urljoin

def scrape_midc_land_bank(max_pages=None, tab_number=1):
    """
    Scrapes tabular data of MIDC land bank plots from Maharashtra government website
    Returns a pandas DataFrame with all land plot information
    
    Args:
        max_pages (int): Maximum number of pages to scrape. If None, scrapes all pages.
        tab_number (int): Tab number to scrape (1=Industrial, 2=Commercial, 3=Residential)
    """
    
    base_url = f"https://land.midcindia.org/LandBank/IndexforAllRecordsPartialView?pageno=0&tab={tab_number}&DeskID=&DistrictID=&IndustrialAreaID=&minsize=&maxsize=&maxprice=&minprice=&isCETP=null&PollutionLevel=0&PropertyTypeCode=&PlotTypeCode="
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        tab_names = {1: "Industrial", 2: "Commercial", 3: "Residential"}
        tab_name = tab_names.get(tab_number, f"Tab {tab_number}")
        
        print(f"Fetching {tab_name} data from MIDC land bank website...")
        print("📊 Expected: ~1181 plots across ~44 pages")
        print("⏱️  Estimated time: ~15-20 minutes")
        
        all_plots_data = []
        page = 1
        start_time = time.time()
        
        while True:
            # Construct URL for current page
            if page == 1:
                url = base_url
            else:
                # Update the pageno parameter for subsequent pages
                url = base_url.replace('pageno=0', f'pageno={page-1}')
            
            print(f"Scraping page {page}...")
            
            # Make the request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main data table - looking for the correct table ID
            plots_data = []
            
            # Look for the main data table with ID 'myTableforPlotUnderAllotmentList'
            table = soup.find('table', id='myTableforPlotUnderAllotmentList')
            
            if table:
                print("Found main data table")
                # Find the tbody with the data
                tbody = table.find('tbody')
                if tbody:
                    rows = tbody.find_all('tr')
                    print(f"Found {len(rows)} data rows in tbody")
                    
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) >= 5:  # Ensure we have all columns
                            # Extract text from each cell, handling nested elements
                            row_data = []
                            for cell in cells:
                                # Get text content, handling nested elements
                                cell_text = cell.get_text(strip=True)
                                row_data.append(cell_text)
                            
                            if len(row_data) >= 5:
                                plots_data.append(row_data[:5])  # Take first 5 columns
                else:
                    print("No tbody found, trying to extract from table directly...")
                    rows = table.find_all('tr')[1:]  # Skip header row
                    for row in rows:
                        cells = row.find_all('td')
                        if len(cells) >= 5:
                            row_data = [cell.get_text(strip=True) for cell in cells]
                            plots_data.append(row_data[:5])
            else:
                print("Main data table not found, searching for alternative structures...")
                # Try to find any table with data
                tables = soup.find_all('table')
                for table in tables:
                    if table.get('id') and 'Table' in table.get('id'):
                        print(f"Found alternative table: {table.get('id')}")
                        rows = table.find_all('tr')[1:]  # Skip header row
                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) >= 5:
                                row_data = [cell.get_text(strip=True) for cell in cells]
                                plots_data.append(row_data[:5])
                        break
            
            # If no data found on this page, we've reached the end
            if not plots_data:
                print(f"No data found on page {page}, stopping...")
                break
            
            all_plots_data.extend(plots_data)
            print(f"Extracted {len(plots_data)} plot records from page {page}")
            
            # Check if we should continue to next page
            if max_pages and page >= max_pages:
                print(f"Reached maximum pages limit ({max_pages})")
                break
            
            # Check for pagination - look for next page indicators
            # Since this appears to be a DataTable, check if there are more pages
            if len(plots_data) < 10:  # If we got fewer than expected records, likely last page
                print("Fewer records than expected, likely reached last page...")
                break
            
            # Check if we're getting duplicate data (same records as previous page)
            # Only check for duplicates if we have enough data to compare
            if page > 1 and len(plots_data) > 0 and len(all_plots_data) >= len(plots_data):
                # Compare first record of current page with the last record of previous page
                current_first_record = plots_data[0] if plots_data else []
                previous_last_record = all_plots_data[-1] if all_plots_data else []
                
                # Check if the first record of current page matches the last record of previous page
                if current_first_record and previous_last_record and current_first_record == previous_last_record:
                    print("Duplicate data detected, stopping...")
                    break
            
            # Progress tracking
            total_so_far = len(all_plots_data)
            elapsed_time = time.time() - start_time
            progress_percent = (total_so_far / 1181) * 100 if 1181 > 0 else 0
            
            print(f"📊 Progress: {total_so_far}/1181 plots ({progress_percent:.1f}%) - Page {page} - Time: {elapsed_time/60:.1f}min")
            
            # Check if we've reached the expected total (1181 plots)
            if total_so_far >= 1181:
                print("🎯 Reached expected total of 1181 plots, stopping...")
                break
            
            page += 1
            time.sleep(0.3)  # Further reduced delay for faster scraping
        
        total_time = time.time() - start_time
        print(f"Total extracted {len(all_plots_data)} plot records from {page-1} pages")
        print(f"⏱️  Total time taken: {total_time/60:.1f} minutes")
            
        # Convert to DataFrame
        if all_plots_data:
            columns = [
                'Sr_No', 'Regional_Office', 'Industrial_Area', 'Plot_No', 'Area_sq_meter'
            ]
            
            df = pd.DataFrame(all_plots_data, columns=columns)
            
            # Add property type column
            df['Property_Type'] = tab_name
            
            # Clean up the data
            df['Sr_No'] = pd.to_numeric(df['Sr_No'], errors='coerce')
            df['Area_sq_meter'] = pd.to_numeric(df['Area_sq_meter'], errors='coerce')
            
            print(f"Successfully scraped {len(df)} {tab_name} plots!")
            return df
        else:
            print("No data found. The page structure might have changed.")
            return pd.DataFrame()
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return pd.DataFrame()
    
    except Exception as e:
        print(f"Error parsing the data: {e}")
        return pd.DataFrame()

def save_data(df, format_type='csv'):
    """
    Save the scraped data to different formats
    """
    if df.empty:
        print("No data to save!")
        return
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    if format_type.lower() == 'csv':
        filename = f'midc_land_plots_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
    
    elif format_type.lower() == 'excel':
        filename = f'midc_land_plots_{timestamp}.xlsx'
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Data saved to {filename}")
    
    elif format_type.lower() == 'json':
        filename = f'midc_land_plots_{timestamp}.json'
        df.to_json(filename, orient='records', indent=2)
        print(f"Data saved to {filename}")

def analyze_data(df):
    """
    Quick analysis of the scraped data
    """
    if df.empty:
        return
    
    print("\n=== DATA SUMMARY ===")
    print(f"Total plots: {len(df)}")
    print(f"Regional Offices: {df['Regional_Office'].nunique()}")
    print(f"Industrial Areas: {df['Industrial_Area'].nunique()}")
    
    if 'Property_Type' in df.columns:
        print(f"Property Types: {df['Property_Type'].nunique()}")
        print("\n=== PROPERTY TYPES ===")
        print(df['Property_Type'].value_counts())
    
    print("\n=== REGIONAL OFFICES ===")
    print(df['Regional_Office'].value_counts())
    
    print("\n=== TOP 5 BY AREA ===")
    columns_to_show = ['Plot_No', 'Regional_Office', 'Industrial_Area', 'Area_sq_meter']
    if 'Property_Type' in df.columns:
        columns_to_show.insert(1, 'Property_Type')
    top_area = df.nlargest(5, 'Area_sq_meter')[columns_to_show]
    print(top_area.to_string(index=False))
    
    print("\n=== SAMPLE DATA ===")
    print(df.head().to_string(index=False))

def scrape_all_property_types(max_pages=None):
    """
    Scrapes data from all three property types: Industrial, Commercial, and Residential
    Returns a combined pandas DataFrame with all property types
    """
    print("🏭 MIDC Land Bank Comprehensive Data Scraper")
    print("=" * 60)
    print("📊 Scraping all property types: Industrial, Commercial, Residential")
    print("⏱️  Estimated total time: ~45-60 minutes")
    print("=" * 60)
    
    all_dataframes = []
    tab_info = {1: "Industrial", 2: "Commercial", 3: "Residential"}
    
    for tab_num, tab_name in tab_info.items():
        print(f"\n🔄 Starting {tab_name} data scraping...")
        print("-" * 40)
        
        df = scrape_midc_land_bank(max_pages=max_pages, tab_number=tab_num)
        
        if not df.empty:
            all_dataframes.append(df)
            print(f"✅ {tab_name}: {len(df)} plots scraped")
        else:
            print(f"⚠️  {tab_name}: No data found")
        
        # Small delay between tabs
        time.sleep(2)
    
    # Combine all dataframes
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"\n🎯 Total combined data: {len(combined_df)} plots")
        return combined_df
    else:
        print("\n❌ No data scraped from any tab")
        return pd.DataFrame()

# Main execution
if __name__ == "__main__":
    # Scrape data from all property types
    plots_df = scrape_all_property_types()
    
    if not plots_df.empty:
        # Analyze the data
        analyze_data(plots_df)
        
        # Save in multiple formats
        save_data(plots_df, 'csv')
        save_data(plots_df, 'excel')
        
        print(f"\n✅ Success! Scraped {len(plots_df)} total MIDC land plots from all property types")
    else:
        print("❌ Failed to scrape data. Please check the website structure.")

# Additional utility functions
def get_plots_by_regional_office(df, office_name):
    """Get all plots in a specific regional office"""
    return df[df['Regional_Office'].str.contains(office_name, case=False, na=False)]

def get_plots_by_industrial_area(df, area_name):
    """Get all plots in a specific industrial area"""
    return df[df['Industrial_Area'].str.contains(area_name, case=False, na=False)]

def search_plots(df, search_term):
    """Search plots by plot number or area"""
    return df[df['Plot_No'].str.contains(search_term, case=False, na=False) | 
              df['Industrial_Area'].str.contains(search_term, case=False, na=False)]