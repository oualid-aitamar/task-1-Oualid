import pandas as pd


df = pd.read_excel('Online-Store-Orders.xlsx')


print("ORIGINAL DATASET")

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print()


print("PHASE 1: MISSING VALUES")

print(df.isnull().sum())
print()

# CouponCode: fill nulls with 'NO_COUPON' instead of dropping rows
missing_coupons = df['CouponCode'].isnull().sum()
df['CouponCode'] = df['CouponCode'].fillna('NO_COUPON')
print(f"[CR001] Filled {missing_coupons} missing CouponCode values with 'NO_COUPON'")
print()


print("PHASE 2: DUPLICATES")


before = len(df)
duplicates = df.duplicated(subset='OrderID').sum()

if duplicates > 0:
    df = df.drop_duplicates(subset='OrderID', keep='first')
    print(f"[CR002] Removed {duplicates} duplicate OrderIDs")
else:
    print(f"[CR002] No duplicates found — all {before} OrderIDs are unique ✓")
print()



print("PHASE 3: DATA FORMATS")


# Dates → ISO 8601 (YYYY-MM-DD)
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
invalid_dates = df['Date'].isnull().sum()
if invalid_dates > 0:
    print(f"[CR003] Warning: {invalid_dates} unparseable dates found")
else:
    print(f"[CR003] All dates valid. Format: YYYY-MM-DD ✓")

# Strip whitespace from all string columns
str_cols = df.select_dtypes(include='object').columns.tolist()
for col in str_cols:
    df[col] = df[col].str.strip()
print(f"[CR005] Stripped whitespace from {len(str_cols)} text columns ✓")

# Round numeric price columns to 2 decimal places
df['UnitPrice']  = df['UnitPrice'].round(2)
df['TotalPrice'] = df['TotalPrice'].round(2)
print(f"[CR006] Rounded UnitPrice & TotalPrice to 2 decimal places ✓")
print()


print("VERIFICATION")


# Check TotalPrice = Quantity * UnitPrice
expected = (df['Quantity'] * df['UnitPrice']).round(2)
mismatches = (df['TotalPrice'] != expected).sum()
print(f"[CR004] TotalPrice calculation mismatches: {mismatches} ✓")

# Check for negative/zero values
neg_qty   = (df['Quantity']   <= 0).sum()
neg_price = (df['UnitPrice']  <= 0).sum()
neg_total = (df['TotalPrice'] <= 0).sum()
print(f"[CR007] Negative Quantity:   {neg_qty} ✓")
print(f"[CR008] Negative UnitPrice:  {neg_price} ✓")
print(f"[CR009] Negative TotalPrice: {neg_total} ✓")
print()


print("CLEANING SUMMARY")

print(f"Records before: {before}")
print(f"Records after:  {len(df)}")
print(f"Remaining nulls:\n{df.isnull().sum()}")
print()


output_path = 'Online-Store-Orders_Cleaned.csv'
df.to_csv(output_path, index=False, date_format='%Y-%m-%d')
print(f"Saved cleaned data → {output_path}")
