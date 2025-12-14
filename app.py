"""
SuperFund Site Safety Checker - Main Application
Streamlit chatbot for checking insurance policy safety based on SuperFund site proximity.
"""
import streamlit as st
import config.settings as settings
from src.section_manager import SectionManager, create_section_header
from src.safety_scorer import SafetyScorer, format_score_report
from src.strategy import get_backend, BackendFactory


# Page configuration
st.set_page_config(
    page_title=settings.APP_TITLE,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for 60/40 layout
st.markdown("""
<style>
    /* 60/40 column split */
    [data-testid="column"]:nth-child(1) {
        width: 60% !important;
    }
    [data-testid="column"]:nth-child(2) {
        width: 40% !important;
    }
    
    /* Section styling */
    .section-container {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #ffffff;
    }
    
    .section-header {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1f77b4;
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Fix chat message text color */
    .stChatMessage p, .stChatMessage div {
        color: #000000 !important;
    }
    
    /* User message styling */
    [data-testid="stChatMessageContent-user"] {
        background-color: #e3f2fd;
        color: #000000;
    }
    
    /* Assistant message styling */
    [data-testid="stChatMessageContent-assistant"] {
        background-color: #f5f5f5;
        color: #000000;
    }
    
    /* Highlighted section */
    .highlighted {
        border: 2px solid #ff4b4b !important;
        box-shadow: 0 0 10px rgba(255,75,75,0.3);
    }
</style>
""", unsafe_allow_html=True)


# Initialize managers
@st.cache_resource
def init_app():
    """Initialize application components."""
    # Validate configuration
    if not settings.validate_config():
        st.error("⚠️ Configuration error. Please check .env file.")
        st.stop()
    
    # Initialize backend
    backend = BackendFactory.create_backend("csv")  # Default to CSV for Phase 1
    
    # Initialize safety scorer
    scorer = SafetyScorer()
    
    return backend, scorer


backend, scorer = init_app()
section_manager = SectionManager()


# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_score_result' not in st.session_state:
    st.session_state.current_score_result = None

if 'current_policy_data' not in st.session_state:
    st.session_state.current_policy_data = None

if 'data_display_type' not in st.session_state:
    st.session_state.data_display_type = 'sites'  # 'sites' or 'policies'

if 'pending_command' not in st.session_state:
    st.session_state.pending_command = None


def process_chat_query(user_input: str):
    """Process user chat input - detect if it's a policy query or address."""
    from src.specifications import policies_in_state, policies_by_coverage_type, high_value_policies
    
    user_lower = user_input.lower()
    
    # Policy commands
    if any(cmd in user_lower for cmd in ['show all policies', 'list all policies', 'all policies']):
        handle_show_all_policies()
    
    elif 'policies in' in user_lower or 'show policies in' in user_lower:
        # Extract state (look for 2-letter state codes or state names)
        state = extract_state_from_query(user_input)
        if state:
            handle_policies_by_state(state)
        else:
            show_error("Could not identify state. Try: 'show policies in NY'")
    
    elif 'high risk policies' in user_lower or 'risky policies' in user_lower:
        handle_high_risk_policies()
    
    elif 'high value policies' in user_lower or 'expensive policies' in user_lower:
        handle_high_value_policies()
    
    elif 'comprehensive policies' in user_lower or 'comprehensive coverage' in user_lower:
        handle_policies_by_coverage('Comprehensive')
    
    elif 'score all policies' in user_lower or 'batch score' in user_lower:
        handle_batch_score_policies()
    
    elif user_input.startswith('policy ') or user_input.upper().startswith('P-'):
        # Show specific policy
        policy_id = user_input.replace('policy ', '').replace('Policy ', '').strip()
        handle_show_policy(policy_id)
    
    else:
        # Default: treat as address for safety score
        handle_address_query(user_input)


def extract_state_from_query(query: str) -> str:
    """Extract state code from query."""
    import re
    
    # Valid US state codes
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    
    # Check for full state names first
    state_names = {
        'new york': 'NY', 'california': 'CA', 'texas': 'TX',
        'florida': 'FL', 'illinois': 'IL', 'washington': 'WA',
        'nevada': 'NV', 'oregon': 'OR', 'arizona': 'AZ',
        'colorado': 'CO', 'massachusetts': 'MA', 'michigan': 'MI'
    }
    
    query_lower = query.lower()
    for name, code in state_names.items():
        if name in query_lower:
            return code
    
    # Extract all two-letter uppercase words
    state_pattern = r'\b([A-Z]{2})\b'
    matches = re.findall(state_pattern, query.upper())
    
    # Filter to only valid state codes first
    valid_matches = [m for m in matches if m in valid_states]
    
    # Return the last valid state code found (more likely to be the target state)
    # Example: "policies in NY" -> matches=['IN', 'NY'] -> return 'NY'
    if valid_matches:
        return valid_matches[-1]
    
    return None


def handle_show_all_policies():
    """Show all policies."""
    with st.spinner("Loading all policies..."):
        policies = backend.get_all_policies()
        
        if policies.empty:
            response = "❌ No policies found in database."
        else:
            response = f"📋 **Found {len(policies)} policies**\n\nDisplaying in data grid below."
            st.session_state.current_policy_data = policies
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_policies_by_state(state: str):
    """Show policies in a specific state."""
    from src.specifications import policies_in_state
    
    with st.spinner(f"Finding policies in {state}..."):
        spec = policies_in_state(state)
        policies = backend.query_policies(spec)
        
        if policies.empty:
            response = f"❌ No policies found in {state}."
        else:
            response = f"📋 **Found {len(policies)} policies in {state}**\n\nDisplaying in data grid below."
            st.session_state.current_policy_data = policies
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_high_risk_policies():
    """Find and display high-risk policies."""
    with st.spinner("Scoring all policies for risk..."):
        results = scorer.batch_score_from_csv()
        
        if results.empty:
            response = "❌ No policies found to score."
        else:
            # Filter for high/critical risk
            high_risk = results[results['risk_level'].isin(['HIGH', 'CRITICAL'])]
            
            if high_risk.empty:
                response = "✅ No high-risk policies found!"
            else:
                response = f"⚠️ **Found {len(high_risk)} high-risk policies**\n\nDisplaying in data grid below."
                st.session_state.current_policy_data = high_risk
                st.session_state.data_display_type = 'policies'
                section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_high_value_policies():
    """Show high-value policies ($1M+)."""
    from src.specifications import high_value_policies
    
    with st.spinner("Finding high-value policies..."):
        spec = high_value_policies(min_value=1000000)
        policies = backend.query_policies(spec)
        
        if policies.empty:
            response = "❌ No high-value policies ($1M+) found."
        else:
            response = f"💰 **Found {len(policies)} high-value policies ($1M+)**\n\nDisplaying in data grid below."
            st.session_state.current_policy_data = policies
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_policies_by_coverage(coverage_type: str):
    """Show policies by coverage type."""
    from src.specifications import policies_by_coverage_type
    
    with st.spinner(f"Finding {coverage_type} policies..."):
        spec = policies_by_coverage_type(coverage_type)
        policies = backend.query_policies(spec)
        
        if policies.empty:
            response = f"❌ No {coverage_type} policies found."
        else:
            response = f"📋 **Found {len(policies)} {coverage_type} policies**\n\nDisplaying in data grid below."
            st.session_state.current_policy_data = policies
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_batch_score_policies():
    """Batch score all policies."""
    with st.spinner("Scoring all policies..."):
        results = scorer.batch_score_from_csv()
        
        if results.empty:
            response = "❌ No policies found to score."
        else:
            response = f"✅ **Scored {len(results)} policies**\n\n"
            response += f"- SAFE: {len(results[results['risk_level'] == 'SAFE'])}\n"
            response += f"- LOW: {len(results[results['risk_level'] == 'LOW'])}\n"
            response += f"- MEDIUM: {len(results[results['risk_level'] == 'MEDIUM'])}\n"
            response += f"- HIGH: {len(results[results['risk_level'] == 'HIGH'])}\n"
            response += f"- CRITICAL: {len(results[results['risk_level'] == 'CRITICAL'])}\n\n"
            response += "Displaying results in data grid below."
            
            st.session_state.current_policy_data = results
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_show_policy(policy_id: str):
    """Show details for a specific policy."""
    with st.spinner(f"Finding policy {policy_id}..."):
        policies = backend.get_all_policies()
        policy = policies[policies['policy_id'].str.upper() == policy_id.upper()]
        
        if policy.empty:
            response = f"❌ Policy {policy_id} not found."
        else:
            p = policy.iloc[0]
            response = f"📋 **Policy {p['policy_id']}**\n\n"
            response += f"- Address: {p['address']}, {p['city']}, {p['state']}\n"
            response += f"- Property Value: ${p['property_value']:,.0f}\n"
            response += f"- Coverage: {p['coverage_type']}\n\n"
            
            # Score this policy
            result = scorer.score_policy(latitude=p['latitude'], longitude=p['longitude'])
            response += f"🎯 Safety Score: {result['score']}/100\n"
            response += f"⚠️ Risk Level: {result['risk_level']}\n"
            response += f"🏭 Nearby Sites: {result['site_count']}"
            
            st.session_state.current_policy_data = policy
            st.session_state.data_display_type = 'policies'
            section_manager.maximize("data_grid")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        st.rerun()


def handle_address_query(address: str):
    """Handle address-based safety score query."""
    with st.spinner("Calculating safety score..."):
        try:
            score_result = scorer.score_policy(address=address)
            st.session_state.current_score_result = score_result
            st.session_state.data_display_type = 'sites'
            
            # Format response
            response = format_score_report(score_result)
            
            # Add assistant response
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            
            # Maximize data grid if sites found
            if score_result['site_count'] > 0:
                section_manager.maximize("data_grid")
            
            st.rerun()
        
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": error_msg
            })
            st.rerun()


def show_error(message: str):
    """Display error message."""
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": f"❌ {message}"
    })
    st.rerun()


def main():
    """Main application layout."""
    
    # Title
    st.title(f"🏭 {settings.APP_TITLE}")
    st.markdown("Check insurance policy safety based on proximity to SuperFund sites")
    st.divider()
    
    # Check if any section is maximized
    if section_manager.any_maximized():
        # Show only the maximized section in full width
        if section_manager.is_maximized("chat"):
            render_chat_section()
        elif section_manager.is_maximized("data_grid"):
            render_data_section()
        elif section_manager.is_maximized("image"):
            render_image_section()
        elif section_manager.is_maximized("debug"):
            render_debug_section()
    else:
        # Normal 60/40 column layout
        col_chat, col_sidebar = st.columns([60, 40])
        
        # ========== LEFT COLUMN: CHAT (60%) ==========
        with col_chat:
            render_chat_section()
        
        # ========== RIGHT COLUMN: DATA/IMAGE/DEBUG (40%) ==========
        with col_sidebar:
            render_data_section()
            render_image_section()
            render_debug_section()


def render_chat_section():
    """Render the chat interface section."""
    st.markdown(f"### {create_section_header('Chat', '💬')}")
    
    # Section controls
    section_manager.render_section_controls("chat")
    
    if not section_manager.is_collapsed("chat") and not section_manager.is_hidden("chat"):
        # Chat history display
        chat_container = st.container(height=400)
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Check for pending command from button click
        if st.session_state.pending_command:
            user_input = st.session_state.pending_command
            st.session_state.pending_command = None  # Clear it
            
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Process query
            process_chat_query(user_input)
        
        # Chat input
        user_input = st.chat_input("Enter an address or policy command (e.g., 'show all policies')...")
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Process query
            process_chat_query(user_input)
        
        # Show available commands below input
        with st.expander("💡 Available Commands", expanded=False):
            st.markdown("**Click any command to run it:**")
            
            st.markdown("**🏢 Address Safety Queries:**")
            col_addr1, col_addr2 = st.columns(2)
            with col_addr1:
                if st.button("📍 123 Main St, Brooklyn, NY", key="cmd_address1", use_container_width=True):
                    st.session_state.pending_command = "123 Main St, Brooklyn, NY"
                    st.rerun()
                if st.button("📍 100 Canal St, New York, NY", key="cmd_address2", use_container_width=True):
                    st.session_state.pending_command = "100 Canal St, New York, NY"
                    st.rerun()
            with col_addr2:
                if st.button("📍 456 Oak Ave, Los Angeles, CA", key="cmd_address3", use_container_width=True):
                    st.session_state.pending_command = "456 Oak Ave, Los Angeles, CA"
                    st.rerun()
                if st.button("📍 789 Elm Rd, Niagara Falls, NY", key="cmd_address4", use_container_width=True):
                    st.session_state.pending_command = "789 Elm Rd, Niagara Falls, NY"
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**📋 Policy Queries:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Show all policies", key="cmd_all", use_container_width=True):
                    st.session_state.pending_command = "show all policies"
                    st.rerun()
                if st.button("🗺️ Policies in NY", key="cmd_state", use_container_width=True):
                    st.session_state.pending_command = "policies in NY"
                    st.rerun()
                if st.button("⚠️ High risk policies", key="cmd_risk", use_container_width=True):
                    st.session_state.pending_command = "high risk policies"
                    st.rerun()
                if st.button("💰 High value policies", key="cmd_value", use_container_width=True):
                    st.session_state.pending_command = "high value policies"
                    st.rerun()
            with col2:
                if st.button("🛡️ Comprehensive policies", key="cmd_comp", use_container_width=True):
                    st.session_state.pending_command = "comprehensive policies"
                    st.rerun()
                if st.button("🔢 Score all policies", key="cmd_score", use_container_width=True):
                    st.session_state.pending_command = "score all policies"
                    st.rerun()
                if st.button("🔍 Policy P-001", key="cmd_specific", use_container_width=True):
                    st.session_state.pending_command = "policy P-001"
                    st.rerun()
                if st.button("🗺️ Policies in CA", key="cmd_state_ca", use_container_width=True):
                    st.session_state.pending_command = "policies in CA"
                    st.rerun()


def render_data_section():
    """Render the data grid section."""
    st.markdown(f"### {create_section_header('Data Grid', '📊')}")
    
    # Section controls
    section_manager.render_section_controls("data_grid")
    
    if not section_manager.is_collapsed("data_grid") and not section_manager.is_hidden("data_grid"):
        # Check what type of data to display
        if st.session_state.data_display_type == 'policies' and st.session_state.current_policy_data is not None:
            # Display policy data
            policy_data = st.session_state.current_policy_data
            
            if not policy_data.empty:
                st.markdown("**Policy Data:**")
                
                # Select columns to display
                display_cols = ['policy_id', 'address', 'city', 'state']
                
                # Add score columns if they exist
                if 'score' in policy_data.columns:
                    display_cols.extend(['score', 'risk_level', 'site_count'])
                
                # Add property value if exists
                if 'property_value' in policy_data.columns:
                    display_cols.append('property_value')
                
                # Filter to only existing columns
                display_cols = [col for col in display_cols if col in policy_data.columns]
                
                # Display dataframe
                st.dataframe(
                    policy_data[display_cols],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Action buttons
                st.markdown("**Actions:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv = policy_data.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="policies.csv",
                        mime="text/csv",
                        key="download_policy_csv"
                    )
                
                with col2:
                    if 'score' not in policy_data.columns:
                        if st.button("🎯 Score These Policies", key="score_policies"):
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": "score all policies"
                            })
                            handle_batch_score_policies()
                
                with col3:
                    if st.button("🔄 Show SuperFund Sites", key="switch_to_sites"):
                        st.session_state.data_display_type = 'sites'
                        st.rerun()
            else:
                st.info("✅ No policies to display")
        
        elif st.session_state.current_score_result:
            # Display SuperFund site data
            nearby_sites = st.session_state.current_score_result['nearby_sites']
            
            if not nearby_sites.empty:
                st.markdown("**Nearby SuperFund Sites:**")
                
                # Display in dataframe
                st.dataframe(
                    nearby_sites[['site_name', 'city', 'state', 'status']],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Action buttons
                st.markdown("**Actions:**")
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = nearby_sites.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="superfund_sites.csv",
                        mime="text/csv",
                        key="download_sites_csv"
                    )
                
                with col2:
                    if st.button("🗺️ Show on Map", key="show_map"):
                        section_manager.activate_section("image")
                        st.rerun()
            else:
                st.info("✅ No nearby unremediated SuperFund sites found!")
        else:
            st.info("Enter a query in chat to see results...")


def render_image_section():
    """Render the image/map section."""
    st.markdown(f"### {create_section_header('Map View', '🗺️')}")
    
    # Section controls
    section_manager.render_section_controls("image")
    
    if not section_manager.is_collapsed("image") and not section_manager.is_hidden("image"):
        if st.session_state.current_score_result:
            st.info("🚧 Map visualization coming in Phase 2")
            
            # Display location info
            location = st.session_state.current_score_result['location']
            st.write(f"**Center Location:** {location[0]:.4f}, {location[1]:.4f}")
            st.write(f"**Radius:** {st.session_state.current_score_result['radius_miles']} miles")
            st.write(f"**Sites:** {st.session_state.current_score_result['site_count']}")
        else:
            st.info("Map will display after running a safety check...")


def render_debug_section():
    """Render the debug section (collapsible by default)."""
    if settings.DEBUG_MODE:
        st.markdown(f"### {create_section_header('Debug Info', '🔧')}")
        
        # Section controls
        section_manager.render_section_controls("debug")
        
        if not section_manager.is_collapsed("debug") and not section_manager.is_hidden("debug"):
            st.json({
                "backend": backend.__class__.__name__,
                "chat_history_count": len(st.session_state.chat_history),
                "score_result_available": st.session_state.current_score_result is not None,
                "section_states": st.session_state.section_states
            })


if __name__ == "__main__":
    main()
