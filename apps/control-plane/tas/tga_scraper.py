"""
Training.gov.au Web Scraper
Fetches qualification and unit data from training.gov.au
"""
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class TrainingGovAuScraper:
    """Scraper for training.gov.au to fetch qualification and unit data"""
    
    BASE_URL = "https://training.gov.au"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_qualification_units(self, qualification_code: str) -> Optional[Dict]:
        """
        Fetch units of competency for a qualification from training.gov.au
        
        Args:
            qualification_code: The qualification code (e.g., 'ICT40120')
            
        Returns:
            Dictionary with qualification details and units, or None if not found
        """
        try:
            # Construct the URL for the qualification page
            url = f"{self.BASE_URL}/Training/Details/{qualification_code}"
            logger.info(f"🔍 Fetching qualification data from: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract qualification title
            title_elem = soup.find('h1')
            if not title_elem:
                logger.error(f"❌ Could not find qualification title for {qualification_code}")
                return None
            
            qual_title = title_elem.text.strip()
            # Remove the code from the title if it's included
            qual_title = qual_title.replace(qualification_code, '').strip()
            
            logger.info(f"📚 Found qualification: {qual_title}")
            
            # Extract packaging rules
            packaging_rules = self._extract_packaging_rules(soup)
            
            # Extract units with groupings
            groupings = self._extract_units(soup, qualification_code)
            
            if not groupings:
                logger.warning(f"⚠️ No units found for {qualification_code}")
                return None
            
            # Determine if qualification has groupings/majors
            has_groupings = len(groupings) > 2 or any(
                g['name'] not in ['Core Units', 'Elective Units', 'core', 'elective']
                for g in groupings
            )
            
            result = {
                'qualification_code': qualification_code,
                'qualification_title': qual_title,
                'packaging_rules': packaging_rules,
                'has_groupings': has_groupings,
                'groupings': groupings
            }
            
            logger.info(f"✅ Successfully fetched {len(groupings)} groupings with {sum(len(g['units']) for g in groupings)} total units")
            return result
            
        except requests.RequestException as e:
            logger.error(f"❌ Network error fetching {qualification_code}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"❌ Error parsing {qualification_code}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _extract_packaging_rules(self, soup: BeautifulSoup) -> str:
        """Extract packaging rules from the qualification page"""
        try:
            # Look for packaging rules section
            packaging_section = soup.find('h2', string=re.compile(r'Packaging Rules', re.I))
            if packaging_section:
                # Get the next sibling element (usually a div or p)
                rules_elem = packaging_section.find_next_sibling()
                if rules_elem:
                    return rules_elem.get_text(strip=True, separator=' ')[:500]  # Limit to 500 chars
            
            # Fallback: look for summary in meta or description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                return meta_desc['content'][:500]
            
            return "Packaging rules as per training.gov.au"
        except Exception as e:
            logger.warning(f"Could not extract packaging rules: {e}")
            return "Packaging rules as per training.gov.au"
    
    def _extract_units(self, soup: BeautifulSoup, qual_code: str) -> List[Dict]:
        """Extract units of competency organized by groupings"""
        groupings = []
        
        try:
            # Look for units section - training.gov.au typically has tables or lists
            # Try to find core units table/section
            core_section = soup.find(['h2', 'h3', 'h4'], string=re.compile(r'Core\s+Unit', re.I))
            if core_section:
                core_units = self._parse_units_section(core_section, 'core')
                if core_units:
                    groupings.append({
                        'name': 'Core Units',
                        'type': 'core',
                        'required': len(core_units),
                        'units': core_units
                    })
            
            # Look for elective units or groupings
            elective_section = soup.find(['h2', 'h3', 'h4'], string=re.compile(r'Elective\s+Unit', re.I))
            if elective_section:
                elective_units = self._parse_units_section(elective_section, 'elective')
                if elective_units:
                    groupings.append({
                        'name': 'Elective Units',
                        'type': 'elective',
                        'required': len(elective_units),
                        'description': 'Select elective units',
                        'units': elective_units
                    })
            
            # Look for group/stream/major sections (e.g., "Group A", "Cloud Computing")
            group_sections = soup.find_all(['h2', 'h3', 'h4'], string=re.compile(r'Group\s+[A-Z]|Stream|Major|Specialisation', re.I))
            for group_section in group_sections:
                group_name = group_section.get_text(strip=True)
                group_units = self._parse_units_section(group_section, 'elective')
                if group_units:
                    groupings.append({
                        'name': group_name,
                        'type': 'elective',
                        'required': 0,
                        'description': f'Select units from {group_name}',
                        'units': group_units
                    })
            
            # If no structured groupings found, try to find all unit codes on the page
            if not groupings:
                all_units = self._find_all_unit_codes(soup)
                if all_units:
                    groupings.append({
                        'name': 'All Units',
                        'type': 'core',
                        'required': len(all_units),
                        'units': all_units
                    })
            
        except Exception as e:
            logger.error(f"Error extracting units: {e}")
            import traceback
            traceback.print_exc()
        
        return groupings
    
    def _parse_units_section(self, section_header, unit_type: str) -> List[Dict]:
        """Parse units from a section (following a header)"""
        units = []
        
        try:
            # Find the next table or list after the header
            container = section_header.find_next(['table', 'ul', 'ol', 'div'])
            if not container:
                return units
            
            # Extract unit codes and titles from table rows or list items
            if container.name == 'table':
                rows = container.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        unit_code = cells[0].get_text(strip=True)
                        unit_title = cells[1].get_text(strip=True)
                        
                        # Validate unit code format (e.g., ICTICT418)
                        if re.match(r'^[A-Z]{3,10}\d{3,4}[A-Z]?$', unit_code):
                            units.append({
                                'code': unit_code,
                                'title': unit_title,
                                'type': unit_type
                            })
            else:
                # Parse from list or div
                items = container.find_all('li') if container.name in ['ul', 'ol'] else container.find_all(['p', 'div'])
                for item in items:
                    text = item.get_text(strip=True)
                    # Try to extract unit code and title (format: "ICTICT418 - Contribute to copyright...")
                    match = re.search(r'([A-Z]{3,10}\d{3,4}[A-Z]?)\s*[-–—]\s*(.+)', text)
                    if match:
                        units.append({
                            'code': match.group(1),
                            'title': match.group(2).strip(),
                            'type': unit_type
                        })
        
        except Exception as e:
            logger.warning(f"Error parsing units section: {e}")
        
        return units
    
    def _find_all_unit_codes(self, soup: BeautifulSoup) -> List[Dict]:
        """Find all unit codes on the page (fallback method)"""
        units = []
        seen_codes = set()
        
        try:
            # Find all text that looks like unit codes
            text = soup.get_text()
            unit_pattern = re.compile(r'\b([A-Z]{3,10}\d{3,4}[A-Z]?)\b')
            
            for match in unit_pattern.finditer(text):
                code = match.group(1)
                if code not in seen_codes:
                    seen_codes.add(code)
                    # Try to find the title nearby
                    # Look for the code in the HTML and get surrounding context
                    elements = soup.find_all(string=re.compile(code))
                    for elem in elements:
                        parent_text = elem.parent.get_text(strip=True)
                        title_match = re.search(rf'{code}\s*[-–—]\s*(.+?)(?:\n|$)', parent_text)
                        if title_match:
                            units.append({
                                'code': code,
                                'title': title_match.group(1).strip()[:200],  # Limit title length
                                'type': 'core'
                            })
                            break
                    else:
                        # No title found, use generic title
                        units.append({
                            'code': code,
                            'title': f'Unit {code}',
                            'type': 'core'
                        })
        
        except Exception as e:
            logger.warning(f"Error finding unit codes: {e}")
        
        return units
