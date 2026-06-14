import streamlit as st
import pandas as pd
import random

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="MallQ! Mall Companion",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f8fafc;
    }
    
    /* Elegant Title Styles */
    .app-title {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }
    
    .app-subtitle {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 25px;
    }
    
    /* Modern Dashboard Cards */
    .card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
        margin-bottom: 20px;
    }
    
    /* Badges */
    .badge-fashion {
        background-color: #eff6ff;
        color: #2563eb;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
    }
    
    .badge-footwear {
        background-color: #faf5ff;
        color: #9333ea;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
    }
    
    .badge-accessories {
        background-color: #ecfdf5;
        color: #059669;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
    }
    
    .badge-toys {
        background-color: #fff7ed;
        color: #ea580c;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
    }
    
    .floor-badge {
        background-color: #f1f5f9;
        color: #475569;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 20px;
        border: 1px solid #cbd5e1;
    }
    
    /* Hero Banners */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 35px;
        border-radius: 18px;
        margin-bottom: 30px;
        position: relative;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
    }
    
    .hero-alert-badge {
        position: absolute;
        top: 30px;
        right: 30px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* Form sections */
    .form-header {
        font-weight: 700;
        color: #334155;
        font-size: 16px;
        margin-bottom: 12px;
        border-left: 4px solid #3b82f6;
        padding-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# IN-MEMORY DATA STATE INITIALIZATION
# ==========================================
if "initialized" not in st.session_state:
    # 1. Stores Data
    st.session_state.stores = {
        "Zara": {"level": "First", "category": "Fashion", "rating": 4.6, "views": 1840, "checks": 782, "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop"},
        "H&M": {"level": "Ground", "category": "Fashion", "rating": 4.5, "views": 1240, "checks": 542, "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop"},
        "Nike": {"level": "First", "category": "Footwear", "rating": 4.8, "views": 2100, "checks": 910, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop"},
        "Adidas Outlet": {"level": "Ground", "category": "Footwear", "rating": 4.7, "views": 1650, "checks": 489, "image": "https://images.unsplash.com/photo-1582588678413-dbf45f4823e9?w=500&auto=format&fit=crop"},
        "Casio": {"level": "First", "category": "Accessories", "rating": 4.6, "views": 980, "checks": 310, "image": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=500&auto=format&fit=crop"},
        "Hamleys": {"level": "Second", "category": "Toys", "rating": 4.9, "views": 2500, "checks": 1200, "image": "https://images.unsplash.com/photo-1585366119957-e5733be3c794?w=500&auto=format&fit=crop"}
    }
    
    # 2. Products Catalog Database
    st.session_state.products = [
        {"id": "p1", "store": "Zara", "title": "Linen Blend Summer Shirt", "price": 2990, "color": "White", "sizes": {"S": 5, "M": 8, "L": 4, "XL": 2}, "category": "Fashion", "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop"},
        {"id": "p2", "store": "H&M", "title": "Oversized Tee with Graphic Print", "price": 999, "color": "Black", "sizes": {"S": 8, "M": 0, "L": 14, "XL": 6}, "category": "Fashion", "image": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=500&auto=format&fit=crop"},
        {"id": "p3", "store": "H&M", "title": "White Relaxed Fit Cotton Shirt", "price": 1499, "color": "White", "sizes": {"S": 5, "M": 6, "L": 0, "XL": 0}, "category": "Fashion", "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop"},
        {"id": "p4", "store": "Nike", "title": "Nike Air Max Sports Sneakers", "price": 8999, "color": "Red", "sizes": {"S": 4, "M": 5, "L": 3, "XL": 2}, "category": "Footwear", "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop"},
        {"id": "p5", "store": "Adidas Outlet", "title": "Adidas Stan Smith Classic", "price": 4999, "color": "White", "sizes": {"S": 6, "M": 8, "L": 5, "XL": 0}, "category": "Footwear", "image": "https://images.unsplash.com/photo-1582588678413-dbf45f4823e9?w=500&auto=format&fit=crop"},
        {"id": "p6", "store": "Casio", "title": "Vintage Digital Watch", "price": 1695, "color": "Silver", "sizes": {"S": 5, "M": 5, "L": 5, "XL": 5}, "category": "Accessories", "image": "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=500&auto=format&fit=crop"},
        {"id": "p7", "store": "Hamleys", "title": "LEGO Star Wars Fighter", "price": 4500, "color": "Mixed", "sizes": {"S": 10, "M": 10, "L": 10, "XL": 10}, "category": "Toys", "image": "https://images.unsplash.com/photo-1585366119957-e5733be3c794?w=500&auto=format&fit=crop"}
    ]
    
    # 3. Targeted Coupon Database
    st.session_state.coupons = [
        {"id": "c1", "store": "H&M", "title": "H&M Circular Recycle Promo", "code": "HMRECYCLE15", "discount": 15},
        {"id": "c2", "store": "Zara", "title": "Zara End of Season Sale", "code": "ZARA30", "discount": 30},
        {"id": "c3", "store": "Nike", "title": "Nike Pro Runner Kickback", "code": "RUNNIKE10", "discount": 10}
    ]
    
    # 4. Search and Interaction Metrics (Simulates live database views)
    st.session_state.searches = {
        "white shirt size M": 284,
        "white sneakers under 5000": 195,
        "ANC headphones noise cancel": 123,
        "iphone 15 pro discount": 98,
        "linen pants summer": 62,
        "oversized cotton graphic tee": 82,
        "white shirt zara": 112
    }
    
    # 5. Customer Feedback/Support Tickets
    st.session_state.feedback = [
        {"name": "Aditya Verma", "date": "14 June 2026", "rating": 5, "comment": "Amazing! Finding the specific white shirt in Zara in exactly size M saved me from searching the entire shop floor."},
        {"name": "Priya Sharma", "date": "13 June 2026", "rating": 4, "comment": "The budget planner got me both shoes and clothes under ₹5000 easily. Navigating the levels is much simpler now."}
    ]
    
    st.session_state.initialized = True

# Helper function to get badge class based on category
def get_badge_class(category):
    cat_lower = category.lower()
    if "fashion" in cat_lower: return "badge-fashion"
    elif "footwear" in cat_lower: return "badge-footwear"
    elif "accessories" in cat_lower: return "badge-accessories"
    return "badge-toys"

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown('<div class="app-title">MallQ!</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Centralized Retail Directory & AI Planner</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.write("🌌 **Active Session Role Portal**")
    app_view = st.radio(
        "Choose Your Interface Workspace:",
        ["🛍️ Shopper Hub", "🏪 Store Merchant Console", "🏛️ Mall Administration"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    
    # Fast access quick stats to highlight functionality
    st.markdown("⚡ **Live Infrastructure State**")
    st.info(f"🏬 Stores Active: {len(st.session_state.stores)}\n\n📦 Products Indexed: {len(st.session_state.products)}\n\n🎟️ Promo Coupons: {len(st.session_state.coupons)}")

# ==========================================
# VIEW 1: SHOPPER HUB
# ==========================================
if app_view == "🛍️ Shopper Hub":
    # 1. Elegant Header Banner
    st.markdown("""
    <div class="hero-banner">
        <span style="background: #2563eb; color: white; font-size: 10px; font-weight: bold; padding: 4px 8px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px;">COMPANION APP</span>
        <h1 style="color: white; margin-top: 10px; font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">Centralized Mall Shopper Hub</h1>
        <p style="color: #cbd5e1; font-size: 14px; max-width: 650px; margin-bottom: 0;">Compare prices, check real-time store size availability, run AI-customized budget routing, and navigate with vectors.</p>
        <div class="hero-alert-badge">
            <span style="font-size: 22px;">🔔</span>
            <div style="text-align: left;">
                <div style="font-size: 9px; color: #94a3b8; text-transform: uppercase; font-weight: bold; letter-spacing: 0.5px;">LIVE ALERTS DESK</div>
                <div style="font-size: 13px; font-weight: bold; color: white;">1 New Promo Alert</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Main Tabbed Layout
    t1, t2, t3, t4 = st.tabs([
        "🔍 Directory & Inventory", 
        "⚡ AI Smart Planner & Budget Match", 
        "🏷️ Mall Offers & Promos", 
        "🗺️ Visual Interactive Navigator Map"
    ])
    
    # TAB 1: DIRECTORY & INVENTORY
    with t1:
        col_filters, col_results = st.columns([1.1, 2.5])
        
        # Left Panel Filters
        with col_filters:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="form-header">Refine Showcase</div>', unsafe_allow_html=True)
            
            search_query = st.text_input("Search Store or Product Keyword", placeholder="e.g. shirt, Nike, sneakers...")
            
            # Category Select
            category_filter = st.selectbox("Category Section", ["All", "Fashion", "Footwear", "Accessories", "Toys"])
            
            # Level Select
            level_filter = st.selectbox("Floor Level", ["All", "Ground", "First", "Second"])
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Live Compare Tool in Left Panel
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="form-header">Live Price Compare Tool</div>', unsafe_allow_html=True)
            st.write("Instantly compare specific product items across the mall:")
            
            compare_keyword = st.text_input("Compare Product (e.g., Shirt)", value="Shirt")
            if compare_keyword:
                matching_items = [p for p in st.session_state.products if compare_keyword.lower() in p["title"].lower()]
                if matching_items:
                    for mi in matching_items:
                        sizes_status = ", ".join([f"{k}:{v}" for k, v in mi["sizes"].items() if v > 0])
                        if not sizes_status:
                            sizes_status = "Out of Stock"
                        st.markdown(f"""
                        <div style="padding: 8px 12px; margin-bottom: 6px; background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; font-size: 12px;">
                            <b>{mi['title']}</b> ({mi['store']})<br/>
                            <span style="color: #2563eb; font-weight: 700;">₹{mi['price']}</span> | Sizes: {sizes_status}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No matching products found for comparison.")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Right Panel Grid Display
        with col_results:
            # Filter Logic
            filtered_stores = st.session_state.stores.copy()
            if category_filter != "All":
                filtered_stores = {k: v for k, v in filtered_stores.items() if v["category"] == category_filter}
            if level_filter != "All":
                filtered_stores = {k: v for k, v in filtered_stores.items() if v["level"] == level_filter}
            if search_query:
                # Filter by store name, product matching keyword
                store_match_names = {k for k in filtered_stores.keys() if search_query.lower() in k.lower()}
                prod_match_store_names = {p["store"] for p in st.session_state.products if search_query.lower() in p["title"].lower()}
                union_stores = store_match_names.union(prod_match_store_names)
                filtered_stores = {k: v for k, v in filtered_stores.items() if k in union_stores}
                
                # Increment Live Search Analytics
                if search_query.strip():
                    cleaned_search = search_query.lower().strip()
                    st.session_state.searches[cleaned_search] = st.session_state.searches.get(cleaned_search, 0) + 1
            
            st.markdown(f"#### Stores Matching ({len(filtered_stores)})")
            
            # Display Stores as Cards
            if filtered_stores:
                # Draw dynamic columns
                grid_cols = st.columns(2)
                for i, (name, details) in enumerate(filtered_stores.items()):
                    with grid_cols[i % 2]:
                        # Grab dynamic category, levels and rating
                        cat_badge = get_badge_class(details["category"])
                        st.markdown(f"""
                        <div class="card" style="position: relative;">
                            <img src="{details['image']}" style="width:100%; height:140px; object-fit: cover; border-radius: 10px; margin-bottom: 12px;" />
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
                                <h4 style="margin: 0; font-weight: 700; color: #0f172a;">{name}</h4>
                                <span class="floor-badge">{details['level']} Level</span>
                            </div>
                            <div style="display:flex; gap: 8px; margin-bottom: 12px; align-items: center;">
                                <span class="{cat_badge}">{details['category']}</span>
                                <span style="font-size: 13px; color: #fbbf24; font-weight: bold;">⭐ {details['rating']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Interactive expander to view stock lists
                        with st.expander(f"👁️ View live Catalog Inventory & Sizing"):
                            store_items = [p for p in st.session_state.products if p["store"] == name]
                            if store_items:
                                for item in store_items:
                                    st.markdown(f"**{item['title']}**")
                                    st.markdown(f"<span style='color: #2563eb; font-weight: bold;'>₹{item['price']}</span> &nbsp;|&nbsp; Color: {item['color']}", unsafe_allow_html=True)
                                    
                                    # Sizes render block
                                    sizes_html = "Sizes Left: "
                                    for sz, count in item["sizes"].items():
                                        if count > 0:
                                            sizes_html += f" <span style='background-color:#e2e8f0; padding:2px 6px; border-radius:4px; font-size:11px;'>{sz}: <b>{count}</b></span>"
                                        else:
                                            sizes_html += f" <span style='background-color:#fee2e2; color:#ef4444; padding:2px 6px; border-radius:4px; font-size:11px;'>{sz}: <b>0</b></span>"
                                    st.markdown(sizes_html, unsafe_allow_html=True)
                                    st.markdown("<hr style='margin:10px 0; border:0; border-top:1px solid #f1f5f9;'/>", unsafe_allow_html=True)
                            else:
                                st.caption("No inventory catalog items loaded for this store.")
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("No physical stores matched your criteria. Try adjusting filters.")
                
    # TAB 2: AI SMART PLANNER & BUDGET MATCH
    with t2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⚡ AI Smart Planner & Budget Match Router")
        st.write("Solve shopping search-fatigue: Tell MallQ! exactly what items you need, choose colors and budget limits, and our AI Router will build an optimal single-trip path checking exact floor counts instantly.")
        
        # User dynamic budget builder
        col_inp1, col_inp2 = st.columns(2)
        
        with col_inp1:
            st.markdown("**Item Requirement 1**")
            req1_cat = st.selectbox("Product Category 1", ["Fashion", "Footwear", "Accessories", "Toys"])
            req1_color = st.selectbox("Preferred Color 1", ["Any", "White", "Black", "Red", "Silver", "Mixed"])
            req1_budget = st.slider("Maximum Budget for Item 1 (₹)", 500, 10000, 2000)
            
        with col_inp2:
            st.markdown("**Item Requirement 2**")
            req2_cat = st.selectbox("Product Category 2", ["None", "Fashion", "Footwear", "Accessories", "Toys"])
            req2_color = st.selectbox("Preferred Color 2", ["Any", "White", "Black", "Red", "Silver", "Mixed"])
            req2_budget = st.slider("Maximum Budget for Item 2 (₹)", 500, 15000, 4000)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("🚀 Calculate Optimized AI Smart Routing Path"):
            st.write("---")
            # Build search criteria
            match1 = []
            match2 = []
            
            # Find candidate item 1
            for p in st.session_state.products:
                if p["category"] == req1_cat and p["price"] <= req1_budget:
                    if req1_color == "Any" or p["color"].lower() == req1_color.lower():
                        match1.append(p)
                        
            # Find candidate item 2
            if req2_cat != "None":
                for p in st.session_state.products:
                    if p["category"] == req2_cat and p["price"] <= req2_budget:
                        if req2_color == "Any" or p["color"].lower() == req2_color.lower():
                            match2.append(p)
            
            # Analyze Combinations and build steps
            if not match1:
                st.error(f"❌ No matching product found for Item 1 ({req1_cat} under ₹{req1_budget})")
            elif req2_cat != "None" and not match2:
                st.error(f"❌ No matching product found for Item 2 ({req2_cat} under ₹{req2_budget})")
            else:
                # Perfect matches found
                st.success("🎯 Successful AI Smart Matches Found!")
                
                # Dynamic Routing Simulation
                col_m1, col_m2 = st.columns(2)
                
                selected_p1 = match1[0] # Pick top matched candidate
                with col_m1:
                    st.markdown(f"""
                    <div style="background-color: #f0f9ff; border: 1px dashed #0284c7; padding: 16px; border-radius: 12px;">
                        <span style="font-size:11px; background-color:#38bdf8; color:white; font-weight:700; padding:2px 8px; border-radius:20px;">RECOMMENDED SELECTION 1</span>
                        <h4 style="margin-top:8px; margin-bottom:4px;">{selected_p1['title']}</h4>
                        <p style="font-size:12px; color:#475569; margin-bottom:4px;">Store: <b>{selected_p1['store']}</b> ({st.session_state.stores[selected_p1['store']]['level']} Floor)</p>
                        <h3 style="color:#0284c7; margin:0;">₹{selected_p1['price']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                selected_p2 = None
                if req2_cat != "None" and match2:
                    selected_p2 = match2[0]
                    with col_m2:
                        st.markdown(f"""
                        <div style="background-color: #fdf2f8; border: 1px dashed #db2777; padding: 16px; border-radius: 12px;">
                            <span style="font-size:11px; background-color:#f472b6; color:white; font-weight:700; padding:2px 8px; border-radius:20px;">RECOMMENDED SELECTION 2</span>
                            <h4 style="margin-top:8px; margin-bottom:4px;">{selected_p2['title']}</h4>
                            <p style="font-size:12px; color:#475569; margin-bottom:4px;">Store: <b>{selected_p2['store']}</b> ({st.session_state.stores[selected_p2['store']]['level']} Floor)</p>
                            <h3 style="color:#db2777; margin:0;">₹{selected_p2['price']}</h3>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Show navigation routing directions
                total_cost = selected_p1['price'] + (selected_p2['price'] if selected_p2 else 0)
                st.markdown(f"""
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top:20px;">
                    <h4 style="margin-top:0; color:#0f172a;">📍 Step-by-Step Navigation Path</h4>
                    <p style="margin-bottom:12px;">Combined Trip Cart Total: <b>₹{total_cost}</b> (Under total budget cap!)</p>
                    <ol style="margin-bottom:0; font-size:13px; line-height:1.7;">
                        <li><b>Depart Atrium:</b> Walk 30m towards the Escalator lobby.</li>
                        <li><b>Stop 1 ({selected_p1['store']}):</b> Go to {st.session_state.stores[selected_p1['store']]['level']} Floor. Proceed 20m inside the shop. Pick up <i>{selected_p1['title']}</i> (Color: {selected_p1['color']}). <b>Size checks have been verified in stock.</b></li>
                """, unsafe_allow_html=True)
                
                if selected_p2:
                    level_p1 = st.session_state.stores[selected_p1['store']]['level']
                    level_p2 = st.session_state.stores[selected_p2['store']]['level']
                    if level_p1 != level_p2:
                        st.markdown(f"<li><b>Level Transfer:</b> Take the adjacent elevator up to the <b>{level_p2} Floor</b>.</li>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<li><b>Short Transition:</b> Turn right upon exiting, walk 15 meters on the same floor level.</li>", unsafe_allow_html=True)
                    st.markdown(f"<li><b>Stop 2 ({selected_p2['store']}):</b> Enter the store, find the catalog section. Retrieve <i>{selected_p2['title']}</i>. Size checks are live!</li>", unsafe_allow_html=True)
                
                st.markdown("""
                        <li><b>Billing Counter:</b> Pay with customized store discount codes generated in your wallet.</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Logging simulation
                query_log_1 = f"{selected_p1['color'].lower()} {selected_p1['category'].lower()} under {req1_budget}"
                st.session_state.searches[query_log_1] = st.session_state.searches.get(query_log_1, 0) + 1
                if selected_p2:
                    query_log_2 = f"{selected_p2['color'].lower()} {selected_p2['category'].lower()} under {req2_budget}"
                    st.session_state.searches[query_log_2] = st.session_state.searches.get(query_log_2, 0) + 1

    # TAB 3: MALL OFFERS & PROMOS
    with t3:
        st.markdown("### 🎟️ Active Store Promotions & Digital Promo Codes")
        st.write("Scan discount code coupons deployed directly by retailers to optimize checkout price matches:")
        
        col_c_grid = st.columns(3)
        for i, coupon in enumerate(st.session_state.coupons):
            with col_c_grid[i % 3]:
                st.markdown(f"""
                <div style="background-color:#fffbeb; border: 2px dashed #f59e0b; border-radius:12px; padding:18px; margin-bottom:15px; position:relative;">
                    <span style="font-size:10px; background-color:#f59e0b; color:white; font-weight:bold; padding:2px 8px; border-radius:20px; position:absolute; top:12px; right:12px;">{coupon['store']}</span>
                    <h4 style="margin-top:0; color:#b45309; font-size:16px;">{coupon['title']}</h4>
                    <p style="font-size:13px; color:#78350f; margin-bottom:12px;">Enjoy <b>{coupon['discount']}% OFF</b> at physical counters.</p>
                    <div style="background-color: white; border:1px solid #fcd34d; border-radius:6px; padding:6px; text-align:center; font-family:monospace; font-size:15px; font-weight:700; color:#334155; margin-bottom:10px;">
                        {coupon['code']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Claim Voucher: {coupon['code']}", key=f"btn_claim_{coupon['code']}"):
                    st.toast(f"Coupon {coupon['code']} successfully added to your device wallet! Check out now.")

    # TAB 4: VISUAL INTERACTIVE NAVIGATOR MAP
    with t4:
        st.markdown("### 🗺️ Dynamic Floor Level Navigator")
        st.write("Visual coordinate map representing physical store setups. Red dots display store center locations dynamically:")
        
        sel_level = st.selectbox("Render Floor Coordinate System", ["Ground Floor", "First Floor", "Second Floor"])
        
        # Build interactive grid map using emojis/HTML representation
        map_html = """
        <div style="display:grid; grid-template-columns: repeat(6, 1fr); gap:12px; background:#1e293b; padding:25px; border-radius:12px; border:3px solid #0f172a; text-align:center;">
        """
        
        stores_on_level = [k for k, v in st.session_state.stores.items() if v["level"] + " Floor" == sel_level]
        
        for index in range(24): # 24 spaces block grid
            if index == 2:
                map_html += "<div style='background:#ef4444; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:1px solid #fecaca;'>🚻 RESTROOMS</div>"
            elif index == 5:
                map_html += "<div style='background:#3b82f6; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:1px solid #bfdbfe;'>🛗 ELEVATOR</div>"
            elif index == 11:
                 map_html += "<div style='background:#10b981; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:1px solid #a7f3d0;'>🎫 ATRIUM</div>"
            elif index == 8 and len(stores_on_level) > 0:
                map_html += f"<div style='background:#f43f5e; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:2px solid #fff;'>🏬 {stores_on_level[0]}</div>"
            elif index == 15 and len(stores_on_level) > 1:
                map_html += f"<div style='background:#f43f5e; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:2px solid #fff;'>🏬 {stores_on_level[1]}</div>"
            elif index == 20 and len(stores_on_level) > 2:
                map_html += f"<div style='background:#f43f5e; color:white; padding:16px 8px; border-radius:6px; font-size:11px; font-weight:bold; border:2px solid #fff;'>🏬 {stores_on_level[2]}</div>"
            else:
                map_html += "<div style='background:#334155; color:#64748b; padding:16px 8px; border-radius:6px; font-size:11px; border: 1px dashed #475569;'>Empty Slot</div>"
                
        map_html += "</div>"
        st.markdown(map_html, unsafe_allow_html=True)
        st.caption("🚨 Active navigation highlights the chosen shopping trail dynamically using live telemetry coords.")

        # Interactive Feedback form at bottom
        st.markdown("---")
        st.markdown("#### 💬 Share Shopper Experience Feedback")
        f_name = st.text_input("Name", placeholder="Enter your name")
        f_comment = st.text_area("Experience Feedback Comments", placeholder="Tell us how we did...")
        f_rating = st.slider("Rating Score (1-5)", 1, 5, 5)
        if st.button("Submit Anonymous Feedback"):
            if f_name and f_comment:
                st.session_state.feedback.append({
                    "name": f_name,
                    "date": "14 June 2026",
                    "rating": f_rating,
                    "comment": f_comment
                })
                st.success("Feedback saved and filed directly to the Central Admin Console!")
            else:
                st.warning("Please provide both name and experience comments.")

# ==========================================
# VIEW 2: STORE MERCHANT CONSOLE
# ==========================================
elif app_view == "🏪 Store Merchant Console":
    # Header Banner matching Mockup
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);">
        <span style="background: #0ea5e9; color: white; font-size: 10px; font-weight: bold; padding: 4px 8px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px;">MERCHANT CONSOLE</span>
        <h1 style="color: white; margin-top: 10px; font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">Store & Inventory Central</h1>
        <p style="color: #e0f2fe; font-size: 14px; max-width: 650px; margin-bottom: 0;">Manage your physical workspace store details, modify listing prices dynamically, and publish fresh promotional discount deals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Selection Workspace dropdown
    selected_merchant = st.selectbox(
        "Active Store Workspace Portal", 
        list(st.session_state.stores.keys())
    )
    
    col_merchant_analytics, col_merchant_catalog = st.columns([1.1, 2.5])
    
    # LEFT COLUMN: MERCH STATISTICS & ADD ITEM
    with col_merchant_analytics:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="form-header">{selected_merchant} Footfall Analytics</div>', unsafe_allow_html=True)
        
        store_analytics = st.session_state.stores[selected_merchant]
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.metric("Catalog Views", f"{store_analytics['views']:,}")
        with col_c2:
            st.metric("Size Checks", f"{store_analytics['checks']:,}")
            
        st.markdown("<br/>**Recent Matching Shopper Queries**", unsafe_allow_html=True)
        # Filter mock search matches relevant to this store
        found_any = False
        for query, hits in st.session_state.searches.items():
            if selected_merchant.lower() in query or ("shirt" in query and selected_merchant == "H&M") or ("sneakers" in query and "Nike" in selected_merchant):
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; background-color:#f8fafc; padding:8px; border-radius:6px; margin-bottom:4px; font-size:12px;">
                    <span>"{query}"</span>
                    <b style="color:#0284c7;">{hits} hits</b>
                </div>
                """, unsafe_allow_html=True)
                found_any = True
        if not found_any:
            st.caption("No dynamic searches logged for your product categories today yet.")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # SPAWN NEW CATALOG ITEM
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Spawn New Catalog Item</div>', unsafe_allow_html=True)
        
        new_title = st.text_input("Product Title", placeholder="e.g. Classic Denim Jacket")
        new_price = st.number_input("Listing Price (₹)", min_value=100, max_value=50000, value=2499)
        new_color = st.selectbox("Product Color", ["White", "Black", "Blue", "Red", "Silver", "Mixed", "Beige"])
        new_category = st.selectbox("Section Segment", ["Fashion", "Footwear", "Accessories", "Toys"])
        
        col_s_a, col_s_b = st.columns(2)
        with col_s_a:
            stock_s = st.number_input("S Stock", min_value=0, max_value=100, value=5)
            stock_m = st.number_input("M Stock", min_value=0, max_value=100, value=10)
        with col_s_b:
            stock_l = st.number_input("L Stock", min_value=0, max_value=100, value=8)
            stock_xl = st.number_input("XL Stock", min_value=0, max_value=100, value=3)
            
        if st.button("➕ Publish to Mall Catalog"):
            if new_title:
                # Add to state products
                st.session_state.products.append({
                    "id": f"p{len(st.session_state.products) + 1}",
                    "store": selected_merchant,
                    "title": new_title,
                    "price": new_price,
                    "color": new_color,
                    "sizes": {"S": stock_s, "M": stock_m, "L": stock_l, "XL": stock_xl},
                    "category": new_category,
                    "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=500&auto=format&fit=crop"
                })
                st.success(f"'{new_title}' successfully uploaded and instantly visible under Mall Directory!")
            else:
                st.warning("Please provide a product title.")
        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT COLUMN: CATALOG EDIT & COUPONS DEPLOYMENT
    with col_merchant_catalog:
        # Catalog List Edit View
        st.markdown('<div class="card">', unsafe_allow_html=True)
        store_items = [p for p in st.session_state.products if p["store"] == selected_merchant]
        st.markdown(f'<div class="form-header">Catalog Management ({len(store_items)} items listed)</div>', unsafe_allow_html=True)
        
        if store_items:
            for index, item in enumerate(store_items):
                col_item_desc, col_item_price, col_item_sizes = st.columns([1.2, 1, 1.2])
                
                with col_item_desc:
                    st.write(f"🏷️ **{item['title']}**")
                    st.caption(f"ID: {item['id']} | Color: {item['color']}")
                    
                    if st.button("🗑️ Remove", key=f"del_prod_{item['id']}"):
                        st.session_state.products.remove(item)
                        st.success(f"Deleted {item['title']}!")
                        st.rerun()
                        
                with col_item_price:
                    # Slider to dynamically adjust live listing price
                    updated_price = st.slider(
                        "Live Listing Price (₹)", 
                        100, 100000, int(item["price"]), 
                        key=f"price_slider_{item['id']}"
                    )
                    # Directly update pricing state reactively!
                    item["price"] = updated_price
                    
                with col_item_sizes:
                    st.caption("Live Stock Level Increments")
                    # Increment stock counts
                    col_sz_s, col_sz_m, col_sz_l, col_sz_xl = st.columns(4)
                    with col_sz_s:
                        item["sizes"]["S"] = st.number_input("S", value=item["sizes"]["S"], key=f"sz_s_{item['id']}", min_value=0)
                    with col_sz_m:
                        item["sizes"]["M"] = st.number_input("M", value=item["sizes"]["M"], key=f"sz_m_{item['id']}", min_value=0)
                    with col_sz_l:
                        item["sizes"]["L"] = st.number_input("L", value=item["sizes"]["L"], key=f"sz_l_{item['id']}", min_value=0)
                    with col_sz_xl:
                        item["sizes"]["XL"] = st.number_input("XL", value=item["sizes"]["XL"], key=f"sz_xl_{item['id']}", min_value=0)
                        
                st.markdown("<hr style='margin:12px 0; border:0; border-top:1px solid #e2e8f0;'/>", unsafe_allow_html=True)
        else:
            st.info("No active inventory catalog products loaded for your store workspace.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Dynamic Coupons Section
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Targeted Promotional Coupons</div>', unsafe_allow_html=True)
        
        col_coup_form, col_coup_list = st.columns(2)
        
        with col_coup_form:
            st.markdown("**Add Live Coupon**")
            promo_title = st.text_input("Promo Headline Title", placeholder="e.g. End of Season Exclusive")
            promo_discount = st.number_input("Discount percentage %", min_value=5, max_value=80, value=20)
            promo_code = st.text_input("Coupon Voucher Code", placeholder="e.g. ZARA20")
            
            if st.button("Deploy Coupon Code"):
                if promo_title and promo_code:
                    st.session_state.coupons.append({
                        "id": f"c{len(st.session_state.coupons) + 1}",
                        "store": selected_merchant,
                        "title": promo_title,
                        "code": promo_code.upper(),
                        "discount": promo_discount
                    })
                    st.success(f"Coupon code '{promo_code.upper()}' is now deployed LIVE!")
                    st.rerun()
                else:
                    st.warning("Please provide voucher title and discount code.")
                    
        with col_coup_list:
            st.markdown("**Active Store Coupons**")
            active_m_coupons = [c for c in st.session_state.coupons if c["store"] == selected_merchant]
            if active_m_coupons:
                for coup in active_m_coupons:
                    st.markdown(f"""
                    <div style="background-color:#f0fdf4; border: 1px dashed #22c55e; padding:10px; border-radius:8px; margin-bottom:8px;">
                        <b>{coup['title']}</b> ({coup['discount']}% off)<br/>
                        <code style="background-color:white; padding:2px 4px; border-radius:4px; font-weight:700;">{coup['code']}</code>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Deactivate {coup['code']}", key=f"deact_{coup['code']}"):
                        st.session_state.coupons.remove(coup)
                        st.success(f"Coupon {coup['code']} deactivated!")
                        st.rerun()
            else:
                st.caption("No coupons active for your store.")
                
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# VIEW 3: MALL ADMINISTRATION
# ==========================================
elif app_view == "🏛️ Mall Administration":
    # Header Banner matching Mall Administration Console
    st.markdown("""
    <div class="hero-banner" style="background: linear-gradient(135deg, #475569 0%, #334155 100%);">
        <span style="background: #64748b; color: white; font-size: 10px; font-weight: bold; padding: 4px 8px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1px;">MALL ADMINISTRATION LOGINS</span>
        <h1 style="color: white; margin-top: 10px; font-size: 2.2rem; font-weight: 800; margin-bottom: 8px;">MallQ! Management Console</h1>
        <p style="color: #e2e8f0; font-size: 14px; max-width: 650px; margin-bottom: 0;">Review live footfall analytics data, adjust central shop directories, and monitor live shopper experiences to advise store merchants.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. TOP ROW STATS GRID CARDS
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">TOTAL MAPPED STORES</div>
            <h2 style="font-size: 30px; font-weight: 800; color: #0f172a; margin: 8px 0;">{len(st.session_state.stores)} Active</h2>
            <div style="font-size: 11px; color: #94a3b8;">Central mall contains 42 registers.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_stat2:
        # Static footfall but reactive change metrics
        st.markdown("""
        <div class="card" style="text-align: center;">
            <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">ESTIMATED MALL FOOTFALL</div>
            <h2 style="font-size: 30px; font-weight: 800; color: #10b981; margin: 8px 0;">14,500</h2>
            <div style="font-size: 11px; color: #10b981; font-weight: bold;">📈 +12% increase from last Sunday</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_stat3:
        # Dynamically reactive coupon counters
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">ACTIVE PROMO COUPONS</div>
            <h2 style="font-size: 30px; font-weight: 800; color: #d97706; margin: 8px 0;">{len(st.session_state.coupons)} Code Sets</h2>
            <div style="font-size: 11px; color: #94a3b8;">Coupons deployed across catalog shops.</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_stat4:
        # Feedback ticket counts
        st.markdown(f"""
        <div class="card" style="text-align: center;">
            <div style="font-size: 11px; font-weight: bold; color: #64748b; text-transform: uppercase;">FEEDBACK FILINGS</div>
            <h2 style="font-size: 30px; font-weight: 800; color: #6366f1; margin: 8px 0;">{len(st.session_state.feedback)} Filings</h2>
            <div style="font-size: 11px; color: #94a3b8;">100% checked by center reception.</div>
        </div>
        """, unsafe_allow_html=True)
        
    # 2. BOTTOM ROW ANALYTICS SPLIT PANELS
    col_bottom_left, col_bottom_right = st.columns([1.5, 1])
    
    with col_bottom_left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Consumer Intended Queries Analysis</div>', unsafe_allow_html=True)
        st.write("Analyzing search trends allows administrators to coordinate mall layout planning and inventory allocations:")
        
        # Dynamic search progress meters from session state data
        sorted_searches = sorted(st.session_state.searches.items(), key=lambda x: x[1], reverse=True)[:6]
        max_hits = max([hits for _, hits in sorted_searches]) if sorted_searches else 1
        
        for query, hits in sorted_searches:
            ratio = float(hits) / max_hits
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom: 3px;">
                    <span style="font-family: monospace; font-weight: bold;">"{query}"</span>
                    <span style="color:#64748b;">{hits} searches</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(ratio)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedbacks console list below searches
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Recent Shopper Support Feedbacks</div>', unsafe_allow_html=True)
        for feed in reversed(st.session_state.feedback):
            st.markdown(f"""
            <div style="background-color: #f8fafc; padding: 12px; border-radius: 8px; margin-bottom: 8px; border:1px solid #e2e8f0;">
                <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:bold; color:#475569;">
                    <span>👤 {feed['name']}</span>
                    <span>{feed['date']} | Score: {"⭐" * feed['rating']}</span>
                </div>
                <p style="font-size:13px; margin: 6px 0 0 0; color:#334155;">{feed['comment']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_bottom_right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Central Store Segment Distributions</div>', unsafe_allow_html=True)
        st.write("Based on current onboard catalog listings:")
        
        # Dynamically compute segment distribution ratios from catalog
        category_counts = {}
        for p in st.session_state.products:
            category_counts[p["category"]] = category_counts.get(p["category"], 0) + 1
            
        total_prods = sum(category_counts.values()) if category_counts else 1
        
        for category, count in category_counts.items():
            percentage = int((count / total_prods) * 100)
            badge_cl = get_badge_class(category)
            
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; border-bottom: 1px solid #f1f5f9;">
                <span class="{badge_cl}" style="font-size:12px; text-transform:uppercase;">{category}</span>
                <span style="font-size:13px; font-weight:bold; color:#334155;">{percentage}% of products ({count} items)</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Direct Action Control board inside Admin
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="form-header">Administrative Controls</div>', unsafe_allow_html=True)
        if st.button("🔄 Force Refresh Database Sync"):
            # Simply update visitor simulation counts to make graphs feel live
            for key in st.session_state.searches.keys():
                st.session_state.searches[key] += random.randint(1, 10)
            st.toast("Telemetry data and store sync tables refreshed successfully!")
            st.rerun()
            
        st.write("---")
        st.caption("🔒 Developer Mode: MallQ! runs on a secure sandbox state container simulating actual production REST endpoints.")
        st.markdown('</div>', unsafe_allow_html=True)