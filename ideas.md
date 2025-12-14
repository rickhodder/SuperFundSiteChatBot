Ideas for my priject. 
I am putting together a streamlit based chatbot and python. 

The chatbot will be able to retrieve data regarding insurance policies and superfund sites. see the docs data

It will have the ability given an address to score the safety of the address based on its proximity (50 miles) to super fund sites that have not been remediated. For each unremediated site, the score will go down 25%, but cannot go lower than 0. It will also return a list of the superfund sites mentioned

It will have a RAG component that will take the scoring result and sites mentioned into a document summarizing the address and its

It will use lang chain to accomplish these things


Id like to access data through apis backed by csv files to begin with but allow for switch to vector db in future maybe using the strategy pattern

Id like a standard approch  to specify criteria for querying that would not need to change upon switching backend - maybe the specification pattern would be of use here

When moving to a vector store - if vector store has lat long coordinates in it, can you call a query that given a lat long find rows with  lat long less than fifty miles from the passed coordinates?

As for the GUI of the chatbot


The gui should be broken into sections.
Each section should have
    a header with
        a title
        a expand/collapse button with an icon that collapses the section to just showing the header
        a maximize/minimize button with an icon that switches between maximizing the section to full screen or back to its original size
    be scrollable

There should be 4 sections
1. Chat (see below)
2. Data (see below)
2. Image (see below)
2. Debug (see below) - debugging output

┌──────────────────────┬──────────┐
│                      │  Data    │
│  Chat (60%)          │  [Grid]  │
│  [Messages]          ├──────────┤
│  [Input]             │  Image   │
│                      │  [Map]   │
│                      ├──────────┤
│                      │  Debug   │
└──────────────────────┴──────────┘

the reason why i have the data section is that one of the things i dont like about chatbots is that when they show data, it is not well formatted, and scrolls the chatbot contents a lot. My thought is that for certain requests it would be better to have the data rendered in a grid section that could be temporarily maxiimzed to easier scroll through the data, and then could be set back to the original size to go back to chat.
I would like the grid to be able to filter and sort, I would like to be able to select one or multiple rows and take some action: if i ask for a list of policies, I would like to see a grid of the policies and have a button column that lets me evaluate the address of the policy against super fund site locationjs within a certain distance
debug section would be messages mostly for development and troubleshooting
The image/map section i see as more of a place where an image could be shown (which may be a map) - for example, given an address, show a map of the address and show any super fund sites within a 50 mile radius
Regarding the tab based interface in streamlit - the reason i'm not a fan of this is that you cannot activate a tab (for example if you are on the chat tab, and ask for a list of policies, I would like it to jump to the data grid to show the results)


Chat is primary focus (natural for chatbot UX)
Context panels always visible in right sidebar
No tab switching needed - all sections visible
Right sidebar sections can be collapsed individually
Any section can be maximized to full screen
