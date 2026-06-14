import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import product
import datetime

# Page configuration
st.set_page_config(
    page_title="MallQ! - Centralized Intelligent Mall Platform",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling
st.markdown("""
<style>
    /* Styling for Metric Cards */
    .metric-card {
        background-color: #f8fafc;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        border-left: 5px solid #6366f1;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e1b4b;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Styling for Product Showcase Cards */
    .product-card {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
    }
    
    /* Badges */
    .badge-floor {
        background-color: #f1f5f9;
        color: #334155;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-promo {
        background-color: #fef3c7;
        color: #b45309;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 5px;
    }
    .badge-stock {
        background-color: #d1fae5;
        color: #065f46;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-low-stock {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. CENTRAL BACKEND DATABASE (MOCK DATA)
# ----------------------------------------
INITIAL_DATA = [
    {
        "id": 1,
        "name": "Slim Fit Cotton Shirt",
        "brand": "Zara",
        "category": "Shirts",
        "sub_category": "Shirt",
        "price": 2490,
        "color": "White",
        "store": "Zara",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop&q=60",
        "sizes": ["S", "M", "L", "XL"],
        "rating": 4.5,
        "offer": "10% Off on Axis Cards",
        "stock": 14
    },
    {
        "id": 2,
        "name": "Casual Oxford Shirt",
        "brand": "H&M",
        "category": "Shirts",
        "sub_category": "Shirt",
        "price": 1499,
        "color": "White",
        "store": "H&M",
        "floor": "First Floor",
        "image_url": "https://images.unsplash.com/photo-1620012253295-c05cd3e713d3?w=500&auto=format&fit=crop&q=60",
        "sizes": ["M", "L", "XL"],
        "rating": 4.2,
        "offer": "Buy 2 Get 1 Free",
        "stock": 8
    },
    {
        "id": 3,
        "name": "511 Slim Fit Jeans",
        "brand": "Levi's",
        "category": "Jeans",
        "sub_category": "Jeans",
        "price": 3499,
        "color": "Blue",
        "store": "Levi's",
        "floor": "First Floor",
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&auto=format&fit=crop&q=60",
        "sizes": ["30", "32", "34", "36"],
        "rating": 4.7,
        "offer": "Flat ₹500 Off on exchange",
        "stock": 15
    },
    {
        "id": 4,
        "name": "Air Max Classic",
        "brand": "Nike",
        "category": "Shoes",
        "sub_category": "Sneakers",
        "price": 7999,
        "color": "Black",
        "store": "Nike",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=60",
        "sizes": ["UK 7", "UK 8", "UK 9", "UK 10"],
        "rating": 4.8,
        "offer": "No Cost EMI available",
        "stock": 3
    },
    {
        "id": 5,
        "name": "Smash v2 Leather Sneakers",
        "brand": "Puma",
        "category": "Shoes",
        "sub_category": "Sneakers",
        "price": 2799,
        "color": "White",
        "store": "Puma",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&auto=format&fit=crop&q=60",
        "sizes": ["UK 6", "UK 7", "UK 8", "UK 9"],
        "rating": 4.3,
        "offer": "Flat 20% Off",
        "stock": 18
    },
    {
        "id": 6,
        "name": "Ultraboost Running Shoes",
        "brand": "Adidas",
        "category": "Shoes",
        "sub_category": "Sneakers",
        "price": 12999,
        "color": "Grey",
        "store": "Adidas",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?w=500&auto=format&fit=crop&q=60",
        "sizes": ["UK 8", "UK 9", "UK 10"],
        "rating": 4.9,
        "offer": "Free Running Socks with purchase",
        "stock": 4
    },
    {
        "id": 7,
        "name": "Vintage Digital Watch",
        "brand": "Casio",
        "category": "Watches",
        "sub_category": "Watch",
        "price": 1695,
        "color": "Silver",
        "store": "Casio",
        "floor": "Second Floor",
        "image_url": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=500&auto=format&fit=crop&q=60",
        "sizes": ["Free Size"],
        "rating": 4.6,
        "offer": "2 Year Extended Warranty",
        "stock": 25
    },
    {
        "id": 8,
        "name": "Minimalist Leather Watch",
        "brand": "Fossil",
        "category": "Watches",
        "sub_category": "Watch",
        "price": 8495,
        "color": "Brown",
        "store": "Fossil",
        "floor": "Second Floor",
        "image_url": "https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=500&auto=format&fit=crop&q=60",
        "sizes": ["Free Size"],
        "rating": 4.4,
        "offer": "Free Custom Engraving",
        "stock": 6
    },
    {
        "id": 9,
        "name": "Lego Star Wars Fighter",
        "brand": "Lego",
        "category": "Toys",
        "sub_category": "Toy",
        "price": 3499,
        "color": "Grey",
        "store": "Hamleys",
        "floor": "Second Floor",
        "image_url": "https://images.unsplash.com/photo-1585366119957-e57b34b11f72?w=500&auto=format&fit=crop&q=60",
        "sizes": ["One Size"],
        "rating": 4.8,
        "offer": "Flat 10% Off",
        "stock": 9
    },
    {
        "id": 10,
        "name": "Hamleys Soft Teddy Bear",
        "brand": "Hamleys",
        "category": "Toys",
        "sub_category": "Toy",
        "price": 1299,
        "color": "Brown",
        "store": "Hamleys",
        "floor": "Second Floor",
        "image_url": "https://images.unsplash.com/photo-1559251606-c623743a6d76?w=500&auto=format&fit=crop&q=60",
        "sizes": ["One Size"],
        "rating": 4.5,
        "offer": "Buy 1 Get Mini Teddy Free",
        "stock": 30
    },
    {
        "id": 11,
        "name": "Polo Collar T-Shirt",
        "brand": "Tommy Hilfiger",
        "category": "T-shirts",
        "sub_category": "T-shirt",
        "price": 2999,
        "color": "Red",
        "store": "Tommy Hilfiger",
        "floor": "First Floor",
        "image_url": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500&auto=format&fit=crop&q=60",
        "sizes": ["S", "M", "L", "XL", "XXL"],
        "rating": 4.4,
        "offer": "15% Off on buying two",
        "stock": 11
    },
    {
        "id": 12,
        "name": "Regular Fit Casual Pants",
        "brand": "Marks & Spencer",
        "category": "Pants",
        "sub_category": "Pants",
        "price": 2299,
        "color": "Beige",
        "store": "Marks & Spencer",
        "floor": "First Floor",
        "image_url": "https://images.unsplash.com/photo-1479064555552-3ef4979f8908?w=500&auto=format&fit=crop&q=60",
        "sizes": ["32", "34", "36", "38"],
        "rating": 4.3,
        "offer": "Flat 10% Off",
        "stock": 13
    },
    {
        "id": 13,
        "name": "Graphic Print Crewneck",
        "brand": "Zara",
        "category": "T-shirts",
        "sub_category": "T-shirt",
        "price": 1790,
        "color": "Black",
        "store": "Zara",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop&q=60",
        "sizes": ["S", "M", "L"],
        "rating": 4.1,
        "offer": "Trendsetter Special Deal",
        "stock": 7
    },
    {
        "id": 14,
        "name": "White Court Classic Shoes",
        "brand": "Adidas",
        "category": "Shoes",
        "sub_category": "Sneakers",
        "price": 3999,
        "color": "White",
        "store": "Adidas",
        "floor": "Ground Floor",
        "image_url": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500&auto=format&fit=crop&q=60",
        "sizes": ["UK 7", "UK 8", "UK 9"],
        "rating": 4.6,
        "offer": "Flat ₹500 discount coupon",
        "stock": 10
    }
]

# Initialize stateful database
if 'db' not in st.session_state:
    st.session_state.db = INITIAL_DATA.copy()

# Initialize simulated search logs for Management Dashboard analytics
if 'search_logs' not in st.session_state:
    st.session_state.search_logs = [
        {"timestamp": datetime.datetime.now(), "category": "Shirts", "query": "white shirt"},
        {"timestamp": datetime.datetime.now(), "category": "Shoes", "query": "sneakers under 5000"},
        {"timestamp": datetime.datetime.now(), "category": "Watches", "query": "fossil"},
        {"timestamp": datetime.datetime.now(), "category": "Jeans", "query": "blue jeans"}
    ]

# ----------------------------------------
# SIDEBAR CONTROL & NAVIGATION
# ----------------------------------------
with st.sidebar:
    st.title("🎛️ MallQ! Control Center")
    st.write("Centralizing modern physical retail.")
    
    # Showcase active simulation capabilities
    st.subheader("🏢 Switch User View")
    user_role = st.radio(
        "Demonstrate Multi-Stakeholder access:",
        ["Shopper Interface", "Store Merchant Dashboard", "Mall Management Portal"]
    )
    
    st.divider()
    st.markdown("""
    **Demo Hint for Your Pitch:**
    1. Go to **Merchant Dashboard**, pick *Zara*, and reduce the price of the **Slim Fit Cotton Shirt** from ₹2490 to ₹1900.
    2. Switch back to **Shopper Interface** and run a search for a 'white shirt and sneakers under ₹5000'.
    3. Watch how the AI planner live-updates the pricing and routes instantly!
    """)
    
    st.divider()
    st.caption("Developed for College Presentation Pitch • Prototypes v1.2")

# ----------------------------------------
# MAIN PAGE HEADER
# ----------------------------------------
col_logo, col_heading = st.columns([1, 6])
with col_logo:
    st.image("https://images.unsplash.com/photo-1563013544-824ae1d704d3?w=150&auto=format&fit=crop&q=60", width=80)
with col_heading:
    st.title("MallQ! ⚡ Elevating Mall Shopping")
    st.write("*Synchronized physical inventory locator, dynamic routing solver, and hyper-local promotion engine.*")

# Expandable Sales Pitch Info Card
with st.expander("💡 View Quick Sales Pitch Cheat Sheet (Open for Presentation)", expanded=True):
    st.markdown("""
    ### 🎯 The Slide Outline / Verbal Presentation Guide:
    * **The Problem:** Shoppers face physical fatigue wandering from Zara on Ground Floor to H&M on the 1st Floor only to find their size is out of stock. Retailers lose sales to instant e-commerce.
    * **The Solution (MallQ!):** This app aggregates real-time inventory from retail store APIs.
    * **Features Demo'd Below:**
      1. **Dynamic Shopping Planner:** Type "White shirt & Sneaker under ₹5000" and get sequential floor-level routes (No backtracking!).
      2. **Live Directory & Stock Check:** Check specific sizes available *before* walking to a physical counter.
      3. **Interactive Business Portals:** Store merchants update local inventory on-the-fly, while Mall managers observe footfall density analytics.
    """)

# ----------------------------------------------------------------------------------------------------------------------
# ROLE 1: SHOPPER INTERFACE
# ----------------------------------------------------------------------------------------------------------------------
if user_role == "Shopper Interface":
    
    tab_planner, tab_dir, tab_deals = st.tabs([
        "🧭 AI Shopping Planner", 
        "🛍️ Live Directory & Floor Map", 
        "🏷️ Live Deals & Compare"
    ])
    
    # TAB 1: AI SHOPPING PLANNER
    with tab_planner:
        st.subheader("🧭 Smart Budget & Route Optimizer")
        st.write("Plan your shopping list. Our solver groups products dynamically, sorts them sequential-floor-wise, and calculates total budget fits.")

        # Preset option button for quick demo during pitch
        col_preset1, col_preset2, _ = st.columns([1.5, 1.5, 4])
        with col_preset1:
            if st.button("🔥 Run Demo Preset (White Shirt + Sneakers Under ₹5000)"):
                st.session_state.search_cats = ["Shirt", "Sneakers"]
                st.session_state.search_colors = ["White"]
                st.session_state.search_budget = 5000
        with col_preset2:
            if st.button("🔄 Reset Fields"):
                st.session_state.search_cats = []
                st.session_state.search_colors = []
                st.session_state.search_budget = 15000

        col_input_1, col_input_2 = st.columns(2)
        with col_input_1:
            all_subcats = sorted(list(set(item['sub_category'] for item in st.session_state.db)))
            selected_cats = st.multiselect(
                "I want to buy:",
                all_subcats,
                default=st.session_state.get('search_cats', ["Shirt", "Sneakers"]),
                key="sel_cats"
            )
            
        with col_input_2:
            all_colors = sorted(list(set(item['color'] for item in st.session_state.db)))
            selected_colors = st.multiselect(
                "Preferred Color (Leave empty for any color):",
                all_colors,
                default=st.session_state.get('search_colors', ["White"]),
                key="sel_colors"
            )

        budget_slider = st.slider(
            "My Maximum Combined Budget (₹)",
            1000, 25000, 
            value=st.session_state.get('search_budget', 5000), 
            step=500,
            key="sel_budget"
        )

        # Solver logic
        def solve_shopping_combos(categories, colors, max_budget):
            if not categories:
                return []
            
            # Group products that match the requested category
            grouped_candidates = []
            for cat in categories:
                candidates = [
                    item for item in st.session_state.db 
                    if item['sub_category'].lower() == cat.lower()
                ]
                
                # Apply color filter if colors are selected
                if colors:
                    color_candidates = [c for c in candidates if c['color'] in colors]
                    # Fallback: if color has zero matches, keep all colors but warn
                    if color_candidates:
                        candidates = color_candidates
                
                if not candidates:
                    return []  # No possible products match
                grouped_candidates.append(candidates)
                
            # Cartesian product across the lists to construct all combinations
            combinations = list(product(*grouped_candidates))
            
            valid_packages = []
            for combo in combinations:
                total_cost = sum(item['price'] for item in combo)
                if total_cost <= max_budget:
                    valid_packages.append({
                        "items": combo,
                        "total_cost": total_cost,
                        "savings": max_budget - total_cost
                    })
                    
            # Sort packages by savings (cheapest options first)
            return sorted(valid_packages, key=lambda x: x['total_cost'])

        st.markdown("### 🗺️ Your Personalized Packages & Map Routing")
        
        # Track search for management metrics
        if selected_cats:
            for cat in selected_cats:
                st.session_state.search_logs.append({
                    "timestamp": datetime.datetime.now(),
                    "category": cat,
                    "query": f"Planner with budget ₹{budget_slider}"
                })

        packages = solve_shopping_combos(selected_cats, selected_colors, budget_slider)

        if not packages:
            st.error("❌ No matching packages found within this budget. Try relaxing color filters, increasing the budget limit, or removing some categories.")
        else:
            st.success(f"🎉 We generated {len(packages)} optimal purchase routes matching your criteria!")
            
            # Display best matches
            for idx, pkg in enumerate(packages[:2]): # Show top 2 packages
                st.markdown(f"#### Option {idx+1}: Optimized Path • Cost ₹{pkg['total_cost']:,} (You Save ₹{pkg['savings']:,})")
                
                # Route visual pathway generator
                # Group and sort by Floor (Ground Floor -> First Floor -> Second Floor) to minimize backtracking
                floor_mapping = {"Ground Floor": 0, "First Floor": 1, "Second Floor": 2}
                sorted_items_for_route = sorted(pkg['items'], key=lambda x: floor_mapping.get(x['floor'], 99))
                
                # Display Route Flow Line
                route_str = "🚶 Start Entrance ➡️ "
                for r_item in sorted_items_for_route:
                    route_str += f"📍 **{r_item['store']}** ({r_item['floor']}) ➡️ "
                route_str += "🏁 Exit/Parking"
                
                st.info(route_str)
                
                # Render item columns in options
                cols = st.columns(len(pkg['items']))
                for col_idx, item in enumerate(pkg['items']):
                    with cols[col_idx]:
                        # Product UI Container Card
                        st.markdown(f"""
                        <div class='product-card'>
                            <img src="{item['image_url']}" style="width:100%; border-radius:8px; height:140px; object-fit:cover;">
                            <div style="padding-top:8px;">
                                <span class="badge-floor">📍 {item['floor']}</span>
                                <span class="badge-stock">Stock: {item['stock']}</span>
                                <h5 style="margin:5px 0 0 0; color:#1e1b4b;">{item['brand']}</h5>
                                <p style="margin:0; color:#475569; font-size:0.8rem; height:40px; overflow:hidden;">{item['name']}</p>
                                <hr style="margin:8px 0;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <span style="font-weight:700; color:#4f46e5;">₹{item['price']:,}</span>
                                    <span style="font-size:0.8rem; color:#f59e0b;">★ {item['rating']}</span>
                                </div>
                                <div style="margin-top:5px; font-size:0.75rem; color:#dc2626; font-weight:600;">🎒 Sizes: {", ".join(item['sizes'])}</div>
                                <span class="badge-promo">🏷️ {item['offer']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.divider()

    # TAB 2: LIVE DIRECTORY & FLOOR MAP
    with tab_dir:
        st.subheader("🏙️ Interactive Mall Navigation Directory")
        st.write("Browse mall occupancy floor by floor. Tap a shop to view current catalog stock status live.")
        
        # 2D Layout Map representation
        st.markdown("""
        <div style="background-color: #0f172a; color: white; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <h4 style="margin-top: 0; color: #38bdf8;">🗺️ Live Interactive Store Location Blueprint</h4>
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div style="background-color: #1e293b; padding: 10px; border-radius: 8px; border-left: 5px solid #ec4899;">
                    <strong style="color: #ec4899;">🏢 SECOND FLOOR</strong> (Entertainment, Watches & Toys)<br/>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block; margin-top: 5px;">🧸 Hamleys Toys</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">⌚ Casio Watches</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">⌚ Fossil Watches</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px; border-radius: 8px; border-left: 5px solid #06b6d4;">
                    <strong style="color: #06b6d4;">🏢 FIRST FLOOR</strong> (Casual Clothes, Denim & Chinos)<br/>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block; margin-top: 5px;">👕 H&M Casuals</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👖 Levi's Denims</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👔 Marks & Spencer</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👚 Tommy Hilfiger</span>
                </div>
                <div style="background-color: #1e293b; padding: 10px; border-radius: 8px; border-left: 5px solid #10b981;">
                    <strong style="color: #10b981;">🏢 GROUND FLOOR</strong> (Premium Retailers & Footwear)<br/>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block; margin-top: 5px;">👟 Nike Shoes</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👟 Puma Sportswear</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👟 Adidas Athletics</span>
                    <span style="font-size: 0.8rem; background-color: #334155; padding: 4px 8px; border-radius: 4px; margin-right: 5px; display: inline-block;">👔 Zara Premium Fashion</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Search and filters
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        with col_s1:
            search_query = st.text_input("🔍 Search products, categories, or brands:", "", key="cat_search")
        with col_s2:
            store_filter = st.selectbox("Filter Store Location:", ["All Stores"] + sorted(list(set(item['store'] for item in st.session_state.db))))
        with col_s3:
            floor_filter = st.selectbox("Filter Floor Level:", ["All Floors", "Ground Floor", "First Floor", "Second Floor"])

        # Log query to analytics
        if search_query:
            st.session_state.search_logs.append({
                "timestamp": datetime.datetime.now(),
                "category": "Generic Search",
                "query": search_query
            })

        # Filter database query
        filtered_items = st.session_state.db
        if search_query:
            filtered_items = [
                i for i in filtered_items 
                if search_query.lower() in i['name'].lower() 
                or search_query.lower() in i['brand'].lower() 
                or search_query.lower() in i['category'].lower()
            ]
        if store_filter != "All Stores":
            filtered_items = [i for i in filtered_items if i['store'] == store_filter]
        if floor_filter != "All Floors":
            filtered_items = [i for i in filtered_items if i['floor'] == floor_filter]

        # Display filtered grid results
        if not filtered_items:
            st.info("No items match your search criteria. Try removing filters.")
        else:
            # Multi-column grid
            grid_cols = st.columns(4)
            for item_idx, item in enumerate(filtered_items):
                with grid_cols[item_idx % 4]:
                    stock_badge = f"<span class='badge-stock'>Qty In Stock: {item['stock']}</span>" if item['stock'] > 5 else f"<span class='badge-low-stock'>Only {item['stock']} Left</span>"
                    st.markdown(f"""
                    <div class='product-card'>
                        <img src="{item['image_url']}" style="width:100%; border-radius:8px; height:180px; object-fit:cover;">
                        <div style="padding-top:10px; position:relative;">
                            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                                <span class="badge-floor">{item['floor']}</span>
                                {stock_badge}
                            </div>
                            <h4 style="margin:5px 0 0 0; color:#1e1b4b;">{item['brand']}</h4>
                            <p style="margin:0; color:#475569; font-size:0.9rem; height:45px; overflow:hidden;">{item['name']}</p>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                                <span style="font-weight:700; color:#4f46e5; font-size:1.15rem;">₹{item['price']:,}</span>
                                <span style="font-size:0.85rem; color:#f59e0b;">★ {item['rating']}</span>
                            </div>
                            <div style="margin-top:5px; font-size:0.8rem; color:#475569;">
                                📦 Available Sizes: <b>{", ".join(item['sizes'])}</b>
                            </div>
                            <span class="badge-promo">{item['offer']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.write("") # Margin spacing

    # TAB 3: LIVE DEALS & COMPARE ENGINE
    with tab_deals:
        st.subheader("📊 Direct Price Comparison Engine")
        st.write("Cross-shop and compare identical or closely-matched product types side-by-side to ensure you secure the best local deal.")
        
        compare_category = st.selectbox("Select product type to compare across mall stores:", sorted(list(set(item['category'] for item in st.session_state.db))))
        
        compare_items = [i for i in st.session_state.db if i['category'] == compare_category]
        
        if len(compare_items) < 2:
            st.info("Not enough different brands available in this category to show side-by-side comparison.")
        else:
            # Build interactive comparison table
            compare_df = pd.DataFrame(compare_items)
            # Pick display fields
            display_df = compare_df[['brand', 'name', 'price', 'floor', 'store', 'offer', 'rating', 'stock']].copy()
            display_df.columns = ['Brand', 'Model/Name', 'Price (INR)', 'Floor', 'Store Name', 'Active Promotion', 'Rating', 'Current Qty']
            
            st.dataframe(display_df, use_container_width=True)
            
            # Interactive Chart comparison
            fig = px.bar(
                compare_df, 
                x='brand', 
                y='price', 
                color='store',
                text='price',
                title=f"Price comparison of {compare_category} across physical stores",
                labels={'brand': 'Retail Brand', 'price': 'Price (INR)', 'store': 'Store'},
                template='plotly_white'
            )
            fig.update_traces(texttemplate='₹%{text:,}', textposition='outside')
            fig.update_layout(yaxis_prefix="₹")
            st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# ROLE 2: STORE MERCHANT INTERFACE
# ----------------------------------------------------------------------------------------------------------------------
elif user_role == "Store Merchant Dashboard":
    st.subheader("🏪 Merchant Management Interface")
    st.write("Allows in-store representatives to broadcast localized deals and manage stock. Updates reflect instantly to nearby foot-shoppers on the map!")
    
    selected_store = st.selectbox("Log in to store terminal:", sorted(list(set(item['store'] for item in st.session_state.db))))
    
    # Store-specific items
    store_items = [i for i in st.session_state.db if i['store'] == selected_store]
    
    # Quick metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Assigned Location</div>
            <div class="metric-value">{store_items[0]['floor']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Managed Catalog SKUs</div>
            <div class="metric-value">{len(store_items)} Items</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MallQ! Integrations</div>
            <div class="metric-value" style="color:#10b981;">Online & Synced</div>
        </div>
        """, unsafe_allow_html=True)

    # Edit Items Form
    st.markdown("### 📝 Live Inventory Adjuster")
    selected_item_name = st.selectbox("Select item to modify live details:", [item['name'] for item in store_items])
    
    # Fetch index of item
    item_index = next((idx for (idx, d) in enumerate(st.session_state.db) if d["name"] == selected_item_name and d["store"] == selected_store), None)
    
    if item_index is not None:
        target_item = st.session_state.db[item_index]
        
        # Form fields to adjust
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            new_price = st.number_input("Adjust Price (₹)", min_value=100, max_value=50000, value=int(target_item['price']), step=50)
            new_stock = st.number_input("Update Stock Count", min_value=0, max_value=200, value=int(target_item['stock']))
        with col_form2:
            new_promo = st.text_input("Active Flash Offer", value=target_item['offer'])
            supported_sizes = st.multiselect("Update Sizes in Stock", ["S", "M", "L", "XL", "XXL", "UK 6", "UK 7", "UK 8", "UK 9", "UK 10", "Free Size"], default=target_item['sizes'])
            
        if st.button("💾 Apply Inventory & Promo Update"):
            # Update stateful DB
            st.session_state.db[item_index]['price'] = new_price
            st.session_state.db[item_index]['stock'] = new_stock
            st.session_state.db[item_index]['offer'] = new_promo
            st.session_state.db[item_index]['sizes'] = supported_sizes
            st.success(f"Successfully broadcasted updates for '{target_item['name']}'! Shoppers' route packages will now adapt.")
            
    # Simulated search queries for this store's category
    st.markdown("### 📈 Live Customer Intent Indicators")
    st.write("These represent anonymized real-time searches made by customers inside the mall. Use this to anticipate stock demands and launch tailored discount codes.")
    
    related_searches = [log for log in st.session_state.search_logs if log['category'].lower() in [item['category'].lower() for item in store_items] or log['category'] == "Generic Search"]
    
    if not related_searches:
        st.info("No query logs compiled yet today.")
    else:
        st.dataframe(pd.DataFrame(related_searches), use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# ROLE 3: MALL MANAGEMENT PORTAL
# ----------------------------------------------------------------------------------------------------------------------
elif user_role == "Mall Management Portal":
    st.subheader("📊 Central Management Command Center")
    st.write("Understand mall footprint metrics, visitor density, tenant performance indices, and lost revenue prevented.")
    
    # Management level KPIs
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Est. Mall Footfall (Today)</div>
            <div class="metric-value">12,482</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">MallQ! App Engagements</div>
            <div class="metric-value">4,129 (33%)</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col3:
        st.markdown("""
        <div class="metric-card" style="border-left: 5px solid #10b981;">
            <div class="metric-label">Est. Bounce Rate Prevented</div>
            <div class="metric-value" style="color:#10b981;">18.4%</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi_col4:
        st.markdown("""
        <div class="metric-card" style="border-left: 5px solid #10b981;">
            <div class="metric-label">Prevented Retail Leakage</div>
            <div class="metric-value" style="color:#10b981;">₹2.4 Lakhs</div>
        </div>
        """, unsafe_allow_html=True)

    # Simulated Live Analytics Graphs
    st.markdown("### 📈 Real-time Analytics Dashboard")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        # 1. Category search intent pie chart
        search_df = pd.DataFrame(st.session_state.search_logs)
        fig_pie = px.pie(
            search_df, 
            names='category', 
            title="Aggregated Shopper Category Search Share (Last 24 Hours)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_g2:
        # 2. Hourly Mall Footfall curve
        hours = [f"{h}:00" for h in range(10, 22)]
        footfall_values = [420, 580, 850, 1100, 950, 1200, 1500, 2200, 2100, 1300, 800, 350]
        
        fig_line = px.line(
            x=hours, 
            y=footfall_values, 
            title="Simulated Hourly Footfall Distribution Pattern",
            labels={'x': 'Business Hours', 'y': 'Active Visitors'},
            markers=True
        )
        fig_line.update_traces(line_color='#6366f1', line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)

    # Floor wise customer congestion levels
    st.markdown("### 🔥 Live Floor Crowding / Congestion Indexes")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.metric(label="Ground Floor Density (Premium Clothes & Shoes)", value="High (81%)", delta="Refuge Escalator: Normal")
    with col_f2:
        st.metric(label="First Floor Density (Casual Clothes & Jeans)", value="Moderate (52%)", delta="Refuge Escalator: Clear")
    with col_f3:
        st.metric(label="Second Floor Density (Watches, Toys & Food Court)", value="Critical (94%)", delta="Refuge Escalator: Congested", delta_color="inverse")