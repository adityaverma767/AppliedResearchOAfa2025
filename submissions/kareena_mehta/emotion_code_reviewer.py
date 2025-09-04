#!/usr/bin/env python3
"""
Emotion-Driven Code Review Assistant
This program checks code comments and commit messages to figure out how a developer is feeling,
then gives them personalized advice based on those feelings.

Author: [Your Name]
"""

import re
import argparse
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from collections import defaultdict, Counter
import json
from datetime import datetime

class EmotionCodeReviewer:
    def __init__(self):
        """Gets the emotion-driven code reviewer ready with the models it needs."""
        print(" Loading emotion analysis models...")
        
        # Grabs the emotion classifier (a small model for computers)
        self.emotion_classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            device=-1  # Uses the computer's main brain
        )
        
        # Grabs the sentiment analyzer
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1
        )
        
        print(" Models loaded good!")

    def extract_code_context(self, code_text):
        """Pulls out comments, function names, and variable names from the code."""
        context = {
            'comments': [],
            'functions': [],
            'variables': [],
            'todo_items': []
        }
        
        lines = code_text.split('\n')
        for line in lines:
            line = line.strip()
            
            # Gets the comments
            if line.startswith('#') or line.startswith('//'):
                comment = re.sub(r'^[#/]+\s*', '', line)
                context['comments'].append(comment)
                
                # Looks for TODO stuff
                if 'todo' in comment.lower() or 'fixme' in comment.lower():
                    context['todo_items'].append(comment)
            
            # Finds where functions are (Python type stuff)
            func_match = re.search(r'def\s+(\w+)', line)
            if func_match:
                context['functions'].append(func_match.group(1))
            
            # Finds variable assignments, like 'x = 5'
            var_match = re.search(r'^(\w+)\s*=', line)
            if var_match:
                context['variables'].append(var_match.group(1))
        
        return context

    def analyze_developer_emotion(self, text_elements):
        """Checks how a coder is feelin' from their comments and commit messages."""
        if not text_elements:
            return {'emotion': 'neutral', 'sentiment': 'neutral', 'confidence': 0.5}
        
        # Puts all the text together to look at
        combined_text = ' '.join(text_elements)
        
        try:
            # Gets the emotion part
            emotion_result = self.emotion_classifier(combined_text)[0]
            
            # Gets the sentiment, like if it's good or bad feels
            sentiment_result = self.sentiment_analyzer(combined_text)[0]
            
            return {
                'emotion': emotion_result['label'].lower(),
                'emotion_confidence': emotion_result['score'],
                'sentiment': sentiment_result['label'].lower(),
                'sentiment_confidence': sentiment_result['score']
            }
        except Exception as e:
            print(f" Analysis error: {e}") # Uh oh, something broke during analysis
            return {'emotion': 'neutral', 'sentiment': 'neutral', 'confidence': 0.5}

    def generate_personalized_feedback(self, code_context, emotion_analysis, commit_msg=""):
        """Makes some feedback, just for them, based on the code and how they feel."""
        feedback = {
            'emotional_insights': [],
            'code_suggestions': [],
            'motivational_notes': [],
            'technical_recommendations': []
        }
        
        emotion = emotion_analysis.get('emotion', 'neutral')
        sentiment = emotion_analysis.get('sentiment', 'neutral')
        
        # What they're feelin'
        if emotion in ['anger', 'frustration']:
            feedback['emotional_insights'].append(
                " Sounds like your kinda annoyed in your comments. Just chill out - "
                "coding problems are good for you!"
            )
            feedback['motivational_notes'].append(
                " Remeber: everyone good at this was bad once. Ur getting there!"
            )
        elif emotion == 'joy':
            feedback['emotional_insights'].append(
                " Really good vibe in your code! Your happy feelings comes through in comments."
            )
        elif emotion == 'sadness':
            feedback['emotional_insights'].append(
                " Looks like your having a hard time coding. "
                "Take a break, or ask for help, don't be shy!"
            )

        # Ideas for better code
        if len(code_context['comments']) == 0:
            feedback['code_suggestions'].append(
                " Maybe put more comments in to say what your doing - "
                "you (and your friends) will be happy later!"
            )
        
        if len(code_context['todo_items']) > 3:
            feedback['code_suggestions'].append(
                f" You got {len(code_context['todo_items'])} TODO stuff to do. "
                "How about doin' some of those first, then adding new things?"
            )
        
        # Checks for stuff that ain't good
        if any(word in ' '.join(code_context['comments']).lower() 
               for word in ['hack', 'dirty', 'terrible', 'broken']):
            feedback['technical_recommendations'].append(
                " I see you saying bad things about your code. Try to make it better "
                "instead of being mean to yourself!"
            )
        
        # Ideas for variable names
        if code_context['variables']:
            short_vars = [v for v in code_context['variables'] if len(v) <= 2]
            if len(short_vars) > 2:
                feedback['technical_recommendations'].append(
                    f" Try to use longer names for variables like: {', '.join(short_vars[:3])}"
                )

        return feedback

    def review_code(self, code_text, commit_message="", developer_name="Developer"):
        """The main job to look over code and feelings."""
        print(f"\n Looking at code for {developer_name}...")
        
        # Grabs the code stuff around it
        context = self.extract_code_context(code_text)
        
        # Looks at feelings from comments and also the commit message
        text_for_analysis = context['comments'] + [commit_message] if commit_message else context['comments']
        emotion_analysis = self.analyze_developer_emotion(text_for_analysis)
        
        # Makes the feedback
        feedback = self.generate_personalized_feedback(context, emotion_analysis, commit_message)
        
        # Puts together the report
        report = {
            'developer': developer_name,
            'timestamp': datetime.now().isoformat(),
            'emotion_analysis': emotion_analysis,
            'code_metrics': {
                'comments_count': len(context['comments']),
                'functions_count': len(context['functions']),
                'todo_count': len(context['todo_items'])
            },
            'feedback': feedback
        }
        
        return report

    def print_report(self, report):
        """Shows the report so it looks nice."""
        print("\n" + "="*60)
        print(f" EMOTION-DRIVEN CODE REVIEW REPORT")
        print(f" Developer: {report['developer']}")
        print(f" Time: {report['timestamp']}")
        print("="*60)
        
        # Feelings stuff
        emotion = report['emotion_analysis']
        print(f"\n EMOTIONAL STATE ANALYSIS:")
        print(f"   Primary Emotion: {emotion.get('emotion', 'N/A').title()}")
        print(f"   Overall Sentiment: {emotion.get('sentiment', 'N/A').title()}")
        
        # Code numbers
        metrics = report['code_metrics']
        print(f"\n CODE METRICS:")
        print(f"   Comments: {metrics['comments_count']}")
        print(f"   Functions: {metrics['functions_count']}")
        print(f"   TODO Items: {metrics['todo_count']}")
        
        # The feedback parts
        feedback = report['feedback']
        
        if feedback['emotional_insights']:
            print(f"\n EMOTIONAL INSIGHTS:")
            for insight in feedback['emotional_insights']:
                print(f"   - {insight}")
        
        if feedback['code_suggestions']:
            print(f"\n CODE SUGGESTIONS:")
            for suggestion in feedback['code_suggestions']:
                print(f"   - {suggestion}")
        
        if feedback['technical_recommendations']:
            print(f"\n TECHNICAL RECOMMENDATIONS:")
            for rec in feedback['technical_recommendations']:
                print(f"   - {rec}")
        
        if feedback['motivational_notes']:
            print(f"\n MOTIVATIONAL NOTES:")
            for note in feedback['motivational_notes']:
                print(f"   - {note}")
        
        print("\n" + "="*60)


def main():
    parser = argparse.ArgumentParser(description="Emotion-Driven Code Review Assistant")
    parser.add_argument("--file", "-f", help="Python file to review")
    parser.add_argument("--commit", "-c", help="Commit message", default="")
    parser.add_argument("--name", "-n", help="Developer name", default="Developer")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample code")
    
    args = parser.parse_args()
    
    reviewer = EmotionCodeReviewer()
    
    if args.demo:
        # This here is demo code with some mad feelings
        sample_code = '''
# This is a terrible hack but I can't figure out the right way
def calculate_stuff(x, y):
    # TODO: fix this mess later
    # I hate this function, it's so confusing
    result = x * y + 42  # why 42? I have no idea anymore
    return result

# Another TODO: refactor everything
def main():
    # This probably won't work but whatever
    a = 5
    b = 10
    print(calculate_stuff(a, b))  # fingers crossed
'''
        
        commit_msg = "ughhh fixed the bug but created 3 more problems... why is coding so hard today"
        
        print(" Running demo with emotionally-charged sample code...")
        report = reviewer.review_code(sample_code, commit_msg, "Demo Developer")
        reviewer.print_report(report)
        
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                code = f.read()
            
            report = reviewer.review_code(code, args.commit, args.name)
            reviewer.print_report(report)
            
        except FileNotFoundError:
            print(f" File {args.file} not found!")
        except Exception as e:
            print(f" Error reading file: {e}") # Oops, couldn't read the file
    else:
        print(" Please provide --file or use --demo")
        print("Example: python emotion_code_reviewer.py --demo")
        print("         python emotion_code_reviewer.py --file my_script.py --commit 'Added new feature'")


if __name__ == "__main__":
    main()