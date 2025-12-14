"""
Section Manager: Control expand/collapse/maximize for UI sections.
Manages session state for dynamic section visibility.
"""
from typing import Literal
import streamlit as st

SectionName = Literal["chat", "data_grid", "image", "debug"]
SectionState = Literal["expanded", "collapsed", "maximized"]


class SectionManager:
    """
    Manages the visibility and state of UI sections.
    Supports expand, collapse, maximize, and programmatic activation.
    """
    
    def __init__(self):
        # Initialize session state if not exists
        if 'section_states' not in st.session_state:
            st.session_state.section_states = {
                'chat': 'expanded',
                'data_grid': 'collapsed',
                'image': 'collapsed',
                'debug': 'collapsed'
            }
        
        if 'highlighted_section' not in st.session_state:
            st.session_state.highlighted_section = None
    
    def get_state(self, section: SectionName) -> SectionState:
        """Get current state of a section."""
        return st.session_state.section_states.get(section, 'collapsed')
    
    def expand(self, section: SectionName):
        """Expand a section."""
        st.session_state.section_states[section] = 'expanded'
    
    def collapse(self, section: SectionName):
        """Collapse a section."""
        st.session_state.section_states[section] = 'collapsed'
    
    def maximize(self, section: SectionName):
        """
        Maximize a section (hide all others completely).
        """
        for sec in st.session_state.section_states.keys():
            if sec == section:
                st.session_state.section_states[sec] = 'maximized'
            else:
                st.session_state.section_states[sec] = 'hidden'
    
    def minimize(self, section: SectionName):
        """
        Minimize/restore a maximized section (show all sections again).
        """
        for sec in st.session_state.section_states.keys():
            st.session_state.section_states[sec] = 'expanded'
    
    def restore_all(self):
        """Restore all sections to expanded state."""
        for sec in st.session_state.section_states.keys():
            st.session_state.section_states[sec] = 'expanded'
    
    def is_expanded(self, section: SectionName) -> bool:
        """Check if section is expanded or maximized."""
        state = self.get_state(section)
        return state in ['expanded', 'maximized']
    
    def is_collapsed(self, section: SectionName) -> bool:
        """Check if section is collapsed."""
        return self.get_state(section) == 'collapsed'
    
    def is_hidden(self, section: SectionName) -> bool:
        """Check if section is hidden (when another section is maximized)."""
        return self.get_state(section) == 'hidden'
    
    def is_maximized(self, section: SectionName) -> bool:
        """Check if section is maximized."""
        return self.get_state(section) == 'maximized'
    
    def any_maximized(self) -> bool:
        """Check if any section is currently maximized."""
        return any(state == 'maximized' for state in st.session_state.section_states.values())
    
    def highlight_section(self, section: SectionName, duration_seconds: int = 3):
        """
        Highlight a section temporarily (e.g., with colored border).
        
        Args:
            section: Section to highlight
            duration_seconds: How long to highlight (not implemented in MVP)
        """
        st.session_state.highlighted_section = section
        # Note: Auto-clear would require JavaScript or rerun logic
    
    def clear_highlight(self):
        """Clear section highlighting."""
        st.session_state.highlighted_section = None
    
    def is_highlighted(self, section: SectionName) -> bool:
        """Check if section is currently highlighted."""
        return st.session_state.highlighted_section == section
    
    def activate_section(self, section: SectionName):
        """
        Programmatically activate a section (expand + highlight).
        Used when query results need to show in a specific section.
        """
        self.expand(section)
        self.highlight_section(section)
    
    def render_section_controls(self, section: SectionName) -> None:
        """
        Render expand/collapse/maximize buttons for a section.
        Call this in the section header.
        
        Args:
            section: Section name
        """
        # Two column layout for inline display
        col1, col2 = st.columns(2)
        
        with col1:
            if self.is_collapsed(section):
                if st.button("▶", key=f"{section}_expand", help="Expand"):
                    self.expand(section)
                    st.rerun()
            else:
                if st.button("▼", key=f"{section}_collapse", help="Collapse"):
                    self.collapse(section)
                    st.rerun()
        
        with col2:
            if not self.is_maximized(section):
                if st.button("⛶", key=f"{section}_maximize", help="Maximize"):
                    self.maximize(section)
                    st.rerun()
            else:
                if st.button("⊟", key=f"{section}_minimize", help="Minimize"):
                    self.minimize(section)
                    st.rerun()
    
    def get_section_css(self, section: SectionName) -> str:
        """
        Generate CSS styling for a section based on its state.
        
        Returns:
            CSS style string
        """
        css = "padding: 10px; border-radius: 5px; margin-bottom: 10px;"
        
        if self.is_highlighted(section):
            css += " border: 2px solid #ff4b4b; box-shadow: 0 0 10px rgba(255,75,75,0.5);"
        else:
            css += " border: 1px solid #e0e0e0;"
        
        if self.is_collapsed(section) or self.is_hidden(section):
            css += " display: none;"
        
        return css


def create_section_header(section_name: str, icon: str = "") -> str:
    """
    Create a formatted section header with icon.
    
    Args:
        section_name: Display name of the section
        icon: Emoji or icon to display
    
    Returns:
        Formatted header string
    """
    return f"{icon} **{section_name}**" if icon else f"**{section_name}**"
