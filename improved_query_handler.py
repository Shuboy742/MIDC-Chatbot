"""
Improved Query Handler for Smart Semantic Matching
Handles spelling mistakes, regional office mappings, and industrial area variations
"""

import re
from difflib import get_close_matches

class SmartQueryHandler:
    def __init__(self):
        """Initialize smart query handler with comprehensive mappings"""
        self.region_mappings = {
        # Direct city to RO mappings (English)
        'pune': 'RO PUNE-I RO PUNE-II',
        'punya': 'RO PUNE-I RO PUNE-II',  # Marathi pronunciation in English
        'puny': 'RO PUNE-I RO PUNE-II',   # Short form
        'chandrapur': 'RO Chandrapur',
        'baramati': 'RO Baramati',
        'nagpur': 'RO NAGPUR',
        'ratnagiri': 'RO RATNAGIRI',
        'aurangabad': 'RO AURANGABAD',
        'mumbai': 'RO THANE-I RO THANE-II',
        'thane': 'RO THANE-I RO THANE-II',
        'amravati': 'RO AMRAVATI',
        'dhule': 'RO DHULE',
        'jalgaon': 'RO Jalgaon',
        'bhusaval': 'RO Jalgaon',  # Bhusaval is under RO Jalgaon
        'bhusawal': 'RO Jalgaon',  # Common misspelling
        'bhusawad': 'RO Jalgaon',  # Another misspelling
        'bhusawal': 'RO Jalgaon',  # Another variation
        
        # Marathi city mappings
        'पुणे': 'RO PUNE-I RO PUNE-II',
        'चंद्रपूर': 'RO Chandrapur',
        'बारामती': 'RO Baramati',
        'नागपूर': 'RO NAGPUR',
        'रत्नागिरी': 'RO RATNAGIRI',
        'औरंगाबाद': 'RO AURANGABAD',
        'मुंबई': 'RO THANE-I RO THANE-II',
        'ठाणे': 'RO THANE-I RO THANE-II',
        'अमरावती': 'RO AMRAVATI',
        'धुळे': 'RO DHULE',
        'जळगाव': 'RO Jalgaon',
        'भुसावळ': 'RO Jalgaon',
        'भुसावल': 'RO Jalgaon',
        }
        
        # Industrial area to RO mappings
        self.area_to_ro_mappings = {
            'bhusaval': 'RO Jalgaon',
            'bhusawal': 'RO Jalgaon',
            'bhusawad': 'RO Jalgaon',
            'talegaon': 'RO PUNE-I',
            'chakan': 'RO PUNE-I',
            'hinjawadi': 'RO PUNE-II',
            'rajiv gandhi infotech park': 'RO PUNE-II',
            'wardha': 'RO Chandrapur',
            'addl. chandrapur': 'RO Chandrapur',
            'baramati': 'RO Baramati',
            'nagpur': 'RO NAGPUR',
            'borgaon meghe': 'RO NAGPUR',
            'bhivapur': 'RO NAGPUR',
            'ratnagiri': 'RO RATNAGIRI',
            'aurangabad': 'RO AURANGABAD',
            'thane': 'RO THANE-I',
            'ambarnath': 'RO THANE-II',
            'kalyan': 'RO THANE-II',
            'bhiwandi': 'RO THANE-II',
            'amravati': 'RO AMRAVATI',
            'ghatanji': 'RO AMRAVATI',
            'bhatkuli': 'RO AMRAVATI',
            'dhule': 'RO DHULE',
            'nandurbar': 'RO DHULE',
            'bhaler': 'RO DHULE',
        }
        
        # Property type mappings (English and Marathi)
        self.property_mappings = {
            'residential': 'Residential',
            'commercial': 'Commercial',
            'industrial': 'Industrial',
            'plots': 'Industrial',  # Common term
            'plot': 'Industrial',   # Singular form
            'land': 'Industrial',   # Land reference
            'price': 'Industrial',  # Price queries
            'rates': 'Industrial',  # Rate queries
            # Marathi property types
            'औद्योगिक': 'Industrial',
            'कॉमर्शियल': 'Commercial',
            'रहिवासी': 'Residential',
            'प्लॉट': 'Industrial',  # General plot reference
            'जमीन': 'Industrial',  # Land reference
            'किंमत': 'Industrial',  # Price in Marathi
            'दर': 'Industrial',     # Rate in Marathi
        }
        
        # Mixed language mappings (English words with Marathi meaning)
        self.mixed_language_mappings = {
            'punya': 'pune',
            'puny': 'pune',
            'plots': 'plots',
            'aahet': 'are',
            'aahe': 'are',
            'ka': 'what',
            'kay': 'what',
            'price': 'price',
            'kimi': 'price',
            'kimti': 'price',
            'dar': 'rate',
            'rate': 'rate',
            'rates': 'rates',
        }
        
        # Comprehensive Marathi transliteration detection
        self.marathi_transliteration_tokens = {
            # Question words
            'ka': 'what',
            'kay': 'what', 
            'kuthe': 'where',
            'kase': 'how',
            'kadhi': 'when',
            'kiti': 'how much',
            'koni': 'who',
            'kashi': 'how',
            'kashala': 'why',
            'kuthun': 'from where',
            'kuthun': 'from where',
            'kuthun': 'from where',
            
            # Location prepositions
            'madhe': 'in',
            'madhye': 'in',
            'madhyat': 'in',
            'var': 'on',
            'la': 'to',
            'hun': 'from',
            'pasun': 'from',
            'sathi': 'for',
            'barobar': 'with',
            'sobat': 'with',
            
            # Action words
            'aahet': 'are',
            'aahe': 'are',
            'ahe': 'is',
            'nahi': 'no',
            'hoi': 'yes',
            'dya': 'give',
            'dakhav': 'show',
            'shodh': 'find',
            'vach': 'read',
            'sang': 'tell',
            'bol': 'say',
            'kar': 'do',
            'ghya': 'take',
            'de': 'give',
            'le': 'take',
            
            # Property and land terms
            'jameen': 'land',
            'jameen': 'land',
            'bhumi': 'land',
            'plot': 'plot',
            'plots': 'plots',
            'bhukhand': 'plot',
            'bhukhand': 'plot',
            'sthal': 'place',
            'jaga': 'place',
            'sthala': 'place',
            
            # Price and cost terms
            'kimti': 'price',
            'kimmat': 'price',
            'dar': 'rate',
            'mulya': 'value',
            'kharcha': 'cost',
            'paisa': 'money',
            'rupya': 'rupees',
            'rs': 'rupees',
            'rupees': 'rupees',
            
            # Size and quantity
            'motha': 'big',
            'lahan': 'small',
            'swast': 'cheap',
            'mahag': 'expensive',
            'jast': 'more',
            'kami': 'less',
            'sagla': 'all',
            'kiti': 'how many',
            'ek': 'one',
            'don': 'two',
            'teen': 'three',
            'char': 'four',
            'pach': 'five',
            
            # Time and availability
            'aata': 'now',
            'aaj': 'today',
            'kal': 'yesterday',
            'udya': 'tomorrow',
            'parso': 'day after',
            'upalabdh': 'available',
            'mila': 'got',
            'nahi': 'not',
            'hoi': 'yes',
            'nako': 'no',
            
            # Regional office terms
            'kendr': 'center',
            'kendr': 'center',
            'kendr': 'center',
            'karya': 'work',
            'karyalay': 'office',
            'prant': 'region',
            'prant': 'region',
            'prant': 'region',
            
            # Common connectors
            'ani': 'and',
            'pan': 'but',
            'ki': 'or',
            'mhanun': 'therefore',
            'karan': 'because',
            'jari': 'even if',
            'tar': 'then',
            'maga': 'then',
            'nantar': 'after',
            'adhi': 'before',
            
            # Polite words
            'krupaya': 'please',
            'dhanyawad': 'thank you',
            'maaf': 'sorry',
            'namaskar': 'hello',
            'namaste': 'hello',
        }
        
        # Comprehensive semantic synonyms and root word mappings
        self.semantic_synonyms = {
            # Location variations
            'pune': ['punya', 'puny', 'pune', 'पुणे'],
            'mumbai': ['mumbai', 'bombay', 'मुंबई'],
            'bhusaval': ['bhusaval', 'bhusawal', 'bhusawad', 'भुसावळ'],
            'jalgaon': ['jalgaon', 'jalgon', 'jalgaun', 'जळगाव'],
            'nagpur': ['nagpur', 'नागपूर'],
            'aurangabad': ['aurangabad', 'औरंगाबाद'],
            'thane': ['thane', 'ठाणे'],
            'amravati': ['amravati', 'अमरावती'],
            'dhule': ['dhule', 'धुळे'],
            'chandrapur': ['chandrapur', 'चंद्रपूर'],
            'ratnagiri': ['ratnagiri', 'रत्नागिरी'],
            'baramati': ['baramati', 'बारामती'],
            
            # Property type variations
            'plots': ['plots', 'plot', 'land', 'जमीन', 'प्लॉट', 'भूखंड'],
            'industrial': ['industrial', 'औद्योगिक', 'industry', 'manufacturing'],
            'commercial': ['commercial', 'कॉमर्शियल', 'business', 'office'],
            'residential': ['residential', 'रहिवासी', 'housing', 'home'],
            
            # Price and rate variations
            'price': ['price', 'cost', 'rate', 'rates', 'किंमत', 'दर', 'मूल्य'],
            'cheap': ['cheap', 'low', 'affordable', 'budget', 'स्वस्त', 'कमी'],
            'expensive': ['expensive', 'high', 'costly', 'महाग', 'जास्त'],
            
            # Availability variations
            'available': ['available', 'उपलब्ध', 'aahet', 'aahe', 'have', 'got'],
            'show': ['show', 'दाखवा', 'dakhav', 'display', 'list'],
            'find': ['find', 'search', 'look', 'शोध', 'shodh'],
            'get': ['get', 'give', 'द्या', 'dya', 'provide'],
            
            # Question words
            'what': ['what', 'ka', 'kay', 'काय', 'kay', 'which'],
            'where': ['where', 'kuthe', 'कुठे', 'location'],
            'how': ['how', 'kase', 'कसे', 'method'],
            'when': ['when', 'kadhi', 'कधी', 'time'],
            
            # Regional office variations
            'ro': ['ro', 'regional office', 'प्रादेशिक कार्यालय'],
            'office': ['office', 'कार्यालय', 'kendr'],
        }
        
        # Intent recognition patterns
        self.intent_patterns = {
            'availability': ['available', 'aahet', 'aahe', 'have', 'got', 'उपलब्ध'],
            'price_inquiry': ['price', 'cost', 'rate', 'rates', 'किंमत', 'दर', 'kay', 'what'],
            'location_search': ['in', 'madhe', 'madhye', 'at', 'मध्ये', 'location'],
            'property_type': ['plots', 'industrial', 'commercial', 'residential', 'प्लॉट'],
            'comparison': ['compare', 'vs', 'versus', 'difference', 'तुलना'],
            'cheapest': ['cheap', 'lowest', 'minimum', 'स्वस्त', 'कमी'],
            'largest': ['big', 'large', 'maximum', 'मोठे', 'जास्त'],
        }
        
        # Common misspellings and variations
        self.spelling_variations = {
            'bhusaval': ['bhusawal', 'bhusawad', 'bhusawal', 'bhusaval'],
            'jalgaon': ['jalgaon', 'jalgon', 'jalgaun'],
            'pune': ['pune', 'punee', 'puna'],
            'mumbai': ['mumbai', 'mumbay', 'bombay'],
            'chandrapur': ['chandrapur', 'chandrapur', 'chandrapur'],
            'nagpur': ['nagpur', 'nagpur', 'nagpur'],
            'aurangabad': ['aurangabad', 'aurangabad', 'aurangabad'],
            'amravati': ['amravati', 'amravati', 'amravati'],
            'dhule': ['dhule', 'dhule', 'dhule'],
            'ratnagiri': ['ratnagiri', 'ratnagiri', 'ratnagiri'],
        }
    
    def _fuzzy_match(self, query_word, word_list, cutoff=0.6):
        """Find fuzzy matches for a word"""
        matches = get_close_matches(query_word.lower(), word_list, n=3, cutoff=cutoff)
        return matches
    
    def _extract_locations(self, query):
        """Extract potential locations from query"""
        query_lower = query.lower()
        locations = []
        
        # Check for direct city names
        for city, ro in self.region_mappings.items():
            if city in query_lower:
                locations.append((city, ro))
        
        # Check for industrial areas
        for area, ro in self.area_to_ro_mappings.items():
            if area in query_lower:
                locations.append((area, ro))
        
        # Check for RO mentions
        ro_pattern = r'ro\s+(\w+)'
        ro_matches = re.findall(ro_pattern, query_lower)
        for ro_match in ro_matches:
            # Find the full RO name
            for city, ro in self.region_mappings.items():
                if ro_match in ro.lower():
                    locations.append((city, ro))
        
        return locations
    
    def _handle_spelling_mistakes(self, query):
        """Handle spelling mistakes in the query"""
        query_lower = query.lower()
        corrected_query = query
        
        # Check for common misspellings
        for correct_word, variations in self.spelling_variations.items():
            for variation in variations:
                if variation in query_lower and variation != correct_word:
                    # Replace the misspelled word with the correct one
                    corrected_query = corrected_query.replace(variation, correct_word)
                    print(f"🔧 Corrected spelling: '{variation}' -> '{correct_word}'")
        
        return corrected_query
    
    def improve_query(self, query):
        """Main function to improve query with comprehensive semantic matching"""
        print(f"🔍 Original query: '{query}'")
        
        # Step 1: Extract root concepts from the query
        concepts = self._extract_root_concepts(query)
        print(f"🧠 Detected concepts: {concepts}")
        
        # Step 2: Handle mixed language queries and semantic synonyms
        mixed_query = self._handle_mixed_language(query)
        if mixed_query != query:
            print(f"🌐 Semantic processing: '{mixed_query}'")
        
        # Step 3: Handle spelling mistakes
        corrected_query = self._handle_spelling_mistakes(mixed_query)
        if corrected_query != mixed_query:
            print(f"✅ Corrected query: '{corrected_query}'")
        
        # Step 4: Extract locations and their RO mappings
        locations = self._extract_locations(corrected_query)
        improvements = []
        
        # Step 5: Add RO context for all found locations
        for location, ro in locations:
            if ro not in improvements:
                improvements.append(ro)
                print(f"📍 Found location: '{location}' -> '{ro}'")
        
        # Step 6: Add property type context based on detected concepts
        for prop_type in concepts['property_types']:
            if prop_type in self.property_mappings:
                improvements.append(self.property_mappings[prop_type])
                print(f"🏢 Found property type: '{prop_type}' -> '{self.property_mappings[prop_type]}'")
        
        # Step 7: Add price-related context
        for price_term in concepts['price_related']:
            if price_term == 'cheap':
                improvements.append('low cost affordable budget')
            elif price_term == 'expensive':
                improvements.append('high cost premium')
            else:
                improvements.append('price rate cost')
            print(f"💰 Found price term: '{price_term}'")
        
        # Step 8: Add availability context
        if concepts['availability_related']:
            improvements.append('available plots land')
            print("📋 Added availability context")
        
        # Step 9: Add intent-based context
        for intent in concepts['intents']:
            if intent == 'cheapest':
                improvements.append('minimum lowest affordable')
            elif intent == 'largest':
                improvements.append('maximum biggest')
            elif intent == 'comparison':
                improvements.append('compare different options')
            print(f"🎯 Found intent: '{intent}'")
        
        # Step 10: Add MIDC context if any relevant terms found
        if (concepts['locations'] or concepts['property_types'] or 
            concepts['price_related'] or concepts['availability_related']):
            improvements.append('MIDC Industrial Area')
            print("🏭 Added MIDC context")
        
        # Step 11: Combine original query with improvements
        if improvements:
            improved_query = f"{corrected_query} {' '.join(improvements)}"
            print(f"🚀 Enhanced query: '{improved_query}'")
        else:
            improved_query = corrected_query
            print(f"ℹ️ No enhancements needed: '{improved_query}'")
        
        return improved_query
    
    def _handle_mixed_language(self, query):
        """Handle mixed language queries, transliteration, and semantic synonyms"""
        words = query.split()
        improved_words = []
        marathi_transliteration_detected = False
        
        for word in words:
            word_lower = word.lower()
            found_synonym = False
            
            # Check Marathi transliteration tokens first
            if word_lower in self.marathi_transliteration_tokens:
                improved_words.append(self.marathi_transliteration_tokens[word_lower])
                marathi_transliteration_detected = True
                found_synonym = True
            
            # Check semantic synonyms for root word mapping
            if not found_synonym:
                for root_word, synonyms in self.semantic_synonyms.items():
                    if word_lower in synonyms:
                        improved_words.append(root_word)
                        found_synonym = True
                        break
            
            # If no semantic synonym found, check mixed language mappings
            if not found_synonym and word_lower in self.mixed_language_mappings:
                improved_words.append(self.mixed_language_mappings[word_lower])
                found_synonym = True
            
            # If still no mapping found, keep original word
            if not found_synonym:
                improved_words.append(word)
        
        # Store transliteration detection for language response selection
        self._last_query_was_transliteration = marathi_transliteration_detected
        
        return " ".join(improved_words)
    
    def _detect_user_intent(self, query):
        """Detect the user's intent from the query"""
        query_lower = query.lower()
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in query_lower:
                    detected_intents.append(intent)
                    break
        
        return detected_intents
    
    def _extract_root_concepts(self, query):
        """Extract root concepts from any user query"""
        query_lower = query.lower()
        concepts = {
            'locations': [],
            'property_types': [],
            'price_related': [],
            'availability_related': [],
            'intents': []
        }
        
        # Extract locations
        for root_word, synonyms in self.semantic_synonyms.items():
            if root_word in ['pune', 'mumbai', 'bhusaval', 'jalgaon', 'nagpur', 'aurangabad', 'thane', 'amravati', 'dhule', 'chandrapur', 'ratnagiri', 'baramati']:
                for synonym in synonyms:
                    if synonym in query_lower:
                        concepts['locations'].append(root_word)
                        break
        
        # Extract property types
        for root_word, synonyms in self.semantic_synonyms.items():
            if root_word in ['plots', 'industrial', 'commercial', 'residential']:
                for synonym in synonyms:
                    if synonym in query_lower:
                        concepts['property_types'].append(root_word)
                        break
        
        # Extract price-related terms
        for root_word, synonyms in self.semantic_synonyms.items():
            if root_word in ['price', 'cheap', 'expensive']:
                for synonym in synonyms:
                    if synonym in query_lower:
                        concepts['price_related'].append(root_word)
                        break
        
        # Extract availability-related terms
        for root_word, synonyms in self.semantic_synonyms.items():
            if root_word in ['available', 'show', 'find', 'get']:
                for synonym in synonyms:
                    if synonym in query_lower:
                        concepts['availability_related'].append(root_word)
                        break
        
        # Detect intents
        concepts['intents'] = self._detect_user_intent(query)
        
        return concepts
    
    def should_respond_in_marathi(self, query):
        """Determine if the response should be in Marathi based on query analysis"""
        query_lower = query.lower()
        
        # Check for Devanagari script (pure Marathi)
        has_devanagari = any('\u0900' <= char <= '\u097F' for char in query)
        if has_devanagari:
            return True
        
        # Check for Marathi transliteration tokens
        marathi_tokens_found = 0
        for token in self.marathi_transliteration_tokens.keys():
            if token in query_lower:
                marathi_tokens_found += 1
        
        # If 2 or more Marathi transliteration tokens found, respond in Marathi
        if marathi_tokens_found >= 2:
            return True
        
        # Check for common Marathi transliteration patterns
        marathi_patterns = [
            'madhe', 'madhye', 'aahet', 'aahe', 'kay', 'ka', 'kuthe', 
            'dya', 'dakhav', 'shodh', 'kimti', 'dar', 'swast', 'mahag'
        ]
        
        pattern_count = sum(1 for pattern in marathi_patterns if pattern in query_lower)
        if pattern_count >= 2:
            return True
        
        return False

# Test the smart query handler
def test_smart_query_handler():
    """Test the smart query handler with various queries"""
    handler = SmartQueryHandler()
    
    test_queries = [
        "give me plots in bhusaval",
        "plots in bhusawal",  # misspelling
        "plots in bhusawad",  # another misspelling
        "plots in RO jalgaon",
        "industrial plots in jalgaon",
        "commercial plots in pune",
        "residential plots in mumbai",
        "plots in talegaon",
        "plots in rajiv gandhi infotech park"
    ]
    
    print("🧪 Testing Smart Query Handler")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n📝 Testing: '{query}'")
        improved = handler.improve_query(query)
        print("-" * 30)

if __name__ == "__main__":
    test_smart_query_handler()
