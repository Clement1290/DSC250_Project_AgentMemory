# Memory Module for Student Emotional Support AI

import datetime

class UserMemory:
    """
    Stores user profile information with counseling-relevant dimensions
    Memory structure:
    {
        "id": "uuid",
        "content": "fact",
        "category": "predefined_category",
        "first_mentioned": "timestamp",
        "last_updated": "timestamp"
    }
    """

def get_fact_retrieval_prompt(new_conversation: str) -> str:
    return f"""
    # Background
    As an AI emotional support specialist for students, extract and structure key information from conversations to enable personalized support.

    # Task
    Analyze the conversation and extract facts about **student** using these categories:
    
    1. Demographics: Name, age, major, university year, cultural background
    2. Relationships: Family dynamics, romantic status, peer conflicts, social support 
    3. Mental State: Persistent emotions (anxiety, loneliness), self-perception, stress triggers
    4. Academic Context: Course workload, GPA pressure, career aspirations
    5. Behavioral Patterns: Sleep habits, substance use, coping mechanisms
    6. Life Events: Recent transitions, traumatic experiences, upcoming challenges
    7. Resources: Support systems, positive hobbies, personal strengths

    # Examples
    
    Input: "I'm a sophomore CS major struggling with panic attacks before exams"
    Output: {{
        "facts": [
            "Academic Context: Computer Science sophomore",
            "Mental State: Experiences exam-related panic attacks"
        ]
    }}

    Input: "My boyfriend and I broke up last week, and my grades are dropping"
    Output: {{
        "facts": [
            "Relationships: Recent romantic breakup",
            "Academic Context: Declining academic performance"
        ]
    }}

    # Conversation
    Below is a 20-round conversation between student and counsellor.
    {new_conversation}

    # Output Rules
    1. Return JSON with "facts" as list of strings
    2. Use "Category: Specific Detail" format
    3. Preserve original language terms when specific
    4. Omit generic statements without concrete information
    """

def get_memory_update_prompt(old_memories:dict, new_facts:dict) -> str:
    return f"""
    # Memory Management Protocol   
    Analyze new facts against existing memories. For each fact:
    - ADD if: New unique information
    - UPDATE if: Contradicts existing memory or adds nuance
    - ARCHIVE if: Outdated (>1 year) with no recent references
    - NO Change if: No new information

    # Conflict Resolution Rules
    1. Recent mentions override older conflicting information
    2. Student's self-report takes priority over inferences

    # Current Memory State
    {old_memories}

    # New Information
    {new_facts}

    # Today date
    {datetime.datetime.now()}

    # Output Requirements
    1. Return JSON with updated "memories" array
    2. Maintain conversation references in "sources"
    3. Preserve temporal metadata

    # Ouput Example
    {{
        "content": "Computer Science sophomore"",
        "category": "Academic Context",
        "first_mentioned": "timestamp",
        "last_updated": "timestamp",
        "event": "ADD"
    }}
    """