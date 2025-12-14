# 💬 Chat Commands Reference

## Policy Query Commands (NEW!)

Now you can query insurance policies directly in the chat! Type any of these commands:

### Show All Policies
```
show all policies
list all policies
all policies
```
**Result:** Displays all 15 policies in the data grid

---

### Policies by State
```
policies in NY
show policies in California
policies in TX
```
**Result:** Shows all policies in the specified state

---

### High-Risk Policies
```
high risk policies
risky policies
```
**Result:** Scores all policies and shows only HIGH and CRITICAL risk ones

---

### High-Value Policies
```
high value policies
expensive policies
```
**Result:** Shows policies worth $1,000,000 or more

---

### Policies by Coverage Type
```
comprehensive policies
comprehensive coverage
```
**Result:** Filters policies by coverage type

---

### Batch Score All Policies
```
score all policies
batch score
```
**Result:** Calculates safety scores for all policies and shows risk breakdown

---

### Show Specific Policy
```
policy P-001
P-007
```
**Result:** Shows detailed info for a specific policy including safety score

---

## Address Queries (Original Functionality)

### Check Address Safety Score
```
123 Main Street, Brooklyn, NY
456 Oak Ave, Los Angeles, CA 90012
```
**Result:** Calculates safety score, shows nearby SuperFund sites

---

## Example Queries to Try

1. **Show all policies:**
   ```
   show all policies
   ```

2. **Find NY policies:**
   ```
   policies in NY
   ```

3. **Find high-risk policies:**
   ```
   high risk policies
   ```

4. **Score all policies:**
   ```
   score all policies
   ```

5. **Check specific policy:**
   ```
   policy P-001
   ```

6. **Check address safety:**
   ```
   123 5th Street, Brooklyn, NY 11215
   ```

---

## How It Works

1. **Type command in chat** → Command is detected
2. **Backend processes query** → Uses Strategy & Specification patterns
3. **Results appear in data grid** → Automatically expands to show data
4. **Download or interact** → Use action buttons to export CSV, score policies, etc.

---

## Data Grid Features

When results appear:

- ✅ **Sortable columns** - Click headers to sort
- ✅ **Download CSV** - Export data to file
- ✅ **Score policies** - Calculate risk for policies
- ✅ **Switch views** - Toggle between policies and SuperFund sites

---

## Tips

- Commands are **case-insensitive** (works with uppercase or lowercase)
- Use **state codes** (NY, CA) or full names (New York, California)
- Click **💡 Available Commands** in chat for quick reference
- Use **Expand/Collapse/Maximize** buttons on sections

---

## Technical Details

**Powered by:**
- **Strategy Pattern** - Swappable CSV/Vector Store backends
- **Specification Pattern** - Composable query filters
- **GeoPy** - Distance calculations
- **Pandas** - Data processing
- **Streamlit** - Interactive UI

---

**All policy commands automatically display results in the data grid!** 📊
