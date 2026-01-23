"""
Transcript Parser for APROCSA CHAT format files
Extracts participant speech and computes linguistic features
"""

import re
from typing import Dict, List, Tuple
from pathlib import Path


class TranscriptParser:
    """Parser for CHAT format transcripts"""
    
    def __init__(self):
        # Pause markers in CHAT format
        self.pause_markers = ['(.)', '(..)', '(...)']
        # Filled pause patterns (e.g., &-um, &-uh)
        self.filled_pause_pattern = re.compile(r'&-\w+')
        # Non-word elements to remove (e.g., &=throat:clears)
        self.non_verbal_pattern = re.compile(r'&=[\w:]+')
        
    def parse_transcript(self, filepath: str) -> Tuple[List[str], List[str]]:
        """
        Parse a CHAT transcript file.
        
        Returns:
            Tuple of (participant_utterances, investigator_utterances)
        """
        participant_utterances = []
        investigator_utterances = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Extract participant speech
                if line.startswith('*PAR:'):
                    utterance = line.split(':', 1)[1].strip()
                    participant_utterances.append(utterance)
                
                # Extract investigator speech (both INV1 and INV2)
                elif line.startswith('*INV1:') or line.startswith('*INV2:'):
                    utterance = line.split(':', 1)[1].strip()
                    investigator_utterances.append(utterance)
        
        return participant_utterances, investigator_utterances
    
    def preprocess_utterance(self, utterance: str) -> Dict:
        """
        Preprocess an utterance and extract linguistic features.
        
        Returns a dictionary with:
        - raw: original utterance
        - cleaned: cleaned utterance
        - tokens: list of word tokens
        - filled_pauses: count of filled pauses
        - pause_markers: count of pause markers
        """
        # Store original
        raw = utterance
        
        # Count filled pauses before removal
        filled_pauses = len(self.filled_pause_pattern.findall(utterance))
        
        # Count pause markers before removal
        pause_marker_count = sum(utterance.count(pm) for pm in self.pause_markers)
        
        # Remove timing information (appears at end of line)
        utterance = re.sub(r'\d+_\d+', '', utterance)
        
        # Remove non-verbal markers
        utterance = self.non_verbal_pattern.sub('', utterance)
        
        # Remove filled pauses
        utterance = self.filled_pause_pattern.sub('', utterance)
        
        # Remove pause markers
        for marker in self.pause_markers:
            utterance = utterance.replace(marker, '')
        
        # Remove retracing markers [//], [/], etc.
        utterance = re.sub(r'\[/?/?\+?\s*\w*\]', '', utterance)
        
        # Remove angle brackets with content (e.g., <word>)
        utterance = re.sub(r'<[^>]+>', '', utterance)
        
        # Remove @ markers (e.g., and@q, the@q)
        utterance = re.sub(r'@\w+', '', utterance)
        
        # Remove incomplete word markers like (a)n(d)
        utterance = re.sub(r'\([a-z]\)', '', utterance)
        
        # Remove special markers like ‡
        utterance = re.sub(r'‡', '', utterance)
        
        # Tokenize: split by whitespace and punctuation
        # Keep punctuation as separate tokens
        tokens = re.findall(r'\b\w+\b|[.,!?;:]', utterance)
        
        # Remove empty strings
        tokens = [t for t in tokens if t]
        
        # Cleaned utterance (join tokens)
        cleaned = ' '.join(tokens)
        
        return {
            'raw': raw,
            'cleaned': cleaned,
            'tokens': tokens,
            'filled_pauses': filled_pauses,
            'pause_markers': pause_marker_count
        }
    
    def compute_statistics(self, utterances: List[str]) -> Dict:
        """
        Compute linguistic statistics for a list of utterances.
        
        Returns:
            Dictionary with statistical measures
        """
        total_utterances = len(utterances)
        
        if total_utterances == 0:
            return {
                'total_utterances': 0,
                'total_tokens': 0,
                'mean_utterance_length': 0,
                'lexical_diversity': 0,
                'filled_pauses_per_100': 0,
                'pause_markers_per_100': 0,
                'unique_types': 0
            }
        
        all_tokens = []
        total_filled_pauses = 0
        total_pause_markers = 0
        utterance_lengths = []
        
        for utterance in utterances:
            processed = self.preprocess_utterance(utterance)
            tokens = processed['tokens']
            
            all_tokens.extend(tokens)
            total_filled_pauses += processed['filled_pauses']
            total_pause_markers += processed['pause_markers']
            utterance_lengths.append(len(tokens))
        
        total_tokens = len(all_tokens)
        unique_types = len(set(all_tokens))
        
        # Type-Token Ratio (TTR)
        lexical_diversity = unique_types / total_tokens if total_tokens > 0 else 0
        
        # Mean utterance length
        mean_utterance_length = sum(utterance_lengths) / total_utterances if total_utterances > 0 else 0
        
        # Pauses per 100 tokens
        filled_pauses_per_100 = (total_filled_pauses / total_tokens * 100) if total_tokens > 0 else 0
        pause_markers_per_100 = (total_pause_markers / total_tokens * 100) if total_tokens > 0 else 0
        
        return {
            'total_utterances': total_utterances,
            'total_tokens': total_tokens,
            'mean_utterance_length': mean_utterance_length,
            'lexical_diversity': lexical_diversity,
            'filled_pauses_per_100': filled_pauses_per_100,
            'pause_markers_per_100': pause_markers_per_100,
            'unique_types': unique_types
        }


def parse_all_transcripts(transcript_dir: str) -> Dict:
    """
    Parse all transcripts in a directory.
    
    Returns:
        Dictionary mapping participant ID to statistics
    """
    parser = TranscriptParser()
    results = {}
    
    transcript_path = Path(transcript_dir)
    
    for file in sorted(transcript_path.glob('*.cha')):
        # Extract participant ID from filename (e.g., aprocsa1554a.cha -> 1554)
        participant_id = file.stem.replace('aprocsa', '').replace('a', '')
        
        # Parse transcript
        par_utterances, inv_utterances = parser.parse_transcript(str(file))
        
        # Compute statistics
        par_stats = parser.compute_statistics(par_utterances)
        inv_stats = parser.compute_statistics(inv_utterances)
        
        results[participant_id] = {
            'participant': par_stats,
            'investigator': inv_stats,
            'par_utterances': par_utterances,
            'inv_utterances': inv_utterances
        }
    
    return results


if __name__ == '__main__':
    # Test the parser
    results = parse_all_transcripts('transcripts')
    
    # Print example
    for pid, data in results.items():
        print(f"\nParticipant {pid}:")
        print(f"  Utterances: {data['participant']['total_utterances']}")
        print(f"  Tokens: {data['participant']['total_tokens']}")
        print(f"  Mean length: {data['participant']['mean_utterance_length']:.2f}")
